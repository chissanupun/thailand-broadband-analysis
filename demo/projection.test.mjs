import assert from 'node:assert/strict';
import { project, nextQuarters } from './projection.js';

// exact 10%/quarter growth → fit recovers it, band collapses to the line
const vals = Array.from({ length: 12 }, (_, i) => 100 * 1.1 ** i);
const p = project(vals, 4);
assert.ok(Math.abs(p.points[0].mid - 100 * 1.1 ** 12) < 1e-6);
assert.ok(Math.abs(p.annualGrowth - (1.1 ** 4 - 1)) < 1e-9);
assert.ok(p.points[0].hi - p.points[0].lo < 1e-6);

// noisy series → band widens with horizon and contains the mid
const noisy = vals.map((v, i) => v * (i % 2 ? 1.08 : 0.93));
const q = project(noisy, 20).points;
assert.ok(q[0].lo < q[0].mid && q[0].mid < q[0].hi);
assert.ok(q[19].hi - q[19].lo > q[0].hi - q[0].lo);

assert.equal(project([1, 2, 3], 4), null);
assert.deepEqual(nextQuarters('2025-Q3', 3), ['2025-Q4', '2026-Q1', '2026-Q2']);
console.log('projection ok');
