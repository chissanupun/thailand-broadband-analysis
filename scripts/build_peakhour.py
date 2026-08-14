# -*- coding: utf-8 -*-
"""
RQ3 — Peak-hour / diurnal profile (กรอบ Lübben & Misfeld 2022)

    python scripts/build_peakhour.py [country ...]

สรุป NDT7 ราย test → โปรไฟล์ตามชั่วโมงท้องถิ่นต่อประเทศ (ระดับชาติ pool ทุกจังหวัด
ตามกรอบ busy-hour ของ L&M — ไม่ใช้พิกัด/tile จึงได้ผลเต็มแม้ประเทศเล็ก)

กฎที่ยึด (ดู HANDOFF §5 / README_for_eda):
  * แปลง test_time (UTC) -> เวลาท้องถิ่นด้วย offset ต่อประเทศ
    ยืนยัน UTC แล้ว: TH peak = 14:00 UTC = 21:00 local (ตรงพีคเย็นแบบ L&M)
    mm = +6:30 (ครึ่งชั่วโมง) · id ใช้ WIB (+7) เพราะประชากรส่วนใหญ่อยู่ชวา/สุมาตรา
    (คร่อม +7/+8/+9 -> เขียนเป็น limitation)
  * ตัด hosting: network_type IN ('broadband','cellular')
  * ตัด throughput <= 0 (โหลดไม่สำเร็จ)
  * latency ตัด sentinel: CASE WHEN min_rtt < 2000 (NDT7 มีค่า 4,294,967 ms)
  * quantile: ประเทศใหญ่ใช้ approx_quantile (t-digest, memory-safe) เพราะ id 367M / ph 262M แถว
    ถ้า group แล้ว exact เสี่ยง OOM · median คลาด <1% รับได้
    แต่ kh/la/mm ใช้ quantile_cont แบบ exact (ดู EXACT_Q) เพราะ p10 คลาดได้ถึง 7.94%
    เมื่อ cell เล็ก และ p10 คือตัวเลข tail degradation ที่เปเปอร์ใช้
  * แต่ละแถว = ทิศทางเดียว -> เก็บ type (download/upload) แยกเป็นมิติ

group: network_type x type x hour_local(0-23) x is_weekend  (= 192 แถว/ประเทศ)

output: data/exports/ndt7_peakhour_<country>.csv
"""
import os
import sys
import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COUNTRIES = {"kh": "cambodia", "la": "laos", "mm": "myanmar", "my": "malaysia",
             "th": "thailand", "vn": "vietnam", "ph": "philippines",
             "id": "indonesia", "sg": "singapore"}

# UTC -> local offset (นาที · ไม่มี DST ในภูมิภาคนี้)
TZ_MIN = {"th": 420, "vn": 420, "kh": 420, "la": 420,   # UTC+7
          "ph": 480, "sg": 480, "my": 480,              # UTC+8
          "mm": 390,                                     # UTC+6:30
          "id": 420}                                     # WIB (majority)

# ประเทศเล็ก -> ใช้ quantile แบบ exact (parquet เล็ก ไม่เสี่ยง OOM)
# เหตุผล: ตรวจกับ exact บนลาวแล้ว median คลาด 0.80% (รับได้) แต่ p10 คลาดถึง 7.94%
# เพราะ t-digest ไม่แม่นที่หางเมื่อ cell เล็ก · ลาวมี 152/192 cell ที่ test < 1000 (ต่ำสุด 69)
# p10 เป็นตัวเลขที่เปเปอร์ใช้ (tail degradation) จึงต้องแม่น -> 3 ประเทศนี้ใช้ exact
EXACT_Q = {"kh", "la", "mm"}


def qfunc(code):
    """ชื่อฟังก์ชัน quantile ที่ใช้กับประเทศนั้น (signature เหมือนกัน สลับได้ตรงๆ)"""
    return "quantile_cont" if code in EXACT_Q else "approx_quantile"


# เมืองหลวง/เขตนครหลวง (ยืนยันจาก parquet) — โหมด --capital ครบ 8 ประเทศ (ไม่รวม sg
# ซึ่งไม่มี periphery ให้เทียบ, ดู README) · (column, value)
# kh/la/mm เพิ่ม 08-14 แก้ equal-scope violation — เดิมเข้าใจผิดว่าข้อมูลไม่พอ
# ที่จริง PhnomPenh 77.3%, Vientiane[prefecture] 72.0%, Yangon 46.3% ของ test ในประเทศ (data-thick)
CAPITAL = {"th": ("province", "Bangkok Metropolis"),
           "vn": ("province", "HàNội"),
           "id": ("province", "JakartaRaya"),
           "my": ("province", "KualaLumpur"),
           "ph": ("region", "NCR"),
           "kh": ("province", "PhnomPenh"),
           "la": ("province", "Vientiane[prefecture]"),
           "mm": ("province", "Yangon")}

SQL = """
WITH f AS (
    SELECT
        network_type, type,
        mean_throughput_mbps, min_rtt, loss_rate, client_ip,
        EXTRACT(hour FROM test_time + to_minutes({off})) AS hour_local,
        (isodow(test_time + to_minutes({off})) >= 6)     AS is_weekend
    FROM read_parquet('{parq}')
    WHERE mean_throughput_mbps > 0
      AND network_type IN ('broadband', 'cellular')
)
SELECT
    network_type, type, hour_local, is_weekend,
    COUNT(*)                                                        AS n_tests,
    approx_count_distinct(client_ip)                               AS n_ips,
    {q}(mean_throughput_mbps, 0.5)                     AS med_mbps,
    {q}(mean_throughput_mbps, 0.25)                    AS p25_mbps,
    {q}(mean_throughput_mbps, 0.10)                    AS p10_mbps,
    AVG(mean_throughput_mbps)                                      AS mean_mbps,
    {q}(CASE WHEN min_rtt < 2000 THEN min_rtt END, 0.5) AS med_rtt,
    AVG(CASE WHEN min_rtt < 2000 THEN min_rtt END)                 AS mean_rtt,
    AVG(loss_rate)                                                 AS mean_loss
FROM f
GROUP BY network_type, type, hour_local, is_weekend
ORDER BY network_type, type, is_weekend, hour_local
"""


# แยก area = capital/rest เพิ่มจาก SQL ปกติ (โหมด --capital)
SQL_CAPITAL = """
WITH f AS (
    SELECT
        CASE WHEN {col} = '{val}' THEN 'capital' ELSE 'rest' END AS area,
        network_type, type,
        mean_throughput_mbps, min_rtt, loss_rate, client_ip,
        EXTRACT(hour FROM test_time + to_minutes({off})) AS hour_local,
        (isodow(test_time + to_minutes({off})) >= 6)     AS is_weekend
    FROM read_parquet('{parq}')
    WHERE mean_throughput_mbps > 0
      AND network_type IN ('broadband', 'cellular')
)
SELECT
    area, network_type, type, hour_local, is_weekend,
    COUNT(*)                                                        AS n_tests,
    approx_count_distinct(client_ip)                               AS n_ips,
    {q}(mean_throughput_mbps, 0.5)                     AS med_mbps,
    {q}(mean_throughput_mbps, 0.25)                    AS p25_mbps,
    {q}(mean_throughput_mbps, 0.10)                    AS p10_mbps,
    AVG(mean_throughput_mbps)                                      AS mean_mbps,
    {q}(CASE WHEN min_rtt < 2000 THEN min_rtt END, 0.5) AS med_rtt,
    AVG(CASE WHEN min_rtt < 2000 THEN min_rtt END)                 AS mean_rtt,
    AVG(loss_rate)                                                 AS mean_loss
FROM f
GROUP BY area, network_type, type, hour_local, is_weekend
ORDER BY area, network_type, type, is_weekend, hour_local
"""


def _connect():
    tmp = f"{ROOT}/.tmp/duckdb".replace("\\", "/")
    os.makedirs(tmp, exist_ok=True)
    con = duckdb.connect()
    con.execute("SET memory_limit='10GB'")
    con.execute(f"SET temp_directory='{tmp}'")
    con.execute("SET preserve_insertion_order=false")
    return con


def build(code):
    parq = f"{ROOT}/data/ndt7/{code}/mlab_{code}_clean.parquet".replace("\\", "/")
    out = f"{ROOT}/data/exports/ndt7_peakhour_{COUNTRIES[code]}.csv"
    con = _connect()
    df = con.execute(SQL.format(parq=parq, off=TZ_MIN[code], q=qfunc(code))).df()
    df.to_csv(out, index=False)
    con.close()
    # sanity: busy hour by volume (download, weekday, ทั้ง broadband+cellular)
    wk = df[(df["type"] == "download") & (~df["is_weekend"])]
    peak = int(wk.groupby("hour_local")["n_tests"].sum().idxmax())
    print(f"  {code}: {len(df):3d} rows -> {os.path.basename(out)}"
          f" · busy hour (local) = {peak:02d}:00 · tests {int(df.n_tests.sum()):,}")
    return df


def build_capital(code):
    parq = f"{ROOT}/data/ndt7/{code}/mlab_{code}_clean.parquet".replace("\\", "/")
    out = f"{ROOT}/data/exports/ndt7_peakhour_capital_{COUNTRIES[code]}.csv"
    col, val = CAPITAL[code]
    con = _connect()
    df = con.execute(SQL_CAPITAL.format(parq=parq, off=TZ_MIN[code], q=qfunc(code),
                                        col=col, val=val.replace("'", "''"))).df()
    df.to_csv(out, index=False)
    con.close()
    cap = int(df.loc[df.area == "capital", "n_tests"].sum())
    tot = int(df.n_tests.sum())
    print(f"  {code}: {len(df):3d} rows -> {os.path.basename(out)}"
          f" · capital({val}) = {cap:,}/{tot:,} tests ({cap/tot:.1%})")
    return df


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--capital":
        for c in (args[1:] or list(CAPITAL)):
            if c not in CAPITAL:
                print(f"  ! skip (no capital def): {c}")
                continue
            build_capital(c)
    else:
        for c in (args or list(COUNTRIES)):
            if c not in COUNTRIES:
                print(f"  ! skip unknown country code: {c}")
                continue
            build(c)
