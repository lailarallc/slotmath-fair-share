#!/usr/bin/env node
// D2 — data invariant gate. Asserts the committed data/slotmath.json against canon
// and the honesty structure, so a drifted cell fails the build before it can deploy
// (DECISIONS 2026-08-26; eng-gate must-address #6). Dependency-free: node builtins only.
//
// Exact, not toleranced (per the frozen-contract decision): money reconciles to the
// cent; Σgap uses a float-epsilon bound (machine precision — the gaps sum to zero
// mathematically; 1e-6 on $32M is bit-noise, not a business tolerance).
import { readFileSync } from "node:fs";
import assert from "node:assert/strict";

// Canonical CY2025 figures (cinderhaven-data-platform canonical_values). Pinning them
// here is the "numbers can't silently drift from the passed gate" guarantee — a
// deliberate canon change is a deliberate edit to these two lines.
const CANONICAL_DOLLARS = 32323139.62; // retail scan, CY2025, to the cent
const CANONICAL_SLOTS = 9176; // active authorized store-SKUs
const N_CELLS = 30;
const round2 = (x) => Math.round(x * 100) / 100;

const url = new URL("../data/slotmath.json", import.meta.url);
const { metadata: m, cells } = JSON.parse(readFileSync(url, "utf8"));

let n = 0;
const ok = (cond, msg) => {
  assert.ok(cond, msg);
  n++;
};

// shape + metadata contract
ok(Array.isArray(cells) && cells.length === N_CELLS, `expected ${N_CELLS} cells, got ${cells?.length}`);
ok(m.schema_version === 1, "schema_version must be 1");
ok(m.band_lower === 0.7 && m.band_upper === 1.3, `band bounds must be 0.7/1.3, got ${m.band_lower}/${m.band_upper}`);
for (const f of ["basis", "basis_note", "gap_sign", "window", "query_date", "gate_git_sha"]) {
  ok(typeof m[f] === "string" && m[f].length > 0, `metadata.${f} missing`);
}
ok(!/no margin/i.test(m.basis), "basis is a public label — must not contain internal 'no margin' language");

// canon + internal consistency (both, so metadata and cells can't drift apart)
const sumSlots = cells.reduce((a, c) => a + c.slots, 0);
const sumDollars = round2(cells.reduce((a, c) => a + c.dollars, 0));
ok(m.total_slots === CANONICAL_SLOTS, `total_slots ${m.total_slots} != canonical ${CANONICAL_SLOTS}`);
ok(m.total_dollars === CANONICAL_DOLLARS, `total_dollars ${m.total_dollars} != canonical ${CANONICAL_DOLLARS}`);
ok(sumSlots === m.total_slots, `Σslots ${sumSlots} != total_slots ${m.total_slots}`);
ok(sumDollars === m.total_dollars, `Σdollars ${sumDollars} != total_dollars ${m.total_dollars}`);

// money identity: signed gaps sum to zero (float epsilon)
const sumGap = cells.reduce((a, c) => a + c.gap_dollars, 0);
ok(Math.abs(sumGap) < 1e-6, `Σgap ${sumGap} is not ~0`);

// channel tagging + the honesty invariant (why club must be flagged, not headlined)
const CHANNELS = new Set(["club", "mass", "grocery"]);
for (const c of cells) ok(CHANNELS.has(c.retail_channel), `${c.retailer}/${c.region}: bad retail_channel ${c.retail_channel}`);
const under = cells.filter((c) => c.verdict === "UNDER");
const over = cells.filter((c) => c.verdict === "OVER");
ok(under.length > 0 && under.every((c) => c.retail_channel === "club"), "every UNDER (below-band) cell must be club — the club-channel caveat");
ok(over.length > 0 && over.every((c) => c.retail_channel !== "club"), "no OVER cell may be club");

// verdict must follow the metadata band bounds (views/checks never hardcode 0.7/1.3)
for (const c of cells) {
  const v = c.index < m.band_lower ? "UNDER" : c.index > m.band_upper ? "OVER" : "in-band";
  ok(c.verdict === v, `${c.retailer}/${c.region}: verdict ${c.verdict} != ${v} (index ${c.index})`);
}

console.log(
  `✓ data/slotmath.json: ${n} invariants hold — ${N_CELLS} cells, ` +
    `$${CANONICAL_DOLLARS.toLocaleString()} / ${CANONICAL_SLOTS} slots, Σgap≈0, ` +
    `${under.length} UNDER (all club) / ${over.length} OVER (none club).`
);
