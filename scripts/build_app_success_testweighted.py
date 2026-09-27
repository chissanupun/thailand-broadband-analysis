"""Test-weighted app success rate (national scope), replaces the median-based
version from commit 64970b8 (Pakkapon, 2026-08-20).

Why replaced: reviewers (AINTEC '26, paper #51) flagged the old metric as not
a real pass rate (min(median/threshold, 1) x 100 is a ratio, not a share of
tests that pass) and cloud gaming never checked the 25ms latency requirement
that Table 1 itself lists. The old CSV also had no source script in the repo
and its numbers don't back-solve to any Ookla/NDT7 export here (see
docs/poster/poster_content.md, "Success-rate definition" note) -- dataset was
switched to Ookla fixed (reproducible, has per-province-quarter test counts
to weight by) as part of this fix, not just the formula. See
docs/paper/proposed-revisions-th.md item 1 and docs/poster/poster_content.md
for the decision trail.

Metric: pass rate = sum(test_count of province-quarters clearing the
threshold) / sum(test_count) x 100, national scope (all provinces, Ookla
fixed broadband, is_reliable rows only). Cloud gaming and voice also require
avg_lat_ms_wt under the app's latency threshold (Ookla latency, not NDT7 --
NDT7 servers are mostly offshore, see AINTEC NDT7 Offshore Servers memory /
proposed-revisions-th.md item 1).
"""
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPORTS = ROOT / 'data' / 'exports'
OUT_DIR = ROOT / 'outputs' / 'app_success_rate_testweighted'
OUT_DIR.mkdir(parents=True, exist_ok=True)

COUNTRY_FILE = {
    'Thailand': 'ookla_province_quarterly.csv',
    'Cambodia': 'ookla_cambodia_province_quarterly.csv',
    'Indonesia': 'ookla_indonesia_province_quarterly.csv',
    'Laos': 'ookla_laos_province_quarterly.csv',
    'Malaysia': 'ookla_malaysia_province_quarterly.csv',
    'Myanmar': 'ookla_myanmar_province_quarterly.csv',
    'Philippines': 'ookla_philippines_province_quarterly.csv',
    'Singapore': 'ookla_singapore_province_quarterly.csv',
    'Vietnam': 'ookla_vietnam_province_quarterly.csv',
}

# app -> (bandwidth threshold Mbps, latency threshold ms or None)
APPS = {
    'Voice': (0.064, 200),
    'Video HD': (5, None),
    'Video UHD': (25, None),
    'Cloud gaming': (44, 25),
}

rows = []
for country, fname in COUNTRY_FILE.items():
    df = pd.read_csv(EXPORTS / fname)
    df = df[df['is_reliable'] == True].copy()
    for quarter, g in df.groupby('quarter'):
        total_tests = g['total_tests'].sum()
        row = {'country': country, 'quarter': quarter, 'total_tests': int(total_tests)}
        for app, (bw_thr, lat_thr) in APPS.items():
            pass_mask = g['avg_d_mbps'] >= bw_thr
            if lat_thr is not None:
                pass_mask &= g['avg_lat_ms_wt'] <= lat_thr
            passed_tests = g.loc[pass_mask, 'total_tests'].sum()
            rate = 100.0 * passed_tests / total_tests if total_tests > 0 else float('nan')
            row[f'nat_{app}'] = round(rate, 4)
        rows.append(row)

out = pd.DataFrame(rows).sort_values(['country', 'quarter'])
out = out[out['quarter'].str.match(r'202[45]-Q[1-4]')]
out.to_csv(OUT_DIR / 'quarterly_app_success_testweighted.csv', index=False)
print(out.to_string())
print(f'\nwritten to {OUT_DIR / "quarterly_app_success_testweighted.csv"}')
