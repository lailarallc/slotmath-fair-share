<script>
	// S1 walking skeleton: prove the frozen JSON renders. Views come in V1-V3.
	let { data } = $props();
	const meta = data.slotmath.metadata;
	const cell = data.slotmath.cells[0];
</script>

<main>
	<h1>Slot Math — S1 skeleton</h1>
	<p>Reads <code>data/slotmath.json</code> (schema v{meta.schema_version}).</p>
	<p data-testid="cell">
		{cell.retailer} / {cell.region} ({cell.retail_channel}) — index {cell.index}, gap
		{cell.gap_dollars}
	</p>
	<p>Basis: {meta.basis}</p>
	{#if meta.query_date === 'STUB'}
		<p><strong>⚠ STUB data</strong> — replaced by the D1 precompute.</p>
	{/if}
</main>
