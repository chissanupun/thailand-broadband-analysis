"""Plots for the test-weighted app success rate (national scope only --
matches what paper.tex / poster abstract.tex actually use, image9-12.png).
Same visual style as the old scripts/build_app_success_figs.py so the swap
is a drop-in replacement.
"""
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPORTS = ROOT / 'outputs' / 'app_success_rate_testweighted'
OUT = EXPORTS

df = pd.read_csv(EXPORTS / 'quarterly_app_success_testweighted.csv')
countries = sorted(df['country'].unique())
quarters = sorted(df['quarter'].unique(), key=lambda q: (int(q[:4]), int(q[-1])))
x_labels = [f"{q[-2:]}-{q[2:4]}" for q in quarters]

MARKERS = ['o', 's', '^', 'D', 'v', 'P', 'X', '*', 'h']
THAILAND_COLOR = '#D62728'

METRICS = [
    ('Voice', 'need >=0.064 Mbps, <=200ms'),
    ('Video HD', 'need >=5 Mbps'),
    ('Video UHD', 'need >=25 Mbps'),
    ('Cloud gaming', 'need >=44 Mbps, <=25ms'),
]


def plot_metric(metric, threshold_label, col):
    fig, ax = plt.subplots(figsize=(11, 5))
    flat = df.groupby('country')[col].apply(lambda s: s.max() - s.min() < 0.5).all()

    for i, country in enumerate(countries):
        sub = df[df['country'] == country].set_index('quarter').reindex(quarters)
        y = sub[col].values
        y_plot = y + (i - len(countries) / 2) * 0.35 if flat else y
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
    ax.set_ylabel('Pass rate (%, test-weighted)')
    ax.set_xlabel('Time')
    ax.set_title(f'{metric} pass rate (national) by country — {threshold_label}', fontsize=12)
    if flat:
        ax.text(0.5, 1.06, 'all countries = 100% every quarter; markers offset vertically for legibility',
                transform=ax.transAxes, ha='center', fontsize=9, style='italic', color='dimgray')
    ax.grid(True, linestyle=':', alpha=0.4)
    ax.legend(ncol=3, fontsize=8, loc='lower left', framealpha=0.9)
    plt.tight_layout()
    fname = f"fig_{metric.lower().replace(' ', '_')}_national.png"
    fig.savefig(OUT / fname, dpi=150)
    plt.close(fig)
    print(f'{fname}: flat={flat}')


for metric, threshold_label in METRICS:
    plot_metric(metric, threshold_label, f'nat_{metric}')

print(f'\nwritten to {OUT}')
