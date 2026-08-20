"""สร้างกราฟ app success rate (median-based) ใหม่ 8 รูป

แทน 8 รูปเดิมจาก commit 64970b8 (Pakkapon) ที่ไม่มีสคริปต์ต้นทางอยู่ใน repo
ปัญหาที่แก้:
  1. Voice / Video HD ทุกประเทศเท่ากับ 100% ทุกไตรมาส เส้นทับกันสนิท อ่านไม่ออกว่าใครเป็นใคร
     -> ใส่ marker เหลื่อมกันตามลำดับ alphabetical (offset แนวตั้งเล็กน้อย + shape ต่างกัน)
     และเขียนกำกับในหัวกราฟว่าค่าจริงคือ 100% ทุกประเทศ ไม่ใช่จอเสีย
  2. fig_cloud_gaming_national.png เดิม hardcode หัวกราฟผิดเป็น "(capital)" ทั้งที่ข้อมูลคือ
     national -> เขียนหัวกราฟจาก scope ตัวแปรเดียวกับข้อมูลเสมอ กันพลาดซ้ำ
"""
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

EXPORTS = Path(__file__).resolve().parent.parent / 'outputs' / 'app_success_rate_median'
OUT = EXPORTS
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(EXPORTS / 'quarterly_app_success_median.csv')
countries = sorted(df['country'].unique())
quarters = sorted(df['quarter'].unique(), key=lambda q: (int(q[:4]), int(q[-1])))
x_labels = [q.replace('Q', '-')[2:] + q[:2][2:] if False else f"{q[-2:]}-{q[2:4]}" for q in quarters]
# quarter like '2024Q1' -> 'Q1-24'
x_labels = [f"{q[4:]}-{q[2:4]}" for q in quarters]

MARKERS = ['o', 's', '^', 'D', 'v', 'P', 'X', '*', 'h']
THAILAND_COLOR = '#D62728'

METRICS = [
    ('Voice', 'need ≥0.064 Mbps'),
    ('Video HD', 'need ≥5 Mbps'),
    ('Video UHD', 'need ≥25 Mbps'),
    ('Cloud gaming', 'need ≥44 Mbps'),
]


def plot_metric(metric, threshold_label, scope, col):
    fig, ax = plt.subplots(figsize=(11, 5))
    flat = df.groupby('country')[col].apply(lambda s: s.max() - s.min() < 0.5).all()

    for i, country in enumerate(countries):
        sub = df[df['country'] == country].set_index('quarter').reindex(quarters)
        y = sub[col].values
        if flat:
            # ทุกประเทศเท่ากันทุกไตรมาส เส้นทับกันสนิท - เหลื่อม marker แนวตั้งเล็กน้อยให้แยกออก
            y_plot = y + (i - len(countries) / 2) * 0.35
        else:
            y_plot = y
        is_th = country == 'Thailand'
        ax.plot(
            x_labels, y_plot,
            marker=MARKERS[i % len(MARKERS)],
            label=country,
            color=THAILAND_COLOR if is_th else None,
            linewidth=2.4 if is_th else 1.3,
            markersize=7 if is_th else 5,
            zorder=5 if is_th else 3,
            alpha=1.0 if is_th else 0.85,
        )

    ax.set_ylim(0, 108)
    ax.axhline(100, color='gray', linestyle='--', linewidth=0.8, alpha=0.6)
    ax.set_ylabel('Success rate (%)')
    ax.set_xlabel('Time')
    title = f'{metric} success rate ({scope}) by country — {threshold_label}'
    ax.set_title(title, fontsize=12)
    if flat:
        ax.text(0.5, 1.06, 'all countries = 100% every quarter; markers offset vertically for legibility',
                transform=ax.transAxes, ha='center', fontsize=9, style='italic', color='dimgray')
    ax.grid(True, linestyle=':', alpha=0.4)
    ax.legend(ncol=3, fontsize=8, loc='lower left', framealpha=0.9)
    plt.tight_layout()
    fname = f"fig_{metric.lower().replace(' ', '_')}_{'capital' if scope == 'capital' else 'national'}.png"
    fig.savefig(OUT / fname, dpi=150)
    plt.close(fig)
    print(f'{fname}: flat={flat}')


for metric, threshold_label in METRICS:
    for scope, prefix in [('national', 'nat_'), ('capital', 'cap_')]:
        col = prefix + metric
        plot_metric(metric, threshold_label, scope, col)

print(f'\nเขียนไฟล์ลง {OUT}')
