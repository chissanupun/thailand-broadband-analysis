"""Statistical significance tests สำหรับ 9 ประเทศ SEA (Ookla fixed broadband)

1. Kruskal-Wallis omnibus: avg_d_mbps ต่างกันจริงข้ามประเทศไหม (province-quarter level)
2. Mann-Whitney U รายคู่ (36 คู่) + Holm correction
3. OLS: mean_dl ~ log(gdp_per_capita) + log(1+density) + C(country), province-clustered SE
4. Spearman: Ookla fixed vs NDT7 fixed UHD pass rate ข้ามประเทศ (cross-check ตัวเลขใน compendium)
"""
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests
import statsmodels.formula.api as smf
from pathlib import Path
from itertools import combinations

EXPORTS = Path(__file__).resolve().parent.parent / 'data' / 'exports'
OUT = Path(__file__).resolve().parent.parent / 'outputs' / 'stat_tests'
OUT.mkdir(parents=True, exist_ok=True)

FILES = {
    'Thailand':    'ookla_province_quarterly.csv',
    'Vietnam':     'ookla_vietnam_province_quarterly.csv',
    'Philippines': 'ookla_philippines_province_quarterly.csv',
    'Singapore':   'ookla_singapore_province_quarterly.csv',
    'Cambodia':    'ookla_cambodia_province_quarterly.csv',
    'Laos':        'ookla_laos_province_quarterly.csv',
    'Malaysia':    'ookla_malaysia_province_quarterly.csv',
    'Myanmar':     'ookla_myanmar_province_quarterly.csv',
    'Indonesia':   'ookla_indonesia_province_quarterly.csv',
}

frames = []
for country, fn in FILES.items():
    d = pd.read_csv(EXPORTS / fn)
    d = d[d['is_reliable'] == True].copy()
    d['country'] = country
    frames.append(d)
df = pd.concat(frames, ignore_index=True)

results = {}

# ---- 1. Kruskal-Wallis omnibus ----
groups = [df[df['country'] == c]['avg_d_mbps'].values for c in FILES]
h_stat, p_kw = stats.kruskal(*groups)
results['kruskal_wallis'] = {'H': h_stat, 'p': p_kw, 'n': len(df), 'k': len(FILES)}
print(f'Kruskal-Wallis: H={h_stat:.1f}, p={p_kw:.2e}, n={len(df)} province-quarters, k={len(FILES)} ประเทศ')

# ---- 2. Mann-Whitney U รายคู่ + Holm ----
pairs = list(combinations(FILES.keys(), 2))
rows = []
for a, b in pairs:
    ga = df[df['country'] == a]['avg_d_mbps'].values
    gb = df[df['country'] == b]['avg_d_mbps'].values
    u, p = stats.mannwhitneyu(ga, gb, alternative='two-sided')
    med_a, med_b = np.median(ga), np.median(gb)
    rows.append({'a': a, 'b': b, 'median_a': med_a, 'median_b': med_b, 'U': u, 'p_raw': p})
pw = pd.DataFrame(rows)
reject, p_holm, _, _ = multipletests(pw['p_raw'], alpha=0.05, method='holm')
pw['p_holm'] = p_holm
pw['sig_holm_0.05'] = reject
pw = pw.sort_values('p_raw')
pw.to_csv(OUT / 'mannwhitney_pairwise.csv', index=False)
n_sig = pw['sig_holm_0.05'].sum()
print(f'Mann-Whitney pairwise: {n_sig}/{len(pw)} คู่ significant หลัง Holm correction (alpha=0.05)')
not_sig = pw[~pw['sig_holm_0.05']]
print('คู่ที่ไม่ต่างกันอย่างมีนัยสำคัญ:')
for _, r in not_sig.iterrows():
    print(f"  {r['a']} (med={r['median_a']:.1f}) vs {r['b']} (med={r['median_b']:.1f}): p_holm={r['p_holm']:.3f}")

# ---- 3. OLS: mean_dl ~ log(gdp) + log(1+density) + C(country), province-clustered SE ----
prov = (df.groupby(['country', 'province'])
          .agg(mean_dl=('avg_d_mbps', 'mean'),
               gdp=('gdp_per_capita_thb_2021', 'first'),
               density=('density_per_km2', 'first'))
          .reset_index())
prov['log_gdp'] = np.log(prov['gdp'])
prov['log_density'] = np.log1p(prov['density'])
prov['province_id'] = prov['country'] + '_' + prov['province']

model = smf.ols('mean_dl ~ log_gdp + log_density + C(country)', data=prov)
fit = model.fit(cov_type='cluster', cov_kwds={'groups': prov['province_id']})
with open(OUT / 'ols_summary.txt', 'w') as f:
    f.write(str(fit.summary()))
print(f"\nOLS: n={int(fit.nobs)} จังหวัด (รวมทุกประเทศ), R2={fit.rsquared:.3f}")
print(f"  log_gdp: coef={fit.params['log_gdp']:.2f}, p={fit.pvalues['log_gdp']:.4f}")
print(f"  log_density: coef={fit.params['log_density']:.2f}, p={fit.pvalues['log_density']:.4f}")
results['ols'] = {
    'n': int(fit.nobs), 'r2': fit.rsquared,
    'coef_log_gdp': fit.params['log_gdp'], 'p_log_gdp': fit.pvalues['log_gdp'],
    'coef_log_density': fit.params['log_density'], 'p_log_density': fit.pvalues['log_density'],
}

# ---- 4. Spearman: Ookla fixed vs NDT7 fixed UHD pass rate ----
ndt7_files = {
    'Thailand':    'ndt7_broadband_thailand_reliable_province_quarterly.csv',
    'Vietnam':     'ndt7_broadband_vietnam_reliable_province_quarterly.csv',
    'Philippines': 'ndt7_broadband_philippines_reliable_province_quarterly.csv',
    'Singapore':   'ndt7_broadband_singapore_reliable_province_quarterly.csv',
    'Cambodia':    'ndt7_broadband_cambodia_reliable_province_quarterly.csv',
    'Laos':        'ndt7_broadband_laos_reliable_province_quarterly.csv',
    'Malaysia':    'ndt7_broadband_malaysia_reliable_province_quarterly.csv',
    'Myanmar':     'ndt7_broadband_myanmar_reliable_province_quarterly.csv',
    'Indonesia':   'ndt7_broadband_indonesia_reliable_province_quarterly.csv',
}
ookla_uhd = {}
for c in FILES:
    d = df[df['country'] == c]
    passed = (d['avg_d_mbps'] * d['total_tests'] >= 25 * d['total_tests'])
    ookla_uhd[c] = 100 * (d.loc[passed, 'total_tests'].sum() / d['total_tests'].sum())

speed_col_candidates = None
ndt7_uhd = {}
for c, fn in ndt7_files.items():
    p = EXPORTS / fn
    if not p.exists():
        continue
    d = pd.read_csv(p)
    d = d[d['is_reliable'] == True]
    passed = d['avg_d_mbps'] >= 25
    ndt7_uhd[c] = 100 * d.loc[passed, 'total_tests'].sum() / d['total_tests'].sum()

common = sorted(set(ookla_uhd) & set(ndt7_uhd))
if len(common) >= 3:
    x = [ookla_uhd[c] for c in common]
    y = [ndt7_uhd[c] for c in common]
    rho, p_sp = stats.spearmanr(x, y)
    print(f'\nSpearman (Ookla UHD% vs NDT7 UHD%, n={len(common)}): rho={rho:.2f}, p={p_sp:.4f}')
    results['spearman'] = {'rho': rho, 'p': p_sp, 'n': len(common), 'countries': common}
else:
    print(f'\nSpearman: หาไฟล์ NDT7 broadband ครบไม่พอ (เจอ {len(common)}/9) ข้ามส่วนนี้')

import json
with open(OUT / 'summary.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)
print(f'\nเขียนผลลง {OUT}')
