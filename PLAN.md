# Fair Share — Current Work Plan

The current arc of work. Updated when the arc changes, not every
session. For session-by-session state, see HANDOFF.md.

---

## Goal

Data readiness check: prove the SSOT's authorization + sales patterns produce
interesting fair-share stories (indices that vary meaningfully from 1.0) before
any planning hardens.

## Why this arc, why now

The brief flags this as the first task and the gate on everything else (~half a
day). If indices come out uniformly ~1.0, the whole tool needs a small upstream
seeded-story conversation before it's worth building. Cheaper to find out now.

## Business question this arc answers

Does the underlying data actually contain the "shelf presence vs. sales"
mismatches the tool is meant to surface — or do we need to seed them?

## Tasks

Work in vertical slices — one thing end-to-end before the next.

- [ ] Locate the SSOT + confirm the grain Door Math consumes (authorization
      matrix, scan grain, store_card v0.3.0 region/identity)
- [ ] Compute the demo-mode index (path 1): share of our authorized slots vs
      share of our sales, per retailer × region
- [ ] Check the distribution — do indices spread away from 1.0, or cluster?
- [ ] Verdict: enough natural spread to demo, OR scope a small seeded-story tweak
- [ ] Write the finding into DECISIONS.md (gate result)

## Open questions to resolve BEFORE build (via /clarify, then /office-hours)

Parked here so they don't get silently decided. Full detail in BRIEF.md.

1. Denominator fork (rec: path 1 — within-brand demo, category feed in client mode)
2. Stack: fleet Dash vs. Lift Math static pattern
3. Name: Slot Math / Shelf Share / Fair Share (naming before subdomain)
4. Over-shelved case: own dollarization (rationalization risk $) or index only?
5. Spin Rate cross-linking depth: visual pairing vs. shared item-level URLs

## Out of scope for this arc

- Building any of the three views (Index / Dollarizer / Heatmap)
- Picking a stack or a name — those are /clarify + /office-hours decisions
- Client-mode category feed / path 2 upstream category-context package
- Any seeded-story authoring (only scoped here if the check demands it)

## Definition of done for this arc

- [ ] The demo-mode index is computed from real SSOT data
- [ ] The index distribution is characterized (spread vs. clustered at 1.0)
- [ ] A go/seed decision is recorded in DECISIONS.md with the evidence
- [ ] If "seed": the minimal seeded-story scope is written down (not yet built)

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
