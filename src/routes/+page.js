// The frozen data contract is imported at build time (S1 stub -> D1 real).
// Swapping data/slotmath.json is a file replacement, not a code change.
import slotmath from '$data/slotmath.json';

export function load() {
	return { slotmath };
}
