# Slot Math — Current Work Plan

The current arc of work. Updated when the arc changes, not every
session. For session-by-session state, see HANDOFF.md.

---

## Project goal (clarified 2026-08-25)

Ship **Slot Math**: a within-footprint allocation tool for buyer meetings —
"which retailers under-carry you relative to demonstrated demand, and what the
next slot is worth there," per retailer × region. Three views (Index, Dollarizer,
Heatmap), both index directions shown and **fully dollarized**. It never calls
itself fair share; true category **Fair Share** is the client-mode/roadmap
upgrade. Full scope, the five resolved forks, and pre-registered gate rules live
in DECISIONS.md (2026-08-25 entries) and BRIEF.md.

Gated by the data-readiness check below — if within-footprint indices come out
flat, the build does not proceed as-is.

---

## Goal (current arc)

Data-readiness gate: run the pre-registered index notebook against the **real SSOT**
and decide go / no-go before any tool code. Office-hours verdict is 🟡 yellow — this
notebook is the single thing that flips it to green.

## Why this arc, why now

Office-hours (2026-08-25) confirmed the whole flagship path rests on one untested
fact: does the within-footprint index actually disperse on honest data? The evidence
the brief cited (Door Math auth gaps) was fixture-authored and banned. The real
warehouse is ~99.5% penetration and homogeneous, so a *presence* index collapses to
~1.0 — but the index is slot-share ÷ **dollar-share**, which can still disperse via
per-slot velocity. Nobody has measured it. 2–4 hours settles a 1–1.5 week commitment.

## Business question this arc answers

On honest SSOT data, does the slot-share ÷ dollar-share index vary enough across
retailer × region to carry a demo — or does it cluster at ~1.0?

## Tasks — ✅ COMPLETE (gate passed 2026-08-25)

- [x] Build the gate against the **REAL SSOT ONLY** (fixture banned) —
      `analysis/readiness_gate.py`, raw.distribution_log slots + raw.scan_data dollars
      via raw.stores, connected through flyctl proxy
- [x] Compute the index per retailer × region: slot-share ÷ dollar-share (dispersion)
- [x] Count cells outside 0.7–1.3; dollarize the widest gap (scan revenue, no margin)
- [x] Verdict: **✅ BUILD** — 11/30 cells outside band, widest $1.22M (Costco West),
      sanity $32.3M CY2025 to the dollar
- [x] Gate result recorded in DECISIONS.md (2026-08-25 — GATE RESULT)

## Open questions — RESOLVED in /clarify + /office-hours (see DECISIONS.md 2026-08-25)

1. Denominator → within-footprint demo (path 1); category feed in client mode. ✓
2. Stack → deferred to /plan-eng-review (lean: static, or static + Heatmap island). ✓
3. Name → **Slot Math** (Fair Share = roadmap). ✓
4. Over-shelved → full symmetric dollarization, defensive-intel framing, scan-revenue
   currency (no margin). ✓
5. Spin Rate cross-link → **visual pairing only** (Spin Rate has no URL state). ✓
   Plus office-hours: positioning reframe (targeting + engagement-qualifier, not buyer
   weapon); dollar authority (reconcile with Void Finder). ✓

## Out of scope for this arc

- Building any of the three views (Index / Dollarizer / Heatmap)
- Picking a stack (→ /plan-eng-review)
- Client-mode category feed / path 2 upstream category-context package
- Any seeded-story or fixture data — the gate runs on the honest warehouse only

## Definition of done for this arc — ✅ MET

- [x] The index is computed from real SSOT data (fixture never touched)
- [x] The distribution is characterized (11/30 outside band; widest $1.22M Costco West)
- [x] A go decision is recorded in DECISIONS.md with the numbers
- [x] Go → unblocked.

## Gate progress

- data-readiness gate → ✅ PASS (2026-08-25)
- **/plan-ceo-review → 🟡 REVISE → resolved** (2026-08-25): 5 must-fixes + 2 scope
  calls all decided and logged in DECISIONS.md "Build sequence & demo scope."
  Net effect: **~1-week 2.5-view demo** (Dollarizer-first, Index, payload Heatmap),
  Costco demoted from headline, client mode described-not-built, one instrumented CTA.
- **/plan-eng-review → 🟡 NEEDS-WORK → resolved** (2026-08-26): stack = SvelteKit
  static + bespoke SVG; freeze-and-commit data flow; first-order gap verbatim (no
  velocity port); 3-value channel enum (club=Costco); GoatCounter CTA + pre-registered
  threshold; Cloudflare Pages (`slotmath`); risk-first build order (walking skeleton
  day 0). Full architecture cluster in DECISIONS.md 2026-08-26.
- **Next: /decompose** the risk-first build order into individually-testable tasks,
  then build the ~1-week 2.5-view demo.

> All three gates passed (data ✅ / product 🟡→resolved / eng 🟡→resolved). Build is
> unblocked. The 7 eng must-address items are folded into the DECISIONS.md build order.

---

## Decomposition: Slot Math 2.5-view demo build

Goal: ship the ~1-week 2.5-view demo (Dollarizer, Index, Heatmap) on
`slotmath.lailarallc.com`, risk-first, off a frozen committed JSON. Full
architecture in DECISIONS.md 2026-08-26 cluster.

Grouped into phases. **S (skeleton) and D (data) are independent roots** — S goes
first per the risk-first order; D can run alongside. Views need both.

Steps:

**Phase S — Walking skeleton & deploy (retire the zero-precedent risks Day 0)**
- [x] S1: Scaffold SvelteKit + `@sveltejs/adapter-static` + Vite; one page renders a
      value read from a committed **stub** JSON (`data/slotmath.json` with 1 fake cell).
      ✅ Built; stub renders into `build/index.html`; schema frozen (DECISIONS 2026-08-26).
    - Depends on: (none)
    - Done when: `npm run build` emits static files to `build/` and `npm run preview`
      shows the stub value; **the stub matches D1's exact JSON schema (same cell keys +
      metadata shape, fake values) so the D1 swap is a file replacement, not a refactor.**
- [x] S2: Add the GoatCounter script to `app.html` and a CTA `<a>` whose click handler
      fires `window.goatcounter.count({ path: 'cta_click', event: true })`; vendor the
      engagement-template deploy-guard as a pre-push hook.
    - Depends on: S1
    - Done when: locally, clicking the CTA calls `count(...)` (verify in devtools
      Network → request to `lailara.goatcounter.com/count`); pre-push hook runs.
      ✅ Script + CTA in built HTML; guards no-op; hook active (`core.hooksPath`). The
      network *send* is localhost-suppressed by GoatCounter — verified on deploy (S3).
- [x] S3: GitHub Actions job — build-in-CI (no token in build container) →
      `wrangler pages deploy build --project-name=slotmath --branch=main`; Git
      integration stays OFF.
    - Depends on: S2
    - Done when: `slotmath.lailarallc.com` serves the skeleton AND one `cta_click`
      event records in GoatCounter from the **deployed** build (adblocker OFF; localhost
      is ignored by design).
    - ✅ **Deployed green** (run 33016551058, 39s) from `lailarallc/slotmath-fair-share`
      using **org secrets** (repo migrated into the org). `slotmath.lailarallc.com` →
      HTTP 200, renders skeleton + GoatCounter script + CTA. `workflow_dispatch` added.
    - **One manual check left (yours):** open the live site adblocker-OFF, click the CTA,
      confirm one `cta_click` in the GoatCounter dashboard. Then S3 is fully closed.

**Phase D — Freeze the data**
- [x] D1: Adapt `analysis/readiness_gate.py`'s aggregation into a precompute that emits
      the 30-cell JSON — per cell: retailer, region, slots, dollars, slot_share,
      dollar_share, signed index, `gap_$`, **`retail_channel` ∈ {club,mass,grocery}**
      (club = Costco) — plus metadata (query date, window=CY2025, gate git SHA,
      schema-version). Run locally via flyctl proxy; commit the JSON.
    - Depends on: (none; needs flyctl auth + proxy)
    - Done when: `data/slotmath.json` is committed with 30 cells + metadata and totals
      = $32,323,140 / 9,176 slots.
      ✅ `analysis/precompute.py` → 30 cells, **$32,323,139.62** / 9,176 (canonical to the
      cent), channels club 5 / mass 5 / grocery 20, full precision (Σgap≈0 to float
      epsilon). File-replace swap confirmed: site renders real data, no code change.
- [ ] D2: Invariant test asserting the committed JSON: sum $32,323,140, 9,176 slots, 30
      cells, `Σgap$ = 0`, all 6 OVER cells non-Costco / all 5 UNDER cells Costco,
      `retail_channel` present on every cell. Wire into the CI gate.
    - Depends on: D1
    - Done when: test passes locally and in CI; flipping one cell's number fails it.

**Phase V — Views (each reads the frozen JSON; needs S1 + D1)**
- [ ] V1: Dollarizer view — headline filters to non-club **OVER** cells (Walmart West
      −$736k, Regional NE 1.84, Sprouts West 1.34); Costco UNDER cells behind the
      "club-normal, not a 3× expansion case" flag; every $ labeled basis+period from
      JSON metadata; both directions shown. **The over-shelved list cross-links to the
      SKU Rationalization tool ("fix-or-kill is the prepared answer").**
    - Depends on: S1, D1
    - Done when: renders the OVER grocery/mass cells with gap$, Costco hidden behind a
      toggle, the over-shelved list links to SKU Rationalization, legible at 1440px & 375px.
- [ ] V2: Index verdict + table — one banner line, one chart, per-cell table; continuous
      index value + gap$ (not just OVER/in-band bucket).
    - Depends on: S1, D1
    - Done when: 30-second-rule layout renders; a boundary cell (Kroger SE 1.299) reads
      "right at the line", at 1440px and 375px.
- [ ] V3: Heatmap qualifier map — region × banner SVG grid, gap-$ colour ramp from
      `lailara_palette`, channel toggle, filter state in URL query params.
    - Depends on: S1, D1
    - Done when: grid renders; changing a filter updates the URL and a reload restores
      the same view; legible at 1440px and 375px.

**Phase F — Finish & integrate**
- [ ] F1: Client-mode **described** roadmap panel — copy naming the IRI/Circana/SPINS
      extract shapes it will accept. No client-mode code.
    - Depends on: S1
    - Done when: panel renders with concrete extract-shape copy; nothing computes.
- [ ] F2: Full Lailara brand frame + copy/voice pass + the CTA closing state ("sell
      across 3+ regions and 2+ banner types? …") wired to the pre-registered metric.
      **Include one line of Spin Rate visual-pairing copy** (conceptual reference — which
      door + which items — no deep link; see DECISIONS 2026-08-26 recontextualization).
    - Depends on: V1, V2, V3, F1
    - Done when: passes the Deployed UI gate at 1440px and 375px; CTA closing state
      present; the Spin Rate pairing line is on the page.
- [ ] B (integration): final deploy with all views; confirm the domain is Active and the
      GoatCounter `cta_click` event records on production; CI invariant test green.
    - Depends on: S3, D2, F2
    - Done when: `slotmath.lailarallc.com` serves the full 2.5-view demo, one production
      `cta_click` records, and the invariant CI job is green.

---

## Arc history

When an arc completes, archive its goal, completion date, and outcome
here. Then start a new arc above. Provides continuity without bloating
the active plan.

### [Date completed] — [Goal]
- Outcome: [what shipped or what was decided]
- Tag: [git tag if one was created]

---

## Improvement history

Track when this project was reviewed and improved via /improve.
Each entry records what was found, what was fixed, and when to
check again.

<!-- Entries are added by /improve — don't delete this section -->
