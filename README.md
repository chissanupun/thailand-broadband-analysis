# Thailand Broadband Analysis

Province-level fixed broadband performance analysis in Thailand, comparing **Ookla Open Data** and **NDT7 (M-Lab)** across Q1/2023 – Q4/2025.

---

## Dataset

### Ookla Open Data
- Fixed broadband performance tiles (Quadkey zoom 16, ~610×610m)
- 11 quarters: Q1/2023 – Q4/2025
- Metrics: Download speed, Upload speed, Latency, Test count
- License: CC BY-NC-SA 4.0
- Source: [ookla-open-data](https://github.com/teamookla/ookla-open-data)

### NDT7 (M-Lab)
- Passive background measurement (differs from Ookla which requires user-initiated tests)
- Source: [M-Lab BigQuery](https://www.measurementlab.net/data/docs/bq/quickstart/)

> Raw data is not included in this repo (too large) — see download instructions below.

---

## Project Structure

```
├── data/
│   ├── geo/                  # Thailand province boundaries (GeoJSON)
│   ├── reference/            # Province reference (population, GDP, internet tier)
│   ├── ookla/
│   │   ├── raw/              # Parquet files (download separately)
│   │   └── processed/        # Master dataset (regenerate from notebook)
│   └── ndt7/
│       ├── raw/
│       └── processed/
├── notebooks/
│   ├── ookla/                # EDA + analysis notebooks
│   └── ndt7/
├── outputs/
│   ├── ookla/                # Figures and maps
│   └── ndt7/
└── docs/
    ├── paper.tex             # Research paper (XeLaTeX, Thai)
    ├── Process.md            # Sprint plan
    └── citations.md          # Data sources and citations
```

---

## Setup

```bash
# Create venv and install dependencies
python3 -m venv datasci
datasci/bin/pip install geopandas pandas numpy scipy matplotlib pyarrow ipykernel nbconvert

# Register Jupyter kernel
datasci/bin/python -m ipykernel install --user --name datasci --display-name "Python (datasci)"
```

## Download Ookla Raw Data

```bash
TARGET_DIR="data/ookla/raw"
mkdir -p "$TARGET_DIR"

for year in 2023 2024 2025; do
    for q in 1 2 3 4; do
        if [ "$q" -eq 1 ]; then month="01"; fi
        if [ "$q" -eq 2 ]; then month="04"; fi
        if [ "$q" -eq 3 ]; then month="07"; fi
        if [ "$q" -eq 4 ]; then month="10"; fi
        URL="https://ookla-open-data.s3.us-west-2.amazonaws.com/parquet/performance/type=fixed/year=${year}/quarter=${q}/${year}-${month}-01_performance_fixed_tiles.parquet"
        curl -L "$URL" -o "$TARGET_DIR/${year}-Q${q}_performance_fixed_tiles.parquet"
    done
done
```

---

## Key Findings (Preliminary)

- Province-level avg download speed: **137–317 Mbps** (2.3× gap)
- GDP per capita varies **7×** across provinces, yet broadband speed gap is much smaller
- National mean UL/DL ratio = **0.852** — evidence of nationwide FTTH fiber deployment
- Slowest province: Mae Hong Son (137 Mbps) — mountainous, border region
- Fastest province: Nonthaburi (317 Mbps)

---

## Paper

Written in XeLaTeX (Thai language) — compile with:

```bash
cd docs && xelatex paper.tex && xelatex paper.tex
```

Requires font: `sudo apt install fonts-thai-tlwg`

---

## License

Code: MIT  
Data: See [citations.md](docs/citations.md) for individual dataset licenses.
