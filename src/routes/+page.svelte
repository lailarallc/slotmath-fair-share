<script>
	// V1 — Dollarizer. The over-shelved "defensive intel" view (build order #1).
	// Leads with clean grocery/mass cells; Costco (club) sits behind a channel flag.
	let { data } = $props();
	const m = data.slotmath.metadata;
	const cells = data.slotmath.cells;

	const byGapDesc = (a, b) => Math.abs(b.gap_dollars) - Math.abs(a.gap_dollars);
	const over = cells.filter((c) => c.verdict === 'OVER').sort(byGapDesc); // all non-club (invariant)
	const under = cells.filter((c) => c.verdict === 'UNDER').sort(byGapDesc); // all Costco / club
	const hero = over[0];
	const overTotal = over.reduce((s, c) => s + Math.abs(c.gap_dollars), 0);
	const underTotal = under.reduce((s, c) => s + Math.abs(c.gap_dollars), 0);
	const maxOver = Math.abs(over[0].gap_dollars);
	const maxUnder = Math.abs(under[0].gap_dollars);

	let showClub = $state(false);

	const usd0 = (n) => '$' + Math.round(Math.abs(n)).toLocaleString('en-US');
	const usdBig = (n) => {
		const a = Math.abs(n);
		return a >= 1e6 ? '$' + (a / 1e6).toFixed(2) + 'M' : '$' + Math.round(a / 1000) + 'K';
	};
	const pct1 = (x) => (x * 100).toFixed(1) + '%';
	const idx = (x) => x.toFixed(2);

	function fireCta() {
		// Param-less conversion event (DECISIONS 2026-08-26).
		window.goatcounter?.count?.({ path: 'cta_click', title: 'CTA click', event: true });
	}
</script>

<div class="lailara-container">
	<!-- Hero ─────────────────────────────────────────────────────────────── -->
	<section class="hero ll-column">
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
	</section>

	<!-- Over-shelved table-as-chart ────────────────────────────────────────── -->
	<section class="block">
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
			cell's share of authorized slots exceeds its share of scan dollars (index above
			{idx(m.band_upper)}). Cinderhaven Provisions, a synthetic dataset.
		</p>

		<!-- SKU Rationalization cross-link -->
		<aside class="crosslink">
			<span class="crosslink-label">Next</span>
			<p>
				Each over-shelved cell is a fix-or-kill question at the SKU level. The prepared answer
				lives in <a href="https://lailarallc.com" target="_blank" rel="noopener">SKU
				Rationalization</a> — which items in that door earn the space, and which to cut.
			</p>
		</aside>
	</section>

	<!-- Channel flag: club (Costco) under-shelved ──────────────────────────── -->
	<section class="block">
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
	</section>

	<!-- CTA / engagement ───────────────────────────────────────────────────── -->
	<section id="engagement" class="block cta-block">
		<a class="cta" href="#engagement" onclick={fireCta}>See what the paid category engagement adds</a>
		<p class="cta-note">Client-mode roadmap panel — built in F1.</p>
	</section>
</div>

<style>
	.lailara-container { color: var(--ll-london-20); }

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

	/* Table as chart */
	.table-scroll { overflow-x: auto; }
	.dollar-table {
		width: 100%;
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
	.rr { font-weight: 600; color: var(--ll-london-5); }
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

	/* SKU Rationalization cross-link */
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

	/* Channel-flag disclosure */
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
	}
</style>
