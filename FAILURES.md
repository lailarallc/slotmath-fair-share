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

### 2026-09-02 — Piping a generated image from the browser to disk was the wrong tool

**Attempted:** Generate the 1200×630 OG card by drawing it on a canvas in the browser
(brand fonts already loaded on prod), then `toDataURL('image/png')` and write the base64 to
`static/og-card.png`.

**Why it didn't work:** There is no path from a browser canvas to disk that doesn't route the
~109KB base64 through the model context — the sandbox blocks downloads, and I can't reproduce a
109KB string into a Bash/Write call without authoring it. The browser can render it but can't
hand it to the filesystem.

**What we tried instead:** Generated the PNG **directly on disk with Pillow** + the brand TTFs
(`data-hygiene-auditor/.../brand_fonts/PlayfairDisplay-Bold.ttf`, `SourceSans3-*.ttf`) — no
transfer, on-brand, 38KB. Lesson: to produce an image asset, draw it with Pillow (or another
on-disk generator) using the TTF brand fonts; use the browser only to *preview* it, never to
ferry bytes to disk.

**Status:** Resolved · **Tags:** og-card, image-generation, pillow, canvas, brand-fonts, ttf, browser-transfer

### 2026-09-02 — Read on `active/` paths failed: the project had moved to `published/`

**Attempted:** Start the audit-fix work by Reading `C:\Users\mssha\projects\active\slotmath-fair-share\src\app.html`.

**Why it didn't work:** The project had been **moved `active/` → `published/`** (it graduated
after v0.1.0 shipped). `active/slotmath-fair-share` no longer exists; the git repo (HEAD intact)
now lives at `published/slotmath-fair-share`, which was the cwd all along. Earlier in the same
session `active/` paths had worked, so the assumption carried until a Read failed.

**What we tried instead:** Verified reality — `pwd`, `git rev-parse` in both locations, confirmed
`published/` is the real repo (HEAD matched, prod deployed from it). Lesson: after a project may
have graduated, confirm cwd with one `pwd`/`git rev-parse` at the start rather than trusting a
remembered path — `active/` → `published/` is a fleet lifecycle move.

**Status:** Resolved · **Tags:** cwd, project-move, active-published, fleet-lifecycle, path-assumption

### 2026-08-27 — GoatCounter count.js leaked the page query string on BOTH the event and the pageview

**Attempted:** Fire the `cta_click` event with `window.goatcounter.count({ path: 'cta_click',
event: true })`, assuming an explicit `path` makes the beacon param-less (the pre-registered
instrumentation rule: never send the query string / channel filter).

**Why it didn't work:** count.js's `get_data` **hardcodes** `q: location.search` — there is no
`vars.q` override — so a visitor clicking from `?channel=grocery` sent `q=?channel=grocery`. The
**auto-pageview** leaked it twice: its path defaults to `pathname+search` AND it also sends `q`.
The F2 review lenses (static analysis) missed it; it only showed in the runtime beacon body, on
the first real click. Two surfaces, identical leak.

**What we tried instead:** Event — wrap `goatcounter.get_data` for the single `count()` call to
blank `q`, then restore (no custom beacon; that stays forbidden). Pageview — suppress the auto
count with `no_onload: true` (confirmed against the live count.js: `if (!goatcounter.no_onload)`
gates the whole auto-count block) and fire one query-free pageview ourselves (`p=location.pathname`,
`q=''`) so the rate **denominator stays alive**. Prod-verified: event q-free, exactly 1 clean
pageview beacon fires. See DECISIONS 2026-08-27 "GoatCounter query-suppression."

**Status:** Resolved · **Tags:** goatcounter, analytics, query-string, privacy, no_onload, get_data, beacon, pre-registered-rule

### 2026-08-27 — `vite preview` served stale builds until the server was restarted

**Attempted:** Rebuild (`npm run build`) then re-verify the deployed `build/` in the running
`vite preview` (started via `preview_start`), expecting the reload to show new output.

**Why it didn't work:** The running preview process kept serving the prior build — reloads and
cache-buster query params didn't refresh it. Cost several confusing "the fix didn't render"
loops before the cause was clear.

**What we tried instead:** `preview_stop` + `preview_start` after each rebuild guarantees a fresh
serve. Lesson: to verify a fresh SvelteKit build in the pane, restart the preview server, don't
just reload the tab.

**Status:** Resolved (workaround) · **Tags:** vite, preview, cache, sveltekit, build, verification

### 2026-08-27 — Reading `url.searchParams` in render broke the prerender build (V3)

**Attempted:** V3's channel filter derived state reactively from
`page.url.searchParams.get('channel')` (`$app/state`) inside the component render.

**Why it didn't work:** `prerender = true` forbids it — the build fails with
`Cannot access url.searchParams on a page with prerendering enabled`. A prerendered page
is baked once with no request, so it can't depend on the query string at render time.

**What we tried instead:** Keep the URL as the single source of truth, but read it
**client-side** — `channel` is a `$state` set by an `afterNavigate` callback
(`new URLSearchParams(location.search)`). Prerender bakes the neutral 'all' state; the
client syncs after every navigation (initial hydration, toggle clicks, back/forward).
Bonus: zero hydration mismatch (SSR/hydration both render 'all'; the client filters
post-mount). Promoted to a durable rule — see DECISIONS 2026-08-27.

**Status:** Resolved · **Tags:** sveltekit, prerender, url-state, searchparams, afternavigate, hydration

### 2026-08-26 — Browser-pane screenshots wouldn't composite (most of the session)

**Attempted:** `computer{action:"screenshot"}` to visually QA V1/V2 at 1440px and 375px.

**Why it didn't work:** "the Browser pane is not displayed, so the page is not compositing
frames." One fresh-tab capture succeeded early; every later attempt (fresh tabs included)
timed out. Environment/display issue, not the site.

**What we tried instead:** `javascript_tool` DOM + `getComputedStyle` checks — conclusive
on structure, data, and responsive behavior (table widths, `display:none`, body
overflow). Handed the aesthetic-only eyeball to the user, who screenshots reliably.

**Status:** Resolved (workaround) · **Tags:** browser, screenshot, compositing, qa, javascript_tool, dom

### 2026-08-26 — First S3 deploy failed: org secret invisible to a personal repo

**Attempted:** Deploy slotmath (still `MsShawnP/slotmath-fair-share`, personal) after the
token was set as a `lailarallc` **org** secret.

**Why it didn't work:** Org secrets only reach repos **inside** that org. A personal-account
repo can't read an org secret, so the credential guard failed fast ("CLOUDFLARE_API_TOKEN
is not set"). The guard worked — the token was in the wrong scope.

**What we tried instead:** Migrated slotmath into the `lailarallc` org; org secrets
(ALL-repos, Team plan) then resolved and it deployed green.

**Status:** Resolved · **Tags:** github, org-secrets, cloudflare, deploy, personal-vs-org, ci

### 2026-08-26 — Invariant negative-test /tmp backup broke on Windows

**Attempted:** In the D2 tamper-test, back up `data/slotmath.json` to `/tmp/sm.bak` (Python
`shutil.copy`) then restore with git-bash `cp /tmp/sm.bak`.

**Why it didn't work:** Windows Python resolves `/tmp` to `C:\tmp`; git-bash `/tmp` is a
different path. The restore couldn't find the backup and the data was left tampered.

**What we tried instead:** `git checkout -- data/slotmath.json` (the committed version is
the source of truth). Lesson: restore committed files via git, not a hand-rolled /tmp copy.

**Status:** Resolved · **Tags:** windows, tmp, git-bash, python, path, negative-test

### 2026-08-25 — Gate script printed to Windows cp1252 console and crashed on Unicode

**Attempted:** `analysis/readiness_gate.py` printed a report with `→`, `✅`, `×` etc.

**Why it didn't work:** Windows Python defaults stdout to cp1252; `UnicodeEncodeError`
on the first non-ASCII char after connecting + querying fine. **Fixed:**
`sys.stdout.reconfigure(encoding="utf-8")` at entry. **Recurs tomorrow** — the precompute
is a fresh script over the same console; add the reconfigure line first, or emit ASCII.

**Status:** Resolved  · **Tags:** windows, cp1252, unicode, stdout, encoding, python

### 2026-08-25 — Gate script connected to the wrong Postgres port

**Attempted:** Ran the gate with `flyctl proxy 5433:5432`; the script connected to 5432.

**Why it didn't work:** `load_env()` reads `POSTGRES_PROXY_PORT` from the SSOT `.env`
(=5432) before its own default, so it ignored the running proxy on 5433 → connection
refused. **Fixed:** `export SLOTMATH_PG_PORT=5433` to override. **Recurs tomorrow** — set
`SLOTMATH_PG_PORT` to match the proxy port every run, or start the proxy on 5432.

**Status:** Resolved  · **Tags:** flyctl, proxy, port, postgres, env, connection

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
