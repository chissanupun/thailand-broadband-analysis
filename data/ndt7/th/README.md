# mlab_th_clean.parquet — Data Handoff README

**Built from:** M-Lab NDT7 speed tests, Thailand, pulled from Google BigQuery
**File:** `data/th/mlab_th_clean.parquet` (~3.4 GB)
**Built by:** `notebooks/th/ndt7/mlab_th_clean.ipynb`

---

## Quick numbers

| | |
|---|---|
| **Rows** | 60,248,884 |
| **Columns** | 21 |
| **Unique client IPs** | 9,416,238 |
| **Date range** | 2023-01-01 → 2025-12-31 |
| **File size** | ~3.4 GB |

Read it with DuckDB (fast, no RAM issues):
```python
import duckdb
df = duckdb.connect().execute("SELECT * FROM read_parquet('data/th/mlab_th_clean.parquet') LIMIT 5").df()
```

---

## What each column means

| Column | Type | What it is |
|---|---|---|
| `id` | string | Unique test ID from M-Lab |
| `date` | date | Date of the test (YYYY-MM-DD) |
| `test_time` | timestamp | Exact datetime of the test |
| `year` | int | Derived from `test_time` |
| `month` | int | Derived from `test_time` (1–12) |
| `hour` | int | Hour of day (0–23), derived from `test_time` |
| `type` | string | `download` or `upload` — each test row is one direction |
| `mean_throughput_mbps` | float | **The speed** — average Mbps during the test |
| `min_rtt` | float | Minimum round-trip time in milliseconds — lower = better latency |
| `loss_rate` | float | Packet loss rate (0.0–1.0) — 0 = no loss |
| `duration` | float | Test duration in seconds |
| `client_ip` | string | Client's IP address (IPv4 or IPv6) |
| `city` | string | Client **city** from M-Lab geo (city-level, 881 distinct — NOT province) — **5.4% NULL** (see note) |
| `province` | string | จังหวัด (77 provinces) — point-in-polygon join จาก `latitude`/`longitude` กับ `data/geo/thailand_provinces.geojson` + nearest-fallback, coverage 100% (null แค่ 7 rows ที่ lat/long เป็น NULL) |
| `latitude` | float | Client latitude (เกือบไม่มี NULL) |
| `longitude` | float | Client longitude (เกือบไม่มี NULL) |
| `isp` | string | Raw ISP name from M-Lab — **0.2% NULL** |
| `network_type` | string | `broadband` / `cellular` — the main classification (ไทยไม่มี unknown/hosting) |
| `category` | string | Finer bucket (see below) |
| `description` | string | Human-readable label for the category |
| `distance_from_server` | float | Haversine km between client and M-Lab test server |

> **Note:** `city` เป็นระดับเมือง (881 เมือง) ไม่ใช่จังหวัด — เมืองใหญ่หลายเมืองแยกจากจังหวัดตัวเอง (Pattaya/Si Racha/Bang Lamung อยู่ใน Chon Buri, Hat Yai อยู่ใน Songkhla, Ko Samui อยู่ใน Surat Thani) ถ้าต้องการระดับจังหวัดให้ใช้ `province` column ที่ join มาแล้ว (ไม่ต้อง map จาก city เอง) — validate แล้วว่า map ถูกต้อง
>
> ความแม่นยำของ `province` ขึ้นกับ geolocation ของ MaxMind (coordinate เป็น city centroid) — IP ที่ MaxMind ระบุตำแหน่งไม่ได้แม่นจะตกที่ centroid สำรอง (เช่น Bangkok Metropolis สูงถึง 64% ส่วนหนึ่งเพราะ fallback นี้) province column สะท้อน coordinate ที่ raw data ให้มาตรงๆ

---

## The most important column: `network_type`

ไทยพิเศษกว่า VN/SG ตรงที่ **ไม่มี unknown และ hosting เลย** — ทุก row classify ได้หมด

| `network_type` | Rows | % | What it means |
|---|---|---|---|
| `broadband` | 31,000,759 | **51.5%** | เน็ตบ้าน/ออฟฟิศ (True, 3BB, AIS Fibre, TOT, CAT, NT ฯลฯ) |
| `cellular` | 29,248,125 | **48.5%** | มือถือ (AIS/AWN, True Move, dtac/TOTAL, NT Mobile ฯลฯ) |

**100% ของ rows ใช้ได้ทันที** — ไม่ต้อง filter ออกอะไรเลย

ทำไม cellular สูงถึง 48.5%? เพราะไทยใช้ smartphone ทำ speed test เยอะมาก + classification ผ่านการ validate ด้วย ip-api ระดับ IP จริงๆ (ไม่ใช่แค่ชื่อ ISP)

---

## Category (finer breakdown ใน broadband)

| category | network_type | rows | % |
|---|---|---|---|
| Mobile | cellular | 29,248,125 | 48.5% |
| Consumer Broadband | broadband | 25,557,828 | **42.4%** |
| Telco & Solution Providers | broadband | 3,418,667 | 5.7% |
| Others | broadband | 1,046,644 | 1.7% |
| Educational | broadband | 342,366 | 0.6% |
| Broadband Enterprise | broadband | 324,286 | 0.5% |
| International Providers & Gateway | broadband | 178,747 | 0.3% |
| Government | broadband | 130,575 | 0.2% |
| Hotel & Resort | broadband | 1,646 | 0.0% |

> ⚠️ **Known limitation:** `category` ของ broadband มีบาง ISP classify ผิด (เช่น UIH, UNINET-TH อยู่ใน Others แทน Telco/Educational) — ดูรายละเอียดใน `mlab_th_clean_README.md` ถ้าจะใช้ category breakdown ละเอียด **ถ้าแค่ Mobile vs Consumer Broadband ใช้ได้เลย ไม่กระทบ**

---

## Speed overview (download/upload)

| network_type | type | Mean (Mbps) | Median (Mbps) | Std |
|---|---|---|---|---|
| broadband | download | 105.2 | 44.3 | 144.0 |
| broadband | upload | 77.7 | 29.0 | 117.5 |
| cellular | download | 28.2 | 10.8 | 56.4 |
| cellular | upload | 14.3 | 4.5 | 41.3 |

Median ต่ำกว่า mean มากเพราะมีคนใช้ Gigabit fiber ดึง mean ขึ้น — ใช้ median เป็นตัวแทนดีกว่าถ้าจะสื่อสารกับคนทั่วไป

---

## Top ISPs

| ISP | network_type | Rows |
|---|---|---|
| TRUE INTERNET CO., LTD. | broadband | 8,924,686 |
| Advance Wireless Network (AWN/AIS) | cellular | 8,566,376 |
| Triple T Internet / 3BB | broadband | 6,388,362 |
| AIS Fibre | broadband | 5,777,192 |
| Total Access Communication (dtac) | cellular | 5,571,684 |
| Realmove / Real Future (True Move H) | cellular | 10,478,905 |
| TOT Public Company | broadband | 4,466,901 |
| CAT TELECOM | broadband | 1,150,758 |

> Note: True Move H ปรากฏในหลายชื่อ (`Realmove Company Limited`, `Real Future Company Limited`) — รวมกันแล้วเป็น ISP cellular อันดับ 1

---

## Data by year

| Year | Rows |
|---|---|
| 2023 | 19,700,569 |
| 2024 | 25,098,713 |
| 2025 | 15,449,602 |

ข้อมูลกระจายสม่ำเสมอกว่า VN — 2024 เยอะสุด

---

## Known data quality notes

- **`city` is 5.4% NULL** — M-Lab geo ครอบคลุมได้ดีกว่า VN/SG แต่ก็ยังมีช่องว่าง `latitude`/`longitude` มีแทบทุก row
- **`isp` is 0.2% NULL** — น้อยมาก ไม่กระทบ
- **มี `province` column แล้ว** (77 จังหวัด, point-in-polygon join, coverage 100%) — ใช้ได้เลย ไม่ต้อง map จาก `city` เอง แต่ระวัง Bangkok Metropolis สูงผิดปกติ (64%) จาก MaxMind fallback centroid
- **`category` มีบาง edge case ผิด** — ดู Known limitation ด้านบน ใช้แค่ `network_type` ปลอดภัยที่สุด
- **Each test = one row for one direction** — download กับ upload เป็นคนละ row ใช้ `id` เดียวกัน
- **ไม่มี unknown/hosting** — ทุก row classify ได้ ใช้ได้ทั้งหมดเลย

---

## How it was cleaned

1. **Dropped** 844,045 rows (1.38%) — `mean_throughput_mbps <= 0` (578,270 rows) หรือ `duration <= 0` (458,574 rows)
2. **Classified `network_type`** ด้วย curated ISP list สำหรับ AIS/AWN, True Move H, dtac → cellular; ที่เหลือ → broadband แล้ว validate ด้วย ip-api per-IP lookup (100% IP coverage — 9,416,238 unique IPs) พบและแก้ 3 กรณี:
   - AWN identity leak (1,858,982 rows flipped broadband→cellular)
   - TOT Mobile Co LTD (1,234,583 rows)
   - National Telecom (1,112,316 rows — แก้ per-IP ไม่ใช่ blanket)
3. **Derived columns** added: `hour`, `year`, `month`, `distance_from_server`, `province` (point-in-polygon join จาก lat/long กับ `data/geo/thailand_provinces.geojson` — 77 จังหวัด, nearest-fallback, coverage 100%)
4. **No rows were modified** — classification เป็น column ใหม่ ข้อมูล measurement เดิมไม่โดนแตะ
