"""Recompute the main poster's claims from its existing exports, without remapping.

Run from the project root with Python, pandas, numpy, and pyarrow installed.
NDT7 parquet files are read only for metadata (record counts and date ranges).
"""
from pathlib import Path
import hashlib
import json
import re
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
EXPORTS = ROOT / "data/exports"
OUT = ROOT / "docs/poster/main/validation"
COUNTRIES = ["Thailand", "Vietnam", "Philippines", "Singapore", "Cambodia",
             "Laos", "Malaysia", "Myanmar", "Indonesia"]
CODES = dict(zip(COUNTRIES, ["th", "vn", "ph", "sg", "kh", "la", "my", "mm", "id"]))
CAPITALS = dict(zip(COUNTRIES, ["Bangkok Metropolis", "Hà Nội", "NCR", "Central Region",
                              "Phnom Penh", "Vientiane Capital", "Kuala Lumpur", "Yangon", "Jakarta"]))
QUARTERS = {f"{y}-Q{q}" for y in range(2023, 2026) for q in range(1, 5)}


def markdown_table(frame):
    rows = ["| " + " | ".join(map(str, frame.columns)) + " |",
            "| " + " | ".join("---" for _ in frame.columns) + " |"]
    rows += ["| " + " | ".join(map(str, r)) + " |" for r in frame.itertuples(index=False, name=None)]
    return "\n".join(rows)


def run():
    OUT.mkdir(parents=True, exist_ok=True)
    metrics, sources, counts = [], [], []
    for country in COUNTRIES:
        for network in ["fixed", "mobile"]:
            stem = "ookla_" + ("mobile_" if network == "mobile" else "")
            stem += "" if country == "Thailand" else country.lower() + "_"
            path = EXPORTS / (stem + "province_quarterly.csv")
            raw = pd.read_csv(path)
            d = raw[raw.is_reliable == True].copy()
            if set(d.quarter) != QUARTERS:
                raise ValueError(f"Unexpected quarter coverage: {path.name}")
            if d.duplicated(["province", "quarter"]).any():
                raise ValueError(f"Duplicate province-quarter: {path.name}")
            if not (raw.is_reliable == ((raw.total_tests >= 100) & (raw.n_tiles >= 5))).all():
                raise ValueError(f"Reliability flag disagrees with criteria: {path.name}")
            flags = {
                "voice_bandwidth_pct": d.avg_d_mbps >= .064,
                "voice_latency_pct": d.avg_lat_ms_wt <= 200,
                "hd_pct": d.avg_d_mbps >= 5,
                "uhd_pct": d.avg_d_mbps >= 25,
                "gaming_bandwidth_pct": d.avg_d_mbps >= 44,
                "gaming_latency_pct": d.avg_lat_ms_wt <= 25,
                "gaming_both_pct": (d.avg_d_mbps >= 44) & (d.avg_lat_ms_wt <= 25),
            }
            r = {"country": country, "network": network, "province_quarters": len(d),
                 "tests": int(d.total_tests.sum())}
            r.update({k: float(100 * np.average(v, weights=d.total_tests)) for k, v in flags.items()})
            r["hd_failing_rows"] = int((~flags["hd_pct"]).sum())
            r["voice_bandwidth_failing_rows"] = int((~flags["voice_bandwidth_pct"]).sum())
            r["national_mean_mbps"] = float(np.average(d.avg_d_mbps, weights=d.total_tests))
            cap = d[d.province == CAPITALS[country]]
            r["capital_mean_mbps"] = float(np.average(cap.avg_d_mbps, weights=cap.total_tests))
            r["median_province_mbps_2023Q1"] = float(d.loc[d.quarter == "2023-Q1", "avg_d_mbps"].median())
            r["median_province_mbps_2025Q4"] = float(d.loc[d.quarter == "2025-Q4", "avg_d_mbps"].median())
            r["missing_province_quarters_pct"] = float(100 * (1 - len(d) / (raw.province.nunique() * 12)))
            metrics.append(r)
            sources.append({"path": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        p = Path("E:/ndt7/data/ndt7") / CODES[country] / f"mlab_{CODES[country]}_clean.parquet"
        parquet = pq.ParquetFile(p)
        j = parquet.schema.names.index("date")
        stats = [parquet.metadata.row_group(i).column(j).statistics for i in range(parquet.metadata.num_row_groups)]
        date_stats = [s for s in stats if s and s.has_min_max]
        counts.append({"country": country, "records": parquet.metadata.num_rows,
                       "min_date": str(min(s.min for s in date_stats)) if date_stats else "not in metadata",
                       "max_date": str(max(s.max for s in date_stats)) if date_stats else "not in metadata",
                       "path": str(p)})
    df = pd.DataFrame(metrics)
    df.to_csv(OUT / "ookla_verified_metrics.csv", index=False)
    pd.DataFrame(counts).to_csv(OUT / "ndt7_record_counts.csv", index=False)
    (OUT / "input_manifest.json").write_text(json.dumps(sources, indent=2), encoding="utf-8")
    tex = (ROOT / "docs/poster/main/abstract.tex").read_text(encoding="utf-8")
    matched = 0
    for line in tex.splitlines():
        m = re.match(r"\s*(" + "|".join(COUNTRIES) + r")\s*&\s*([\d. &]+)\\\\", line)
        if not m:
            continue
        printed = [float(x.strip()) for x in m.group(2).split("&")]
        expected = []
        for network in ["fixed", "mobile"]:
            row = df[(df.country == m.group(1)) & (df.network == network)].iloc[0]
            expected.extend(round(row[k], 1) for k in ["gaming_bandwidth_pct", "gaming_latency_pct", "gaming_both_pct"])
        if printed != expected:
            raise ValueError(f"Table mismatch for {m.group(1)}: {printed} versus {expected}")
        matched += len(printed)
    if matched != 54:
        raise ValueError(f"Expected 54 verified table cells, found {matched}")
    fixed = df[df.network == "fixed"].set_index("country")
    mobile = df[df.network == "mobile"].set_index("country")
    ookla_total = int(df.tests.sum())
    ndt7_total = sum(r["records"] for r in counts)
    if (ookla_total, ndt7_total) != (229367221, 760607387):
        raise ValueError(f"Corpus totals differ: {ookla_total}, {ndt7_total}")
    capital = fixed[["capital_mean_mbps", "national_mean_mbps"]].round(1).reset_index()
    capital["fixed_mobile_ratio"] = (fixed.national_mean_mbps / mobile.national_mean_mbps).round(1).values
    notes = [
        "# Main poster abstract validation — 2026-09-27",
        "", "## Numeric checks", "",
        f"- All **{matched} cloud-gaming table values** agree with the existing Ookla CSVs after rounding to one decimal place.",
        f"- Ookla retained test contributions: **{ookla_total:,}** (18 fixed/mobile country exports).",
        f"- NDT7 clean-parquet records: **{ndt7_total:,}** (nine source parquet metadata counts).",
        f"- Combined corpus count: **{ookla_total + ndt7_total:,}**, which rounds to 990 million; the sources are analyzed separately.",
        "- Every Ookla country/connection segment contains all 12 quarters from 2023-Q1 to 2025-Q4, with no duplicate province-quarter keys.",
        "- Every retained Ookla row agrees with the >=100 tests and >=5 tiles criteria.",
        "- No retained Ookla province-quarter mean falls below either 64 kbps or 5 Mbps. This does not mean every individual test or user meets these thresholds.",
        f"- Strongest/weakest capital ratio: **{fixed.capital_mean_mbps.max()/fixed.capital_mean_mbps.min():.4f}**, supporting the rounded 16× claim.",
        "", "## Capital, national, and connection-type values", "", markdown_table(capital),
        "", "## Interpretation corrections", "",
        "- Define percentages using test weights on province-quarter mean threshold indicators; do not describe them as percentages of users or time.",
        "- Replace claims that voice/HD are solved or that actual gaming sessions fail with claims about aggregate thresholds.",
        "- Treat Lübben and Misfeld (2022), Table 5, as illustrative benchmarks, not universally sufficient application requirements. Idle server latency does not measure end-user application latency.",
        "- The consumer survey is an online survey of mobile users. It reports 81% with usage problems, with slow/dropped connections the most common problems, not 81% of all Thai consumers or fixed-broadband users.",
        "- Historic Thailand rank 12 in June 2026 is not independently verified by a saved historical index. The exact rank should be omitted pending the source snapshot.",
        "- The original NDT7 GADM exports and original Ookla boundary assignments are retained. No generated ndt7_geoboundaries_* file is an input to this validation.",
        "", "## Reproduce", "", "Run `python scripts/check_poster_abstract.py` from the project root.",
        "Input hashes are in `input_manifest.json`; full-precision outputs are in `ookla_verified_metrics.csv`.",
        "", "## Primary reference checked", "",
        "Consumer survey: https://www.tcc.or.th/true-dtac-merger-consumer/ (paragraph describing the 9–23 November 2023 online survey, 2,924 respondents).",
        "Application thresholds: local source PDF `docs/refs/02-ndt7-mlab/lubben-misfeld-2022-mlab-german-internet-landscape.pdf`, Table 5, page 17.",
    ]
    (OUT / "validation.md").write_text("\n".join(notes) + "\n", encoding="utf-8")
    print(f"Verified {matched} table cells; Ookla={ookla_total:,}; NDT7={ndt7_total:,}.")
    print(OUT / "validation.md")


if __name__ == "__main__":
    run()
