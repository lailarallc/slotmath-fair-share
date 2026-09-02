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

### 2026-09-02 — Data credit wording + canonical figures (Max audit)
- **Decision:** The on-page data credit is **"Built on Cinderhaven synthetic data (50 SKUs,
  6 retailers, 640 doors)"** + the standard Lailara footer tagline. The brand entity name is
  **"Cinderhaven Provisions"** — this **IS** canon (`canonical_values.yml:509` flags
  "Cinderhaven Foods" as the brand-name error and names "Cinderhaven Provisions" correct), so it
  is never dropped where the brand is named; the *dataset* credit uses "Cinderhaven synthetic
  data" (the fleet convention).
- **Why:** All three counts and the totals are canon-verified against
  `cinderhaven-data-platform/reference/canonical_values.yml`: 50 SKUs, 6 retailers, **640 doors**
  (stores_selling CY2025), $32,323,139.62 CY2025 revenue, 9,176 authorized store-SKUs — matching
  the frozen JSON to the cent. Global rule: all figures must match canon.
- **Scope:** on-page footer + footnotes; any future copy naming the dataset or the brand.
- **Do not:** drop "Provisions" (it is canon, not an error); do not assert the 50/6/640 figures
  from memory — they trace to `canonical_values.yml`; do not use "Cinderhaven Foods".

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
- **RESOLVED (eng gate, 2026-08-26):** superseded by the architecture cluster below.
  User released the reuse constraint ("choose the best tools to make it shine"), so the
  pick is on craft, not fleet consistency — it lands on the same framework the panel named.

### 2026-08-26 — Stack: SvelteKit static + hand-authored views (eng gate)
- **Decision:** **SvelteKit (Svelte 5) + `@sveltejs/adapter-static` + Vite**; **hand-authored
  views, no charting library — SVG where geometry demands it, semantic HTML where the form is
  tabular** (amended 2026-08-27, see below); light, purposeful motion; styled to the Lailara
  design system. Fully static output; the Heatmap's interactivity compiles away to static
  files (the "static vs. island" fork is a false choice).
- **Amendment 2026-08-27 (V3 build):** original wording said "all three views as hand-authored
  SVG." The lock's *substance* is **hand-authored, no charting library** — that stands. The
  medium is chosen per form: **SVG where geometry is continuous** (V2 index strip — a position
  scale), **semantic HTML where the form is a labeled grid or list** (V1 Dollarizer table, V3
  Heatmap banner × region matrix). HTML there is a *win*, not a compromise: real `<th>` headers,
  selectable values, colorblind-safe signed numbers, and the proven `.table-scroll` mobile
  pattern — all of which an SVG grid of `<rect>`+`<text>` would surrender for zero gain. Rule of
  thumb: continuous geometry → SVG; grid/tabular → HTML. Still no D3/Plotly, still no
  request-time compute.
- **Why:** best-in-class for a small, high-polish, data-forward microsite — near-zero
  runtime, total design control for the brand frame + 30-second read, smooth interaction.
  Charts follow the `dataviz` skill; polish follows `ce-frontend-design` + the Deployed UI
  gate (1440px & 375px).
- **Alternatives considered:** Observable Framework (great for data apps, but opinionated
  toward dashboards; fights a bespoke branded narrative + CTA funnel) — rejected;
  React/Next static export — rejected (heavier runtime, overkill for 30 frozen cells).
- **Do not:** add a charting lib (D3/Plotly) or any request-time compute.

### 2026-08-27 — URL-state on prerendered pages: client-side read via `afterNavigate`
- **Decision:** On a prerendered route (`prerender = true`), keep the URL the single source
  of truth for view/filter state, but read the query string **client-side** — a `$state`
  set from `new URLSearchParams(location.search)` inside an `afterNavigate` callback — and
  drive changes with plain anchor links (`/?channel=…#hash`). Never read `url.searchParams`
  (or `$page.url`) during render.
- **Why:** the prerender build hard-fails with `Cannot access url.searchParams on a page
  with prerendering enabled` — a baked page can't depend on a request-time query (see
  FAILURES 2026-08-27). The anchor-link + `afterNavigate` pattern keeps back-button and
  reload restore for free, and produces **zero hydration mismatch** because SSR/hydration
  both render the baked default (e.g. 'all') and the client only filters post-mount. Anchor
  links also need no `goto`/store imports and stay shareable.
- **Scope:** any prerendered view with filter/query state (V3 Heatmap channel filter today;
  future views).
- **Do not:** read `page.url.searchParams` / `$page.url` in render or a `$derived` on a
  prerendered route; don't reach for `goto` or navigation stores when a plain anchor +
  `afterNavigate` does the job.

### 2026-08-26 — Data flow: freeze-and-commit (INVERTED from Lift Math)
- **Decision:** SSOT (Fly Postgres, reachable only via interactive `flyctl auth` + proxy)
  → **precompute run LOCALLY once by a human who can auth** → emit a **provenance-stamped
  frozen JSON** (query date, window=CY2025, gate git SHA, schema-version) → **commit the
  JSON** → CI builds the front end from the committed JSON only (no DB, no proxy, no
  warehouse secret in CI) → deploy.
- **Why:** Lift Math regenerates gitignored JSON in CI because its source is a pip package
  CI can read; Slot Math's source is a live socket CI cannot reach, and the demo is a
  frozen CY2025 snapshot with no freshness requirement. Keep a documented `make data`
  refresh target that names the flyctl prerequisites.
- **Do not:** wire the DB/flyctl into `build.sh` or CI — it breaks every deploy.

### 2026-08-26 — Dollarization: ship the gate's first-order gap verbatim
- **Decision:** per cell, `gap$ = (dollar_share − slot_share) × Σscan$`, **signed**
  (+ = under-shelved / push-first; − = over-shelved / defensive-intel). Currency =
  comparable-store scan revenue (`dollars_sold`), **no margin**. Precompute to JSON.
  Invariant: `Σgap$ = 0`.
- **Why:** this is the gate-validated formula. Void Finder's median-comparable-velocity
  answers the *void* question, is strictly positive/additive, and structurally cannot
  express the negative-gap over-shelved lead case. Reconciliation with Void Finder is
  **dimensional** (same units), not numeric — the tools measure different things and
  *should* differ per cell.
- **Do not:** port Void Finder velocity machinery; do not type any dollar figure into
  prose — every $ names basis+period ("scan revenue · CY2025 · no margin") from the frozen
  file's metadata.

### 2026-08-26 — Channel-awareness: 3-value enum tagged at compute time
- **Decision:** tag each of the 30 cells with `retail_channel ∈ {club, mass, grocery}` at
  precompute time. `club` = Costco only (`retailer_id == 'RET-COSTCO'`); there is **no
  channel/format column** in the data, so this hardcoded one-retailer map is the source
  (do NOT reuse dbt `channel_type` — that's retailer/distributor/DTC, not retail format).
  3-value (not binary) so the headline can be honest: Walmart is **mass**, not "grocery".
- **Front end:** headline / Index verdict default-filters to non-club **OVER** cells (lead
  Walmart West −$736k, Regional NE 1.84, Sprouts West 1.34); all 5 Costco UNDER cells sit
  behind the channel flag labeled "club-normal, not a 3× expansion case". Render index as a
  **continuous value + gap$**, not only an OVER/in-band bucket (so boundary cells read as
  "right at the line").
- **Do not:** headline any Costco/club figure without the flag.

### 2026-08-26 — Instrumentation: ~~Plausible~~ → GoatCounter custom event + pre-registered threshold
- **Decision:** **GoatCounter** (free hosted, goatcounter.com) custom event `cta_click`,
  fired once, **param-less** (no query string, no selection state, no identifiers — the
  URL carries retailer/region/channel; never send it). Cookieless, no consent banner.
  Event API: `window.goatcounter.count({ path: 'cta_click', title: 'CTA click',
  event: true })` in the CTA click handler; add the GoatCounter script to `app.html`.
- **Switched from Plausible (2026-08-26):** Plausible cloud is **paid** ($9/mo after a
  30-day trial) — a recurring bill for one metric. GoatCounter's free hosted tier
  **explicitly permits small-to-medium business use**, is cookieless, and supports the
  same custom-event + pageview counts the metric needs. **Rejected Plausible self-hosted
  (CE):** requires Docker + ClickHouse + Postgres — Docker is broken on this machine
  ([[cinderhaven-ssot-connection]]) and a ClickHouse stack for one event is overkill.
  GoatCounter self-host (single Go binary + SQLite) is the free fallback if hosted traffic
  ever exceeds "reasonable" (it won't for this demo).
- **Pre-registered before deploy (same discipline as the data gate — UNCHANGED):**
  `cta_click_rate = unique cta_click ÷ unique pageviews`. **Min-sample guard:** no kill
  until ≥150 unique pageviews OR 8 weeks. **Rule:** ≥5% → funnel works, scale; 2–5% →
  iterate the page, re-measure; <2% at min-sample → the on-page qualifier→engagement
  hypothesis is falsified for this demo (stop optimizing; revisit whether a demo is a lead
  source). **Acceptance:** verify the event actually records in the DEPLOYED build before
  calling the demo done.
- **Do not:** ship the CTA as an uninstrumented `<a href>`; do not roll a custom beacon
  (that's request-time compute); do not add cookies or a consent banner.
- **Cloudflare zone-level Web Analytics RUM on lailarallc.com MUST stay Disabled
  (2026-08-26, corrected):** the source was **zone-level** RUM on the `lailarallc.com`
  zone entry — NOT the per-Pages-project toggle. Zone RUM edge-injects
  `static.cloudflareinsights.com/beacon.min.js` into **every property on the domain**
  (fleet-wide, not just slotmath), a **second tracker** the single-tracker, cookieless
  posture never sanctioned (verified injected on the live site 2026-08-26; the slotmath
  Pages-project toggle was already off and was never the source). Re-enabling zone RUM
  re-injects the unsanctioned tracker across the whole fleet. **Disable path:** Cloudflare
  → Web Analytics → Manage site (`lailarallc.com`) → **Disable**. Dashboard action; not
  disable-able from repo code or CLI without dashboard/token access. The per-project Pages
  toggle is **irrelevant** to this — do not treat it as the guard. **Now Disabled
  fleet-wide (2026-08-27, per Shawn's call);** beacon verified gone on a fresh load,
  GoatCounter intact as the single tracker.
- **Acceptance MET (2026-08-26):** live CTA click → POST `lailara.goatcounter.com/count?p=cta_click`
  → 200, event dashboard-confirmed; pageviews recording. S3 acceptance criterion closed.

### 2026-08-27 — GoatCounter query-suppression: strip the page query on BOTH the event and the pageview
- **Decision:** The param-less instrumentation rule (never send the `?channel=…` filter) is
  enforced with a specific mechanism that MUST stay in place:
  - **Event (`fireCta`, `+page.svelte`):** wrap `window.goatcounter.get_data` for the single
    `count()` call to set `d.q = ''`, then restore it in `finally`.
  - **Pageview (`app.html`):** set `window.goatcounter = { no_onload: true }` **before** count.js
    loads to suppress its auto-pageview, then fire ONE query-free pageview ourselves once count.js
    is ready (`p = location.pathname`, `q = ''`).
- **Why:** count.js **hardcodes** `q: location.search` in `get_data` (no `vars.q` override), and its
  auto-pageview path is `pathname+search` — so both surfaces leaked the channel filter on a
  deep-link arrival (FAILURES 2026-08-27). Verified on prod: event q-free; exactly **1** clean
  pageview beacon fires. Confirmed against the live count.js source that `if (!goatcounter.no_onload)`
  gates the entire auto-count block.
- **Scope:** GoatCounter instrumentation (this tool; the same trap applies to any fleet tool using
  count.js with URL state).
- **Do not:** remove `no_onload` and rely on the auto-pageview (it leaks `q` and re-adds `search`
  to the path); do not drop the `get_data` wrap from `fireCta`; do not "simplify" to a plain
  `count({path:'cta_click'})` (that reintroduces `q=location.search`); do not roll a custom beacon.
  If the manual pageview is ever removed, the rate **denominator dies** — always verify exactly one
  clean pageview beacon fires on prod after touching this.

### 2026-08-26 — Deploy: Cloudflare Pages, build-in-CI, project name `slotmath`
- **Decision:** Cloudflare Pages via GitHub Actions (build-in-CI so no token enters the
  build container), `wrangler pages deploy build --project-name=slotmath --branch=main`,
  main-only, gated on the invariant + deploy-guard jobs. **Project name & subdomain =
  `slotmath` EXPLICITLY** (not the repo name `slotmath-fair-share`). One-time **manual
  domain attach** of `slotmath.lailarallc.com` FIRST (no committed script exists);
  Cloudflare Git integration stays **OFF**. Vendor the engagement-template deploy-guard +
  `lailara-frame` (css/fonts) now; ship demo config only.
- **Why:** repo name contains the banned term — copying Lift Math's `--project-name=<repo>`
  leaks `fair-share` onto the shared `*.pages.dev` URL before the custom domain resolves.
- **Do not:** enable Git integration (bypasses the guard); do not rename the Pages project
  later (orphans its host).

### 2026-08-26 — Build order: RISK-first (walking skeleton before views)
- **Decision (supersedes the CEO gate's value-order for BUILD sequencing):**
  1. **Day-0 walking skeleton** — trivial static page off a stub JSON, deployed end-to-end
     to `slotmath.lailarallc.com` (manual domain attach here), deploy-guard vendored, Git
     integration OFF, and a **working instrumented CTA firing one recorded GoatCounter
     event in the deployed build**. Retires stack + deploy + domain + CTA + guard on day 1.
  2. **Freeze the data** — run the precompute locally (flyctl), emit the provenance-stamped
     30-cell JSON (per-cell gap$, signed index, `retail_channel`), commit it.
  3. **Invariant test** — assert JSON sums to $32,323,140, 9,176 slots, 30 cells, Σgap$=0,
     all 6 OVER cells non-Costco / all 5 UNDER cells Costco. Wire into CI.
  4. **View #1 — Dollarizer** (headline non-club OVER; Costco behind the flag; basis+period
     label on every $ from JSON metadata).
  5. **View #2 — Index verdict + table** (continuous index + gap$; 30-second layout).
  6. **View #3 — Heatmap qualifier map** (region × banner SVG grid, gap-$ color ramp from
     `lailara_palette`, URL-state in query params).
  7. **Client-mode described roadmap panel** (copy authoring; names the IRI/Circana/SPINS
     extract shapes) + final Deployed UI gate pass (1440px & 375px).
- **Why:** the CEO value-order is right for VALUE but wrong for RISK — all three views render
  off the same gate-validated JSON (analytic risk already retired), while the two
  zero-precedent items (CTA, live deploy + manual domain attach) must fail fast, not on day 6
  of a 1-week budget.

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
- **Recontextualized (2026-08-26, decompose):** the CEO reframe (demo = internal
  targeting + engagement-qualifier; Heatmap is the "which door first" qualifier map that
  needs no deep link) narrows this from "strongest buyer-deck slide" to **a lightweight
  conceptual pairing** — one line of copy in F2 ("which door + which items — pair with
  Spin Rate"). It survives, recontextualized; it is NOT dropped and NOT a deep link.

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

### 2026-08-26 — Frozen JSON data contract (`data/slotmath.json`, S1/D1)
- **Decision:** one committed file is the single source for all three views + the D2
  invariant. Shape:
  - `metadata`: `query_date`, `window` ("CY2025"), `window_start` (2024-12-28),
    `window_end` (2025-12-27), `gate_git_sha`, `schema_version`, `total_slots` (9176),
    `total_dollars` (32323140.xx, full precision), `band_lower` (0.7), `band_upper`
    (1.3), `gap_sign` (documented convention), `basis` (display), `basis_note`
    (provenance).
  - `cells[30]`: `retailer`, `region`, `retail_channel ∈ {club,mass,grocery}`, `slots`,
    `dollars`, `slot_share`, `dollar_share`, `index`, `gap_dollars`, `verdict`.
- **Four rules (from schema-freeze review):**
  1. **Store full precision** — `dollars`/`gap_dollars` at 2 decimals (as the gate CSV),
     `slot_share`/`dollar_share`/`index` at full float. **Round only in the view layer.**
     The D2 invariant is **exact** (Σdollars = 32323140.xx, Σgap = 0), never toleranced.
  2. **Bounds live in metadata** (`band_lower`/`band_upper`) — views and D2 read them;
     never hardcode 0.7/1.3 in view code.
  3. **Sign convention documented in the file** (`gap_sign`: "positive = under-shelved
     (expansion $); negative = over-shelved"); views must never re-derive it.
  4. **Basis is split** — `basis` = "retail scan revenue (CY2025)" (printable, public);
     `basis_note` = "revenue basis, no margin step — fleet Dollar Authority decision"
     (provenance only). "no margin" is internal methodology language — never a public label.
- **Naming:** `gap_dollars` (not `gap_$`). `units` from the gate CSV is **dropped** — no
  view or D2 reads it.
- **Do not:** round in the file; hardcode band bounds or the sign in a view; print
  `basis_note` on a public surface.

---

## Output Formats

### 2026-08-26 — Single scrolling page + sticky sub-nav (not a tab SPA) — LOCKED
- **Why:** The three views are sections of one prerendered page with a sticky anchor
  sub-nav (Dollarizer / Index / Heatmap) + stub sections for not-yet-built views. **Locked
  at the page-vs-tabs gate (2026-08-26):** the CEO gate fixed a funnel order (defensive
  intel → verdict → qualifier map → CTA closing state); one page preserves that read, tabs
  fragment it. Tabs' one edge (a clean per-view meeting screen) is ~90% covered by anchor
  links. **V3's Heatmap filters go in query params on top of `#heatmap`** (back-button
  friendly) — not a routing layer.
- **Scope:** front-end structure
- **Do not:** convert to a tab SPA; do not add a dangling anchor to a not-yet-built section
  (SvelteKit prerender fails on it) — add a stub section first, as `#engagement`/`#heatmap` do.

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

## Build sequence & demo scope (CEO gate, 2026-08-25)

The product gate returned **Revise** (fundable; 5 pre-build fixes). All resolved below.

### 2026-08-25 — Costco/club cells demoted from the headline (channel-awareness)
- **Why:** The widest number ($1.22M Costco West) is one we distrust as a club-channel
  artifact (clubs carry few SKUs at huge velocity → low slot-share/high dollar-share is
  club-normal, not a 3× expansion case). Leading a trust-building tool with a
  walk-back-required headline is an unforced credibility hit that compounds across all 7
  tools.
- **Decision:** Lead Index verdict + Dollarizer with the clean over-shelved
  **conventional-grocery** cells (Walmart West −$736k, Regional NE 1.84, Sprouts West
  1.34). Club cells appear only behind an explicit channel-awareness flag ("club-normal —
  not a 3× slot-expansion case"); if channel-awareness can't ship in scope, exclude club
  cells from the headline rather than caveat in place.
- **Do not:** headline any Costco/club figure without the channel flag.

### 2026-08-25 — Build order by value; demo is 2.5 views
- **Why:** The plan's own "one genuinely meeting-ready output" (the over-shelved
  defensive-intel $) was buried behind Index + symmetric dollarization + a payload-free
  Heatmap. Build the useful thing first.
- **Decision — build order:** (1) **Over-shelved defensive-intel Dollarizer**, (2) **Index
  verdict + table**, (3) **Heatmap** — kept, but **repurposed as the "which door first"
  qualifier map**: region × banner grid color-coded by dollarized gap $. It stops being
  decoration the moment it's the qualifier's map (no Spin Rate deep link needed).
- **Scope:** "2.5-view" demo (Index, Dollarizer, payload Heatmap).
- **Do not:** ship the Heatmap as a bare index grid with no gap-$ payload.

### 2026-08-25 — Success metric: one on-page instrumented conversion event
- **Why:** "Converts to paid syndicated engagement" is unfalsifiable on a public demo —
  the true qualifier needs the visitor's own Circana/SPINS data, which they lack at demo
  time. Without one instrumented event, a no-conversion post-mortem has zero data.
- **Decision:** Add a visitor-actionable **closing state** ("sell across 3+ regions and
  2+ banner types? your within-footprint spread is wide enough that category data moves
  real dollars — here's what that engagement produces") + **one instrumented CTA click**
  that names the paid engagement = the single on-page conversion event, with an
  iterate/kill threshold. "Converts to paid engagement" stays the off-site outcome, not
  the on-page metric.
- **Do not:** set the shipped metric to anything the artifact can't observe.

### 2026-08-25 — Client mode: describe now, build at first qualified engagement
- **Why:** Nobody exercises client mode at demo time (needs prospect-brought
  IRI/Circana/SPINS). Building intake for data no client has handed over is speculative
  scope. Fleet precedent: Void Finder shipped demo-only first and grew client mode in
  place when the need was real; the first engagement pays for building it.
- **Decision:** Ship the demo; present client mode as a **described roadmap panel** that
  names exactly what it will accept (IRI/Circana/SPINS extract shapes) so the promise is
  concrete. Client-mode code builds at the first qualified engagement.
- **Scope:** estimate drops to **~1 week** for the 2.5-view demo (gate already PASSED).
- **Do not:** build engagement-template intake / category-fair-share compute pre-engagement.
- **Supersedes:** the earlier "~1–1.5 weeks incl. client mode" estimate.

### 2026-08-25 — Top-line framing resolves the two-identity problem
- **Why:** The headline business question still read buyer-facing ("is our shelf presence
  proportional") while the locked positioning is internal targeting/qualifier — an outsider
  couldn't tell who sits in front of it.
- **Decision:** Make the two **internal jobs** the top-line ("Which door do we push
  first?" and "Is our spread wide enough to justify buying category data?"); the verdict
  banner answers those. Keep the buyer-facing "fair share / proportional shelf" framing
  explicitly labeled as the **client-mode roadmap upgrade**, not the demo's headline.
- **Note:** aligns the artifact to the already-locked positioning; does not reopen it.

### 2026-08-27 — cinderhaven-promo-response v0.5.0 is a no-op for slotmath; keep the frozen snapshot
- **Decision:** slotmath keeps its frozen, provenance-stamped JSON unchanged through
  promo-response v0.5.0. Verified on both sides: that package never reads or writes
  `raw.scan_data` / `raw.distribution_log` (its criterion 11, AST-denylist tested), and
  slotmath's analysis scripts (`readiness_gate.py`, `precompute.py`) read only
  `raw.scan_data`, `raw.distribution_log`, `raw.stores` — zero references to the
  package's overlay namespace (`promo_events` / `promo_scan_delta` / `promo_scan_truth`)
  anywhere in this repo (grep-verified 2026-08-27, by the Cowork advisor).
- **Why:** v0.5.0 moved only that package's additive overlay artifacts. Canonical
  trailing-52-week scan revenue — $32,323,139.62 unrounded; **$32,323,140** as asserted
  by slotmath's invariant — is untouched by construction. The frozen JSON's inputs are
  byte-identical before and after v0.5.0, so re-freezing would reproduce identical
  numbers: the snapshot stands on unchanged provenance, not on a launch-clock tradeoff.
- **Revisit only:** at the first client-mode engagement, or if slotmath ever begins
  consuming the overlay namespace.

---

## Reversed / Superseded

When a decision is overturned:
1. Strike through the original entry above (don't delete)
2. Add a new entry below with the replacement decision
3. Note the link in both directions

This preserves the history of why something is the way it is.
