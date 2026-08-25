# Slot Math — Failure Log

What was attempted that didn't work, why it didn't work, and what was
tried next.

Lower bar than DECISIONS.md — capture failures even when they didn't
produce a durable rule. The whole point: future-you (or future-Claude)
shouldn't re-attempt dead ends because the lesson got lost.

---

## Format

### YYYY-MM-DD — [One-line failure description]

**Attempted:** [What was tried]

**Why it didn't work:** [Concrete reason, not "it broke." If the
failure mode was technical, name the specific issue. If the failure
mode was scope or approach, name that.]

**What we tried instead:** [The next attempt, which may also have
failed and may have its own entry below]

**Status:** Resolved / open / abandoned

**Tags:** [keywords for future text-search — e.g., "rendering, pandoc,
quarto" or "scope, scrollytelling, decoration"]

---

## Entries

[New entries get added here, most recent at the top]

### 2026-08-25 — Brief cited fixture-authored spread as readiness evidence (corrected)

**Attempted:** The brief claimed "Door Math's authorization-to-scan gaps suggest
[fair-share stories] exist naturally, which would mean zero data authoring" — cited as
evidence the readiness gate would pass.

**Why it didn't work:** Office-hours grounding verified that Door Math's per-retailer
spread comes from its **demo fixture** (`cinderhaven-store-universe`), whose never-scan
rates are hard-coded in `constants.py` (`NEVER_SCAN_RATES` 3%–15%). The real SSOT
warehouse is ~99.5% authorized-selling penetration and deliberately homogeneous (0.69pt
partner-spread band). Citing fixture-authored spread as evidence is exactly the class of
"massaging" the fleet's honesty gate forbids. Separately, that number measures
authorization-to-scan *presence*, not the slot-share ÷ sales-share *proportionality* the
index computes.

**What we tried instead:** Corrected the gate to run against the **real SSOT only**
(fixture explicitly banned) with spread defined on **velocity/dollar-share dispersion**
(which can vary even at ~100% penetration). See DECISIONS.md "Data-readiness gate rule →
Office-hours correction." The gate design (thresholds, flat→stop) was sound; only the
evidence source was wrong.

**Status:** Resolved (design corrected; notebook not yet run)

**Tags:** readiness-gate, fixture, evidence-error, ssot, penetration, proportionality,
door-math, office-hours

### 2026-08-25 — Brief assumed a Void Finder "× margin" dollarizer that doesn't exist (corrected)

**Attempted:** The brief specified the Dollarizer as "N slots × median velocity × **margin**
= $/yr," described as reusing Void Finder's machinery.

**Why it didn't work:** Verified against Void Finder — it dollarizes on comparable-store
scan **revenue** (median weekly scan dollars × weeks). There is no cost/margin column in
the Cinderhaven schema, and a margin factor was deliberately cut from Void Finder as
"dimensionally invalid" (commit `8daf6d7`, now guarded by `review.yaml`). The reuse claim
was also over-stated: the velocity logic is entangled private helpers (copy-adapt, not
import), and the "N slots" count multiplier has no analog in Void Finder (which accrues
by void-weeks).

**What we tried instead:** Slot Math quotes the **same currency as Void Finder** —
comparable-store scan revenue, labeled as such, reconciling with Void Finder's figure. A
margin basis is a fleet-wide roadmap decision, not a one-tool fork. See DECISIONS.md
"Dollar authority."

**Status:** Resolved (design corrected)

**Tags:** dollarizer, margin, void-finder, reuse-claim, scan-revenue, dimensional-error

### 2026-08-25 — Brief assumed a Spin Rate deep-link that's structurally impossible (corrected)

**Attempted:** The brief proposed the Heatmap cross-link into Spin Rate's hidden-gem
quadrant, with item-level deep links as a candidate.

**Why it didn't work:** Verified — Spin Rate has zero URL-addressable state (no
`dcc.Location`, no query parsing; all state in session/memory `dcc.Store`). Every visitor
lands on the default view; a deep link cannot target a quadrant, SKU, or filter without
adding routing to Spin Rate (out of scope).

**What we tried instead:** The pre-registered cross-link rule's else-branch fires: **visual
pairing only**, with "URL-state support" logged as Spin Rate's own roadmap item. See
DECISIONS.md "Spin Rate cross-link: RESOLVED to visual pairing only."

**Status:** Resolved

**Tags:** spin-rate, cross-link, deep-link, url-state, dash, dcc-location
