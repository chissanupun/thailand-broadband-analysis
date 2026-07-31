# Data Sources & Citations

All sources used in this project. Wikipedia replaced with primary official sources throughout.

---

## 1. Primary Dataset — Ookla Speedtest Fixed Broadband Performance

**Used for:** Core analysis dataset. Quarterly tile-level fixed broadband download speed, upload speed, latency, test count, device count across Thailand (2023 Q1 – 2025 Q4).

**Citation (APA):**
> Ookla. (2023–2025). *Speedtest® by Ookla® Global Fixed and Mobile Network Performance Maps* [Dataset]. Retrieved [access date] from Amazon Web Services Open Data Registry. https://registry.opendata.aws/speedtest-global-performance/

**Official attribution (required by CC BY-NC-SA 4.0 license):**
> "Speedtest® by Ookla® Global Fixed and Mobile Network Performance Maps was accessed on [DATE] from AWS. Based on [AUTHOR'S] analysis of Speedtest® by Ookla® Global Fixed and Mobile Network Performance Maps for 2023 Q1 – 2025 Q4. Ookla trademarks used under license and reprinted with permission."

**License:** Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)

**Repository:** https://github.com/teamookla/ookla-open-data

**S3 path pattern:**
```
s3://ookla-open-data/parquet/performance/type=fixed/year={YEAR}/quarter={Q}/{YEAR}-{MM}-01_performance_fixed_tiles.parquet
```

---

## 2. Province Population Data

**Used for:** Population (Dec 2024), population density per province in `province_reference.csv`.

**⚠️ Wikipedia replaced by:**

**Primary source — DOPA Bureau of Registration Administration (BORA):**
> กรมการปกครอง กระทรวงมหาดไทย (Bureau of Registration Administration, Department of Provincial Administration, Ministry of Interior). (2024). *สถิติประชากรและบ้านจากการทะเบียนราษฎร ณ เดือนธันวาคม พ.ศ. 2567* [Population and household statistics from civil registration, December 2024]. https://stat.bora.dopa.go.th

**Citation (APA):**
> Bureau of Registration Administration (BORA), Department of Provincial Administration (DOPA). (2025). *Population statistics by province, December 2024*. Ministry of Interior, Thailand. Retrieved from https://stat.bora.dopa.go.th

**Secondary/aggregated source — NSO Statistical Yearbook:**
> National Statistical Office of Thailand (NSO). (2025). *Statistical Yearbook Thailand 2025*. National Statistical Office, Ministry of Digital Economy and Society, Bangkok, Thailand. https://www.nso.go.th/public/e-book/Statistical-Yearbook/SYB-2025/99/

**Note:** NSO compiles DOPA civil registration data. Both are citable; DOPA is the upstream primary source, NSO is the aggregated publication. For academic papers, cite NSO Statistical Yearbook (has ISBN/ISSN) or DOPA directly.

---

## 3. Gross Provincial Product (GPP) per Capita

**Used for:** `gdp_per_capita_thb_2021` column in `province_reference.csv`. Economic proxy for expected internet quality.

**⚠️ Wikipedia and thaiwebsites.com replaced by:**

**Primary source — NESDC:**
> Office of the National Economic and Social Development Council (NESDC). (2023). *Gross Regional and Provincial Product: Chain Volume Measures* [Report, data year 2021]. Office of the Prime Minister, Bangkok, Thailand. https://www.nesdc.go.th/en/info/gross-regional-and-provincial-product-gpp/

**Citation (APA):**
> สำนักงานสภาพัฒนาการเศรษฐกิจและสังคมแห่งชาติ [Office of the National Economic and Social Development Council (NESDC)]. (2023). *ผลิตภัณฑ์มวลรวมภาค และจังหวัด แบบปริมาณลูกโซ่ ฉบับ พ.ศ. 2566 [Gross Regional and Provincial Product, Chain Volume Measures, 2023 edition]*. NESDC. https://www.nesdc.go.th/en/info/gross-regional-and-provincial-product-gpp/

**Data year:** 2021 (latest available at time of writing; NESDC publishes with ~2 year lag)

---

## 4. Thailand Province Boundaries (GeoJSON)

**Used for:** Spatial join of Ookla tile centroids to Thai provinces. Map visualizations.

**Current file:** `data/thailand_provinces.geojson` (77 provinces, EPSG:4326, property: `name`)

**Possible sources (verify which was used):**

**Option A — cvibhagool/thailand-map (MIT License):**
> cvibhagool. (n.d.). *thailand-provinces.geojson* [GitHub repository]. Retrieved from https://github.com/cvibhagool/thailand-map

**Option B — GADM v4.1 (recommended for academic papers — authoritative):**
> GADM. (2022). *GADM database of Global Administrative Areas, version 4.1: Thailand (THA), Admin Level 1* [Dataset]. University of California, Davis. https://gadm.org/download_country.html

**Option C — apisit/thailand.json (MIT License):**
> Toompakdee, A. (2012–present). *thailand.json: Thailand GeoJSON file* [GitHub repository]. https://github.com/apisit/thailand.json

**Recommendation:** Use **GADM v4.1** for publication — it is the standard administrative boundary dataset cited in peer-reviewed GIS literature. Has consistent province name handling and explicit academic license.

**GADM citation (APA):**
> University of California, Davis. (2022). *GADM database of Global Administrative Areas, version 4.1* [Dataset]. https://gadm.org

---

## 5. National Internet Infrastructure Context

**Used for:** Background context, internet tier assumptions in `province_reference.csv`, EDA interpretation.

**5a. NBTC — National Broadband & Telecoms Commission Thailand:**
> สำนักงานคณะกรรมการกิจการกระจายเสียง กิจการโทรทัศน์ และกิจการโทรคมนาคมแห่งชาติ [NBTC]. (2024). *TTID: Thailand Telecom Industry Database — Fixed Broadband Subscribers & Penetration*. https://ttid.nbtc.go.th/internet_sub

> NBTC. (2024). *Internet statistics report in Thailand*. http://webstats.nbtc.go.th

**Key stats used:**
- Fixed broadband: 15.75 subscribers per 100 people (2023)
- Total fixed BB subscribers: 11,291,200 (2023)

**5b. Speedtest Global Index (Ookla):**
> Ookla. (2024). *Speedtest Global Index: Thailand fixed broadband performance* [Online report]. https://www.speedtest.net/global-index/thailand

**Key stats used:**
- National avg fixed download: ~237 Mbps (13th globally, early 2025)

**5c. ETDA / Digital Economy report:**
> Electronic Transactions Development Agency (ETDA). (2024). *Thailand Internet User Behavior Survey 2024*. Ministry of Digital Economy and Society. https://www.etda.or.th/en/

**Key stats used:**
- Urban internet usage: 92% of population
- Rural internet usage: 85% of population

---

## 6. Public Perception & Discourse — "Is Thai Internet Good or Bad?"

**Used for:** Introduction framing — the contradiction between national-level rankings ("good") and user-reported complaints ("bad") that motivates this paper's research question.

**6a. Ookla — Speedtest Global Index ranking (the "good" side):**
> Nation Thailand. (2025, March 1). *Thailand ranks 13th in the world for fixed broadband speed*. https://www.nationthailand.com/business/tech/40046895

**Key stats used:** Thailand fixed broadband — 13th globally, 237.05 Mbps avg download. Thailand mobile — 39th globally, 101.56 Mbps avg download. Gap between fixed rank and mobile rank is itself evidence the "good/bad" question depends on network type.

**6b. ETDA / Statista — user complaint survey (the "bad" side):**
> Electronic Transactions Development Agency (ETDA). (2024, March 18). *Leading online issues that caused annoyances among internet users in Thailand in 2022* [Graph]. Statista. https://www.statista.com/statistics/1129934/thailand-leading-online-problems-internet-users/

**Key stat used:** 64.65% of Thai internet users cite slow connection speed as their top annoyance (2022 survey, published by ETDA — same agency already cited in §5c).

**6c. Nation Thailand — telecom duopoly / outage coverage (the "bad" side, post-merger):**
> Nation Thailand. (2025, May 23). *Thai telecom outages expose duopoly flaws, experts call for fair competition*. https://www.nationthailand.com/business/tech/40050343

**Key stats used:** Foundation for Consumers survey — 81% of users experienced network issues in the prior 6 months; NBTC complaint volume rose from <1,000 to ~3,000 cases in the first 7 months of 2025; nationwide True Corporation outage (May 2025) caused documented business losses.

**6d. Methodology reference — comparing two independent measurement platforms:**
> MacMillan, K., Mangla, T., Saxon, J., Marwell, N. P., & Feamster, N. (2023). *A Comparative Analysis of Ookla Speedtest and Measurement Labs Network Diagnostic Test (NDT7)*. Proc. ACM Meas. Anal. Comput. Syst., 7(1), Article 19. https://dl.acm.org/doi/epdf/10.1145/3579448

**Used for:** Cross-validation methodology between Ookla and NDT7 (see `comparison-research.md`); also already the source PDF at `docs/macmillan2023_ndt7_vs_ookla.pdf`.

**6e. Application-requirement thresholds + busy-hour method (RQ1 and RQ4):**
> Lübben, R., & Misfeld, N. (2022). *Exploring the Measurement Lab Open Dataset for Internet Performance Evaluation: The German Internet Landscape*. Electronics, 11(1), 162. https://doi.org/10.3390/electronics11010162

**Verified against the published paper 2026-07-30.** Earlier drafts of this project cited this work with
the wrong author initial ("Misfeld, T.") and a placeholder title ("App-requirement thresholds for
network quality") that does not exist. Both are corrected above.

**Key content used — Table 5, "Exemplary application requirements":**

| Application | Data rate | Latency |
|---|---|---|
| Voice | 64 kbps | 200 ms |
| Video streaming (HD) | 5 Mbps | few seconds |
| Video streaming (UHD) | 25 Mbps | few seconds |
| Cloud gaming | 44 Mbps | 25 ms |

All four RQ1 thresholds in `paper_draft.md` match this table exactly. We apply the voice row's latency
criterion only, not its 64 kbps rate.

**6f. Primary sources behind the thresholds** — Lübben & Misfeld's table is a compilation, so these are
the sources that actually establish each number. Traced from their reference list, 2026-07-30.

> **Voice, 200 ms** — International Telecommunication Union. (2003). *ITU-T Recommendation G.114:
> One-Way Transmission Time*. https://www.itu.int/rec/T-REC-G.114-200305-I/en

> **Cloud gaming, 44 Mbps** — Di Domenico, A., Perna, G., Trevisan, M., Vassio, L., & Giordano, D.
> (2021). *A Network Analysis on Cloud Gaming: Stadia, GeForce Now and PSNow*. Network, 1(3), 247–260.
> https://doi.org/10.3390/network1030015

> **Cloud gaming, 25 ms** — Flinck Lindström, S., Wetterberg, M., & Carlsson, N. (2020). *Cloud Gaming:
> A QoE Study of Fast-paced Single-player and Multiplayer Gaming*. IEEE/ACM UCC 2020, Leicester, UK,
> pp. 34–45.

> **HD 5 Mbps and UHD 25 Mbps** — Netflix Help Center, *Netflix-recommended internet speeds*.
> https://help.netflix.com/en/node/306 — note Lübben & Misfeld assert this in prose with **no numbered
> citation**, the only threshold in their table lacking one.

⚠️ **Netflix has since revised its UHD figure.** The help page now publishes **15 Mbps** for Ultra HD,
not the 25 Mbps in force when Lübben & Misfeld compiled Table 5 (verified by direct fetch 2026-07-30).
This matters: at 15 Mbps every country in our study clears UHD at ≥98.5%, and the Myanmar (22.1%) and
Indonesia (88.1%) UHD shortfalls we report at 25 Mbps disappear entirely. `paper_draft.md` §3.4 now
carries a sensitivity table and states that UHD is a descriptive tier boundary only — **cloud gaming
carries the RQ1 argument**, and both of its criteria rest on peer-reviewed measurement rather than
vendor guidance.

**Also used for RQ4:** their §4.2 "Busy Hours and Days" is the method our peak-hour analysis follows —
identify busy hours from measurement volume, then test whether achievable throughput falls during them.
Their paper is an M-Lab NDT study of Germany, i.e. the same dataset family we use, which makes it the
closest antecedent to this study rather than merely a source of numbers.

---

## 7. Summary Table — Source vs. Use

| Data | Column in CSV | Primary Source | Alternative to |
|------|---------------|----------------|----------------|
| Province boundaries | (GeoJSON) | GADM v4.1 | apisit/thailand.json |
| Population Dec 2024 | `pop_2024` | DOPA/BORA stat.bora.dopa.go.th | Wikipedia |
| Area (km²) | `area_km2` | NSO Statistical Yearbook 2025 | Wikipedia |
| GPP per capita 2021 | `gdp_per_capita_thb_2021` | NESDC GPP Chain Volume Measures | Wikipedia / thaiwebsites.com |
| Internet tier (proxy) | `internet_tier` | Derived (NESDC + NBTC context) | — |
| Fixed BB speed tiles | (parquet files) | Ookla Open Data (CC BY-NC-SA 4.0) | — |
| Mobile speed tiles | (parquet files) | Ookla Open Data (CC BY-NC-SA 4.0) | — |
| Per-test network diagnostics | (NDT7 tables) | M-Lab NDT7 via BigQuery Public Datasets | — |
| "Good/bad" perception framing | (paper §1 only) | Ookla Speedtest Global Index, ETDA/Statista, Nation Thailand | — |

---

## 8. Note on Wikipedia

Wikipedia was used during initial exploration only. For publication, all data traces back to:
- **DOPA** (population)
- **NESDC** (GPP/economic)
- **NSO** (area, density, demographic aggregates)
- **NBTC** (broadband penetration, subscribers)
- **Ookla** (speed measurement data — primary dataset)

Wikipedia is not cited in the final paper. Use the primary government sources above.

---

## 9. Eight-Country Expansion — Additional Sources (2026-07-27 scope shift)

Project scope moved from Thailand-primary to an equal 8-country comparison (§2.1 of
`paper_draft.md`). Sections 1–8 above cover Thailand-specific sources only; this section
covers the sources added for the other seven countries. All four already appear in
`paper_draft.md`'s own References list — reproduced here so `citations.md` stays the
single place that documents dataset provenance/license per project convention.

**9a. Spatial boundaries — geoBoundaries (all 8 countries, ADM1):**
> geoBoundaries. (2023). *geoBoundaries Global Database of Political Administrative Boundaries* [Dataset]. https://www.geoboundaries.org

**Used for:** Province/state/region (ADM1) boundaries for all eight countries, WGS84/EPSG:4326.
**License:** Open (see site for per-boundary attribution terms).
**Known limitation:** Myanmar layer has 14 units, not the official 15 — Naypyidaw (split from
Mandalay Region in 2005) is not delineated separately; its population/area are folded into
Mandalay Region. Flagged in `paper_draft.md` §2.1.3 and §5 wherever it affects a result.

**9b. GDP per capita — World Bank (Cambodia, Myanmar, Laos, Singapore):**
> World Bank. (2026). *GDP per capita (current US$) and GDP per capita, PPP (current international $)* [Dataset]. World Bank Open Data. https://data.worldbank.org

**Used for:** National GDP per capita, repeated across every province for the four countries
with no official sub-national GDP series (Cambodia, Myanmar, Laos, Singapore). Any GDP
regression term for these countries has zero within-country variance by construction — see
`paper_draft.md` §5 (Limitations).

**9c. GDP by state — Department of Statistics Malaysia (DOSM):**
> Department of Statistics Malaysia (DOSM). (2022). *Gross Domestic Product (GDP) by State, 2021*. https://www.dosm.gov.my

**Used for:** `gdp_per_capita` column for Malaysia — the one non-Thailand country with a real
state-level GDP series (used directly, not a repeated national figure).

**9d. Cambodia — National Institute of Statistics (confirms no sub-national series):**
> National Institute of Statistics, Ministry of Planning, Cambodia. *Statistical Yearbook* [confirms no province-level GRDP series currently published]. https://www.nis.gov.kh

**Used for:** Documents the absence of a Cambodian province-level GDP series — justifies why
Cambodia falls back to the World Bank national figure (9b) rather than a real sub-national one.

### 9e. Summary Table Addendum — Non-Thailand Countries

| Data | Column in CSV | Primary Source | Countries |
|------|---------------|-----------------|-----------|
| Province/state/region boundaries | (GeoJSON, ADM1) | geoBoundaries | Indonesia, Philippines, Vietnam, Malaysia, Myanmar, Cambodia, Laos, Singapore |
| GDP per capita (national, repeated per province) | `gdp_per_capita_*` | World Bank Open Data | Cambodia, Myanmar, Laos, Singapore |
| GDP per capita (real state-level) | `gdp_per_capita_*` | DOSM Malaysia | Malaysia |
| Sub-national GDP availability check | — | Cambodia NIS Statistical Yearbook | Cambodia |

**Still open (per `docs/Process.md`):** VN NDT7 collaborator data source needs its own
citation entry once confirmed; not yet documented here.
