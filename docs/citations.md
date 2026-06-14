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

## 6. Summary Table — Source vs. Use

| Data | Column in CSV | Primary Source | Alternative to |
|------|---------------|----------------|----------------|
| Province boundaries | (GeoJSON) | GADM v4.1 | apisit/thailand.json |
| Population Dec 2024 | `pop_2024` | DOPA/BORA stat.bora.dopa.go.th | Wikipedia |
| Area (km²) | `area_km2` | NSO Statistical Yearbook 2025 | Wikipedia |
| GPP per capita 2021 | `gdp_per_capita_thb_2021` | NESDC GPP Chain Volume Measures | Wikipedia / thaiwebsites.com |
| Internet tier (proxy) | `internet_tier` | Derived (NESDC + NBTC context) | — |
| Fixed BB speed tiles | (parquet files) | Ookla Open Data (CC BY-NC-SA 4.0) | — |

---

## 7. Note on Wikipedia

Wikipedia was used during initial exploration only. For publication, all data traces back to:
- **DOPA** (population)
- **NESDC** (GPP/economic)
- **NSO** (area, density, demographic aggregates)
- **NBTC** (broadband penetration, subscribers)
- **Ookla** (speed measurement data — primary dataset)

Wikipedia is not cited in the final paper. Use the primary government sources above.
