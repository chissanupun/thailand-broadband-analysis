# -*- coding: utf-8 -*-
"""
ชุดที่ 2 — ASN x quarter (โครงสร้างตลาด/ISP)

    python scripts/build_isp_quarterly.py [country ...]

ต่างจากชุด province x quarter ตรงที่ **ไม่ใช้พิกัดและไม่ใช้ tile เลย** จึงไม่โดนปัญหา
city-centroid ที่ทำให้ลาว/กัมพูชาไม่มีข้อมูลระดับจังหวัด — ประเทศเล็กก็ได้ผลเต็ม ๆ

กฎที่ยึดตาม HANDOFF:
  * **จัดกลุ่มด้วย `asn` เท่านั้น** ห้ามใช้ `isp` (ip-api คืนชื่อองค์กรลูกค้าสำหรับ leased line
    เช่น AS4750 มีชื่อ isp ถึง 420 ชื่อ) และห้ามใช้ `operator` จัดกลุ่ม (null เยอะ MM 56%)
  * `operator` / `as_name` ใช้เป็น**ป้ายแสดงผล**เท่านั้น เลือกตัวที่พบบ่อยสุดของแต่ละ ASN
  * ถ่วงน้ำหนักด้วย **test** ไม่ใช่ address (CGNAT ทำให้ ASN มือถือมี test/address สูงกว่ามาก)
  * latency ใช้สูตรเดียวกับชุด province: AVG(CASE WHEN min_rtt < 2000 THEN min_rtt END)
  * is_reliable = total_tests >= 100 (เกณฑ์เดียวกับชุด province)

output: data/exports/ndt7_isp_<country>_quarterly.csv
"""
import os, sys
import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COUNTRIES = {"kh": "cambodia", "la": "laos", "mm": "myanmar", "my": "malaysia",
             "th": "thailand", "vn": "vietnam", "ph": "philippines", "id": "indonesia",
             "sg": "singapore"}

SQL = """
WITH f AS (
    SELECT
        COALESCE(CAST(asn AS VARCHAR), '(unknown)') AS asn,
        operator, as_name, network_type, type,
        mean_throughput_mbps, min_rtt, client_ip,
        (CAST(year AS VARCHAR) || '-Q' || CAST(CAST(CEIL(month / 3.0) AS INT) AS VARCHAR)) AS quarter
    FROM read_parquet('{parq}')
    WHERE mean_throughput_mbps > 0
      AND network_type IN ('broadband', 'cellular')
),
-- ป้ายชื่อต่อ ASN: เลือก operator / as_name ที่พบบ่อยสุด (ไม่ใช้จัดกลุ่ม ใช้แสดงผลอย่างเดียว)
label AS (
    SELECT asn,
           mode(operator) FILTER (WHERE operator IS NOT NULL) AS operator,
           mode(as_name)  FILTER (WHERE as_name  IS NOT NULL) AS as_name
    FROM f GROUP BY asn
),
dl AS (
    SELECT asn, network_type, quarter,
           AVG(mean_throughput_mbps)                      AS avg_d_mbps,
           median(mean_throughput_mbps)                   AS med_d_mbps,
           AVG(CASE WHEN min_rtt < 2000 THEN min_rtt END) AS avg_lat_ms,
           median(min_rtt) FILTER (WHERE min_rtt < 2000)  AS med_lat_ms,
           COUNT(*)                                       AS total_tests,
           approx_count_distinct(client_ip)               AS n_ips_approx
    FROM f WHERE type = 'download' GROUP BY asn, network_type, quarter
),
ul AS (
    SELECT asn, network_type, quarter,
           AVG(mean_throughput_mbps)    AS avg_u_mbps,
           median(mean_throughput_mbps) AS med_u_mbps
    FROM f WHERE type = 'upload' GROUP BY asn, network_type, quarter
)
SELECT
    dl.asn,
    label.operator,
    label.as_name,
    dl.network_type,
    dl.quarter,
    CAST(SUBSTR(dl.quarter, 1, 4) AS INT)  AS year,
    CAST(SUBSTR(dl.quarter, 7, 1) AS INT)  AS quarter_num,
    dl.avg_d_mbps, ul.avg_u_mbps, dl.med_d_mbps, ul.med_u_mbps,
    dl.avg_lat_ms, dl.med_lat_ms,
    dl.total_tests,
    dl.n_ips_approx,
    -- ส่วนแบ่งตลาดวัดด้วย test ภายใน network_type x quarter เดียวกัน
    100.0 * dl.total_tests / SUM(dl.total_tests) OVER (
        PARTITION BY dl.network_type, dl.quarter) AS market_share_pct,
    (dl.total_tests >= 100) AS is_reliable
FROM dl
LEFT JOIN ul    ON dl.asn = ul.asn AND dl.network_type = ul.network_type AND dl.quarter = ul.quarter
LEFT JOIN label ON dl.asn = label.asn
ORDER BY dl.network_type, dl.quarter, dl.total_tests DESC
"""


def build(code):
    parq = f"{ROOT}/data/ndt7/{code}/mlab_{code}_clean.parquet".replace("\\", "/")
    out = f"{ROOT}/data/exports/ndt7_isp_{COUNTRIES[code]}_quarterly.csv"
    con = duckdb.connect()
    con.execute("SET memory_limit='10GB'")
    con.execute(f"SET temp_directory='{ROOT}/.tmp/duckdb'".replace("\\", "/"))
    con.execute("SET preserve_insertion_order=false")
    df = con.execute(SQL.format(parq=parq)).df()
    df.to_csv(out, index=False)
    n_asn = df.asn.nunique()
    rel = int(df.is_reliable.sum())
    noop = int(df.operator.isna().sum())
    print(f"  {code}: {len(df):5d} แถว · {n_asn:5d} ASN · reliable {rel:5d} "
          f"({rel/len(df):5.1%}) · operator ว่าง {noop:4d} -> {os.path.basename(out)}")
    return df


if __name__ == "__main__":
    for c in (sys.argv[1:] or list(COUNTRIES)):
        build(c)
