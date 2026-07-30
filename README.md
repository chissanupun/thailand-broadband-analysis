# Southeast Asian Broadband Analysis

Province/region-level broadband performance analysis across Southeast Asia, comparing **Ookla Open Data** (fixed + mobile) against **NDT7 (M-Lab)** across Q1/2023 – Q4/2025. The paper's core comparison (`docs/paper_draft.md`) is a fully symmetric **8-country** analysis — Thailand, Vietnam, the Philippines, Singapore, Cambodia, Laos, Malaysia, and Myanmar — no country treated as the reference case, same pipeline applied unmodified to all eight. Thailand additionally has an 8-province district-level deep dive, purely because that's the only country with district-level reference data compiled, not because it's the paper's focus.

**Indonesia was added as a 9th country (2026-07-30)** — Ookla + NDT7 raw data and exports exist, but it is not yet reflected in the paper's Results/Discussion (see `docs/paper_draft.md`'s 2026-07-30 data-coverage note).

---

## Dataset

### Ookla Open Data
- Fixed + mobile broadband performance tiles (Quadkey zoom 16, ~610×610m)
- 12 complete quarters per country: Q1/2023 – Q4/2025 (2025-Q3 gap fixed — see `docs/paper_draft.md` Contributions)
- Metrics: Download speed, Upload speed, Latency, Test count
- Coverage: all 9 countries (8 in the paper's core comparison + Indonesia, added 2026-07-30), both fixed and mobile
- License: CC BY-NC-SA 4.0
- Source: [ookla-open-data](https://github.com/teamookla/ookla-open-data)

### NDT7 (M-Lab)
- Passive background measurement (differs from Ookla which requires user-initiated tests)
- Coverage: **all 9 countries** as of 2026-07-30 — the paper's original 8 (Thailand, Vietnam, Philippines, Singapore, Cambodia, Laos, Malaysia, Myanmar) are now all covered: Philippines and Malaysia were the last two to land, via a collaborator's ip-api ASN relabel (`HANDOFF.md`, 2026-07-29); Singapore's NDT7 pipeline was added 2026-07-30. Indonesia was also added 2026-07-30 as a 9th country (Ookla + NDT7 both new). **Singapore predates the ASN-relabel methodology** (no `asn` column) — its ISP/market-share sections are skipped rather than shown with unreliable name-based grouping (see `docs/paper_draft.md` Table 1).
- Source: [M-Lab BigQuery](https://www.measurementlab.net/data/docs/bq/quickstart/)

> Raw data is not included in this repo (too large) — see download instructions below.

---

## Project Structure

```
├── data/
│   ├── geo/                  # Province/region boundaries per country (GeoJSON)
│   ├── reference/            # Province reference (population, GDP, internet tier) per country
│   ├── ookla/
│   │   ├── raw/              # Parquet files (global, download separately, filtered per-country downstream)
│   │   └── processed/        # Master dataset (regenerate from notebook)
│   └── ndt7/
│       ├── raw/
│       ├── processed/
│       └── {id,kh,la,mm,my,ph,sg,th,vn}/   # Per-country clean parquet + README (9 countries)
├── notebooks/
│   ├── ookla/                # Per-country EDA + analysis notebooks (9 countries)
│   ├── ndt7/main/             # Per-country prep + EDA notebook pairs (9 countries)
│   └── comparison/           # Cross-country / cross-platform RQ notebooks (RQ1, RQ2, ...)
├── outputs/
│   ├── ookla/                # Figures and maps
│   └── ndt7/
└── docs/
    ├── paper.tex             # Research paper (XeLaTeX, Thai)
    ├── paper_draft.md        # Working English draft (Intro/Data/Methodology, SEA-scoped)
    ├── Process.md            # Sprint plan
    └── citations.md          # Data sources and citations
```

---

## Setup

```bash
# Create venv and install dependencies
python3 -m venv datasci
datasci/bin/pip install geopandas pandas numpy scipy statsmodels matplotlib pyarrow ipykernel nbconvert

# Register Jupyter kernel
datasci/bin/python -m ipykernel install --user --name datasci --display-name "Python (datasci)"
```

## Download Ookla Raw Data

Ookla's parquet releases are global — the same files are filtered per-country downstream (Step 1 of the processing pipeline, see `docs/paper_draft.md` §3.1), so no per-country download is needed.

```bash
TARGET_DIR="data/ookla/raw"
mkdir -p "$TARGET_DIR"

for year in 2023 2024 2025; do
    for q in 1 2 3 4; do
        if [ "$q" -eq 1 ]; then month="01"; fi
        if [ "$q" -eq 2 ]; then month="04"; fi
        if [ "$q" -eq 3 ]; then month="07"; fi
        if [ "$q" -eq 4 ]; then month="10"; fi
        for type in fixed mobile; do
            URL="https://ookla-open-data.s3.us-west-2.amazonaws.com/parquet/performance/type=${type}/year=${year}/quarter=${q}/${year}-${month}-01_performance_${type}_tiles.parquet"
            curl -L "$URL" -o "$TARGET_DIR/${year}-Q${q}_performance_${type}_tiles.parquet"
        done
    done
done
```

---

## Key Findings (Preliminary)

**Thailand (fixed broadband, province level):**
- Province-level avg download speed: **137–317 Mbps** (2.3× gap)
- GDP per capita varies **7×** across provinces, yet broadband speed gap is much smaller
- National mean UL/DL ratio = **0.852** — evidence of nationwide FTTH fiber deployment
- Slowest province: Mae Hong Son (137 Mbps) — mountainous, border region
- Fastest province: Nonthaburi (317 Mbps)

**Regional (Ookla fixed, 8-country context — the paper's original scope; excludes Indonesia, added 2026-07-30 and not yet analyzed):**
- Thailand clears every app-requirement download threshold (HD/UHD/cloud-gaming) in all 77 provinces, every quarter — Myanmar is the outlier, dropping to 20.6% UHD (25 Mbps) pass rate
- Thailand's absolute download speed stays **2nd-highest of 8 countries** (behind only Singapore) throughout 2023–2025, despite posting the 2nd-*slowest* % growth (+42%, vs. Myanmar/Cambodia/Vietnam's 126–164% catch-up growth from a much lower base)
- Cross-platform check (Ookla vs. NDT7, Thailand + Vietnam only): the two sources broadly agree in direction — both show fixed broadband growing steadily over the 3-year period — though absolute levels differ substantially (NDT7 runs ~3x lower than Ookla, consistent with MacMillan et al. 2023's finding that NDT7 underreports relative to active-test platforms)

---

## Paper

Written in XeLaTeX (Thai language) — compile with:

```bash
cd docs && xelatex paper.tex && xelatex paper.tex
```

Requires font: `sudo apt install fonts-thai-tlwg`

`docs/paper_draft.md` holds the current working English draft (Introduction/Data/Methodology sections, SEA-scoped) and is ahead of `paper.tex`, which still needs that content ported in and translated.

---

## License

Code: MIT  
Data: See [citations.md](docs/citations.md) for individual dataset licenses.
