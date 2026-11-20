// Log-linear trend (constant growth rate) with an 80% prediction interval.
// ponytail: 12 quarterly points → a 5-year line is extrapolation; shown as illustrative only.

const T90 = { 4: 1.533, 5: 1.476, 6: 1.440, 7: 1.415, 8: 1.397, 9: 1.383, 10: 1.372 }; // one-sided 0.90, df

export const MIN_POINTS = 6;

// values: Mbps per quarter in order (no gaps assumed). Returns null if too short.
export function project(values, horizon) {
  const n = values.length;
  if (n < MIN_POINTS) return null;
  const y = values.map(Math.log);
  const xm = (n - 1) / 2;
  const ym = y.reduce((a, b) => a + b, 0) / n;
  let sxx = 0, sxy = 0;
  for (let i = 0; i < n; i++) { sxx += (i - xm) ** 2; sxy += (i - xm) * (y[i] - ym); }
  const b = sxy / sxx, a = ym - b * xm;
  let sse = 0;
  for (let i = 0; i < n; i++) sse += (y[i] - (a + b * i)) ** 2;
  const s = Math.sqrt(sse / (n - 2));
  const t = T90[Math.min(n - 2, 10)];
  const out = [];
  for (let i = n; i < n + horizon; i++) {
    const fit = a + b * i;
    const half = t * s * Math.sqrt(1 + 1 / n + (i - xm) ** 2 / sxx);
    out.push({ mid: Math.exp(fit), lo: Math.exp(fit - half), hi: Math.exp(fit + half) });
  }
  return { points: out, annualGrowth: Math.exp(4 * b) - 1 };
}

export function nextQuarters(last, k) {
  let [yr, q] = last.split('-Q').map(Number);
  const out = [];
  for (let i = 0; i < k; i++) { q++; if (q > 4) { q = 1; yr++; } out.push(`${yr}-Q${q}`); }
  return out;
}
