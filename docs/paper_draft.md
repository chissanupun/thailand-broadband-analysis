# Is Southeast Asian Internet Good or Bad? An Empirical Comparison of Broadband Quality Across Eight Southeast Asian Countries

*Draft — Introduction, Data, and Methodology sections only. Results/Discussion/Conclusion not yet written. Working format is Markdown, not the LaTeX manuscript (`docs/paper.tex`, currently left untouched pending a separate template decision).*

*Scope update (2026-07-20): the country set was expanded from four (Thailand, Vietnam, the Philippines, Singapore) to eight, adding Cambodia, Myanmar, Laos, and Malaysia on the Ookla side. This expansion round is Ookla-only — NDT7 cross-validation (Section 2.2/3.3) remains scoped to Thailand and Vietnam for now and has not been extended to the four new countries.*

## 1. Introduction

High-speed internet has become critical infrastructure for economic and social development in the 21st century. High-quality broadband access directly affects labor productivity, education, government service delivery, and national competitiveness. Multiple empirical studies find that a 10% increase in broadband penetration can raise GDP per capita by 1–3% in developing countries (Röller & Waverman, 2001).

Thailand, however, still lacks academic research that systematically evaluates the "quality" of its internet nationwide using real measurement data. What exists instead is a set of mutually contradictory claims from two different kinds of sources.

On one side, national-level statistics suggest Thai internet is "good": the Speedtest Global Index by Ookla ranks Thailand's fixed broadband 13th in the world, with an average download speed of 237.05 Mbps (March 2025 data) — more than double the global average (Nation Thailand, 2025a).

On the other side, real-user perception data and news coverage suggest Thai internet is "bad": Thailand's Electronic Transactions Development Agency (ETDA) found that 64.65% of Thai internet users cited "slow internet speed" as their top annoyance (ETDA, 2024). Following the True–dtac telecom merger, the Foundation for Consumers found that 81% of users experienced network problems (dropped connections/outages) in the preceding 6 months, and complaints to the NBTC (National Broadcasting and Telecommunications Commission) surged from under 1,000 to nearly 3,000 in the first 7 months of 2025 — including a nationwide True network outage in May 2025 that caused significant economic damage to businesses (Nation Thailand, 2025b). Notably, Thailand's mobile internet ranks only 39th in the world (Nation Thailand, 2025a) — a stark contrast to its fixed-broadband ranking, suggesting the answer to "is Thai internet good or bad" may depend heavily on which network type and which area is being discussed, rather than having one single national answer.

This contradiction between national-aggregate statistics and real user experience is the gap this research aims to close. Rather than relying on subjective opinion from news or social media, this study uses real network-quality measurement data at the tile/test level from two independent sources — Ookla Open Data (covering both fixed and mobile broadband) and M-Lab NDT7 — comparing results between the two platforms descriptively (trend direction, threshold pass rates), following the comparative framework of MacMillan et al. (2023), who compared Ookla and NDT7 in a US context.

**Scope note (revised from the original single-country framing):** the original version of this study asked only whether *Thailand's* internet is good or bad. The current version extends the same question regionally: is Thailand's broadband quality good or bad *relative to its Southeast Asian neighbors* — Vietnam, the Philippines, Singapore, Cambodia, Myanmar, Laos, and Malaysia — using the same Ookla methodology across all eight countries. NDT7 data is used where it exists (currently Thailand and Vietnam only; Philippines pending delivery from a collaborator; Singapore's NDT7 scope is still unconfirmed; Cambodia/Myanmar/Laos/Malaysia are Ookla-only as of this draft) as a descriptive side-by-side comparison, not a formal cross-validation study.

This research therefore aims to answer: what is the real quality of Thai internet, as measured empirically — both in absolute terms, at province level nationwide (77 provinces) and district level in 8 sample provinces, and in relative terms, against seven other Southeast Asian countries (Vietnam, the Philippines, Singapore, Cambodia, Myanmar, Laos, and Malaysia) — covering both fixed and mobile broadband? The study uses Ookla Open Data covering Q1 2023 through Q4 2025 (11–12 quarters depending on country) and M-Lab NDT7 data for the overlapping period where available (currently Thailand: Q4 2023–Q1 2025; Vietnam: Q1 2023–Q4 2025).

### 1.1 Research Objectives

This research has four main objectives:

1. Measure and compare internet quality (download speed, upload speed, and latency) for both fixed and mobile broadband, at the province and district level across Thailand, in both spatial and temporal dimensions.
2. Compare Thailand's broadband quality against seven other Southeast Asian countries (Vietnam, the Philippines, Singapore, Cambodia, Myanmar, Laos, and Malaysia) on the same Ookla metrics.
3. Compare Ookla and NDT7 results descriptively wherever both sources overlap, noting any gap between the two and contextual factors (latency, test density, measurement methodology — active vs. passive) that may explain it.
4. Answer the question "is [Southeast Asian] internet good or bad" by comparing real measured results against international rankings (Speedtest Global Index) and explaining the apparent contradiction between national-level statistics and user perception.

**Contributions.**

- **A public-perception/national-statistic gap, quantified.** We document a concrete contradiction between Thailand's #13-globally fixed-broadband ranking and real-user annoyance/outage data (Section 1), and treat closing that gap empirically — rather than resolving it rhetorically — as the paper's central problem.
- **An eight-country Southeast Asian comparison on one consistent pipeline.** The same tile-to-province methodology (Section 3.1) is applied unmodified across Thailand, Vietnam, the Philippines, Singapore, Cambodia, Myanmar, Laos, and Malaysia, so cross-country differences reflect measured variation rather than differing methodology per country.
- **A reliability threshold applied consistently, not just computed.** `is_reliable` (`total_tests>=100 & n_tiles>=5`) is enforced identically across both data sources and all eight countries before any downstream statistic is computed (Section 3.1, Step 5), rather than left as an unused diagnostic column.

### 1.2 Research Hypotheses

This study hypothesizes that Thai internet is not uniformly "good" or "bad" nationwide, but varies significantly in quality by area and network type: fixed broadband in urban areas and economically stronger provinces will show world-class quality consistent with Ookla's reported ranking, while mobile internet and rural or economically weaker provinces will show significantly lower quality. This spatial and network-type variation is expected to explain why public perception conflicts with national-aggregate statistics.

Regionally, we hypothesize that Thailand sits toward the upper end of the Southeast Asian pack on fixed broadband — behind Singapore, but ahead of the other six countries in this study (Vietnam, the Philippines, Cambodia, Myanmar, Laos, and Malaysia; Malaysia's ranking relative to Thailand is treated as an open question rather than assumed).

We also expect Ookla and NDT7 results to be **directionally consistent** (both trending the same way over time) even though the **absolute magnitudes measured may differ substantially**, given the two platforms' different measurement methodologies (active/user-initiated vs. passive/background) and different user populations.

### 1.3 Research Scope

The research covers both fixed (wired) and mobile (cellular) broadband from Ookla Open Data, covering all provinces/administrative regions of eight countries, at the province/region level, with a district-level deep dive in 8 sample Thai provinces: Bangkok, Nakhon Ratchasima, Khon Kaen, Chiang Mai, Phuket, Chonburi, Songkhla, and Rayong.

| Country | Provinces/states/regions |
|---|---|
| Thailand | 77 |
| Vietnam | 64 |
| Philippines | 17 |
| Singapore | 5 (aggregated planning areas) |
| Cambodia | 25 |
| Laos | 18 |
| Malaysia | 16 (13 states + 3 federal territories) |
| Myanmar | 14 (Naypyidaw union territory not separately delineated in the source boundary data; folded into Mandalay Region — see 2.3) |

The Ookla study period is Q1 2023 through Q4 2025 for all eight countries (some countries have a few missing quarters depending on data availability). M-Lab NDT7 data is used for descriptive comparison currently for Thailand (Q4 2023–Q1 2025 overlap) and Vietnam (Q1 2023–Q4 2025 overlap); Philippines NDT7 is being collected by a research collaborator and not yet available; Singapore, Cambodia, Myanmar, Laos, and Malaysia NDT7 are not yet in scope.

---

## 2. Data

This research draws on five main data sources.

### 2.1 Network Performance Data (Ookla Open Data)

Ookla Open Data is an open dataset released under the Creative Commons Attribution 4.0 International (CC BY 4.0) license, compiled from real-world internet speed tests submitted through the Speedtest by Ookla application worldwide. Data is stored in *tile* format using the Quadkey system at zoom level 16, where each tile is approximately 610 × 610 meters at the equator. Each tile reports the average of the following variables:

| Field | Description |
|---|---|
| `avg_d_kbps` | average download speed (kilobits per second) |
| `avg_u_kbps` | average upload speed (kilobits per second) |
| `avg_lat_ms` | average latency (milliseconds) |
| `tests` | number of tests in the tile |
| `devices` | number of devices tested |

Each quarterly release covers roughly 6.3 million tiles worldwide. This study uses both *fixed* (wired broadband) and *mobile* (cellular) tile sets, loaded via Amazon S3 paths of the form:

```
s3://ookla-open-data/parquet/performance/type=fixed/
  year={YEAR}/quarter={Q}/{YEAR}-{MM}-01_performance_fixed_tiles.parquet
s3://ookla-open-data/parquet/performance/type=mobile/
  year={YEAR}/quarter={Q}/{YEAR}-{MM}-01_performance_mobile_tiles.parquet
```

Structure and processing steps are identical between the two types, differing only in the source parquet path. Country coverage as of this draft:

| Country | Provinces/regions | Ookla status |
|---|---|---|
| Thailand | 77 | Done — full EDA, fixed + mobile combined |
| Vietnam | 64 | Done |
| Philippines | 17 | Done |
| Singapore | 5 (aggregated planning areas) | Done, but small-n — some multivariate models degenerate |
| Cambodia | 25 | Done — no official sub-national GDP available (see 2.4) |
| Laos | 18 | Done — no official sub-national GDP available (see 2.4) |
| Malaysia | 16 | Done — real state-level GDP (DOSM) |
| Myanmar | 14 | Done — no official sub-national GDP available (see 2.4); Naypyidaw folded into Mandalay Region (see 2.3) |

All eight countries' raw Ookla tiles come from the same global quarterly parquet releases (no per-country download was needed for the four newly added countries) — only the boundary and reference data below had to be newly compiled per country.

### 2.2 M-Lab Network Diagnostic Test Data (NDT7)

M-Lab's Network Diagnostic Test (NDT7) is another open dataset, published via Google BigQuery Public Datasets. Unlike Ookla, results are stored per-test (not pre-aggregated into tiles), giving a finer-grained view of the distribution of measured values.

**Thailand.** The Thailand NDT7 pipeline joins raw per-test logs (`mlab_results/*.parquet`, ~5.2M client-IP rows in the lookup table) against an ISP-classification table built by keyword matching on ISP name (`client_complete.parquet`: `client_ip`, `isp`, `category`, `description`, `network_type`), splitting traffic into `broadband` and `cellular`.

**Vietnam.** Vietnam NDT7 data (delivered by a research collaborator, 2026-07-13) uses a more rigorous approach: because Vietnam's largest ISPs (Viettel, VNPT) are conglomerates running both mobile and fixed service on the same ASN, ISP name alone cannot distinguish network type. Classification instead uses a **per-IP ip-api lookup** — three rounds of fetching covering the full ~1.84M-IP conglomerate population, achieving 100% resolution (0% `unknown`, down from an initial 8.5%) — combined with curated name lists for smaller ISPs and keyword matching for hosting/CDN traffic. This yields **four** `network_type` categories rather than Thailand's two: `broadband` (89.2% of rows), `cellular` (5.1%), `hosting` (5.6%, CDN/cloud/VPN — excluded from consumer analysis), and `unknown` (0%). Province is assigned via point-in-polygon join against `vietnam_provinces.geojson` with a nearest-polygon fallback, achieving 100% coverage across 63 provinces. Delivered as a single pre-joined file, `mlab_vn_clean.parquet` (24.7M rows, 21 columns, 1.2 GB), already containing per-test throughput, latency, ISP classification, and province — see `data/ndt7/vn/README.md` for full methodology.

**Philippines / Singapore.** Philippines NDT7 is being collected by a collaborator and not yet delivered as of this draft. Singapore NDT7 scope is unconfirmed.

### 2.3 Spatial Boundary Data (GeoJSON)

Administrative boundaries (ADM1: province/state/region) for all eight countries, in GeoJSON format, WGS84/EPSG:4326 coordinate system, used for spatial joins to assign each Ookla tile or NDT7 test point to a province/region. The four newly added countries (Cambodia, Myanmar, Laos, Malaysia) were sourced from geoBoundaries' open ADM1 release, same as the original four. One data limitation: geoBoundaries' Myanmar ADM1 boundary set contains 14 units rather than the official 15 (7 states + 7 regions + Naypyidaw union territory) — Naypyidaw, carved administratively out of Mandalay Region in 2005, is not delineated as a separate polygon in this source. Its 2014 census population and area are folded into Mandalay Region for this study, which should be read as a coarsening of that one unit rather than a missing-data gap.

### 2.4 Province/Region Reference Data

A dataset compiled by the researcher from official sources per country, containing:

- **Population**: national statistical/civil-registry sources per country (e.g., Thailand's Department of Provincial Administration; Wikipedia-sourced census/estimate figures for the four newly added countries)
- **Area and density**: Wikipedia / national mapping agencies
- **GDP per capita**: national economic-planning agencies per country (e.g., Thailand's NESDC) where available, expressed in three forms — raw nominal value, USD PPP, and THB-equivalent for cross-country comparability. For Cambodia, Myanmar, and Laos, no official sub-national (province-level) GDP series exists — Cambodia's National Institute of Statistics confirms provincial economic accounts are still under development, and no equivalent was found for Myanmar or Laos — so national GDP per capita (World Bank, 2021, current US$) is repeated across all provinces for these three countries, following the same convention already used for Singapore (which also lacks sub-national GDP). This is a real data-quality limitation: any GDP-vs-speed regression for these four countries (Singapore included) has zero within-country GDP variance by construction and cannot identify a GDP effect. Malaysia is the exception among the new countries — real state-level nominal GDP per capita for 2021 is published by Malaysia's Department of Statistics (DOSM) and is used directly, on the same footing as Thailand/Vietnam/Philippines.
- **Internet Tier**: a researcher-defined hypothetical variable (four tiers, from "expected fastest" to "expected slowest," based on economic/urbanization proxies) — see Table 1 for the Thailand tier assignment used as the template. Where a usable proxy exists, tier is derived from that (Cambodia: quartiles of HDI-by-province, Cambodia Human Development Report 2023; Malaysia: quartiles of actual GDP per capita); otherwise (Myanmar, Laos) tier is derived from quartiles of population density, the same fallback proxy used elsewhere in this study when no better economic signal is available.

**Table 1. Internet Tier definitions (Thailand)**

| Tier | Description | Example provinces |
|---|---|---|
| 1 | Expected fastest | Bangkok, Chonburi, Rayong, Phuket |
| 2 | Above average | Chiang Mai, Khon Kaen, Surat Thani |
| 3 | Middle (mid-GDP provincial cities) | Nakhon Ratchasima, Phitsanulok, Udon Thani |
| 4 | Expected slowest | Mae Hong Son, Narathiwat, Nong Bua Lamphu |

---

## 3. Methodology

### 3.1 Data Processing Pipeline

**Step 1 — Spatial filtering.** From the global Ookla dataset, tiles are first filtered to each country's bounding box before loading into memory, reducing data volume, using PyArrow's `filters` parameter against each country's geographic extremes (north–south–east–west).

**Step 2 — Province/region assignment (spatial join).** Tile centroid coordinates (`tile_x`, `tile_y`) are converted to a Point GeoDataFrame in EPSG:4326, then spatially joined against the province/region boundary layer using an `intersects` predicate.

**Step 3 — Province-level aggregation (weighted average).** Download speed, upload speed, and latency are aggregated to the province level as a test-count-weighted average:

$$\bar{v}_j = \frac{\sum_{i \in j} w_i \cdot v_i}{\sum_{i \in j} w_i}$$

where $\bar{v}_j$ is the weighted average for province $j$, $v_i$ is the measured value for tile $i$, and $w_i$ is the test count in tile $i$. Weighting by test count gives tiles with more tests (reflecting denser, more reliable user populations) proportionally more influence on the province average than tiles with only a handful of tests.

**Step 4 — Master dataset construction.** All quarters are combined and merged with province reference data. For Thailand this yields 77 provinces × 11 quarters = 847 rows (before coverage/reliability checks); the same pipeline runs per country. Speed units are converted from kbps to Mbps, and derived variables are computed, including the upload/download ratio (`ul_dl_ratio`).

**Step 5 — Reliability filter.** A per-province-quarter `is_reliable` flag — `total_tests >= 100 AND n_tiles >= 5` — is computed and (as of the 2026-07-07 revision) actually applied to filter all downstream statistics in every country notebook, rather than merely computed and left unused.

**Step 6 — NDT7 province-level aggregation.** Because NDT7 delivers per-test points rather than pre-aggregated tiles, records are first binned into the same zoom-16 slippy-tile scheme Ookla publishes in (so `n_tiles` stays a comparable spatial-coverage proxy across both sources and across countries), aggregated per tile (mean/median throughput, mean latency, test count; tiles with fewer than 3 tests are dropped), then aggregated up to province × quarter using the same test-count-weighted average as Step 3. The same `is_reliable` threshold (`total_tests>=100 & n_tiles>=5`) is applied. For Vietnam, per-test province was already assigned via the collaborator's point-in-polygon join (more precise than a tile-centroid join); the tile-binning step is retained purely to keep `n_tiles`/`is_reliable` comparable with the Ookla-side and Thailand-side methodology, not because the underlying province assignment needs it.

### 3.2 Cross-Country Comparison

To compare Thailand against the other seven countries, each country's province-level, reliability-filtered data is collapsed to one row per province (mean across all reliable quarters), then compared as follows:

1. **Distributional comparison** — box plots of mean download/upload speed by country.
2. **Omnibus test** — Kruskal-Wallis H-test across the eight country groups (chosen over one-way ANOVA given the small sample sizes for Singapore, n=5, and Myanmar, n=14, where a normality assumption is hard to justify).
3. **Pairwise comparison** — Mann-Whitney U test, Thailand vs. each other country individually, to identify which specific country/countries differ from Thailand rather than only that "some" country differs.
4. **Cross-country regression** — OLS of `mean_dl ~ log(GDP per capita) + log(population density) + country` (Thailand as reference category), to test whether a country-level fixed effect remains significant after controlling for socioeconomic context — i.e., whether cross-country gaps are explained by wealth/density or reflect something country-specific. Note the GDP term is degenerate for Singapore, Cambodia, Myanmar, and Laos (no within-country GDP variance — see 2.4), so this regression's GDP coefficient is identified mainly off Thailand/Vietnam/Philippines/Malaysia's within-country variation, and country fixed effects for the zero-variance countries should be read with that caveat in mind.
5. **Fixed-vs-mobile gap** — the same comparison repeated for mobile data, and the fixed/mobile speed ratio computed per country, to check whether Thailand's public fixed (#13 globally) vs. mobile (#39 globally) ranking split is visible in the measured data and whether it is unusually large relative to its neighbors.
6. **Capital/top-city comparison** — a supplementary comparison of each country's capital province/region against its own national average, and each country's top-5 fastest provinces, to check whether "how good is a country's internet" is being driven by the capital specifically or is broader-based.

### 3.3 Ookla-vs-NDT7 Cross-Validation

For each country where both sources exist (currently Thailand and Vietnam), Ookla and NDT7 results are compared at the province × quarter level, restricted to `is_reliable` rows in both sources, over the quarters where both datasets overlap:

1. **Coverage comparison** — the share of provinces meeting the reliability threshold, plotted over time for both sources, since NDT7 reliable coverage is not necessarily stable across quarters (Vietnam's NDT7 coverage, for instance, decays from ~48% of provinces reliable in Q1 2023 to ~11% by Q4 2025, with data volume heavily concentrated in one quarter — a caveat that must be carried into any interpretation of later-period comparisons).
2. **Distributional comparison** — histograms of download/upload speed for each source.
3. **Province-level agreement** — provinces with reliable data in *both* sources are averaged across the overlap period, then compared with Pearson and Spearman correlation, to test whether the two sources agree on relative province ranking even if absolute values differ.
4. **Magnitude gap** — the mean/ratio of Ookla vs. NDT7 download speed, tested for statistical significance with a paired Wilcoxon signed-rank test (chosen over a paired t-test given no strong reason to assume the paired differences are normally distributed).

A necessary caveat: this is not a paired test in the strict sense (different users, different times, different service providers measured by each platform), and there is no ground truth establishing which source is "more accurate." Any gap found may reflect both genuine network differences and methodology differences between an active, user-initiated test (Ookla) and a passive, background test (NDT7) — consistent with MacMillan et al. (2023), who found NDT7 tends to underreport speed by 12–56% relative to Ookla-style active tests, particularly when latency (RTT) exceeds 200 ms.

### 3.4 Correlation and Regression Analysis

Pearson correlation and ordinary least squares (OLS) regression are used to test the relationship between GDP per capita and mean download speed, and between log(population density) and mean download speed, within each country. Population density is log-transformed due to its strongly right-skewed distribution. A multivariate OLS extending this to `mean_dl ~ log(GDP) + log(density) + tier + region` is fit per country to test whether these factors jointly explain speed variation (see Results for country-by-country R² and coefficient significance).

### 3.5 Upload/Download Ratio Analysis

The upload-to-download speed ratio (UL/DL ratio) is used as an indirect indicator of underlying network technology, since:

- Fiber (GPON/FTTH): ratio ≈ 0.9–1.0
- HFC cable: ratio ≈ 0.2–0.5
- ADSL: ratio ≈ 0.1–0.2

A national average ratio close to 1.0 is taken as evidence of widespread fiber (FTTH) deployment.

### 3.6 Anomaly/Divergence Detection (dropped, 2026-07-20)

An earlier iteration of this pipeline computed a composite per-province "divergence score" — seven z-scored dimensions (tier-expectation residual, GDP-expectation residual, density-expectation residual, regional deviation, UL/DL ratio deviation, latency regional deviation, and coverage deviation) summed to surface a "divergence leaderboard" of the most anomalous provinces. This was removed from all eight Ookla EDA notebooks as no longer a necessary part of the analysis. `paper.tex`'s existing methodology text (which still describes an even older seven-flag version of this idea) should likewise be treated as superseded and dropped rather than reconciled, once the LaTeX manuscript is revisited. Tier, GDP, and density are still analyzed directly (Sections 3.2 and 3.4) — only the composite anomaly-scoring layer on top of them was cut.

### 3.7 Tools and Software

All analysis is performed in Python 3.12, in an isolated virtual environment (`datasci` kernel), using the following core libraries:

| Library | Use |
|---|---|
| `pandas`, `numpy` | tabular data handling and processing |
| `geopandas` | spatial analysis (spatial join, CRS handling) |
| `pyarrow` | reading Parquet files with predicate pushdown |
| `scipy.stats` | statistical analysis (Pearson/Spearman correlation, Kruskal-Wallis, Mann-Whitney, Wilcoxon, z-scores) |
| `statsmodels` | OLS regression, including multivariate and cross-country fixed-effects models |
| `matplotlib` | data visualization |

---

## 4. Preliminary Results

*Full Results/Discussion write-up is still pending completion of Section 3.2's cross-country statistical tests (Kruskal-Wallis/Mann-Whitney/OLS with country fixed effects) and Section 3.3's Ookla-vs-NDT7 agreement tests, neither of which has a notebook yet as of this draft. The finding below is posted early because the analysis (`notebooks/comparison/rq2_trends.ipynb`) is already complete.*

### 5.1 Thailand's download growth is regionally slow in relative terms, but not in absolute terms

Extending RQ2's quarterly trend method across all eight countries (Ookla fixed, median download per quarter) shows Thailand's Q1-2023-to-Q4-2025 growth (+42.0%, 207.1 → 294.0 Mbps) is the **second-slowest of the eight countries** — only the Philippines grows slower (+23.6%):

| Country | 2023-Q1 (Mbps) | 2025-Q4 (Mbps) | % growth |
|---|---|---|---|
| Myanmar | 20.3 | 53.6 | +163.8% |
| Cambodia | 25.3 | 61.7 | +144.1% |
| Vietnam | 92.4 | 209.2 | +126.4% |
| Singapore | 282.0 | 553.8 | +96.4% |
| Laos | 32.0 | 62.2 | +94.4% |
| Malaysia | 124.6 | 223.6 | +79.5% |
| **Thailand** | **207.1** | **294.0** | **+42.0%** |
| Philippines | 96.4 | 119.1 | +23.6% |

Read alongside RQ1's snapshot finding (Thailand clears every app-requirement threshold in all 77 provinces every quarter, with no headroom to gain from), this is best read as a **high-base/catch-up effect rather than stagnation**: the four fastest-growing countries (Myanmar, Cambodia, Vietnam, Laos) all start from a much lower 2023 base (20–92 Mbps), consistent with catch-up growth, and Thailand's absolute download level stays **second-highest of the eight countries throughout the entire period**, behind only Singapore.

One comparison does not fit that base-effect story cleanly and is flagged for the Discussion section rather than resolved here: Singapore, the only country starting *above* Thailand (282 Mbps), still posts +96.4% growth — more than double Thailand's rate — showing a high base does not mechanically cap growth. Malaysia (+79.5% from a lower 2023 base of 124.6 Mbps than Thailand's) growing nearly twice as fast as Thailand from a lower starting point is the sharpest open question, plausibly pointing to a difference in infrastructure-investment cycle timing rather than pure diminishing-returns economics — worth investigating once the cross-country regression (Section 3.2) is run.

---

## 5. Limitations and Future Directions

This study's cross-country, cross-platform design surfaces several limitations worth stating plainly rather than glossing over, since they bound how far the eventual results can be generalized.

**GDP identification is degenerate for four of eight countries.** Singapore, Cambodia, Myanmar, and Laos have no official sub-national GDP series, so national GDP per capita is repeated across every province within each of those countries (Section 2.4). Any regression term for GDP (Sections 3.2 item 4, 3.4) has zero within-country variance for these four — the coefficient is identified almost entirely off Thailand, Vietnam, the Philippines, and Malaysia's within-country spread. Country fixed effects for the zero-variance countries should be read as absorbing GDP's effect rather than isolating a genuinely GDP-independent residual.

**NDT7 cross-validation covers only 2 of 8 countries, and coverage is not stable over time.** Ookla-vs-NDT7 comparison (Section 3.3) is currently limited to Thailand and Vietnam; the Philippines is pending a collaborator delivery, and Singapore/Cambodia/Myanmar/Laos/Malaysia have no NDT7 cross-validation planned yet. Even within Vietnam, NDT7's reliable-province coverage decays sharply over the study period (~48% of provinces reliable in Q1 2023 down to ~11% by Q4 2025, with volume heavily concentrated in one quarter) — later-period Ookla-vs-NDT7 comparisons rest on a shrinking, non-random subset of provinces.

**No ground truth exists for the Ookla-vs-NDT7 gap.** Because the two platforms sample different users at different times through different mechanisms (active/user-initiated vs. passive/background), any measured gap is confounded between genuine network differences and methodology differences (Section 3.3). We do not have — and this design cannot produce — a way to attribute a given gap to one cause over the other; MacMillan et al. (2023)'s finding that NDT7 underreports speed by 12–56% relative to Ookla in a US context is used as prior context, not as a correction applied to our numbers.

**One administrative unit is coarsened by a source-data gap.** geoBoundaries' Myanmar ADM1 layer does not delineate Naypyidaw separately from Mandalay Region; its population/area are folded into Mandalay for this study (Section 2.3), so any Myanmar province-level result should be read with that one unit understood as a merged aggregate, not a genuine administrative boundary.

**The composite divergence-scoring layer was cut mid-project (Section 3.6) rather than completed.** An earlier per-province anomaly score across seven z-scored dimensions was implemented in all eight Ookla notebooks and then removed as not necessary for the analysis; tier, GDP, and density are still analyzed directly, but a synthesized "which provinces break the pattern" view is not part of the current results.

**Future work.** Extending NDT7 cross-validation to the remaining six countries (contingent on data availability), revisiting whether a lighter-weight anomaly/outlier flag is worth reintroducing now that the composite-score approach has been dropped, and reconciling `paper.tex`'s older methodology text (which still describes a superseded seven-flag anomaly framework) once the LaTeX manuscript is revisited, are the most immediate next steps.

---

## References

- Röller, L.-H., & Waverman, L. (2001). *Telecommunications Infrastructure and Economic Development: A Simultaneous Approach*. The American Economic Review, 91(4), 909–923.
- Ookla. (2023). *Speedtest by Ookla Global Fixed and Mobile Network Performance Maps* [Dataset]. https://github.com/teamookla/ookla-open-data
- International Telecommunication Union. (2024). *Measuring digital development: Facts and Figures 2024*. ITU Publications.
- MacMillan, K., Mangla, T., Saxon, J., Marwell, N. P., & Feamster, N. (2023). *A Comparative Analysis of Ookla Speedtest and Measurement Lab's Network Diagnostic Test (NDT7)*. Proceedings of the ACM on Measurement and Analysis of Computing Systems, 7(1), Article 19. https://dl.acm.org/doi/epdf/10.1145/3579448
- Nation Thailand. (2025a, March 1). *Thailand ranks 13th in the world for fixed broadband speed*. https://www.nationthailand.com/business/tech/40046895
- Nation Thailand. (2025b, May 23). *Thai telecom outages expose duopoly flaws, experts call for fair competition*. https://www.nationthailand.com/business/tech/40050343
- Electronic Transactions Development Agency (ETDA). (2024, March 18). *Leading online issues that caused annoyances among internet users in Thailand in 2022* [Graph]. Statista. https://www.statista.com/statistics/1129934/thailand-leading-online-problems-internet-users/
- geoBoundaries. (2023). *geoBoundaries Global Database of Political Administrative Boundaries* [Dataset]. https://www.geoboundaries.org
- World Bank. (2026). *GDP per capita (current US$) and GDP per capita, PPP (current international $)* [Dataset]. World Bank Open Data. https://data.worldbank.org
- Department of Statistics Malaysia (DOSM). (2022). *Gross Domestic Product (GDP) by State, 2021*. https://www.dosm.gov.my
- National Institute of Statistics, Ministry of Planning, Cambodia. *Statistical Yearbook* [confirms no province-level GRDP series currently published]. https://www.nis.gov.kh
