# -*- coding: utf-8 -*-
"""สร้าง notebooks/ndt7/main/indonesia_ndt7_prep.ipynb ตามแบบ philippines/laos"""
import json, pandas as pd

REF = r"E:\thailand-broadband-analysis\data\reference\indonesia_reference.csv"
OUT = r"E:\thailand-broadband-analysis\notebooks\ndt7\main\indonesia_ndt7_prep.ipynb"

ref = pd.read_csv(REF)
pmap = {r.province_th.replace(" ", ""): r.province_en for r in ref.itertuples()}
map_lines = "\n".join(f"    {k!r}: {v!r}," for k, v in sorted(pmap.items()))

md0 = """# NDT7 (M-Lab) Data Prep — Indonesia Broadband + Mobile, Province x Quarter

Aggregates `../../../data/ndt7/id/mlab_id_clean.parquet` (367,247,163 rows — the largest of the
eight countries) into province x quarter format, split into Broadband and Mobile/Cellular,
mirroring the other NDT7 prep notebooks.

**Structural choices — deliberate, mirroring `philippines_ndt7_prep.ipynb`:**

1. **No zoom-16 tile-binning.** The v2 parquet already carries a clean `province` column from a
   GADM point-in-polygon join. `n_tiles` is left as `NaN` and **`is_reliable` uses
   `total_tests >= 100` only** — the same rule now used by every NDT7 country. NDT7 coordinates
   come from MaxMind at *city-centroid* granularity, so a tile count measures how many cities
   MaxMind knows in a province, not how well the data is spread; Ookla keeps `n_tiles >= 5`
   because its coordinates are genuinely spatial. Running tile-binning over 367M rows to produce
   a column nothing reads would be pure cost.
2. **Output granularity is ADM1 province (34).** Indonesia split Papua into new provinces during
   2022–24 and now has 38, but this dataset is pinned at **34**: the parquet was joined with
   GADM 4.1 (2022 boundaries), `data/geo/indonesia_provinces.geojson` is geoBoundaries ADM1
   (2017), and the BPS GRDP table used for the reference CSV is the 2021 edition — all three
   agree on 34. See `data/reference/indonesia_reference_PROVENANCE.md`.
3. **Province names need mapping.** The parquet stores run-together Indonesian names
   (`JawaBarat`, `SumateraUtara`) while the reference CSV and geojson use readable English
   (`West Java`, `North Sumatra`). `PROVINCE_MAP` below covers all 34 — verified against the
   real parquet, not assumed.

**Outputs:**
- `data/exports/ndt7_indonesia_province_quarterly.csv` — Broadband
- `data/exports/ndt7_mobile_indonesia_province_quarterly.csv` — Mobile/Cellular
"""

c_imports = """import duckdb
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

RAW_PARQUET = '../../../data/ndt7/id/mlab_id_clean.parquet'
ID_REF_CSV  = '../../../data/reference/indonesia_reference.csv'

con = duckdb.connect()
# ไฟล์ 19 GB / 367M แถว — ต้องตั้งไม่งั้น OOM
con.execute("SET memory_limit='10GB'")
con.execute("SET temp_directory='../../../.tmp/duckdb'")   # ที่พักตอน spill
con.execute("SET preserve_insertion_order=false")
print('rows:', con.execute(f"SELECT COUNT(*) FROM read_parquet('{RAW_PARQUET}')").fetchone()[0])"""

md_flood = """### 0. Flood check — ตรวจว่ามี client_ip ตัวเดียวยิงรัวจนบิดค่าไหม

`philippines_ndt7_prep.ipynb` ตัด IP หนึ่งตัวทิ้ง (`58.69.220.245`) เพราะยิงรัว ตรงนี้ตรวจแบบเดียวกัน
สำหรับอินโด **ตรวจก่อน ไม่ได้เดา** — ถ้าเจอตัวที่ผิดปกติ ให้ใส่ใน `FLOOD_IPS` แล้วรันใหม่"""

c_flood = """_top = con.execute(f\"\"\"
    SELECT client_ip, COUNT(*) AS n, COUNT(DISTINCT province) AS n_prov
    FROM read_parquet('{RAW_PARQUET}')
    WHERE network_type IN ('broadband','cellular')
    GROUP BY 1 ORDER BY n DESC LIMIT 10
\"\"\").df()
_total = con.execute(f\"\"\"SELECT COUNT(*) FROM read_parquet('{RAW_PARQUET}')
    WHERE network_type IN ('broadband','cellular')\"\"\").fetchone()[0]
_top['pct_of_all'] = (100 * _top['n'] / _total).round(3)
print(f"consumer rows = {_total:,}")
display(_top)
print("\\nเกณฑ์คร่าว ๆ: ถ้า IP เดียวเกิน ~0.5% ของทั้งประเทศ ให้สงสัยไว้ก่อน")"""

c_floodlist = """# ใส่ IP ที่ยืนยันแล้วว่า flood จากผลด้านบน (ว่างไว้ = ไม่ตัดอะไร)
FLOOD_IPS = ()
_flood_sql = ("AND client_ip NOT IN (" + ", ".join(f"'{ip}'" for ip in FLOOD_IPS) + ")") if FLOOD_IPS else ""
print('ตัด IP:', FLOOD_IPS or 'ไม่ตัด')"""

md_sql = """### 1. Province x Quarter Aggregation (DuckDB)

รวบงานระดับแถวทั้งหมดไว้ใน query เดียว — กรอง, ติดไตรมาส, group by province x quarter x type x
network_type ไม่มีการ loop ฝั่ง Python

ตัด `hosting` ออกตั้งแต่ใน SQL (เหลือ `broadband`/`cellular`) และตัดแถวที่ `province IS NULL`
(อินโดมี 6,896 แถว = 0.002%)"""

c_sql = """sql = f\"\"\"
SELECT
    province,
    network_type,
    type,
    (CAST(year AS VARCHAR) || '-Q' || CAST(CAST(CEIL(month / 3.0) AS INT) AS VARCHAR)) AS year_q,
    AVG(mean_throughput_mbps)                        AS avg_thr,
    AVG(CASE WHEN min_rtt < 2000 THEN min_rtt END)   AS avg_lat,
    COUNT(*)                                         AS test_count
FROM read_parquet('{RAW_PARQUET}')
WHERE mean_throughput_mbps > 0
  AND province IS NOT NULL
  AND network_type IN ('broadband', 'cellular')
GROUP BY province, network_type, type, year_q
\"\"\"

prov_q_all = con.execute(sql).df()
print(f"province x quarter x type x network rows: {len(prov_q_all):,}")
print(f"quarters: {len(prov_q_all['year_q'].unique())} | provinces: {prov_q_all['province'].nunique()}")
print(prov_q_all.groupby('network_type')['test_count'].sum().apply(lambda x: f'{x:,}'))"""

md_map = """### 2. Province Name Mapping — parquet (`JawaBarat`) → reference (`West Java`)

ทำหลัง aggregate เพราะผลลัพธ์เหลือแค่หลักพันแถว map ด้วย pandas ได้สบาย เหมือนที่ลาวทำ

`assert` ไว้ให้ fail ทันทีถ้ามีชื่อไหนไม่ถูก map — จะได้ไม่เงียบ ๆ แล้วไปโผล่เป็น NaN ตอน join"""

c_map = f"""# parquet เก็บชื่ออินโดนีเซียแบบเขียนติดกัน -> ชื่ออังกฤษอ่านง่ายใน indonesia_reference.csv
# ตรวจกับ parquet จริงแล้ว ครบทั้ง 34 ไม่มีตกหล่น
PROVINCE_MAP = {{
{map_lines}
}}

_before = set(prov_q_all['province'])
_unmapped = _before - set(PROVINCE_MAP)
assert not _unmapped, f"มีชื่อจังหวัดที่ยังไม่ได้ map: {{_unmapped}}"

prov_q_all['province'] = prov_q_all['province'].map(PROVINCE_MAP)
print(f"map แล้ว {{len(PROVINCE_MAP)}} ชื่อ | เหลือ {{prov_q_all['province'].nunique()}} จังหวัด")"""

md_build = """### 3. Province-Level Aggregation (per network type) + Reference Merge

กาง download/upload ออกเป็นคอลัมน์ merge ข้อมูลอ้างอิง (GDP/density/tier) แล้วคำนวณ `is_reliable`

**ไม่มี `n_tiles`** — `is_reliable = total_tests >= 100` อย่างเดียว (ดูหัวเล่ม)"""

c_build = """def build_province_quarterly(prov_q_all, network_type, ref):
    d = prov_q_all[prov_q_all['network_type'] == network_type]
    print(f"[{network_type}] province x quarter x type rows: {len(d):,}")

    dl = d[d['type'] == 'download'].rename(
        columns={'avg_thr': 'avg_d_mbps', 'avg_lat': 'avg_lat_ms_wt', 'test_count': 'total_tests'})
    ul = d[d['type'] == 'upload'].rename(columns={'avg_thr': 'avg_u_mbps'})

    dl_stats = dl[['year_q', 'province', 'avg_d_mbps', 'avg_lat_ms_wt', 'total_tests']]
    ul_stats = ul[['year_q', 'province', 'avg_u_mbps']]

    master = pd.merge(dl_stats, ul_stats, on=['year_q', 'province'], how='outer')
    master = master.rename(columns={'year_q': 'quarter'})
    master['year'] = master['quarter'].str.slice(0, 4).astype(int)
    master['quarter.1'] = master['quarter'].str.slice(6, 7).astype(int)
    master['n_tiles'] = np.nan   # ไม่ใช้กับ NDT7 — ดูหัวเล่ม

    master['is_reliable'] = master['total_tests'] >= 100
    print(f"[{network_type}] province x quarter rows: {len(master)} | "
          f"reliable: {master['is_reliable'].sum()} ({master['is_reliable'].mean():.1%})")

    master = master.merge(
        ref[['province_en', 'region', 'internet_tier', 'pop_2024', 'gdp_per_capita_raw_2021',
             'density_per_km2', 'gdp_per_capita_usd_ppp_2021', 'gdp_per_capita_thb_2021']],
        left_on='province', right_on='province_en', how='left'
    ).drop(columns=['province_en'])

    missing_ref = master[master['region'].isna()]['province'].unique()
    if len(missing_ref):
        print(f"[{network_type}] WARNING — provinces with no reference match: {list(missing_ref)}")

    return master


EXPORT_COLS = ['province', 'quarter', 'year', 'quarter.1', 'avg_d_mbps', 'avg_u_mbps',
               'avg_lat_ms_wt', 'total_tests', 'n_tiles', 'is_reliable', 'region',
               'internet_tier', 'pop_2024', 'gdp_per_capita_raw_2021', 'density_per_km2',
               'gdp_per_capita_usd_ppp_2021', 'gdp_per_capita_thb_2021']

ref = pd.read_csv(ID_REF_CSV)
print(f"reference: {len(ref)} จังหวัด | region: {sorted(ref['region'].unique())}")"""

md_bb = "---\n## Part 1 — Broadband"
c_bb1 = "broadband_master = build_province_quarterly(prov_q_all, 'broadband', ref)\nbroadband_master.head()"
c_bb2 = """out_bb = broadband_master[EXPORT_COLS].copy()
OUT_PATH_BB = '../../../data/exports/ndt7_indonesia_province_quarterly.csv'
out_bb.to_csv(OUT_PATH_BB, index=False)
print(f"Exported {len(out_bb)} rows -> {OUT_PATH_BB}")
out_bb.head(3)"""

md_mb = "---\n## Part 2 — Mobile/Cellular"
c_mb1 = "mobile_master = build_province_quarterly(prov_q_all, 'cellular', ref)\nmobile_master.head()"
c_mb2 = """out_mb = mobile_master[EXPORT_COLS].copy()
OUT_PATH_MB = '../../../data/exports/ndt7_mobile_indonesia_province_quarterly.csv'
out_mb.to_csv(OUT_PATH_MB, index=False)
print(f"Exported {len(out_mb)} rows -> {OUT_PATH_MB}")
out_mb.head(3)"""

md_sum = """## Summary

- **Input:** `data/ndt7/id/mlab_id_clean.parquet` — 367,247,163 rows, ISP-classified (v2) and
  province-joined. ไฟล์ใหญ่ที่สุดในชุด (19 GB)
- **Output:** province x quarter aggregates, 34 ADM1 provinces, Broadband และ Mobile แยกกัน
- **Reliability:** `total_tests >= 100` เท่านั้น — ไม่มี `n_tiles` เหมือนทุกประเทศ NDT7 ตอนนี้
  (Ookla ยังใช้ `n_tiles >= 5` อยู่ อย่าเอาไปเทียบกันตรง ๆ)
- **ข้อควรระวังของอินโดโดยเฉพาะ** (ดู `data/reference/indonesia_reference_PROVENANCE.md`):
  - `pop_2024` จริง ๆ เป็นตัวเลข **mid-2025** จาก BPS — คงชื่อคอลัมน์ไว้เพื่อให้ notebook อื่นไม่พัง
  - `internet_tier` เป็น **ควอร์ไทล์ GDP ตรง ๆ ไม่มีการปรับมือ** ต่างจากของไทย → ห้ามเทียบ tier ข้ามประเทศ
  - **34 จังหวัด ไม่ใช่ 38** — ยุบปาปัวใหม่กลับเข้า Papua/West Papua ให้ตรง GADM 4.1 (2022)
  - **Jakarta กิน test ไป ~124M จาก 331M (37%)** — MaxMind ลงพิกัดเป็น centroid เมือง
    ค่าเฉลี่ยระดับประเทศจึงเอนไปทางจาการ์ตาหนักมาก ต้องระวังตอนตีความ
"""


def md(s): return {"cell_type": "markdown", "metadata": {}, "source": s.splitlines(keepends=True)}
def code(s): return {"cell_type": "code", "execution_count": None, "metadata": {},
                     "outputs": [], "source": s.splitlines(keepends=True)}

nb = {
    "cells": [md(md0), code(c_imports), md(md_sql), code(c_sql), md(md_map), code(c_map), md(md_build), code(c_build),
              md(md_bb), code(c_bb1), code(c_bb2), md(md_mb), code(c_mb1), code(c_mb2), md(md_sum)],
    "metadata": {"kernelspec": {"display_name": "datasci", "language": "python", "name": "python3"},
                 "language_info": {"name": "python", "version": "3.11.5"}},
    "nbformat": 4, "nbformat_minor": 5,
}
json.dump(nb, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
open(OUT, "a", encoding="utf-8").write("\n")
print("เขียน", OUT, f"({len(nb['cells'])} cells)")
