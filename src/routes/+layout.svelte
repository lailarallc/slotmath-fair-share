<script>
	// Lailara brand frame (vendored lailara-frame.css). Header + main + dark footer.
	let { children } = $props();
</script>

<div class="lailara-page">
	<header class="lailara-header">
		<nav class="lailara-nav-inner">
			<a href="https://lailarallc.com" class="lailara-wordmark" target="_blank" rel="noopener">Lailara LLC</a>
			<span class="lailara-tool-name">Slot Math</span>
		</nav>
	</header>

	<main class="lailara-main">
		{@render children()}
	</main>

	<footer class="lailara-footer">
		<div class="lailara-footer-inner">
			<p>Built by <a href="https://lailarallc.com" target="_blank" rel="noopener">Lailara LLC</a> — data hygiene and analytics consulting for specialty food brands scaling into national retail.</p>
			<p class="lailara-footer-note">
				Built on Cinderhaven synthetic data (50 SKUs, 6 retailers, 640 doors) — not a client.
				Figures are retail scan revenue, CY2025.
			</p>
		</div>
	</footer>
</div>
