# mlab_vn_clean.parquet — คู่มือใช้งานข้อมูล

**ที่มา:** M-Lab NDT7 speed test, เวียดนาม, ดึงมาจาก Google BigQuery
**ไฟล์:** `data/vn/mlab_vn_clean.parquet` (~1.2 GB)
**สร้างโดย:** `notebooks/vn/mlab_vn_clean.ipynb`

---

## ตัวเลขสำคัญ

| | |
|---|---|
| **จำนวน rows** | 24,667,548 |
| **จำนวน columns** | 21 |
| **Unique client IPs** | 2,538,560 |
| **ช่วงเวลา** | 2023-01-01 → 2025-12-31 |
| **ขนาดไฟล์** | ~1.2 GB |

เปิดด้วย DuckDB (เร็ว ไม่กิน RAM):
```python
import duckdb
df = duckdb.connect().execute("SELECT * FROM read_parquet('data/vn/mlab_vn_clean.parquet') LIMIT 5").df()
```

---

## ความหมายของแต่ละ column

| Column | Type | ความหมาย |
|---|---|---|
| `id` | string | Test ID ไม่ซ้ำกัน จาก M-Lab |
| `date` | date | วันที่ทดสอบ (YYYY-MM-DD) |
| `test_time` | timestamp | วันและเวลาทดสอบแบบ exact |
| `year` | int | ปี — derive มาจาก `test_time` |
| `month` | int | เดือน (1–12) — derive มาจาก `test_time` |
| `hour` | int | ชั่วโมง (0–23) — derive มาจาก `test_time` |
| `type` | string | `download` หรือ `upload` — แต่ละ row คือหนึ่งทิศทาง |
| `mean_throughput_mbps` | float | **ความเร็วเน็ต** — ค่าเฉลี่ย Mbps ตลอดการทดสอบ |
| `min_rtt` | float | Minimum round-trip time (ms) — ยิ่งต่ำยิ่งดี (latency) |
| `loss_rate` | float | อัตราการสูญหายของ packet (0.0–1.0) — 0 = ไม่หายเลย |
| `duration` | float | ระยะเวลาการทดสอบ (วินาที) |
| `client_ip` | string | IP address ของผู้ทดสอบ (IPv4 หรือ IPv6) |
| `city` | string | เมืองของผู้ทดสอบจาก M-Lab geo — **มี NULL 14.6%** (ดูหมายเหตุ) |
| `province` | string | จังหวัด/province (63 จังหวัด) — join จาก `latitude`/`longitude` แบบ point-in-polygon กับ nearest-fallback, coverage 100% |
| `latitude` | float | Latitude ของผู้ทดสอบ (ไม่มี NULL) |
| `longitude` | float | Longitude ของผู้ทดสอบ (ไม่มี NULL) |
| `isp` | string | ชื่อ ISP ดิบจาก M-Lab — **มี NULL 8.1%** (IPs ที่ไม่มีชื่อ) |
| `network_type` | string | `broadband` / `cellular` / `hosting` / `unknown` — column หลักที่ใช้ filter |
| `category` | string | หมวดย่อยละเอียดขึ้น (ดูด้านล่าง) |
| `description` | string | ป้ายชื่อแบบอ่านออก สำหรับ category |
| `distance_from_server` | float | ระยะทาง Haversine (km) ระหว่าง client กับ M-Lab server |

---

## column ที่สำคัญที่สุด: `network_type`

**filter ด้วย column นี้ก่อนทุกครั้ง**

| `network_type` | Rows | % | ความหมาย |
|---|---|---|---|
| `broadband` | 22,014,446 | **89.2%** | เน็ตบ้าน/ออฟฟิศ (Viettel fiber, VNPT, FPT, CMC ฯลฯ) |
| `hosting` | 1,385,446 | 5.6% | CDN, cloud, VPN, datacenter — ไม่ใช่ traffic ของผู้ใช้จริง |
| `cellular` | 1,267,656 | **5.1%** | มือถือ (Viettel Mobile, VNPT Mobile, MobiFone, Vietnamobile) |

**สำหรับวิเคราะห์เน็ตผู้บริโภค ให้ใช้ `WHERE network_type IN ('broadband', 'cellular')` — ครอบคลุม 94.4% ของทั้งหมด**

`unknown` = **0%** — หลัง deep fetch สองรอบ (ครอบคลุม Viettel/VNPT conglomerate IPs ที่เหลือทั้งหมด รวม IPv6) ทุก row ถูก resolve ว่าเป็น mobile หรือ fixed ครบ 100% ไม่มี `network_type` column ที่เหลือเป็น `unknown` อีกต่อไปในชุดข้อมูลนี้

---

## ภาพรวมความเร็ว (broadband + cellular เท่านั้น)

| network_type | type | Mean (Mbps) | Median (Mbps) | Std |
|---|---|---|---|---|
| broadband | download | 68.3 | 42.2 | 89.0 |
| broadband | upload | 45.0 | 22.5 | 71.5 |
| cellular | download | 36.8 | 21.6 | 50.6 |
| cellular | upload | 18.9 | 10.0 | 32.1 |

Std สูงเป็นเรื่องปกติ — เวียดนามมีความแตกต่างระหว่างเมือง/ชนบท และ ISP แต่ละเจ้ามาก

---

## Top ISPs

| ISP | network_type | Rows |
|---|---|---|
| Viettel Group | broadband | 8,010,422 |
| VNPT Corp | broadband | 7,023,813 |
| FPT Telecom | broadband | 3,903,116 |
| VIETNAM POSTS AND TELECOMMUNICATIONS GROUP | broadband | 1,245,197 |
| Viettel Group | cellular | 486,808 |
| Viettel Corporation | broadband | 396,468 |

หมายเหตุ: หลัง deep fetch สองรอบ, Viettel Group/VNPT Corp conglomerate IPs ถูก resolve ครบ 100% แล้ว — ไม่มี row ไหนเหลืออยู่ใน `unknown` อีกต่อไป

---

## ข้อมูลแยกตามปี

| ปี | Rows |
|---|---|
| 2023 | 1,263,325 |
| 2024 | 3,895,740 |
| 2025 | 19,508,483 |

ปี 2025 มากที่สุดเพราะ M-Lab NDT7 ได้รับความนิยมขึ้นเรื่อยๆ — ระวังเวลาเปรียบเทียบข้ามปี เพราะ volume ไม่เท่ากัน

---

## หมายเหตุคุณภาพข้อมูล

- **`city` NULL 14.6%** — M-Lab geo lookup ครอบคลุมไม่ครบทุก IP แต่ `latitude`/`longitude` มีเสมอ ใช้ทำ spatial analysis ได้ปกติ
- **`isp` NULL 8.1%** — IPs ที่ M-Lab ไม่รู้จักชื่อ ถูก resolve ด้วย ip-api แล้วส่วนใหญ่กลายเป็น hosting/unknown
- **`unknown` = 0%** — หลัง deep fetch สองรอบครอบคลุม Viettel/VNPT conglomerate tail ทั้งหมด (รวม IPv6) ไม่มี row ไหนเหลือเป็น `unknown` แล้ว แต่ column ยัง reserve ค่านี้ไว้เผื่อข้อมูลเวอร์ชันอนาคต
- **แต่ละ row = หนึ่งทิศทางเท่านั้น** — download กับ upload เป็นคนละ row แชร์ `id` เดียวกัน ไม่มี "combined" row
- **`category` / `description`** — ละเอียดกว่า `network_type` แต่มี edge case บ้าง ใช้ `network_type` เป็น primary filter จะปลอดภัยที่สุด

---

## ขั้นตอนการ clean

1. **ลบ** 259,657 rows (1.04%) ที่ `mean_throughput_mbps <= 0` หรือ `duration <= 0` — ข้อมูลที่ผิดปกติ
2. **จำแนก `network_type`** ด้วย ip-api per-IP lookup สำหรับ conglomerate ใหญ่ (Viettel/VNPT ใช้ ASN เดียวกันทั้ง mobile และ fixed) และ curated name list สำหรับ ISP อื่นๆ — deep fetch สองรอบครอบคลุม conglomerate tail ทั้งหมด (~1.84M unique IPs รวม IPv6) ทำให้ `unknown` ลดจาก 8.5% เหลือ **0%**
3. **เพิ่ม derived columns** ได้แก่ `hour`, `year`, `month`, `distance_from_server`, `province` (point-in-polygon join จาก lat/long, coverage 100%)
4. **ไม่มีการแก้ไขข้อมูลเดิม** — classification เป็น column ใหม่ทั้งหมด ตัวเลข measurement เดิมไม่ถูกแตะ
