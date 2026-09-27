# Main poster abstract validation — 2026-09-27

## Numeric checks

- All **54 cloud-gaming table values** agree with the existing Ookla CSVs after rounding to one decimal place.
- Ookla retained test contributions: **229,367,221** (18 fixed/mobile country exports).
- NDT7 clean-parquet records: **760,607,387** (nine source parquet metadata counts).
- Combined corpus count: **989,974,608**, which rounds to 990 million; the sources are analyzed separately.
- Every Ookla country/connection segment contains all 12 quarters from 2023-Q1 to 2025-Q4, with no duplicate province-quarter keys.
- Every retained Ookla row agrees with the >=100 tests and >=5 tiles criteria.
- No retained Ookla province-quarter mean falls below either 64 kbps or 5 Mbps. This does not mean every individual test or user meets these thresholds.
- Strongest/weakest capital ratio: **16.4055**, supporting the rounded 16× claim.

## Capital, national, and connection-type values

| country | capital_mean_mbps | national_mean_mbps | fixed_mobile_ratio |
| --- | --- | --- | --- |
| Thailand | 298.8 | 276.9 | 3.2 |
| Vietnam | 161.4 | 159.7 | 1.8 |
| Philippines | 159.6 | 132.0 | 1.9 |
| Singapore | 361.0 | 394.8 | 2.1 |
| Cambodia | 55.6 | 53.0 | 1.4 |
| Laos | 55.6 | 51.2 | 1.4 |
| Malaysia | 212.3 | 194.8 | 1.1 |
| Myanmar | 22.0 | 24.6 | 0.8 |
| Indonesia | 63.4 | 41.2 | 1.1 |

## Interpretation corrections

- Define percentages using test weights on province-quarter mean threshold indicators; do not describe them as percentages of users or time.
- Replace claims that voice/HD are solved or that actual gaming sessions fail with claims about aggregate thresholds.
- Treat Lübben and Misfeld (2022), Table 5, as illustrative benchmarks, not universally sufficient application requirements. Idle server latency does not measure end-user application latency.
- The consumer survey is an online survey of mobile users. It reports 81% with usage problems, with slow/dropped connections the most common problems, not 81% of all Thai consumers or fixed-broadband users.
- Historic Thailand rank 12 in June 2026 is not independently verified by a saved historical index. The exact rank should be omitted pending the source snapshot.
- The original NDT7 GADM exports and original Ookla boundary assignments are retained. No generated ndt7_geoboundaries_* file is an input to this validation.

## Applied and compiled

- Added Indonesia to the four bandwidth-constrained fixed markets in the abstract, results and conclusion. Yangon remains the selected Myanmar comparison region at the user's explicit request.

- Updated the existing main abstract and synchronized its HotCRP text field.
- Compiled in the new Overleaf project and downloaded `main/abstract.pdf`.
- Checked all three rendered pages: two pages of content, references only on page three.
- July 2026 rank 12 is included at the user's explicit request, based on their observation of August rank 9 and an improvement of 3. This is consistent with July rank 12, not June. The browser security policy blocked inspection of the official Speedtest page; the historical rank has not been independently verified.
- The built-in editor compiler failed with an environment-directory error; the delivered PDF was compiled by Overleaf.

## Reproduce

Run `python scripts/check_poster_abstract.py` from the project root.
Input hashes are in `input_manifest.json`; full-precision outputs are in `ookla_verified_metrics.csv`.

## Primary reference checked

Consumer survey: https://www.tcc.or.th/true-dtac-merger-consumer/ (paragraph describing the 9–23 November 2023 online survey, 2,924 respondents).
Application thresholds: local source PDF `docs/refs/02-ndt7-mlab/lubben-misfeld-2022-mlab-german-internet-landscape.pdf`, Table 5, page 17.
