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
  per retailer × region) and the dollarized gap at the extremes (Void Finder
  comparable-velocity logic). **If spread is real** (roughly, banners outside
  0.7–1.3 with a dollarized gap worth a buyer conversation) → ship the
  within-footprint tool under the honest reframe. **If flat** → stop; the tool drops
  in priority or the category package becomes the entry price, decided then.
- **Scope:** global (gates all build work)
- **Do not:** massage a flat result into a demo.

---

## Visualization & Dollarization

### 2026-08-25 — Over-shelved case gets full symmetric dollarization, framed as defensive intel
- **Why:** Honest-both-ways is the product. Over-shelved = N over-slots × velocity ×
  margin = $/yr at-risk, shown at full size (never hidden). Framing requirement that
  answers the "arguing against its own user" worry: present it as *defensive intel*,
  never an indictment — copy frame "This is the number the buyer's category manager
  will compute eventually. See it first, walk in with the answer." Cross-link the
  over-shelved list to the SKU Rationalization tool (fix-or-kill is the prepared
  answer). Same logic as Lift Math showing its own error at full size.
- **Scope:** Dollarizer view + copy
- **Do not:** ship the unpriced-risk-line half-measure — a gestured-at number on a
  site whose pitch is "dollarized, not opinion" would be the fleet's first ungrounded
  claim.

### 2026-08-25 — Spin Rate cross-link: pre-registered rule, no undocumented coupling
- **Why:** Spin Rate is a Dash app and may expose no URL-addressable state. Rule
  stated before checking: **if** it exposes stable URL state (quadrant/item filters
  in the URL) → one-way deep link, params documented as a contract in **both** repos'
  DECISIONS **plus a CI link-check test here** that requests the target URL shape so a
  contract break fails loudly. **If not** → visual pairing now, and log "URL-state
  support" as Spin Rate's own roadmap item (becomes a one-line change here later).
- **Scope:** Heatmap / cross-tool links
- **Do not:** create an undocumented dependency on Spin Rate's URL schema (option 1
  is off the table either way).

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
