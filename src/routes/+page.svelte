<script>
	// Slot Math — single scrolling page, three view sections + shared CTA.
	//   #dollarizer (V1) · #index (V2) · #heatmap (V3 stub) · #engagement (CTA)
	let { data } = $props();
	const m = data.slotmath.metadata;
	const cells = data.slotmath.cells;

	const byGapDesc = (a, b) => Math.abs(b.gap_dollars) - Math.abs(a.gap_dollars);
	const over = cells.filter((c) => c.verdict === 'OVER').sort(byGapDesc); // all non-club (invariant)
	const under = cells.filter((c) => c.verdict === 'UNDER').sort(byGapDesc); // all Costco / club
	const inBand = cells.filter((c) => c.verdict === 'in-band');
	const hero = over[0];
	const overTotal = over.reduce((s, c) => s + Math.abs(c.gap_dollars), 0);
	const maxOver = Math.abs(over[0].gap_dollars);
	const maxUnder = Math.abs(under[0].gap_dollars);
	const allByIndex = [...cells].sort((a, b) => a.index - b.index); // ascending: under → over

	let showClub = $state(false);

	const usd0 = (n) => '$' + Math.round(Math.abs(n)).toLocaleString('en-US');
	const usdBig = (n) => {
		const a = Math.abs(n);
		return a >= 1e6 ? '$' + (a / 1e6).toFixed(2) + 'M' : '$' + Math.round(a / 1000) + 'K';
	};
	const pct1 = (x) => (x * 100).toFixed(1) + '%';
	// Boundary cells (within NEAR_EDGE of a band bound) show 3 decimals so two rows that
	// both round to 1.30 with opposite verdicts (Kroger SE 1.299 in-band, Sprouts SE 1.301
	// over) read as "right at the line", not a contradiction. Done-when requirement.
	const NEAR_EDGE = 0.015;
	const nearEdge = (x) => Math.abs(x - m.band_lower) < NEAR_EDGE || Math.abs(x - m.band_upper) < NEAR_EDGE;
	const idx = (x) => (nearEdge(x) ? x.toFixed(3) : x.toFixed(2));
	const gapSigned = (g) => (g >= 0 ? '+' : '−') + usd0(g);
	const vClass = (v) => (v === 'in-band' ? 'v-inband' : v === 'UNDER' ? 'v-under' : 'v-over');

	// Distribution strip scale
	const AXIS_MIN = 0.3;
	const AXIS_MAX = 1.9;
	const CW = 700;
	const PADL = 40;
	const PADR = 40;
	const xScale = (i) => PADL + ((i - AXIS_MIN) / (AXIS_MAX - AXIS_MIN)) * (CW - PADL - PADR);
	const stripColor = { UNDER: 'var(--ll-hk-35)', OVER: 'var(--ll-tokyo-40)', 'in-band': 'var(--ll-london-40)' };

	function fireCta() {
		window.goatcounter?.count?.({ path: 'cta_click', title: 'CTA click', event: true });
	}
</script>

<nav class="subnav">
	<div class="subnav-inner">
		<a href="#dollarizer">Dollarizer</a>
		<a href="#index">Index</a>
		<a href="#heatmap">Heatmap</a>
	</div>
</nav>

<div class="lailara-container">
	<!-- ═══ V1 · DOLLARIZER ═══════════════════════════════════════════════════ -->
	<section id="dollarizer">
		<div class="hero ll-column">
			<p class="eyebrow">Over-shelved · defensive intel</p>
			<p class="ll-headline-number hero-number">{usdBig(hero.gap_dollars)}</p>
			<h1 class="ll-section-title hero-find">
				of scan revenue sits behind more shelf than it earns — at {hero.retailer},
				{hero.region} region.
			</h1>
			<p class="hero-lede">
				At six retailer–region cells, your authorized shelf runs ahead of your scan sales.
				{hero.retailer}'s {hero.region} region leads: {pct1(hero.slot_share)} of your slots on
				{pct1(hero.dollar_share)} of your dollars — an index of {idx(hero.index)}. This is the
				number a category manager computes on their own syndicated data. See it first, and walk
				into the reset with the answer already in hand.
			</p>
		</div>

		<div class="block">
			<h2 class="ll-section-title">Where the shelf runs ahead of the sales</h2>
			<p class="subhead">
				Six conventional-grocery and mass cells, ranked by the scan revenue over-covered.
			</p>
			<div class="table-scroll">
				<table class="dollar-table" aria-label="Over-shelved cells by scan revenue over-covered">
					<thead>
						<tr>
							<th scope="col">Retailer · region</th>
							<th scope="col" class="num">Index</th>
							<th scope="col" class="num wide">Scan revenue over-covered</th>
						</tr>
					</thead>
					<tbody>
						{#each over as c (c.retailer + c.region)}
							<tr>
								<td>
									<span class="rr">{c.retailer}</span>
									<span class="region">· {c.region}</span>
									<span class="chip chip-{c.retail_channel}">{c.retail_channel}</span>
								</td>
								<td class="num">{idx(c.index)}</td>
								<td class="num bar-cell">
									<span class="bar-num">{usd0(c.gap_dollars)}</span>
									<span class="bar-track">
										<span class="bar-fill over" style="width:{(Math.abs(c.gap_dollars) / maxOver) * 100}%"></span>
									</span>
								</td>
							</tr>
						{/each}
					</tbody>
					<tfoot>
						<tr>
							<td>Total over-covered</td>
							<td class="num"></td>
							<td class="num">{usd0(overTotal)}</td>
						</tr>
					</tfoot>
				</table>
			</div>
			<p class="footnote">
				Basis: retail scan revenue (CY2025). Over-covered = the scan-revenue scale by which a
				cell's share of authorized slots exceeds its share of scan dollars (above the
				{m.band_upper} band). Cinderhaven Provisions, a synthetic dataset.
			</p>

			<aside class="crosslink">
				<span class="crosslink-label">Next</span>
				<p>
					Each over-shelved cell is a fix-or-kill question at the SKU level. The prepared answer
					lives in <a href="https://lailarallc.com" target="_blank" rel="noopener">SKU
					Rationalization</a> — which items in that door earn the space, and which to cut.
				</p>
			</aside>
		</div>

		<div class="block">
			<button class="disclosure" onclick={() => (showClub = !showClub)} aria-expanded={showClub}>
				{showClub ? '−' : '+'} Club channel (Costco) — {under.length} under-shelved cells
			</button>
			{#if showClub}
				<div class="club-panel">
					<p class="caveat">
						Costco is a club channel: few SKUs at high velocity. A low index here is
						<strong>club-normal</strong>, not a literal {(1 / under[0].index).toFixed(1)}×
						slot-expansion case. Shown for completeness, kept out of the headline on purpose.
					</p>
					<div class="table-scroll">
						<table class="dollar-table" aria-label="Costco under-shelved cells">
							<thead>
								<tr>
									<th scope="col">Retailer · region</th>
									<th scope="col" class="num">Index</th>
									<th scope="col" class="num wide">Scan revenue under-shelved</th>
								</tr>
							</thead>
							<tbody>
								{#each under as c (c.retailer + c.region)}
									<tr>
										<td>
											<span class="rr">{c.retailer}</span>
											<span class="region">· {c.region}</span>
											<span class="chip chip-club">club</span>
										</td>
										<td class="num">{idx(c.index)}</td>
										<td class="num bar-cell">
											<span class="bar-num">{usd0(c.gap_dollars)}</span>
											<span class="bar-track">
												<span class="bar-fill under" style="width:{(Math.abs(c.gap_dollars) / maxUnder) * 100}%"></span>
											</span>
										</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
				</div>
			{/if}
		</div>
	</section>

	<!-- ═══ V2 · INDEX ════════════════════════════════════════════════════════ -->
	<section id="index" class="block">
		<p class="eyebrow">The index · shelf vs. sales</p>
		<h2 class="ll-section-title index-verdict">
			Your shelf tracks your sales in {inBand.length} of {cells.length} cells. The other
			{under.length + over.length} miss — and they miss with a pattern.
		</h2>

		<div class="kpis">
			<div class="kpi kpi-under">
				<span class="kpi-n">{under.length}</span>
				<span class="kpi-l">under-shelved<br />all club (Costco)</span>
			</div>
			<div class="kpi kpi-inband">
				<span class="kpi-n">{inBand.length}</span>
				<span class="kpi-l">in band<br />0.7–1.3, proportional</span>
			</div>
			<div class="kpi kpi-over">
				<span class="kpi-n">{over.length}</span>
				<span class="kpi-l">over-shelved<br />grocery &amp; mass</span>
			</div>
		</div>

		<p class="index-lede">
			Costco is under-shelved in every region — club-normal, not an expansion order. The
			over-covered cells (Walmart, Sprouts, Regional Group) are where a category manager pushes
			back. Below: all {cells.length} retailer–region cells, ranked by index.
		</p>

		<!-- Distribution strip -->
		<figure class="strip">
			<figcaption class="chart-title">Where every cell falls</figcaption>
			<div class="strip-wrap">
				<svg viewBox="0 0 {CW} 108" class="strip-svg" role="img"
					aria-label="Index distribution: 5 club cells below the 0.7 band, 19 in band, 6 above 1.3">
					<!-- band -->
					<rect x={xScale(m.band_lower)} y="26" width={xScale(m.band_upper) - xScale(m.band_lower)}
						height="46" fill="var(--ll-london-95)" stroke="var(--ll-london-85)" stroke-width="1" />
					<!-- 1.0 reference -->
					<line x1={xScale(1)} x2={xScale(1)} y1="22" y2="76" stroke="var(--ll-london-40)"
						stroke-width="1" stroke-dasharray="2 3" />
					<!-- cell ticks -->
					{#each cells as c (c.retailer + c.region)}
						<line x1={xScale(c.index)} x2={xScale(c.index)} y1="30" y2="68"
							stroke={stripColor[c.verdict]} stroke-width="2.5" opacity="0.85" />
					{/each}
					<!-- axis labels -->
					<text x={xScale(m.band_lower)} y="90" text-anchor="middle" class="strip-lab">0.7</text>
					<text x={xScale(1)} y="90" text-anchor="middle" class="strip-lab">1.0</text>
					<text x={xScale(m.band_upper)} y="90" text-anchor="middle" class="strip-lab">1.3</text>
					<text x={xScale(AXIS_MIN)} y="90" text-anchor="start" class="strip-lab strip-lab-mute">0.3</text>
					<text x={xScale(AXIS_MAX)} y="90" text-anchor="end" class="strip-lab strip-lab-mute">1.9</text>
				</svg>
			</div>
			<div class="legend">
				<span class="lg lg-under">under-shelved</span>
				<span class="lg lg-inband">in band</span>
				<span class="lg lg-over">over-shelved</span>
			</div>
			<p class="footnote">
				Index = share of authorized slots ÷ share of scan dollars. The 0.7–1.3 band is shelf
				proportional to sales. n = {cells.length} retailer–region cells, CY2025.
			</p>
		</figure>

		<!-- 30-cell table -->
		<div class="table-scroll">
			<table class="dollar-table index-table" aria-label="All 30 cells ranked by index">
				<thead>
					<tr>
						<th scope="col">Retailer · region</th>
						<th scope="col" class="num col-footprint">Slots / sales</th>
						<th scope="col" class="num">Index</th>
						<th scope="col" class="num">Gap ($)</th>
					</tr>
				</thead>
				<tbody>
					{#each allByIndex as c (c.retailer + c.region)}
						<tr class={vClass(c.verdict)}>
							<td>
								<span class="rr">{c.retailer}</span>
								<span class="region">· {c.region}</span>
								<span class="chip chip-{c.retail_channel}">{c.retail_channel}</span>
							</td>
							<td class="num col-footprint footprint">{pct1(c.slot_share)} / {pct1(c.dollar_share)}</td>
							<td class="num idx-cell {vClass(c.verdict)}">
								{idx(c.index)}
								{#if nearEdge(c.index)}<span class="at-line">at the line</span>{/if}
							</td>
							<td class="num gap-cell {vClass(c.verdict)}">{gapSigned(c.gap_dollars)}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
		<p class="footnote">
			Gap ($) = scan-revenue scale of the mis-allocation; positive = under-shelved (expansion),
			negative = over-shelved. Sorted by index, low to high. Retail scan revenue, CY2025.
		</p>
	</section>

	<!-- ═══ V3 · HEATMAP (stub) ═══════════════════════════════════════════════ -->
	<section id="heatmap" class="block">
		<p class="eyebrow">Which door first</p>
		<h2 class="ll-section-title">Region × banner map</h2>
		<p class="index-lede">The "which door first" view — region × banner, colour-coded by gap. Coming.</p>
	</section>

	<!-- ═══ CTA / ENGAGEMENT ══════════════════════════════════════════════════ -->
	<section id="engagement" class="block cta-block">
		<a class="cta" href="#engagement" onclick={fireCta}>See what the paid category engagement adds</a>
		<p class="cta-note">Client mode — roadmap panel, coming.</p>
	</section>
</div>

<style>
	.lailara-container { color: var(--ll-london-20); }
	section[id] { scroll-margin-top: 118px; }

	/* Sub-nav */
	.subnav {
		position: sticky;
		top: var(--ll-nav-height);
		z-index: 40;
		background: var(--ll-canvas);
		border-bottom: 1px solid var(--ll-london-85);
	}
	.subnav-inner {
		max-width: var(--ll-max-width);
		margin: 0 auto;
		padding: 0 24px;
		display: flex;
		gap: 24px;
		height: 44px;
		align-items: center;
	}
	.subnav a {
		font-family: var(--ll-sans);
		font-size: 14px;
		font-weight: 600;
		color: var(--ll-london-35);
		text-decoration: none;
	}
	.subnav a:hover { color: var(--ll-chicago-20); }

	/* Hero */
	.hero { padding-top: 8px; }
	.eyebrow {
		font-family: var(--ll-sans);
		text-transform: uppercase;
		letter-spacing: 0.08em;
		font-size: 13px;
		font-weight: 600;
		color: var(--ll-red-42);
		margin: 0 0 12px;
	}
	.hero-number { color: var(--ll-london-5); margin: 0; }
	.hero-find { color: var(--ll-london-5); margin: 8px 0 16px; font-weight: 700; }
	.hero-lede {
		font-family: var(--ll-sans);
		font-size: 17px;
		line-height: 1.6;
		color: var(--ll-london-20);
		margin: 0;
	}

	/* Blocks / section rhythm */
	.block {
		margin-top: 48px;
		padding-top: 32px;
		border-top: 1px solid var(--ll-london-85);
	}
	.subhead {
		font-family: var(--ll-sans);
		font-size: 15px;
		color: var(--ll-london-35);
		margin: 6px 0 20px;
		max-width: var(--ll-body-max-width);
	}

	/* Table as chart (shared) */
	.table-scroll { overflow-x: auto; }
	.dollar-table {
		width: 100%;
		min-width: 460px;
		border-collapse: collapse;
		font-family: var(--ll-sans);
		font-size: 15px;
	}
	.dollar-table th, .dollar-table td {
		padding: 12px 12px;
		border-bottom: 1px solid var(--ll-london-85);
		text-align: left;
		vertical-align: middle;
	}
	.dollar-table thead th {
		font-size: 12px;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.04em;
		color: var(--ll-london-35);
		border-bottom: 1px solid var(--ll-london-40);
	}
	.dollar-table .num { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
	.dollar-table .wide { min-width: 220px; }
	.dollar-table tfoot td {
		font-weight: 700;
		color: var(--ll-london-5);
		border-bottom: none;
		border-top: 1px solid var(--ll-london-40);
	}
	.rr { font-weight: 600; color: var(--ll-london-5); white-space: nowrap; }
	.region { color: var(--ll-london-35); }
	.chip {
		display: inline-block;
		font-size: 11px;
		font-weight: 500;
		letter-spacing: 0.02em;
		padding: 1px 6px;
		margin-left: 6px;
		border-radius: var(--ll-radius);
		background: var(--ll-london-95);
		color: var(--ll-london-35);
		vertical-align: middle;
	}
	.chip-club { background: var(--ll-sg-95); color: var(--ll-sg-35); }

	.bar-cell { min-width: 200px; }
	.bar-num { display: block; margin-bottom: 5px; color: var(--ll-london-5); }
	.bar-track { display: block; width: 100%; height: 6px; background: var(--ll-london-90); border-radius: var(--ll-radius); }
	.bar-fill { display: block; height: 6px; border-radius: var(--ll-radius); }
	.bar-fill.over { background: var(--ll-tokyo-40); }
	.bar-fill.under { background: var(--ll-hk-35); }

	.footnote {
		font-family: var(--ll-sans);
		font-size: 11px;
		font-style: italic;
		color: var(--ll-london-35);
		margin: 14px 0 0;
		max-width: var(--ll-body-max-width);
	}

	/* Cross-link */
	.crosslink {
		display: flex;
		gap: 14px;
		align-items: baseline;
		margin-top: 24px;
		padding: 16px 18px;
		background: var(--ll-london-95);
		border-left: 3px solid var(--ll-chicago-20);
	}
	.crosslink-label {
		font-family: var(--ll-sans);
		text-transform: uppercase;
		letter-spacing: 0.06em;
		font-size: 12px;
		font-weight: 600;
		color: var(--ll-chicago-20);
		flex-shrink: 0;
	}
	.crosslink p { margin: 0; font-family: var(--ll-sans); font-size: 15px; line-height: 1.55; color: var(--ll-london-20); }
	.crosslink a { color: var(--ll-london-20); text-decoration: underline; }
	.crosslink a:hover { color: var(--ll-chicago-20); }

	/* Disclosure */
	.disclosure {
		font-family: var(--ll-sans);
		font-size: 15px;
		font-weight: 600;
		color: var(--ll-london-20);
		background: none;
		border: none;
		padding: 0;
		cursor: pointer;
	}
	.disclosure:hover { color: var(--ll-chicago-20); }
	.club-panel { margin-top: 16px; }
	.caveat {
		font-family: var(--ll-sans);
		font-size: 15px;
		line-height: 1.55;
		color: var(--ll-london-20);
		background: var(--ll-sg-95);
		border-left: 3px solid var(--ll-sg-55);
		padding: 12px 16px;
		margin: 0 0 16px;
		max-width: var(--ll-body-max-width);
	}

	/* ── V2 Index view ── */
	.index-verdict { color: var(--ll-london-5); margin: 8px 0 20px; max-width: var(--ll-body-max-width-wide); }
	.kpis { display: flex; gap: 16px; flex-wrap: wrap; margin: 0 0 20px; }
	.kpi {
		flex: 1 1 160px;
		padding: 14px 16px;
		background: var(--ll-london-95);
		border-top: 3px solid var(--ll-london-40);
	}
	.kpi-under { border-top-color: var(--ll-hk-35); }
	.kpi-over { border-top-color: var(--ll-tokyo-40); }
	.kpi-inband { border-top-color: var(--ll-london-40); }
	.kpi-n {
		display: block;
		font-family: var(--ll-serif);
		font-size: 34px;
		font-weight: 700;
		line-height: 1;
		color: var(--ll-london-5);
	}
	.kpi-l { display: block; font-family: var(--ll-sans); font-size: 13px; color: var(--ll-london-35); margin-top: 6px; line-height: 1.4; }
	.index-lede {
		font-family: var(--ll-sans);
		font-size: 17px;
		line-height: 1.6;
		color: var(--ll-london-20);
		margin: 0 0 24px;
		max-width: var(--ll-body-max-width);
	}

	/* Distribution strip */
	.strip { margin: 0 0 8px; }
	.chart-title { font-family: var(--ll-serif); font-size: 18px; font-weight: 700; color: var(--ll-london-5); margin: 0 0 8px; }
	.strip-wrap { width: 100%; }
	.strip-svg { width: 100%; height: auto; display: block; }
	:global(.strip-lab) { font-family: var(--ll-sans); font-size: 13px; fill: var(--ll-london-35); }
	:global(.strip-lab-mute) { fill: var(--ll-london-70); }
	.legend { display: flex; gap: 18px; margin: 6px 0 0; }
	.lg { font-family: var(--ll-sans); font-size: 12px; color: var(--ll-london-35); display: flex; align-items: center; }
	.lg::before { content: ''; width: 12px; height: 3px; margin-right: 6px; display: inline-block; }
	.lg-under::before { background: var(--ll-hk-35); }
	.lg-inband::before { background: var(--ll-london-40); }
	.lg-over::before { background: var(--ll-tokyo-40); }

	/* Index table — fits mobile (no bar column); scrolls not needed */
	.index-table { min-width: 0; }
	.index-table tbody tr { border-left: 3px solid transparent; }
	.index-table tbody tr.v-under { border-left-color: var(--ll-hk-35); }
	.index-table tbody tr.v-over { border-left-color: var(--ll-tokyo-40); }
	.index-table tbody tr.v-inband { border-left-color: var(--ll-london-85); }
	.index-table td:first-child { padding-left: 12px; }
	.footprint { color: var(--ll-london-35); font-size: 13px; }
	.idx-cell { font-weight: 600; }
	.idx-cell.v-under, .gap-cell.v-under { color: var(--ll-hk-20); }
	.idx-cell.v-over, .gap-cell.v-over { color: var(--ll-tokyo-30); }
	.idx-cell.v-inband { color: var(--ll-london-20); }
	.gap-cell.v-inband { color: var(--ll-london-35); }
	.at-line {
		display: block;
		font-size: 10px;
		font-weight: 400;
		font-style: italic;
		color: var(--ll-london-40);
		letter-spacing: 0.02em;
		margin-top: 2px;
	}

	/* CTA */
	.cta-block { text-align: left; }
	.cta {
		display: inline-block;
		background: var(--ll-chicago-20);
		color: #fff;
		font-family: var(--ll-sans);
		font-weight: 600;
		font-size: 15px;
		padding: 12px 22px;
		border-radius: var(--ll-radius);
		text-decoration: none;
	}
	.cta:hover { background: var(--ll-chicago-10); }
	.cta-note { font-family: var(--ll-sans); font-size: 13px; color: var(--ll-london-35); margin: 10px 0 0; }

	@media (max-width: 640px) {
		.dollar-table { font-size: 13px; }
		.dollar-table th, .dollar-table td { padding: 10px 8px; }
		.crosslink { flex-direction: column; gap: 6px; }
		.col-footprint { display: none; } /* Index table: drop the extra column on mobile — 3 cols fit 375, no wall */
		.kpi-n { font-size: 28px; }
	}
</style>
