<script>
	// S1 skeleton: prove the frozen JSON renders. Views come in V1-V3.
	// S2: one instrumented CTA — the single on-page conversion event.
	let { data } = $props();
	const meta = data.slotmath.metadata;
	const cell = data.slotmath.cells[0];

	function fireCta() {
		// Param-less conversion event (DECISIONS 2026-08-26): no query string,
		// no selection state, no identifiers. Guarded — count.js loads async and
		// is absent under an adblocker.
		window.goatcounter?.count?.({
			path: 'cta_click',
			title: 'CTA click',
			event: true
		});
	}
</script>

<main>
	<h1>Slot Math — skeleton</h1>
	<p>Reads <code>data/slotmath.json</code> (schema v{meta.schema_version}).</p>
	<p data-testid="cell">
		{cell.retailer} / {cell.region} ({cell.retail_channel}) — index {cell.index}, gap
		{cell.gap_dollars}
	</p>
	<p>Basis: {meta.basis}</p>
	{#if meta.query_date === 'STUB'}
		<p><strong>⚠ STUB data</strong> — replaced by the D1 precompute.</p>
	{/if}

	<a class="cta" href="#engagement" onclick={fireCta}>
		See what the paid category engagement adds
	</a>

	<!-- Stub anchor for the CTA. F1 fills this with the described client-mode
	     roadmap panel (IRI/Circana/SPINS extract shapes). -->
	<section id="engagement">
		<p>Client-mode roadmap panel — built in F1.</p>
	</section>
</main>
