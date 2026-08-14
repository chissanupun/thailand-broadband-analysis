"""สร้างรูปเพิ่มสำหรับ RQ1 กับ RQ2 — 8 ประเทศ ตัดสิงคโปร์ รวมอินโดนีเซีย

ต่อจาก build_cross_country_figs_8c.py ซึ่งสร้างรูปที่ 1 กับ 2 ของ results_th.md
ตัวนี้เติมรูปที่ยังขาด อ่านจาก data/exports จริงทั้งหมด ไม่ hardcode ตัวเลข

ที่สร้าง:
  02_all_country_mobile_dl.png  ความเร็วมือถือรายประเทศ (RQ1)
  05_fixed_vs_mobile.png        fixed เทียบ mobile รายประเทศ (RQ1)
  06_province_spread.png        การกระจายรายจังหวัดในแต่ละประเทศ (RQ1)
  07_growth_trajectory.png      เส้นการเติบโตรายไตรมาส 2023-Q1 ถึง 2025-Q4 (RQ2)
  08_growth_vs_base.png         โตเร็วแค่ไหน เทียบกับฐานที่เริ่ม (RQ2)
  09_capital_vs_top5.png        เมืองหลวงเทียบ 5 จังหวัดที่เร็วสุด (RQ1)

หมายเหตุ capital_top5_comparison.csv ใน data/exports ใช้ไม่ได้ — เป็นไฟล์ยุค 9 ประเทศ
มีสิงคโปร์และไม่มีอินโดนีเซีย รูปที่ 09 จึงคำนวณใหม่จาก province_quarterly โดยตรง
"""
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPORTS = ROOT / 'data' / 'exports'
OUT = ROOT / 'outputs' / 'ookla' / 'cross_country'
OUT.mkdir(parents=True, exist_ok=True)

FIXED = {
    'Thailand':    'ookla_province_quarterly.csv',
    'Vietnam':     'ookla_vietnam_province_quarterly.csv',
    'Philippines': 'ookla_philippines_province_quarterly.csv',
    'Cambodia':    'ookla_cambodia_province_quarterly.csv',
    'Laos':        'ookla_laos_province_quarterly.csv',
    'Malaysia':    'ookla_malaysia_province_quarterly.csv',
    'Myanmar':     'ookla_myanmar_province_quarterly.csv',
    'Indonesia':   'ookla_indonesia_province_quarterly.csv',
}

MOBILE = {
    'Thailand':    'ookla_mobile_province_quarterly.csv',
    'Vietnam':     'ookla_mobile_vietnam_province_quarterly.csv',
    'Philippines': 'ookla_mobile_philippines_province_quarterly.csv',
    'Cambodia':    'ookla_mobile_cambodia_province_quarterly.csv',
    'Laos':        'ookla_mobile_laos_province_quarterly.csv',
    'Malaysia':    'ookla_mobile_malaysia_province_quarterly.csv',
    'Myanmar':     'ookla_mobile_myanmar_province_quarterly.csv',
    'Indonesia':   'ookla_mobile_indonesia_province_quarterly.csv',
}

CAPITALS = {
    'Thailand':    'Bangkok Metropolis',
    'Vietnam':     'Hà Nội',
    'Philippines': 'NCR',
    'Cambodia':    'Phnom Penh',
    'Laos':        'Vientiane Capital',
    'Malaysia':    'Kuala Lumpur',
    'Myanmar':     'Yangon',
    'Indonesia':   'Jakarta',
}

BLUE, ORANGE, GREY = '#0072B2', '#D55E00', '#999999'


def load(files):
    frames = []
    for country, fn in files.items():
        d = pd.read_csv(EXPORTS / fn)
        d = d[d['is_reliable'] == True].copy()
        d['country'] = country
        frames.append(d)
    return pd.concat(frames, ignore_index=True)


def weighted(g):
    return (g['avg_d_mbps'] * g['total_tests']).sum() / g['total_tests'].sum()


fx = load(FIXED)
mb = load(MOBILE)

nat_fx = fx.groupby('country').apply(weighted, include_groups=False).sort_values(ascending=False)
nat_mb = mb.groupby('country').apply(weighted, include_groups=False)
order = list(nat_fx.index)

# ---- 02 ความเร็วมือถือรายประเทศ ----
mb_sorted = nat_mb.sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(9.5, 5.5))
bars = ax.bar(mb_sorted.index, mb_sorted.values, color=ORANGE)
for b, v in zip(bars, mb_sorted.values):
    ax.text(b.get_x() + b.get_width() / 2, v + 1, f'{v:.0f}', ha='center', fontsize=9)
ax.set_ylabel('Mean download (Mbps), test-weighted')
ax.set_title('Mobile mean download by country — 8 countries, Q1 2023–Q4 2025',
             fontsize=12, fontweight='bold')
ax.set_ylim(0, mb_sorted.max() * 1.15)
ax.spines[['top', 'right']].set_visible(False)
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
fig.savefig(OUT / '02_all_country_mobile_dl.png', dpi=150)
plt.close(fig)
print(f'02 mobile: สูงสุด {mb_sorted.index[0]} {mb_sorted.iloc[0]:.1f} · '
      f'ต่ำสุด {mb_sorted.index[-1]} {mb_sorted.iloc[-1]:.1f} · '
      f'ต่างกัน {mb_sorted.max()/mb_sorted.min():.1f} เท่า')

# ---- 05 fixed เทียบ mobile ----
x = range(len(order))
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.bar([i - 0.2 for i in x], [nat_fx[c] for c in order], width=0.4, color=BLUE, label='Fixed broadband')
ax.bar([i + 0.2 for i in x], [nat_mb[c] for c in order], width=0.4, color=ORANGE, label='Mobile')
for i, c in enumerate(order):
    ax.text(i, max(nat_fx[c], nat_mb[c]) + 5, f'{nat_fx[c]/nat_mb[c]:.1f}×',
            ha='center', fontsize=9, color=GREY)
ax.set_xticks(list(x))
ax.set_xticklabels(order, rotation=30, ha='right')
ax.set_ylabel('Mean download (Mbps), test-weighted')
ax.set_title('Fixed vs mobile mean download — 8 countries (label = fixed/mobile ratio)',
             fontsize=12, fontweight='bold')
ax.spines[['top', 'right']].set_visible(False)
ax.legend()
plt.tight_layout()
fig.savefig(OUT / '05_fixed_vs_mobile.png', dpi=150)
plt.close(fig)
print('05 fixed/mobile ratio: ' + ' · '.join(f'{c} {nat_fx[c]/nat_mb[c]:.1f}×' for c in order))

# ---- 06 การกระจายรายจังหวัด ----
def prov_stats(x):
    return pd.Series({'mean_dl': (x['avg_d_mbps'] * x['total_tests']).sum() / x['total_tests'].sum(),
                      'n_tests': x['total_tests'].sum()})


prov = (fx.groupby(['country', 'province'])
          .apply(prov_stats, include_groups=False)
          .reset_index())
prov['test_share'] = prov['n_tests'] / prov.groupby('country')['n_tests'].transform('sum')
data = [prov.loc[prov['country'] == c, 'mean_dl'].values for c in order]
fig, ax = plt.subplots(figsize=(10, 5.5))
bp = ax.boxplot(data, tick_labels=order, showfliers=True, patch_artist=True,
                medianprops=dict(color='black', linewidth=1.6),
                flierprops=dict(marker='o', markersize=3, alpha=0.5))
for patch in bp['boxes']:
    patch.set_facecolor(BLUE)
    patch.set_alpha(0.55)
for i, c in enumerate(order):
    ax.scatter([i + 1], [nat_fx[c]], marker='D', color=ORANGE, zorder=4, s=42,
               label='National mean (test-weighted)' if i == 0 else None)
ax.set_yscale('log')
ax.set_ylabel('Province mean download (Mbps), log scale')
ax.set_title('Within-country spread of provincial fixed download — 8 countries',
             fontsize=12, fontweight='bold')
ax.spines[['top', 'right']].set_visible(False)
ax.legend()
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
fig.savefig(OUT / '06_province_spread.png', dpi=150)
plt.close(fig)
print('06 spread (min–max รายจังหวัด, เท่า):')
for c in order:
    v = prov.loc[prov['country'] == c, 'mean_dl']
    print(f'  {c:12s} n={len(v):3d}  {v.min():6.1f} – {v.max():6.1f}  = {v.max()/v.min():.1f}×')

# ---- 07 เส้นการเติบโตรายไตรมาส ----
traj = (fx.groupby(['country', 'quarter'])['avg_d_mbps'].median().reset_index())
quarters = sorted(traj['quarter'].unique())
fig, ax = plt.subplots(figsize=(10, 5.5))
cmap = plt.get_cmap('tab10')
ends = {}
for i, c in enumerate(order):
    s = traj[traj['country'] == c].set_index('quarter').reindex(quarters)['avg_d_mbps']
    ax.plot(quarters, s.values, marker='o', markersize=3.5, linewidth=1.8,
            color=cmap(i), label=c)
    ends[c] = (s.iloc[-1], cmap(i))

# กันป้ายชื่อทับกันตรงปลายเส้น ประเทศกลุ่มล่างค่าใกล้กันมาก
span = max(v for v, _ in ends.values()) - min(v for v, _ in ends.values())
min_gap = span * 0.045
label_y = None
for c, (v, col) in sorted(ends.items(), key=lambda kv: -kv[1][0]):
    label_y = v if label_y is None else min(v, label_y - min_gap)
    ax.annotate(c, (len(quarters) - 1, v), xytext=(len(quarters) - 0.7, label_y),
                fontsize=8, color=col, va='center',
                arrowprops=dict(arrowstyle='-', color=col, lw=0.6, alpha=0.6))
ax.set_ylabel('Median provincial download (Mbps)')
ax.set_title('Fixed broadband growth, Q1 2023 – Q4 2025 — median province',
             fontsize=12, fontweight='bold')
ax.spines[['top', 'right']].set_visible(False)
ax.set_xlim(-0.4, len(quarters) + 2.2)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
fig.savefig(OUT / '07_growth_trajectory.png', dpi=150)
plt.close(fig)

first, last = quarters[0], quarters[-1]
g = traj.pivot(index='country', columns='quarter', values='avg_d_mbps')[[first, last]]
g.columns = ['start', 'end']
g['growth_pct'] = (g['end'] / g['start'] - 1) * 100
g = g.sort_values('growth_pct', ascending=False)
print(f'07/08 การเติบโต {first} -> {last}:')
for c, r in g.iterrows():
    print(f'  {c:12s} {r["start"]:6.1f} -> {r["end"]:6.1f}  {r["growth_pct"]:+6.1f}%')

# ---- 08 โตเร็วแค่ไหน เทียบฐานที่เริ่ม ----
fig, ax = plt.subplots(figsize=(9.5, 5.5))
ax.scatter(g['start'], g['growth_pct'], s=80, color=BLUE, zorder=3)
for c, r in g.iterrows():
    ax.annotate(c, (r['start'], r['growth_pct']), xytext=(7, 4),
                textcoords='offset points', fontsize=9)
ax.set_xlabel(f'Median provincial download at {first} (Mbps)')
ax.set_ylabel(f'Growth to {last} (%)')
ax.set_title('Catch-up: starting level vs growth — 8 countries',
             fontsize=12, fontweight='bold')
ax.spines[['top', 'right']].set_visible(False)
ax.grid(alpha=0.25)
plt.tight_layout()
fig.savefig(OUT / '08_growth_vs_base.png', dpi=150)
plt.close(fig)

# ---- 09 เมืองหลวงเทียบ 5 จังหวัดที่เร็วสุด ----
# จังหวัดที่ถือทราฟฟิกน้อยกว่า THIN ของประเทศ วาดเป็นวงกลมกลวง อันดับของมันเชื่อไม่ได้
# ตัวอย่าง บ่อแก้วของลาวเป็นที่ 1 ด้วยการทดสอบแค่ 10,477 ครั้ง เทียบเวียงจันทน์ 191,022
THIN = 0.05

fig, ax = plt.subplots(figsize=(10, 5.5))
for i, c in enumerate(order):
    v = prov[prov['country'] == c].sort_values('mean_dl', ascending=False)
    top5 = v.head(5)
    thick = top5[top5['test_share'] >= THIN]
    thin = top5[top5['test_share'] < THIN]
    cap_row = v[v['province'] == CAPITALS[c]]
    ax.scatter([i] * len(thick), thick['mean_dl'], s=38, color=GREY, zorder=2,
               label=f'Top-5 province (≥{THIN:.0%} of national tests)' if i == 0 else None)
    ax.scatter([i] * len(thin), thin['mean_dl'], s=38, facecolors='none', edgecolors=GREY,
               linewidths=1.1, zorder=2,
               label=f'Top-5 province (<{THIN:.0%} — thin data)' if i == 0 else None)
    if not cap_row.empty:
        ax.scatter([i], cap_row['mean_dl'].values, s=95, color=ORANGE, marker='D', zorder=4,
                   label='Capital' if i == 0 else None)
    rank = int((v['mean_dl'] > cap_row['mean_dl'].values[0]).sum()) + 1
    solid = v[v['test_share'] >= THIN]
    rank_solid = int((solid['mean_dl'] > cap_row['mean_dl'].values[0]).sum()) + 1
    lbl = f'#{rank}/{len(v)}' if rank == rank_solid else f'#{rank}/{len(v)}\n(#{rank_solid} ≥{THIN:.0%})'
    ax.annotate(lbl, (i, top5['mean_dl'].max()), xytext=(0, 9),
                textcoords='offset points', ha='center', fontsize=8, color=GREY)
ax.set_xticks(range(len(order)))
ax.set_xticklabels(order, rotation=30, ha='right')
ax.set_yscale('log')
ax.set_ylim(top=ax.get_ylim()[1] * 1.6)
ax.set_ylabel('Province mean download (Mbps), log scale')
ax.set_title('Capital vs the five fastest provinces — 8 countries (label = capital rank)',
             fontsize=12, fontweight='bold')
ax.spines[['top', 'right']].set_visible(False)
ax.legend(loc='lower left', fontsize=8)
plt.tight_layout()
fig.savefig(OUT / '09_capital_vs_top5.png', dpi=150)
plt.close(fig)

print(f'09 อันดับเมืองหลวง (เกณฑ์ข้อมูลบาง = ถือทราฟฟิกน้อยกว่า {THIN:.0%} ของประเทศ):')
for c in order:
    v = prov[prov['country'] == c].sort_values('mean_dl', ascending=False).reset_index(drop=True)
    cap = v[v['province'] == CAPITALS[c]].iloc[0]
    rank = int((v['mean_dl'] > cap['mean_dl']).sum()) + 1
    solid = v[v['test_share'] >= THIN].reset_index(drop=True)
    rank_solid = int((solid['mean_dl'] > cap['mean_dl']).sum()) + 1
    top = v.iloc[0]
    flag = ' ← ข้อมูลบาง' if top['test_share'] < THIN else ''
    print(f'  {c:12s} {CAPITALS[c]:20s} อันดับ {rank}/{len(v)} · เฉพาะจังหวัดข้อมูลหนา {rank_solid}/{len(solid)}')
    print(f'  {"":12s}   ที่ 1 = {top["province"]:18s} {top["mean_dl"]:6.1f} Mbps  '
          f'n={top["n_tests"]:12,.0f} ({top["test_share"]:.1%}){flag}')
    print(f'  {"":12s}   เมืองหลวง          {cap["mean_dl"]:6.1f} Mbps  '
          f'n={cap["n_tests"]:12,.0f} ({cap["test_share"]:.1%})')


# ---- 04 ค่าย 5 จังหวัดเร็วสุดรายประเทศ สร้างใหม่แทนของเดิมที่ยังเป็น 9 ประเทศ ----
# ของเดิมมีสิงคโปร์และไม่มีอินโดนีเซีย และสร้างจาก capital_top5_comparison.csv
# ซึ่งเป็นไฟล์ยุค 9 ประเทศ ตัวนี้อ่านจาก province_quarterly โดยตรง
# แท่งลายทางคือจังหวัดที่ถือทราฟฟิกน้อยกว่า THIN ของประเทศ อันดับเชื่อไม่ได้
PALETTE = ['#E63946', '#F4A261', '#2A9D8F', '#457B9D', '#E9C46A',
           '#6D6875', '#8D99AE', '#B5838D']

fig, axes = plt.subplots(2, 4, figsize=(19, 8.5))
for ax, (i, c) in zip(axes.ravel(), enumerate(order)):
    v = prov[prov['country'] == c].sort_values('mean_dl', ascending=False).head(5)
    y = range(len(v))[::-1]
    col = PALETTE[i % len(PALETTE)]
    for yy, (_, r) in zip(y, v.iterrows()):
        thin_bar = r['test_share'] < THIN
        ax.barh(yy, r['mean_dl'], color=col, alpha=0.45 if thin_bar else 1.0,
                hatch='///' if thin_bar else None, edgecolor=col)
        ax.text(r['mean_dl'], yy, f"  {r['mean_dl']:.0f}  (n={r['n_tests']/1000:,.0f}k, {r['test_share']:.1%})",
                va='center', fontsize=7.5, color='#333')
    ax.set_yticks(list(y))
    ax.set_yticklabels(v['province'])
    ax.set_xlim(0, v['mean_dl'].max() * 1.65)
    ax.set_title(c, fontsize=12, fontweight='bold')
    ax.set_xlabel('Mbps', fontsize=9)
    ax.spines[['top', 'right']].set_visible(False)
fig.suptitle('Top 5 Fastest Provinces/Regions per Country — Fixed Broadband (8 countries)\n'
             f'hatched = province carries <{THIN:.0%} of national tests; its rank is not reliable',
             fontsize=13, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(OUT / '04_top5_provinces_per_country.png', dpi=150)
plt.close(fig)
print('04 จังหวัดที่ 1 ของแต่ละประเทศ (* = ข้อมูลบาง):')
for c in order:
    t = prov[prov['country'] == c].sort_values('mean_dl', ascending=False).iloc[0]
    print(f'  {c:12s} {t["province"]:20s} {t["mean_dl"]:6.1f}  {t["test_share"]:5.1%}'
          f'{" *" if t["test_share"] < THIN else ""}')

print(f'\nเขียนไฟล์ลง {OUT}')
