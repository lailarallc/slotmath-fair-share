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
- [x] Go → unblocked. **Next: /plan-ceo-review → /plan-eng-review → /decompose**
      before defining the build arc.

> **Open methodology item for /plan-eng-review + copy:** channel-awareness (club vs.
> conventional grocery). Costco's under-shelf signal is partly a club-channel artifact;
> don't headline it unqualified. See DECISIONS.md gate-result caveat.

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
