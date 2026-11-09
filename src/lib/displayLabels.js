// Public display labels for trade partners (rule decided 2026-11-05, lailara-website
// DECISIONS): a Cinderhaven dollar figure never sits beside a real retailer name.
// data/slotmath.json keeps the real names (frozen, provenance-stamped); only rendered
// text goes through here. The map is vendored from cinderhaven-data-platform
// (reference/retailer_display_labels.json); scripts/check_retailer_labels.py checks text.
import labels from '../../reference/retailer_display_labels.json';

const LABELS = new Map(
	[...Object.values(labels.retailers), ...Object.values(labels.distributors)].map((p) => [p.name, p.label])
);

/** Display label for a retailer name. Capitalized by default (table cell, row header,
 *  sentence start); pass false for mid-sentence use. Names not in the map pass through. */
export function retailerLabel(name, capitalize = true) {
	const label = LABELS.get(name) ?? name;
	return capitalize ? label.charAt(0).toUpperCase() + label.slice(1) : label;
}
