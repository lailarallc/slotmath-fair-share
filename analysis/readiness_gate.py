#!/usr/bin/env python3
"""
Slot Math — data-readiness gate (throwaway, pre-registered).

Runs the office-hours-corrected gate against the REAL SSOT only:
  index = (share of our authorized slots) / (share of our scan dollars),
          per retailer x region.
Spread is defined on velocity/dollar dispersion (presence is saturated at
~99.5%), so the sales side uses scan DOLLARS, not authorization presence.

Decision rule (pre-registered — see DECISIONS.md 2026-08-25):
  >= 2-3 cells outside 0.7-1.3 WITH a dollarized gap worth a buyer
  conversation  -> BUILD.
  Clusters at ~1.0 / no material gap -> within-footprint demo is dead on
  honest data; tool drops to client-mode-only and we STOP.

BANNED: the Door Math `cinderhaven-store-universe` fixture. This script
touches raw.distribution_log / raw.scan_data / raw.stores in the live
warehouse ONLY.

Connection: via `flyctl proxy` to the Fly.io prod Postgres (Docker-free
workaround). Credentials come from the SSOT repo's .env — values are never
printed. Run the proxy first (see --help epilog).
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import timedelta

SSOT_DIR = r"C:\Users\mssha\projects\active datasources\cinderhaven-data-platform"
BAND_LO, BAND_HI = 0.7, 1.3


def load_env() -> dict:
    """Load POSTGRES_* from the SSOT .env without echoing any value."""
    try:
        from dotenv import dotenv_values
    except ImportError:
        sys.exit("python-dotenv not installed. `pip install python-dotenv`.")
    env_path = os.path.join(SSOT_DIR, ".env")
    if not os.path.exists(env_path):
        sys.exit(f"No .env at {env_path}")
    vals = dotenv_values(env_path)
    # Connection is through the local flyctl proxy, so host/port are local.
    port = os.environ.get("SLOTMATH_PG_PORT") or vals.get("POSTGRES_PROXY_PORT") or "5433"
    return {
        "host": os.environ.get("SLOTMATH_PG_HOST", "127.0.0.1"),
        "port": port,
        "dbname": vals.get("POSTGRES_DB", "cinderhaven"),
        "user": vals.get("POSTGRES_USER", "postgres"),
        "password": vals.get("POSTGRES_PASSWORD", ""),
        "sslmode": os.environ.get("PGSSLMODE", "disable"),
    }


def connect(cfg: dict):
    import psycopg2
    try:
        return psycopg2.connect(
            host=cfg["host"], port=cfg["port"], dbname=cfg["dbname"],
            user=cfg["user"], password=cfg["password"], sslmode=cfg["sslmode"],
            connect_timeout=10,
        )
    except Exception as e:  # noqa: BLE001
        sys.exit(
            f"Could not connect to Postgres on {cfg['host']}:{cfg['port']} "
            f"(db={cfg['dbname']}, user={cfg['user']}).\n"
            f"  {type(e).__name__}: {e}\n\n"
            "Is the flyctl proxy running? Start it (in a separate terminal):\n"
            f"  flyctl proxy {cfg['port']}:5432 -a cinderhaven-db\n"
            "…and make sure `flyctl auth login` has been done first."
        )


SLOTS_SQL = """
SELECT s.chain_name AS retailer,
       COALESCE(s.region, '(no region)') AS region,
       COUNT(DISTINCT d.sku || '|' || d.store_id) AS slots
FROM raw.distribution_log d
JOIN raw.stores s ON s.store_id = d.store_id
WHERE d.authorized_date <= %(wend)s
  AND (d.deauthorized_date IS NULL OR d.deauthorized_date > %(wend)s)
GROUP BY 1, 2
"""

DOLLARS_SQL = """
SELECT s.chain_name AS retailer,
       COALESCE(s.region, '(no region)') AS region,
       SUM(sc.dollars_sold) AS dollars,
       SUM(sc.units_sold)   AS units
FROM raw.scan_data sc
JOIN raw.stores s ON s.store_id = sc.store_id
WHERE sc.week_ending > %(wstart)s AND sc.week_ending <= %(wend)s
GROUP BY 1, 2
"""


def run(weeks: int, as_of: str | None, gap_threshold: float, save_csv: bool):
    import pandas as pd

    cfg = load_env()
    conn = connect(cfg)
    try:
        with conn.cursor() as cur:
            if as_of:
                wend = as_of
            else:
                cur.execute("SELECT MAX(week_ending) FROM raw.scan_data")
                wend = cur.fetchone()[0]
        wstart = wend - timedelta(weeks=weeks)
        params = {"wend": wend, "wstart": wstart}
        slots = pd.read_sql(SLOTS_SQL, conn, params=params)
        dollars = pd.read_sql(DOLLARS_SQL, conn, params=params)
    finally:
        conn.close()

    df = slots.merge(dollars, on=["retailer", "region"], how="outer")
    df[["slots", "dollars", "units"]] = df[["slots", "dollars", "units"]].fillna(0)
    df["dollars"] = df["dollars"].astype(float)

    total_slots = df["slots"].sum()
    total_dollars = df["dollars"].sum()
    if total_slots == 0 or total_dollars == 0:
        sys.exit("No slots or no scan dollars in window — check the window/connection.")

    df["slot_share"] = df["slots"] / total_slots
    df["dollar_share"] = df["dollars"] / total_dollars
    # index = slot_share / dollar_share; inf where a cell has slots but $0 scans
    df["index"] = df.apply(
        lambda r: (r["slot_share"] / r["dollar_share"]) if r["dollar_share"] > 0 else float("inf"),
        axis=1,
    )
    # first-order scan-revenue gap (currency = scan revenue, NO margin):
    #   (dollar_share - slot_share) * total_dollars
    #   >0 = under-shelved opportunity ; <0 = over-shelved / over-covered
    df["gap_$"] = (df["dollar_share"] - df["slot_share"]) * total_dollars
    df["verdict"] = df["index"].apply(
        lambda x: "UNDER" if x < BAND_LO else ("OVER" if x > BAND_HI else "in-band")
    )
    df = df.sort_values("index").reset_index(drop=True)

    cells = len(df)
    outside = df[(df["index"] < BAND_LO) | (df["index"] > BAND_HI)]
    n_outside = len(outside)
    max_abs_gap = df["gap_$"].abs().max()

    # ---- report ----
    pd.set_option("display.float_format", lambda v: f"{v:,.3f}")
    pd.set_option("display.max_rows", None)
    pd.set_option("display.width", 160)
    print("=" * 78)
    print("SLOT MATH — DATA READINESS GATE (real SSOT, fixture banned)")
    print("=" * 78)
    print(f"Window: {wstart} → {wend}  ({weeks} weeks)")
    print(f"Total authorized slots (sku×store pairs): {int(total_slots):,}")
    print(f"Total scan dollars in window:            ${total_dollars:,.0f}")
    print(f"Cells (retailer × region):               {cells}")
    print("-" * 78)
    show = df[["retailer", "region", "slots", "dollars", "index", "gap_$", "verdict"]].copy()
    show["dollars"] = show["dollars"].map(lambda v: f"${v:,.0f}")
    show["gap_$"] = show["gap_$"].map(lambda v: f"${v:,.0f}")
    print(show.to_string(index=False))
    print("-" * 78)
    print(f"Cells outside {BAND_LO}-{BAND_HI}: {n_outside} of {cells}")
    if n_outside:
        widest = outside.reindex(outside["gap_$"].abs().sort_values(ascending=False).index)
        print("Widest gaps (by |scan-revenue gap|):")
        for _, r in widest.head(5).iterrows():
            print(f"  {r['retailer']:<16} {r['region']:<14} index={r['index']:.2f}  "
                  f"gap=${r['gap_$']:,.0f}  ({r['verdict']})")
    print(f"Max |gap|: ${max_abs_gap:,.0f}   (gate $ threshold: ${gap_threshold:,.0f})")

    # ---- verdict ----
    build = n_outside >= 2 and max_abs_gap >= gap_threshold
    print("=" * 78)
    if build:
        print("GATE: ✅ BUILD — real, dollarizable spread exists on honest data.")
        print("      Proceed to /plan-ceo-review → /plan-eng-review → /decompose.")
    elif n_outside >= 2:
        print("GATE: ⚠️  SPREAD but THIN $ — indices disperse, but the widest gap is")
        print(f"      below ${gap_threshold:,.0f}. Human call: is it worth a buyer")
        print("      conversation? If not, treat as client-mode-only.")
    else:
        print("GATE: 🛑 FLAT — index clusters at ~1.0 on honest data.")
        print("      The within-footprint demo is dead on honest data; Slot Math")
        print("      drops to CLIENT-MODE-ONLY and we STOP. No fixture fallback.")
    print("=" * 78)

    if save_csv:
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        os.makedirs(out_dir, exist_ok=True)
        out = os.path.join(out_dir, "readiness_gate.csv")
        df.to_csv(out, index=False)
        print(f"Saved per-cell detail → {out}")


def main():
    try:  # Windows consoles default to cp1252; the report uses →/✅ etc.
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    p = argparse.ArgumentParser(
        description="Slot Math data-readiness gate (real SSOT only).",
        epilog=(
            "Prereqs: `flyctl auth login`, then in a separate terminal:\n"
            "  flyctl proxy 5433:5432 -a cinderhaven-db\n"
            "Then: python analysis/readiness_gate.py"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--weeks", type=int, default=52, help="trailing scan window (default 52)")
    p.add_argument("--as-of", default=None, help="window end YYYY-MM-DD (default: max scan week)")
    p.add_argument("--gap-threshold", type=float, default=50_000,
                   help="min |scan-revenue gap| to call the spread buyer-worthy (default 50000)")
    p.add_argument("--no-csv", action="store_true", help="don't write the per-cell CSV")
    a = p.parse_args()
    run(a.weeks, a.as_of, a.gap_threshold, save_csv=not a.no_csv)


if __name__ == "__main__":
    main()
