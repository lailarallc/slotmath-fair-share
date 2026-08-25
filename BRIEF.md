# Fair Share — Tool Brief

> **Status:** Input to the Claude Code project process (brainstorm → clarify →
> office-hours → plan reviews). This is the idea and its known forks, not a
> frozen spec. The process should interrogate everything here; the Open
> Questions section is deliberate ammunition for `/clarify`.

## The business question

**"Is our shelf presence proportional to our sales — and what's the gap worth?"**

The buyer-meeting argument tool. A brand holding 12% of category sales on 8% of
the category's item slots has a quantified expansion case; a brand at 15% of
slots on 9% of sales has a problem the buyer will find first. Fair Share computes
the index both directions and prices the gap — the honest-both-ways framing is
the differentiator, same as the rest of the series.

## Fit

Seventh tool in the Cinderhaven series (Door Math, Spin Rate, Void Finder,
Decompose, Trial vs Repeat, Lift Math). Direct pairing with **Spin Rate**: Spin
Rate says which items earn their space; Fair Share says whether the amount of
space matches the sales. From the original buzzword-series ranking it was #4,
promoted to next-up because it needs no new data authoring in its base form and
its machinery is already built.

Brainstorm lineage: 4a (share index), 4b (item-count version), 4c
(space-to-sales dollarizer), 4d (regional heatmap) — four brainstorm entries,
one tool, three views. Same collapse logic as Lift Math's five-into-three.

## The metric

**Fair-share index = share of item slots ÷ share of sales, per retailer × region.**

Facings data does not exist in this universe (and rarely exists for small brands
in reality), so the item-count proxy is the honest version, stated as such — the
brainstorm called this "the realistic small-brand version" and that framing
should survive into the copy.

- Below 1.0 = under-shelved → expansion argument, dollarized.
- Above 1.0 = the buyer's argument against you → shown at full size, because
  knowing it first is the point.

## THE fork the process must resolve first (denominator)

True fair share needs **category** sales — all brands, not just Cinderhaven — and
the SSOT is one brand's data. Three paths, in order of preference:

1. **Demo ships the within-brand version; engagement accepts real category
   data.** Demo metric: share of our authorized slots vs share of our sales, by
   retailer × region — "which retailers under-carry us relative to how we sell
   there." Weaker claim, honestly named, fully computable today. Client mode (the
   existing engagement scaffold) accepts a syndicated category feed as an optional
   input — when a client brings IRI/Circana/SPINS data, the tool computes true
   category fair share. The gap between demo and engagement becomes a sales
   argument rather than a fake. **(Recommended.)**
2. **Author a category-context package upstream** (a `cinderhaven-category-context`
   sibling of promo-response: synthetic competitor items and sales by category ×
   retailer). Real option, real cost — new realism criteria, plausibility audit,
   weeks not days. Defensible later; heavy as an entry price. **(Roadmap item.)**
3. **Reuse Competitive Shelf Intelligence data** — it already tracks competitor
   assortment, but scoped to one category on two retail surfaces. Partial at best;
   probably a supplementary view, not the denominator.

Recommendation is path 1, with path 2 logged as the roadmap upgrade. The process
should pressure-test this.

## Views (three)

1. **Index** — the verdict view, 30-second rule applies: one banner line ("At
   [retailer], we hold X% of authorized slots and Y% of sales — index 0.7"), one
   chart, per-retailer × region table. Both directions shown.
2. **Dollarizer** — the gap priced with Void Finder's comparable-store velocity
   machinery: N missing slots × median velocity of comparable carried stores ×
   margin = $/year unclaimed (or at-risk, for the over-shelved case). The number
   that turns a reset conversation into a negotiation.
3. **Heatmap** — region × banner grid of the index; local strength with
   under-representation = the cheapest expansion wins. Natural cross-link to Spin
   Rate's hidden-gem quadrant.

## Reuse inventory

Comparable-store velocity logic (Void Finder), store identity/region (store_card
v0.3.0), authorization matrix + scan grain (SSOT, as Door Math consumes it),
Lailara brand frame, engagement client-mode scaffold with POS intake preflight,
URL-state conventions from Lift Math if the stack supports them.

No truth machinery, no blindness gates, no pre-registration — this is a
measurement tool, not an estimation tool. That distinction keeps it light; the
process shouldn't import Lift Math's rigor apparatus where there's no
counterfactual being estimated.

## Data readiness check (first task, before any planning hardens)

Verify the SSOT's authorization patterns actually produce interesting fair-share
stories — Door Math's authorization-to-scan gaps suggest they exist naturally,
which would mean zero data authoring. If the indices come out uniformly ~1.0, a
small seeded-story conversation happens upstream (far smaller than
promo-response — assortment allocation tweaks, not causal response models).

## Open questions — deliberate `/clarify` material

1. The denominator fork above (rec: path 1).
2. **Stack:** fleet Dash vs the Lift Math static pattern. No request-time compute
   here either; precomputed + light front end is viable. Genuine choice.
3. **Name:** series voice, undecided. Candidates: Slot Math, Shelf Share, Fair
   Share played straight (Decompose precedent). Naming before subdomain, per the
   Lift Math lesson.
4. Does the over-shelved case get its own dollarization (rationalization risk $)
   or just the index? (Lean: yes — it feeds the SKU Rationalization tool's story.)
5. Cross-linking depth with Spin Rate: visual pairing only, or shared item-level
   URLs?

## Estimate

~1–1.5 weeks at current fleet rigor (client mode included), assuming path 1 on
the denominator and no upstream authoring. The data readiness check is half a day
and gates everything.
