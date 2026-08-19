# Claude Log

Running log of changes Claude made to this project, and why. Newest entry on top.

---

## 2026-07-10 — GDP currency fix (real fix, after a false start)

**False start (reverted, not committed anywhere):** First pass assumed the mislabeled `gdp_per_capita_thb_2021` column held raw local currency (VND/PHP/SGD) for non-Thailand countries, and divided by a 2021 nominal FX rate. Produced nonsense (~$0.16/capita) — wrong premise.

**Actual root cause,** found by reading the notebooks that built the reference CSVs (`notebooks/ookla/vietnam_eda.ipynb` etc.): the column was never raw local currency for VN/PH/SG. Notebook markdown says it was compiled as **USD PPP, 2011 base year**, from Wikipedia/PSA/GSO/Singstat (`prov_ref['gdp_per_capita_usd_2021'] = prov_ref['gdp_per_capita_thb_2021']  # already USD-equivalent in source data`). Thailand's own column, by contrast, genuinely is nominal THB 2021 (NESDC, per `citations.md` §3). So the four countries were never on a common unit *or* base year — worse than a label bug.

**Fix applied (user chose: "pull fresh World Bank/IMF PPP figures"):**
1. Pulled live from World Bank API (`NY.GDP.PCAP.PP.CD`, date=2021): Thailand 20,242.77 · Vietnam 12,048.90 · Philippines 8,857.79 · Singapore 132,617.35 (GDP per capita, PPP, current international $).
2. For each country, computed a population-weighted mean of the original province-level column, then a scaling factor = `official_WB_value / that_weighted_mean`.
3. Applied the factor uniformly to every province's original value — this **anchors each country's absolute level to the real 2021 WB figure while preserving each province's original relative share within its country**. Assumption (limitation to state in the paper): within-country relative provincial GDP disparity is assumed to hold under this rescaling — not independently verified per province.
4. Applied to all 4 reference CSVs (`data/reference/*.csv`) and all 8 export CSVs (`data/exports/ookla*_province_quarterly.csv`, fixed + mobile × 4 countries).

**New schema (reference + export CSVs), replacing the old ambiguous `gdp_per_capita_thb_2021`:**
- `gdp_per_capita_raw_2021` — original value, kept unchanged as an audit trail. **Meaning differs by country**: Thailand = genuine nominal THB (NESDC); Vietnam/Philippines/Singapore = source-compiled USD PPP, 2011 base (not local currency). Do not use directly in cross-country comparisons.
- `gdp_per_capita_usd_ppp_2021` — **main column, use this for the SEA cross-country regression.** Anchored to official World Bank 2021 PPP figures as described above.
- `gdp_per_capita_thb_2021` — secondary/illustrative THB-equivalent (`usd_ppp × ~31.98` THB/USD, 2021 approx annual average). Flag: this mixes a PPP valuation with a market exchange rate — it is NOT an official nominal THB figure, just a reader-friendly conversion. Fine for context, not for regression.

**Known gap, not fixed:** no genuine local-currency (VND/PHP/SGD) province-level series exists in this pipeline — the source data for those three countries was already USD-PPP by the time it reached this repo. If literal local-currency figures are needed later, that requires pulling actual province-level nominal GDP from GSO (Vietnam), PSA (Philippines), or Singstat directly — not attempted here.

**Exchange rate and PPP-conversion figures used are not independently verified beyond the single World Bank API pull** — recommend double-checking `NY.GDP.PCAP.PP.CD` values and the THB/USD 2021 average against a second source before final submission.

---

## 2026-07-10 — paper.tex: switch to ACM template, set direction

**Context:** Paper target is AINTEC conference (ACM-sponsored, ACM Digital Library). Old `docs/paper.tex` was Thai-language, XeLaTeX+polyglossia, custom preamble — incompatible with ACM's required `acmart` class (Libertine font, no custom margins/fonts allowed) and with AINTEC's English/ACM DL convention.

**What changed:**
- Replaced `docs/paper.tex` preamble with `\documentclass[sigconf]{acmart}` (ACM proceedings template).
- Stripped ACM's own tutorial/sample content (Template Overview, Typefaces, sample authors "Ben Trovato" etc., Lorem ipsum appendix) — none of that is part of the actual paper.
- Kept doc skeleton: title (placeholder, English translation of original Thai title), abstract env, CCS/keywords, Intro/Methodology/Results/Discussion/Conclusion sections (all empty, marked TODO), acks env.
- Carried over the working bibliography (`thebibliography` env) from the old Thai draft — Röller & Waverman 2001, Ookla Open Data, ITU 2024, MacMillan et al. 2023 (Ookla vs NDT7 comparison methodology), Nation Thailand ranking/outage articles, ETDA complaints survey.
- Left `\acmConference`, `\acmDOI`, `\acmISBN`, author name/affiliation as placeholders — need real values once AINTEC submission/rights-form details are known.

**Did NOT touch:** acmart's actual template mechanics (documentclass options, margins, fonts, spacing) — only content within the doc body. ACM's "don't modify the template" rule refers to layout, not to filling in your own paper text.

---

## 2026-07-10 — Direction change: SEA cross-country comparison becomes main finding

**Decision (user):** Key finding shifts from "Ookla vs NDT7 cross-validation within Thailand" to **Thailand vs. other SEA countries (Vietnam, Philippines, Singapore)** using Ookla data for all four. NDT7 cross-validation is kept, but demoted to a secondary/robustness check scoped to Thailand only (not dropped).

**Data check done before committing to this direction** — confirmed all four country exports share identical schema and time coverage:
- `data/exports/ookla_province_quarterly.csv` (Thailand, 847 rows)
- `data/exports/ookla_vietnam_province_quarterly.csv` (704 rows)
- `data/exports/ookla_philippines_province_quarterly.csv` (187 rows)
- `data/exports/ookla_singapore_province_quarterly.csv` (55 rows)
- Mobile equivalents also exist for all four (`ookla_mobile_*_province_quarterly.csv`)
- Columns: `province, quarter, year, avg_d_mbps, avg_u_mbps, avg_lat_ms_wt, total_tests, n_tiles, is_reliable, region, internet_tier, pop_2024, gdp_per_capita_thb_2021, density_per_km2`
- All cover 2023-Q1 → 2025-Q4 (12 quarters), fixed + mobile both present.

**Two caveats flagged for methodology (unresolved as of this entry):**
1. **Admin granularity mismatch across countries** — Thailand 77 provinces, Vietnam ~64, Philippines ~17 regions, Singapore only 5 planning regions. Not apples-to-apples at "province" level; likely needs country-level rollup as the primary comparison, with province/district-level detail kept as Thailand-only deep dive.
2. **GDP column currency** — `gdp_per_capita_thb_2021` for non-Thailand rows (e.g. Vietnam ~3791, vs Thailand ~77048) looks like it's still in local currency (VND/PHP/SGD), not converted to a common unit (THB/USD/PPP). User said this is "fixed" (2026-07-10 message) — verify actual conversion logic next time reference CSVs are touched, this log entry doesn't confirm what the fix was.

**Not yet done:** Actual Introduction/Methodology text for the SEA-comparison framing — waiting on user's direction for structure/framing before writing.
