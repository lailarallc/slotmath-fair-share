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
- [x] D2: Invariant test asserting the committed JSON: sum $32,323,140, 9,176 slots, 30
      cells, `Σgap$ = 0`, all 6 OVER cells non-Costco / all 5 UNDER cells Costco,
      `retail_channel` present on every cell. Wire into the CI gate.
    - Depends on: D1
    - Done when: test passes locally and in CI; flipping one cell's number fails it.
      ✅ `scripts/check-invariants.mjs` (77 assertions incl. canon $32,323,139.62/9,176,
      Σgap≈0, verdict↔band-bounds, UNDER⊆club/OVER∩club=∅). Negative-tested: catches a
      tampered cell. Wired as a CI `invariant` job that `deploy` **needs**. `npm run check`.

**Phase V — Views (each reads the frozen JSON; needs S1 + D1)**
- [x] V1: Dollarizer view — headline filters to non-club **OVER** cells (Walmart West
      −$736k, Regional NE 1.84, Sprouts West 1.34); Costco UNDER cells behind the
      "club-normal, not a 3× expansion case" flag; every $ labeled basis+period from
      JSON metadata; both directions shown. **The over-shelved list cross-links to the
      SKU Rationalization tool ("fix-or-kill is the prepared answer").**
    - Depends on: S1, D1
    - Done when: renders the OVER grocery/mass cells with gap$, Costco hidden behind a
      toggle, the over-shelved list links to SKU Rationalization, legible at 1440px & 375px.
      ✅ Built + deployed: hero ($736K Walmart West, 9.0%/6.7%, idx 1.34), 6-cell
      over-shelved table-as-chart (Tokyo bars, total $1.64M), Costco disclosure w/
      club-normal caveat, SKU-Rationalization cross-link, Lailara brand frame (vendored
      fonts+CSS). All colors are --ll-* tokens. ✅ Desktop QA passed (user), nits fixed
      (footnote "above the 1.3 band"; no internal task-id on prod), mobile 375px verified
      (table scrolls in its container, body no horizontal overflow, header intact).
- [x] V2: Index verdict + table — one banner line, one chart, per-cell table; continuous
      index value + gap$ (not just OVER/in-band bucket).
    - Depends on: S1, D1
    - Done when: 30-second-rule layout renders; a boundary cell (Kroger SE 1.299) reads
      "right at the line", at 1440px and 375px.
    - ✅ Built + deployed: verdict banner (19/30 in band; KPIs 5 under-all-club / 19 / 6
      over) + SVG index distribution strip (0.7–1.3 band, 30 verdict-coloured ticks, 1.0
      ref) + 30-cell table sorted by index, signed/coloured gap$, verdict left-border.
      Single scrolling page w/ sticky sub-nav; #heatmap stub added. **Mobile verified by
      DOM:** index table fits 375 (327px, no overflow), Slots/sales column hidden, no
      scroll wall, body no horizontal overflow. ⏳ Aesthetic eyeball (strip/KPI polish)
      pending user — pane can't screenshot this session.
- [x] V3: Heatmap qualifier map — region × banner grid, gap-$ colour ramp from
      `lailara_palette`, channel toggle, filter state in URL query params.
    - Depends on: S1, D1
    - Done when: grid renders; changing a filter updates the URL and a reload restores
      the same view; legible at 1440px and 375px.
    - ✅ Built + verified by DOM. Grid = semantic HTML `<table>` (banners × regions),
      not raw SVG — genuinely tabular, so more accessible (th headers, selectable text,
      colorblind-safe signed $) and reuses the `.table-scroll` mobile pattern; still
      hand-authored / no charting lib (honors the real DECISIONS lock). **Deliberate
      deviation from the "SVG grid" wording** — all done-when criteria met better this way.
      gap-$ ramp reuses V1/V2 semantics (tokyo=over, hk=under/club, grey=in-band, 3 tiers
      by |gap|). Channel toggle = anchor links (`/?channel=…#heatmap`) → SvelteKit client
      nav; URL is single source of truth, `afterNavigate` syncs `channel` client-side
      (prerender bakes neutral 'all' — a static page can't read the query). **Verified:**
      all tiers match frozen JSON; toggle click updates URL + grid; back button restores
      prior filter; deep-link/reload restores filtered view; 375px = 0 page overflow, table
      fits (327px, no wall), chips dropped; no console/hydration errors; 77 invariants hold.
      ✅ **User QA passed on prod (2026-08-27):** 30 tiles exact + signs + shading (incl. the
      Kroger SE −$382K-but-in-band grey call), URL round-trip (filter/back/deep-load) clean,
      1440 legible + Economist voice, club footnote drops in grocery view. 375 accepted on
      Code's DOM verification (0 overflow, 327px) — no mobile pixels this session (screenshots
      down; user's capture path can't resize a maximized window). One F2 cosmetic candidate
      logged (filter-reactive headline). Deployed green: run 33092368590, invariant + deploy
      both success.

**Phase F — Finish & integrate**
- [x] F1: Client-mode **described** roadmap panel — copy naming the IRI/Circana/SPINS
      extract shapes it will accept. No client-mode code.
    - Depends on: S1
    - Done when: panel renders with concrete extract-shape copy; nothing computes.
    - ✅ Built + verified by DOM. New `#roadmap` section between Heatmap and CTA: frames the
      upgrade from within-footprint index (what the demo showed) → **true category Fair Share**
      (your share of category slots ÷ your share of category sales, per door), the number a
      category manager adjudicates. Three extract-shape cards — (1) Category sales $ / units by
      retailer × region, (2) Distribution %ACV + TDP, (3) your share in the category — named as
      IRI / Circana / SPINS, grain retailer × region. Pure copy: **nothing computes** (footnote
      states it). Economist voice, honest-both-ways. Stale "roadmap panel, coming" CTA note
      removed; CTA href now → `#roadmap` (still fires `cta_click`). Verified: section order
      dollarizer→index→heatmap→roadmap→engagement, cards render + chicago border, 375px cards
      stack full-width 0 overflow, no console errors, build warning-free. ⏳ Prod pixels = user
      (screenshots down this session).
> **F2 polish candidates (decide at F2, do not build early):**
> - Mobile card-stack for the dollar tables (each cell a stacked card, $ visible without
>   horizontal scroll). Not built now — the hero delivers the headline $ without scroll,
>   so nothing's broken; building it today is speculative scope.
> - **Filter-reactive V3 heatmap headline** (user QA 2026-08-27, cosmetic — not a defect).
>   The heatmap headline is hard-wired to the global hero (Walmart West −$736K), but the
>   intro copy invites "the clean grocery story"; when filtered to Grocery, headline and
>   copy disagree. Fix: derive the headline cell from the *visible* channel's top
>   over-shelved cell (grocery → Sprouts West −$178K), so the lead tracks the filter.
>   `hero` today = global `over[0]`; make it `$derived` off `visibleBanners`/`channel`,
>   pick the max-|gap| OVER cell among visible banners, fall back to global hero when the
>   filter yields no OVER cell (e.g. Club → keep an under-shelved-framed line or the
>   channel-awareness note). Copy stays honest in every filter state. Cosmetic; not urgent.

- [x] F2: Full Lailara brand frame + copy/voice pass + the CTA closing state ("sell
      across 3+ regions and 2+ banner types? …") wired to the pre-registered metric.
      **Include one line of Spin Rate visual-pairing copy** (conceptual reference — which
      door + which items — no deep link; see DECISIONS 2026-08-26 recontextualization).
    - Depends on: V1, V2, V3, F1
    - Done when: passes the Deployed UI gate at 1440px and 375px; CTA closing state
      present; the Spin Rate pairing line is on the page.
    - ✅ Built + verified. Closing-state panel (qualifier "three or more regions and two or
      more channels" — reworded from "banner types" for page-vocabulary consistency) wraps the
      instrumented `cta_click` CTA. One conceptual Spin Rate "Pair with" aside, no deep link.
      Brand-frame finish: page `<title>` + meta description (tab title was blank); DS focus
      rings (2px London-5, offset 2px) on CTA / toggle / sub-nav / links. Copy/voice pass clean
      (no banned words, no exclamations, honest-both-ways). **Ran a 5-lens adversarial review
      workflow** (design-system / voice / a11y / responsive / spec-completeness) — spec lens
      returned zero gaps; applied 9 confirmed fixes: heatmap in-band tile London-95→85 (step-95
      forbidden as data fill) + swatch match; axis labels London-70→40 (was ~1.9:1, now 5.2:1
      AA); under-3 tile HK-35→20 (white was ~4.0:1, now 7.0:1 AA); chart-title 18→22/18;
      crosslink prose measure-capped; scroll-margin 118→126px; British→American spelling;
      `.closing` padding to grid. Gate: 1440 & 375 zero-overflow, console clean, 77 invariants
      hold. **One judgment item flagged to user (not applied):** the V1 hero "the number a
      category manager computes on their own syndicated data / walk into the reset with the
      answer in hand" — review reads it as over-claiming equivalence with the paid category
      number (roadmap reserves that). QA-passed V1 copy + core positioning → user's call.
- [x] B (integration): final deploy with all views; confirm the domain is Active and the
      GoatCounter `cta_click` event records on production; CI invariant test green.
    - Depends on: S3, D2, F2
    - Done when: `slotmath.lailarallc.com` serves the full 2.5-view demo, one production
      `cta_click` records, and the invariant CI job is green.
    - ✅ **CLOSED (2026-08-27, user-confirmed on the GoatCounter dashboard).** Full demo live
      end-to-end (all views verified on prod), production `cta_click` recorded as a q-free
      event from a filtered page, CI invariant green, domain Active. **B surfaced + fixed a
      pre-registered-rule violation** not in its original scope: GoatCounter's count.js was
      leaking the page query string (a visitor's `?channel=` filter) on BOTH the `cta_click`
      event (`q=location.search`) and the auto-pageview (path `pathname+search` + `q`). Fixed
      both via a `get_data` wrap (event) and `no_onload` + a manual query-free pageview
      (denominator kept alive — verified exactly 1 clean pageview beacon fires on prod). No
      custom beacon. See DECISIONS/FAILURES 2026-08-27. **The 2.5-view demo arc is complete.**

---

## Arc history

When an arc completes, archive its goal, completion date, and outcome
here. Then start a new arc above. Provides continuity without bloating
the active plan.

### 2026-08-27 — Ship the ~1-week 2.5-view Slot Math demo (Dollarizer / Index / Heatmap + roadmap + CTA)
- Outcome: **Shipped.** Full static SvelteKit demo live and rule-clean at
  `slotmath.lailarallc.com` — Dollarizer (over-shelved defensive intel), Index (verdict + 30-cell
  table), Heatmap qualifier map (banner × region, channel filter in the URL), F1 client-mode
  roadmap panel, F2 brand-frame finish + closing-state CTA + Spin Rate pairing. All 3 planning
  gates passed (data ✅ / product 🟡→resolved / eng 🟡→resolved); 11 build tasks (S1–S3, D1–D2,
  V1–V3, F1, F2, B) all complete. Frozen 30-cell JSON ($32,323,139.62 / 9,176 slots), CI invariant
  gate (77 assertions), org reusable deploy workflow. Instrumentation param-less on both beacon
  surfaces (query-leak found + fixed at B); GoatCounter `cta_click`/pageview threshold armed.
- Tag: **v0.1.0**
- Post-launch (2026-09-02): Max audit fixes deployed (proxy honesty line, SKU link, social
  meta + OG card, canon-verified data credit); repo made **public** (clean secret scan); added
  to the `MsShawnP` profile README (Sales-penetration table, top-line **43 tools / 34 live**).
  Project graduated `active/` → `published/`. **Launch fully closed.**

### [Date completed] — [Goal]
- Outcome: [what shipped or what was decided]
- Tag: [git tag if one was created]

---

## Improvement history

Track when this project was reviewed and improved via /improve.
Each entry records what was found, what was fixed, and when to
check again.

<!-- Entries are added by /improve — don't delete this section -->
