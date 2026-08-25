# Slot Math — Decisions Log

Permanent record of choices that should survive session turnover.
If a decision is reversed, strike it through and add the replacement
below — don't delete.

---

## Format

Each entry:
- **Date** — when decided
- **Decision** — one sentence, imperative voice
- **Why** — the reasoning, including what was tried and rejected
- **Scope** — what this applies to (file, chunk, deliverable, or "global")
- **Do not** — explicit anti-instructions, if any

---

## Architecture & Pipeline

### 2026-08-25 — Stack decision deferred to /plan-eng-review
- **Why:** No request-time compute is needed (tool is precomputed), so the choice
  is interactivity vs. deployment/maintenance overhead, not capability. Fleet Dash
  gives interactivity out of the box but is a Fly.io app to maintain; the Lift Math
  static pattern (precompute → JSON → light front end + URL-state) is cheaper and
  matches the 30-second buyer-meeting use. The one view that genuinely wants
  interaction is the Heatmap (region × banner filtering). Lean recorded for the
  gate: **static, or static + a small interactive island for the Heatmap only.**
- **Scope:** global (architecture)
- **Do not:** pick a stack silently before /plan-eng-review resolves it.

---

## Data & Schema

### 2026-08-25 — Denominator = within-footprint (path 1); category fair share is client-mode/roadmap
- **Why:** True category fair share needs all-brand category sales; the SSOT is one
  brand's data. Path 1 ships the honest within-footprint claim now and accepts a
  syndicated category feed (IRI/Circana/SPINS) in client mode for true fair share.
  Path 2 (author a synthetic `cinderhaven-category-context` package) is weeks of
  realism/plausibility work — logged as the roadmap upgrade, **not built**. Path 3
  (reuse Competitive Shelf Intelligence) is partial at best; supplementary view only.
- **Scope:** global (the core metric)
- **Do not:** call the demo "fair share"; do not build the category-context package
  as entry price unless the readiness gate (below) forces it.

### 2026-08-25 — Data-readiness gate rule (pre-registered before results)
- **Why:** The tool is only worth building if SSOT authorization + sales patterns
  already contain shelf-vs-sales mismatches. Rule stated before looking: **measure**
  within-footprint index spread (share of our authorized slots ÷ share of our sales,
  per retailer × region) and the dollarized gap at the extremes. **If spread is real**
  (roughly, banners outside 0.7–1.3 with a dollarized gap worth a buyer conversation)
  → ship the within-footprint tool under the honest reframe. **If flat** → stop; the
  tool drops in priority or the category package becomes the entry price, decided then.
- **Scope:** global (gates all build work)
- **Do not:** massage a flat result into a demo.

- **Office-hours correction (2026-08-25) — pins the source and the mechanism:**
  - **Source: the REAL SSOT only** — `raw.distribution_log` (drop_duplicates on
    sku,store_id = the slot footprint) joined to `raw.scan_data` (units/dollars) via
    `dim_stores`. **The Door Math demo fixture (`cinderhaven-store-universe`) is
    explicitly BANNED as evidence** — its per-retailer spread is hard-coded in
    `constants.py` (`NEVER_SCAN_RATES` 3%–15%), which is exactly the upstream
    massaging this gate exists to forbid.
  - **Mechanism: velocity / dollar-share dispersion, not authorization presence.**
    The real warehouse is ~99.5% authorized-selling penetration and deliberately
    homogeneous (0.69pt partner-spread band), so a *presence*-based index collapses
    to ~1.0. The index is slot-share ÷ **dollar/sales-share** (proportionality) — it
    can still disperse at ~100% penetration via per-slot velocity. Nobody has measured
    it; the notebook does.
  - **Flat ≈ 1.0 → the within-footprint demo is dead on honest data; tool drops to
    client-mode-only and we stop.** No fixture fallback.

### 2026-08-25 — GATE RESULT: ✅ PASS. Build the within-footprint demo.
- **Ran:** `analysis/readiness_gate.py` against the live SSOT via flyctl proxy
  (fixture never touched). Window auto = CY2025 (2024-12-28 → 2025-12-27).
- **Sanity:** total scan $ = **$32,323,140** (= canonical $32.3M CY2025 to the
  dollar); 9,176 authorized slots (= canonical). Confirms real warehouse, right window.
- **Result:** **11 of 30 retailer × region cells fall outside 0.7–1.3.** Widest gap
  **Costco West: index 0.33, $1.22M** under-shelved. Costco is under-shelved in all
  five regions (0.33–0.60); over-shelved cells include Walmart West (1.34, −$736k),
  Regional NE (1.84), Sprouts West (1.34). Per-cell detail: `analysis/output/readiness_gate.csv`.
- **Mechanism confirmed:** presence is saturated (~99.5%), so spread is entirely
  velocity/dollar dispersion — exactly what office-hours said had to be true for the
  demo to live. It is.
- **Decision:** proceed to build. Unblocks /plan-ceo-review → /plan-eng-review → /decompose.
- **Caveat carried into build (NOT a gate failure):** the Costco signal is dominant
  because club channels structurally carry few SKUs at huge velocity — a 0.33 index may
  be "club-normal," not a literal 3× slot-expansion case. **The index and/or copy likely
  need channel-awareness (club vs. conventional grocery).** The cleaner, less-arguable
  stories are the over-shelved grocery cells. Resolve in /plan-eng-review + copy.
- **Do not:** headline "Costco under-shelves you by $1.2M" without the club-channel
  framing — that's the kind of unqualified claim the honesty brand can't ship.

---

## Visualization & Dollarization

### 2026-08-25 — Over-shelved case gets full symmetric dollarization, framed as defensive intel
- **Why:** Honest-both-ways is the product. Over-shelved shown at full size (never
  hidden), dollarized symmetric to the under-shelved side. Framing requirement that
  answers the "arguing against its own user" worry: present it as *defensive intel*,
  never an indictment — copy frame "This is the number the buyer's category manager
  will compute eventually. See it first, walk in with the answer." Cross-link the
  over-shelved list to the SKU Rationalization tool (fix-or-kill is the prepared
  answer). Same logic as Lift Math showing its own error at full size.
- **Scope:** Dollarizer view + copy
- **Do not:** ship the unpriced-risk-line half-measure — a gestured-at number on a
  site whose pitch is "dollarized, not opinion" would be the fleet's first ungrounded
  claim.
- **Office-hours correction (2026-08-25):** ~~"N over-slots × velocity × **margin** =
  $/yr"~~ — the "× margin" step is WRONG and is struck. Verified against Void Finder:
  it dollarizes on comparable-store scan **revenue** (median weekly scan dollars ×
  weeks); there is no margin/cost column in the Cinderhaven schema and a margin factor
  was cut from Void Finder as dimensionally invalid (commit `8daf6d7`). See the Dollar
  Authority decision below for the corrected currency. Symmetric dollarization stays —
  once the currency is scan revenue (not a bespoke margin step), applying it in both
  directions is cheap, not a doubled risk.

### 2026-08-25 — Spin Rate cross-link: RESOLVED to visual pairing only
- **Why:** The pre-registered rule said "check Spin Rate's URL state first." Verified:
  Spin Rate has **zero URL-addressable state** — no `dcc.Location`, no query parsing;
  all filter/selection state lives in session/memory `dcc.Store`. A deep link is
  therefore impossible without code changes to Spin Rate (out of scope). The rule's
  else-branch fires automatically.
- **Decision:** visual pairing only (reference the hidden-gem quadrant conceptually;
  no deep link). Log "URL-state support (add `dcc.Location` + query-param callbacks)"
  as **Spin Rate's own roadmap item**; if/when it ships, this becomes a one-line change
  here (and only then does the contract + CI link-check test apply).
- **Scope:** Heatmap / cross-tool links
- **Do not:** build a deep link against Spin Rate today; do not add URL state to Spin
  Rate as part of Slot Math's scope.

### 2026-08-25 — Dollar authority: Slot Math quotes the same currency as Void Finder
- **Why:** Three fleet tools (Void Finder, Door Math, Slot Math) can price the same
  retailer × region gap. If they use different currencies they contradict each other in
  front of the exact adversary the honesty framing respects (the category manager
  reading two of our tools side by side). Void Finder's verified currency is
  **comparable-store scan revenue** (median comparable-store weekly scan dollars ×
  weeks; no margin). Slot Math dollarizes in that same currency, **labeled as scan
  revenue**, and must reconcile with Void Finder's figure for the same void.
- **Scope:** Dollarizer, both directions; any $ the tool prints
- **Do not:** introduce a margin/contribution step unilaterally. A margin basis is now
  *buildable* (an `economics()` helper exists upstream), but switching the fleet's
  dollar basis is a **fleet-wide decision across all tools at once** — logged as a
  roadmap item, never a one-tool fork.

---

## Positioning & Product framing

### 2026-08-25 — The demo is an internal targeting + engagement-qualifier tool, NOT the in-room buyer weapon
- **Why:** The demo's metric is brand-vs-self across the brand's own footprint; a buyer
  allocates on brand-vs-**category** within *their* stores, holding syndicated
  Circana/IRI data that outranks a brand's self-supplied distribution. The two indices
  are orthogonal and can point opposite ways (ours 1.5 "under-carried"; their Circana
  0.6 "underperforms the category") — and the buyer holds the governing one. So the
  demo cannot honestly be sold as the in-room argument; the category weapon is exactly
  the part gated behind client mode.
- **Decision:** The demo's two jobs are (1) **which door to push first** — where the
  brand's own footprint shows demand outrunning slots — and (2) **whether the spread is
  big enough to justify paying for the syndicated category work** (client mode).
  Success metric = **converts to the paid category engagement**, not "wins the meeting"
  (a conversion story no other portfolio tool has). The **over-shelved defensive-intel
  number is the single meeting-ready output** (the number the category manager computes
  anyway — see it first). No in-room *offensive* claim ships in the demo.
- **The Circana answer belongs to the ENGAGEMENT, not demo copy:** when their category
  number points the other way, the brand's honest reply is *composition, not
  contradiction* — "both numbers are real; that's why the ask is targeted: these SKUs
  (Spin Rate), these stores (Void Finder), not more slots blindly." A targeted proposal
  survives Circana because it doesn't dispute it. Log as engagement methodology; keep
  out of demo marketing claims.
- **Scope:** global (copy, positioning, case-study / `/work` page framing)
- **Do not:** describe Slot Math as "the buyer-meeting argument tool" — that phrase from
  the brief is **superseded everywhere**. Carry the correction into the case-study
  framing so the marketing never promises the weapon the demo isn't.

---

## Data sources & grain bindings (verified against real repos, 2026-08-25)

### 2026-08-25 — Bind to the actual fleet objects, not the brief's remembered names
- **Why:** Office-hours grounding checked every reuse claim against the real repos.
  Corrections that change the build:
  - **Store dimension is `dim_stores`, not "store_card"** (no such entity exists). Pull
    region/retailer/volume_tier from `raw.stores → stg_stores → dim_stores` directly —
    NOT from Door Math's `STORE_INFO` aggregate, which drops region.
  - **Category sales denominator (client mode) comes from `engagement-template`
    `pos.py`** (`scan_spec` + `intake()`, grain store_id×sku×week_ending) — NOT from
    `competitive-shelf-intelligence`, which holds price/shelf-presence only (no
    units/dollars, one category, Amazon+Walmart). Slot Math becomes engagement
    consumer repo #31.
  - **Void Finder velocity logic is copy-adapt, not import** — it lives in private,
    entangled helpers (`_store_velocity`, `_cohort_medians`, `_attach_comparables`)
    hardcoded to weekly-scan schema, a 13-week window, and volume_tier+region cohorts.
    Lift the *pattern* (median comparable-store velocity + widening basis ladder);
    budget to rebuild the assembly. The "N slots" multiplier is a count with no analog
    in Void Finder (which accrues by void-weeks) and must be re-derived.
  - **No all-commodity volume in the SSOT** → true ACV-weighted shelf share cannot be
    sourced; use `volume_tier` (A/B/C) proxy and state it as a proxy.
  - **Canonical basis-labeling is mandatory:** every dollar names basis + period (e.g.
    "$32.3M retail scan (CY2025)"); **6 contracted retailers** (Walmart, Costco, Whole
    Foods, Sprouts, Kroger, Regional Group) — **not Wegmans**; 50 SKUs / 5 product
    lines. Canon is `cinderhaven-data-platform/reference/canonical_values.yml` /
    Postgres — never hardcode a figure from a README/constant/fixture.
- **Scope:** global (data layer)
- **Do not:** cite `CINDERHAVEN_CANONICAL.md` values (retired pointer); print a bare
  total without basis+period.

---

## Output Formats

[Decisions about deliverable formats, structure, organization]

---

## Writing & Voice / Naming

### 2026-08-25 — Name: Slot Math ships, Fair Share is the roadmap it grows into
- **Why:** The demo is allocation math, not category fair share, so "Fair Share"
  would over-claim on it. "Slot Math" fits the series pattern (Door Math, Spin Rate,
  Lift Math) and the honest claim, and is broad enough that client-mode category fair
  share still lives under it. Repo/directory stays `slotmath-fair-share`; the compound
  keeps both the shipping name and the roadmap concept.
- **Scope:** global (product name, copy, subdomain)
- **Do not:** name the subdomain before the name is final (it is now: slotmath);
  do not label the within-footprint demo "Fair Share" anywhere in copy.

---

## Reversed / Superseded

When a decision is overturned:
1. Strike through the original entry above (don't delete)
2. Add a new entry below with the replacement decision
3. Note the link in both directions

This preserves the history of why something is the way it is.
