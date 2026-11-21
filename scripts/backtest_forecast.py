"""Backtest an ML forecaster for province-level speeds against simple baselines.

Data: demo/data.json (reliable province-quarters only, same as the poster).
Series: every (country, network, province) plus each national series.
Model: one gradient-boosting model pooled over all series, predicting next-quarter
log-change from recent log-lags, recent growth, country, network and capital flag.
Baselines: naive (last value) and per-series log-linear trend (what the demo's
projection tab uses).

Evaluation: origin 2024-Q4, forecast 2025-Q1..Q4 recursively (h = 1..4), train only
on targets up to the origin. Also rolling one-step-ahead for each 2025 quarter.
Writes outputs/forecast_backtest/{metrics.json, report.md}.

Run: uv run --with scikit-learn --with numpy python scripts/backtest_forecast.py
"""
import json
import math
from pathlib import Path

import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / 'demo' / 'data.json').read_text(encoding='utf-8'))
OUT = ROOT / 'outputs' / 'forecast_backtest'
QUARTERS = sorted(DATA['Thailand']['fixed']['national'])
QI = {q: i for i, q in enumerate(QUARTERS)}
COUNTRIES = sorted(DATA)
NLAG = 2
SEED = 0


def all_series():
    out = []
    for c in COUNTRIES:
        for net in ('fixed', 'mobile'):
            block = DATA[c][net]
            out.append(dict(country=c, net=net, name='__national__', kind='national', s=block['national']))
            for p, s in block['provinces'].items():
                out.append(dict(country=c, net=net, name=p, kind='capital' if p == DATA[c]['capital'] else 'province', s=s))
    for r in out:  # dense array with NaN for missing quarters
        r['y'] = np.array([math.log(r['s'][q]) if q in r['s'] and r['s'][q] > 0 else np.nan for q in QUARTERS])
    return out


def features(r, lags):
    """lags: list of log values, most recent first (len NLAG+1 for growth over 2 steps)."""
    onehot = [1.0 if r['country'] == c else 0.0 for c in COUNTRIES]
    return [*lags[:NLAG], lags[0] - lags[1], 1.0 if r['net'] == 'mobile' else 0.0,
            1.0 if r['kind'] == 'capital' else 0.0, 1.0 if r['kind'] == 'national' else 0.0, *onehot]


def training_rows(series, last_target):
    X, y = [], []
    for r in series:
        v = r['y']
        for t in range(NLAG, last_target + 1):
            win = v[t - NLAG:t + 1]
            if np.isnan(win).any():
                continue
            lags = list(v[t - NLAG:t][::-1])
            X.append(features(r, lags))
            y.append(v[t] - v[t - 1])
    return np.array(X), np.array(y)


def fit(series, last_target):
    X, y = training_rows(series, last_target)
    m = HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05, max_leaf_nodes=15,
                                      min_samples_leaf=30, l2_regularization=1.0, random_state=SEED)
    m.fit(X, y)
    return m, len(y)


def ml_path(m, r, origin, h):
    v = list(r['y'][:origin + 1])
    out = []
    for _ in range(h):
        lags = v[::-1][:NLAG]
        if any(np.isnan(lags)):
            return None
        nxt = v[-1] + m.predict([features(r, lags)])[0]
        v.append(nxt)
        out.append(nxt)
    return out


def trend_path(r, origin, h, min_pts=6):
    v = r['y'][:origin + 1]
    idx = np.where(~np.isnan(v))[0]
    if len(idx) < min_pts:
        return None
    b, a = np.polyfit(idx, v[idx], 1)
    return [a + b * (origin + k) for k in range(1, h + 1)]


def naive_path(r, origin, h):
    last = r['y'][origin]
    return None if np.isnan(last) else [last] * h


def ape(pred_log, true_log):
    return abs(math.exp(pred_log) - math.exp(true_log)) / math.exp(true_log)


def summarize(errs):
    a = np.array(errs)
    return dict(n=int(len(a)), mape=round(float(a.mean() * 100), 2), median_ape=round(float(np.median(a) * 100), 2),
                p90_ape=round(float(np.quantile(a, 0.9) * 100), 2))


def main():
    series = all_series()
    origin = QI['2024-Q4']
    H = 4
    model, ntrain = fit(series, origin)

    methods = {'ml': lambda r: ml_path(model, r, origin, H), 'trend': lambda r: trend_path(r, origin, H),
               'naive': lambda r: naive_path(r, origin, H)}
    # evaluate only series where every method can forecast and the truth exists: same rows for all
    errs = {k: {h: [] for h in range(1, H + 1)} for k in methods}
    by_country = {k: {} for k in methods}
    signed = {h: [] for h in range(1, H + 1)}  # ml log-residuals, for empirical bands
    nat = {k: [] for k in methods}
    for r in series:
        paths = {k: f(r) for k, f in methods.items()}
        if any(p is None for p in paths.values()):
            continue
        for h in range(1, H + 1):
            truth = r['y'][origin + h]
            if np.isnan(truth):
                continue
            for k, p in paths.items():
                e = ape(p[h - 1], truth)
                errs[k][h].append(e)
                by_country[k].setdefault(r['country'], []).append(e)
                if r['kind'] == 'national':
                    nat[k].append(e)
            signed[h].append(truth - paths['ml'][h - 1])

    # rolling one-step-ahead for each 2025 quarter (retrain each time)
    rolling = {k: [] for k in methods}
    for q in ('2025-Q1', '2025-Q2', '2025-Q3', '2025-Q4'):
        o = QI[q] - 1
        m, _ = fit(series, o)
        for r in series:
            truth = r['y'][o + 1]
            ps = {'ml': ml_path(m, r, o, 1), 'trend': trend_path(r, o, 1), 'naive': naive_path(r, o, 1)}
            if np.isnan(truth) or any(p is None for p in ps.values()):
                continue
            for k, p in ps.items():
                rolling[k].append(ape(p[0], truth))

    metrics = dict(
        origin='2024-Q4', horizon=H, train_rows=ntrain, series=len(series),
        multi_step={k: {f'h{h}': summarize(v[h]) for h in v} | {'all': summarize(sum(v.values(), []))} for k, v in errs.items()},
        national_series_all_h={k: summarize(v) for k, v in nat.items()},
        rolling_one_step={k: summarize(v) for k, v in rolling.items()},
        by_country_all_h={k: {c: summarize(v)['mape'] for c, v in sorted(d.items())} for k, d in by_country.items()},
        ml_log_residual_q10_q90={f'h{h}': [round(float(np.quantile(v, .1)), 4), round(float(np.quantile(v, .9)), 4)] for h, v in signed.items()},
    )
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'metrics.json').write_text(json.dumps(metrics, indent=2))

    lines = ['# Forecast backtest', '', f"Origin {metrics['origin']}, forecast 2025-Q1..Q4. Train rows: {ntrain}. Series: {len(series)}.", '',
             '| method | h1 MAPE | h2 | h3 | h4 | all MAPE | all median APE | rolling 1-step MAPE | national series MAPE |', '|---|---|---|---|---|---|---|---|---|']
    for k in methods:
        ms = metrics['multi_step'][k]
        lines.append(f"| {k} | {ms['h1']['mape']} | {ms['h2']['mape']} | {ms['h3']['mape']} | {ms['h4']['mape']} | {ms['all']['mape']} | "
                     f"{ms['all']['median_ape']} | {metrics['rolling_one_step'][k]['mape']} | {metrics['national_series_all_h'][k]['mape']} |")
    lines += ['', '## MAPE by country (all horizons)', '', '| country | ml | trend | naive |', '|---|---|---|---|']
    for c in COUNTRIES:
        lines.append(f"| {c} | {metrics['by_country_all_h']['ml'].get(c)} | {metrics['by_country_all_h']['trend'].get(c)} | {metrics['by_country_all_h']['naive'].get(c)} |")
    (OUT / 'report.md').write_text('\n'.join(lines) + '\n')
    print('\n'.join(lines))
    export_demo(series, model, origin, H, metrics)


def export_demo(series, bt_model, origin, H, metrics):
    """demo/forecast.json: per country/network/area -> 2025 backtest paths + 2026 ML forecast with empirical band."""
    final, _ = fit(series, len(QUARTERS) - 1)
    band = metrics['ml_log_residual_q10_q90']
    last = len(QUARTERS) - 1
    future = [f'{2026}-Q{k}' for k in range(1, H + 1)]
    out = {'backtest_quarters': QUARTERS[origin + 1:origin + 1 + H], 'future_quarters': future,
           'summary': {k: metrics['multi_step'][k]['all'] for k in ('ml', 'trend', 'naive')},
           'rolling_one_step': metrics['rolling_one_step'], 'series': {}}
    r2 = lambda xs: [round(math.exp(x), 1) for x in xs]
    for r in series:
        bt = {'ml': ml_path(bt_model, r, origin, H), 'trend': trend_path(r, origin, H), 'naive': naive_path(r, origin, H)}
        fc = ml_path(final, r, last, H)
        if fc is None or any(v is None for v in bt.values()):
            continue
        lo = [x + band[f'h{h}'][0] for h, x in enumerate(fc, 1)]
        hi = [x + band[f'h{h}'][1] for h, x in enumerate(fc, 1)]
        key = f"{r['country']}|{r['net']}|{r['name']}"
        out['series'][key] = {'backtest': {k: r2(v) for k, v in bt.items()}, 'ml': r2(fc), 'lo': r2(lo), 'hi': r2(hi)}
    p = ROOT / 'demo' / 'forecast.json'
    p.write_text(json.dumps(out, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    print(f"wrote {p} ({p.stat().st_size // 1024} KB, {len(out['series'])} series)")


if __name__ == '__main__':
    main()
