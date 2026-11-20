"""Build demo/data.json for the poster demo site from the same exports the poster uses.

Speed: Ookla province-quarter exports, reliable rows only, test-weighted national mean
(same rule as build_cross_country_figs_8c.py). Pass rates: quarterly_app_success_testweighted.csv.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPORTS = ROOT / 'data' / 'exports'
PASS_CSV = ROOT / 'outputs' / 'app_success_rate_testweighted' / 'quarterly_app_success_testweighted.csv'
OUT = ROOT / 'demo' / 'data.json'

FILES = {
    'Thailand':    ('ookla_province_quarterly.csv', 'ookla_mobile_province_quarterly.csv'),
    'Vietnam':     ('ookla_vietnam_province_quarterly.csv', 'ookla_mobile_vietnam_province_quarterly.csv'),
    'Philippines': ('ookla_philippines_province_quarterly.csv', 'ookla_mobile_philippines_province_quarterly.csv'),
    'Cambodia':    ('ookla_cambodia_province_quarterly.csv', 'ookla_mobile_cambodia_province_quarterly.csv'),
    'Laos':        ('ookla_laos_province_quarterly.csv', 'ookla_mobile_laos_province_quarterly.csv'),
    'Malaysia':    ('ookla_malaysia_province_quarterly.csv', 'ookla_mobile_malaysia_province_quarterly.csv'),
    'Myanmar':     ('ookla_myanmar_province_quarterly.csv', 'ookla_mobile_myanmar_province_quarterly.csv'),
    'Indonesia':   ('ookla_indonesia_province_quarterly.csv', 'ookla_mobile_indonesia_province_quarterly.csv'),
    'Singapore':   ('ookla_singapore_province_quarterly.csv', 'ookla_mobile_singapore_province_quarterly.csv'),
}

CAPITALS = {
    'Thailand': 'Bangkok Metropolis', 'Vietnam': 'Hà Nội', 'Philippines': 'NCR',
    'Cambodia': 'Phnom Penh', 'Laos': 'Vientiane Capital', 'Malaysia': 'Kuala Lumpur',
    'Myanmar': 'Yangon', 'Indonesia': 'Jakarta', 'Singapore': 'Central Region',
}

PASS_COLS = {'voice': 'nat_Voice', 'hd': 'nat_Video HD', 'uhd': 'nat_Video UHD', 'cloud': 'nat_Cloud gaming'}


def read_rows(path):
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        # header has "quarter" twice ("2023-Q1" then 1); index() takes the first
        ix = {k: header.index(k) for k in ('province', 'quarter', 'avg_d_mbps', 'total_tests', 'is_reliable')}
        for r in reader:
            if r[ix['is_reliable']] != 'True':
                continue
            yield r[ix['province']], r[ix['quarter']], float(r[ix['avg_d_mbps']]), float(r[ix['total_tests']])


def network(path):
    provinces, nat = {}, {}
    for prov, q, mbps, tests in read_rows(path):
        provinces.setdefault(prov, {})[q] = round(mbps, 2)
        s = nat.setdefault(q, [0.0, 0.0])
        s[0] += mbps * tests
        s[1] += tests
    national = {q: round(a / b, 2) for q, (a, b) in sorted(nat.items())}
    return {'national': national, 'provinces': {p: dict(sorted(v.items())) for p, v in sorted(provinces.items())}}


def main():
    passes = {}
    with open(PASS_CSV, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            passes.setdefault(r['country'], {})[r['quarter']] = {k: round(float(r[c]), 1) for k, c in PASS_COLS.items()}

    data = {}
    for country, (fixed_fn, mobile_fn) in FILES.items():
        fixed = network(EXPORTS / fixed_fn)
        if CAPITALS[country] not in fixed['provinces']:
            raise SystemExit(f'capital {CAPITALS[country]} missing for {country}')
        data[country] = {
            'capital': CAPITALS[country],
            'fixed': fixed,
            'mobile': network(EXPORTS / mobile_fn),
            'pass': dict(sorted(passes[country].items())),
        }

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    for c, d in data.items():
        qs = sorted(d['fixed']['national'])
        print(f"{c:12s} fixed {qs[0]}..{qs[-1]} n={len(qs)} last={d['fixed']['national'][qs[-1]]:7.1f} "
              f"provinces={len(d['fixed']['provinces'])} mobile_q={len(d['mobile']['national'])}")
    print(f'wrote {OUT} ({OUT.stat().st_size // 1024} KB)')


if __name__ == '__main__':
    main()
