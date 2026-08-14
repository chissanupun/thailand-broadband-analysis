"""สร้างรูปที่ 1 กับ 2 ใหม่ 8 ประเทศ ตัดสิงคโปร์ รวมอินโดนีเซีย

รูปเดิมมาจาก build_slides_all_countries.py ซึ่ง hardcode ตัวเลขไว้ในสคริปต์
(สิงคโปร์ mean=376 เป็นค่าคงที่ ไม่ได้อ่านจากข้อมูล) และไม่มีอินโดนีเซีย
ตัวนี้อ่านจาก data/exports จริงทั้งหมด
"""
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

EXPORTS = Path(__file__).resolve().parent.parent / 'data' / 'exports'
OUT = Path(__file__).resolve().parent.parent / 'outputs' / 'ookla' / 'cross_country'
OUT.mkdir(parents=True, exist_ok=True)

FILES = {
    'Thailand':    'ookla_province_quarterly.csv',
    'Vietnam':     'ookla_vietnam_province_quarterly.csv',
    'Philippines': 'ookla_philippines_province_quarterly.csv',
    'Cambodia':    'ookla_cambodia_province_quarterly.csv',
    'Laos':        'ookla_laos_province_quarterly.csv',
    'Malaysia':    'ookla_malaysia_province_quarterly.csv',
    'Myanmar':     'ookla_myanmar_province_quarterly.csv',
    'Indonesia':   'ookla_indonesia_province_quarterly.csv',
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

BLUE, ORANGE = '#0072B2', '#D55E00'

frames = []
for country, fn in FILES.items():
    d = pd.read_csv(EXPORTS / fn)
    d = d[d['is_reliable'] == True].copy()
    d['country'] = country
    frames.append(d)
df = pd.concat(frames, ignore_index=True)


def weighted(g):
    return (g['avg_d_mbps'] * g['total_tests']).sum() / g['total_tests'].sum()


# ---- รูปที่ 1: ความเร็วดาวน์โหลดเฉลี่ยรายประเทศ ----
nat = df.groupby('country').apply(weighted, include_groups=False).sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(9.5, 5.5))
bars = ax.bar(nat.index, nat.values, color=BLUE)
for b, v in zip(bars, nat.values):
    ax.text(b.get_x() + b.get_width() / 2, v + 4, f'{v:.0f}', ha='center', fontsize=9)
ax.set_ylabel('Mean download (Mbps), test-weighted')
ax.set_title('Fixed broadband mean download by country — 8 countries, Q1 2023–Q4 2025',
             fontsize=12, fontweight='bold')
ax.set_ylim(0, nat.max() * 1.15)
ax.spines[['top', 'right']].set_visible(False)
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
fig.savefig(OUT / '01_all_country_fixed_dl.png', dpi=150)
plt.close(fig)

ratio = nat.max() / nat.min()
print(f'รูปที่ 1: สูงสุด {nat.index[0]} {nat.iloc[0]:.1f} · ต่ำสุด {nat.index[-1]} {nat.iloc[-1]:.1f} · ต่างกัน {ratio:.1f} เท่า')

# ---- รูปที่ 2: เมืองหลวงเทียบทั้งประเทศ ----
cap_mask = df.apply(lambda r: r['province'] == CAPITALS.get(r['country']), axis=1)
cap = df[cap_mask].groupby('country').apply(weighted, include_groups=False)
missing = [c for c in FILES if c not in cap.index]
if missing:
    raise SystemExit(f'ไม่เจอจังหวัดเมืองหลวงของ: {missing} — ตรวจชื่อใน CAPITALS')

order = nat.index
fig, ax = plt.subplots(figsize=(9.5, 5.5))
ax.bar(order, [cap[c] for c in order], color=ORANGE, label='Capital province')
ax.scatter(order, [nat[c] for c in order], marker='D', color='black', zorder=3,
           s=45, label='National mean')
ax.set_ylabel('Mean download (Mbps), test-weighted')
ax.set_title('Capital province vs national mean — 8 countries',
             fontsize=12, fontweight='bold')
ax.spines[['top', 'right']].set_visible(False)
ax.legend()
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
fig.savefig(OUT / '03_capital_vs_national.png', dpi=150)
plt.close(fig)

print('รูปที่ 2 เมืองหลวงเทียบทั้งประเทศ:')
for c in order:
    flag = '  <-- เมืองหลวงต่ำกว่าค่าเฉลี่ยประเทศ' if cap[c] < nat[c] else ''
    print(f'  {c:12s} capital {cap[c]:7.1f} | national {nat[c]:7.1f} | {cap[c]-nat[c]:+7.1f}{flag}')

print(f'\nเขียนไฟล์ลง {OUT}')
