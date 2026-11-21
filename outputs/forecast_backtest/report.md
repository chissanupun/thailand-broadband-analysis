# Forecast backtest

Origin 2024-Q4, forecast 2025-Q1..Q4. Train rows: 3318. Series: 558.

| method | h1 MAPE | h2 | h3 | h4 | all MAPE | all median APE | rolling 1-step MAPE | national series MAPE |
|---|---|---|---|---|---|---|---|---|
| ml | 12.22 | 16.49 | 18.49 | 20.53 | 16.94 | 8.24 | 10.42 | 12.46 |
| trend | 12.18 | 15.65 | 19.38 | 22.78 | 17.5 | 13.0 | 12.37 | 13.19 |
| naive | 11.25 | 15.4 | 17.94 | 22.68 | 16.82 | 12.6 | 11.1 | 12.34 |

## MAPE by country (all horizons)

| country | ml | trend | naive |
|---|---|---|---|
| Cambodia | 11.47 | 26.54 | 14.95 |
| Indonesia | 9.73 | 14.05 | 13.42 |
| Laos | 16.83 | 23.74 | 21.41 |
| Malaysia | 5.81 | 26.47 | 6.45 |
| Myanmar | 26.58 | 26.04 | 23.83 |
| Philippines | 7.49 | 9.9 | 10.43 |
| Singapore | 7.77 | 7.55 | 15.58 |
| Thailand | 12.17 | 13.95 | 14.7 |
| Vietnam | 33.76 | 17.65 | 24.19 |
