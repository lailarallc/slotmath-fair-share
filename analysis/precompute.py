#!/usr/bin/env python3
"""
Slot Math — precompute the frozen data contract (D1).

Runs the SAME real-SSOT aggregation as the readiness gate, adds retail_channel
and provenance metadata, and writes data/slotmath.json — the single source the
three views + the D2 invariant read (DECISIONS 2026-08-26 "Frozen JSON data
contract"). Committing this file is the whole data update; the front end never
touches the DB.

Full precision is stored (round only in the view layer); the D2 invariant is
exact, never toleranced. Connection is via flyctl proxy — see readiness_gate.py.

  flyctl proxy 5433:5432 -a cinderhaven-db      # in another terminal
  SLOTMATH_PG_PORT=5433 python analysis/precompute.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from readiness_gate import BAND_HI, BAND_LO, DOLLARS_SQL, SLOTS_SQL, connect, load_env  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# retail_channel per retailer (chain_name). 3-value enum so copy can be honest:
# Walmart is mass/supercenter, not "conventional grocery" (DECISIONS 2026-08-26).
CHANNEL = {"Costco": "club", "Walmart": "mass"}  # everyone else -> grocery


def channel_for(retailer: str) -> str:
    return CHANNEL.get(retailer, "grocery")


def git_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO, text=True
        ).strip()
    except Exception:  # noqa: BLE001
        return "unknown"


def main():
    import pandas as pd

    cfg = load_env()
    conn = connect(cfg)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT MAX(week_ending) FROM raw.scan_data")
            wend = cur.fetchone()[0]
        wstart = wend - timedelta(weeks=52)
        params = {"wend": wend, "wstart": wstart}
        slots = pd.read_sql(SLOTS_SQL, conn, params=params)
        dollars = pd.read_sql(DOLLARS_SQL, conn, params=params)
    finally:
        conn.close()

    df = slots.merge(dollars, on=["retailer", "region"], how="outer")
    df[["slots", "dollars"]] = df[["slots", "dollars"]].fillna(0)
    df["dollars"] = df["dollars"].astype(float)

    total_slots = int(df["slots"].sum())
    total_dollars = round(float(df["dollars"].sum()), 2)
    if total_slots == 0 or total_dollars == 0:
        sys.exit("No slots or scan dollars in window — check connection/window.")

    df["slot_share"] = df["slots"] / total_slots
    df["dollar_share"] = df["dollars"] / total_dollars
    df["index"] = df.apply(
        lambda r: (r["slot_share"] / r["dollar_share"]) if r["dollar_share"] > 0 else float("inf"),
        axis=1,
    )
    df["gap_dollars"] = (df["dollar_share"] - df["slot_share"]) * total_dollars
    df["retail_channel"] = df["retailer"].map(channel_for)
    df["verdict"] = df["index"].apply(
        lambda x: "UNDER" if x < BAND_LO else ("OVER" if x > BAND_HI else "in-band")
    )
    df = df.sort_values("index").reset_index(drop=True)

    cells = [
        {
            "retailer": r["retailer"],
            "region": r["region"],
            "retail_channel": r["retail_channel"],
            "slots": int(r["slots"]),
            "dollars": round(float(r["dollars"]), 2),
            "slot_share": float(r["slot_share"]),      # full precision
            "dollar_share": float(r["dollar_share"]),  # full precision
            "index": float(r["index"]),                # full precision
            "gap_dollars": float(r["gap_dollars"]),     # full precision (Σ=0 to float epsilon; view rounds)
            "verdict": r["verdict"],
        }
        for _, r in df.iterrows()
    ]

    out = {
        "metadata": {
            "query_date": date.today().isoformat(),
            "window": "CY2025",
            "window_start": str(wstart),
            "window_end": str(wend),
            "gate_git_sha": git_sha(),
            "schema_version": 1,
            "total_slots": total_slots,
            "total_dollars": total_dollars,
            "band_lower": BAND_LO,
            "band_upper": BAND_HI,
            "gap_sign": "positive = under-shelved (expansion $); negative = over-shelved",
            "basis": "retail scan revenue (CY2025)",
            "basis_note": "revenue basis, no margin step — fleet Dollar Authority decision",
        },
        "cells": cells,
    }

    path = os.path.join(REPO, "data", "slotmath.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, allow_nan=False)  # allow_nan=False: fail on inf/nan
        f.write("\n")
    channels = {c: sum(1 for x in cells if x["retail_channel"] == c) for c in ("club", "mass", "grocery")}
    print(f"wrote {path}")
    print(f"  {len(cells)} cells | total ${total_dollars:,.2f} | {total_slots} slots")
    print(f"  channels: {channels} | window {wstart} -> {wend}")


if __name__ == "__main__":
    main()
