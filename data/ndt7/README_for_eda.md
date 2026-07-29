# NDT7 Clean Data — คู่มือสำหรับทำ EDA (v2 · 8 ประเทศ)

**อัปเดต 29 ก.ค. 2026 · นี่คือฉบับจริงฉบับเดียว** ไฟล์ `README_for_eda.md` ใน folder ประเทศย่อย
เป็นแค่ตัวชี้มาที่นี่

ข้อมูลความเร็วเน็ต M-Lab NDT7 ผ่านการ clean + ติด label ประเภทการเชื่อมต่อครบ 100% แล้ว
**schema เหมือนกันทั้ง 8 ไฟล์** (ยกเว้น PH มี `region` เพิ่มมา 1 คอลัมน์) เขียนโค้ดครั้งเดียวใช้ได้หมด

> วิธีการทำข้อมูล → [`CLEANING_OVERVIEW.md`](CLEANING_OVERVIEW.md) · บริบทงาน → [`HANDOFF.md`](../../HANDOFF.md)
> **ตัวเลขทั้งหน้านี้ verify ตรงจาก parquet เมื่อ 29 ก.ค. 2026** ไม่ได้ลอกจากเอกสารเก่า

---

## ⚠️ ก่อนใช้ — เลข v2 ไม่เท่า v1

สัดส่วน cellular ลดลงทุกประเทศและ**อันดับประเทศสลับ** (MY ตกจาก #1 ไป #4, TH ขึ้น #1)
notebook เก่าที่ยังไม่ re-run ถือเลขผิดอยู่ · ดู `CLEANING_OVERVIEW.md` หัวข้อแรก

---

## ไฟล์ข้อมูล

ทุกไฟล์อยู่ใน repo นี้แล้ว path คือ `data/ndt7/<c>/mlab_<c>_clean.parquet`

| | ประเทศ | แถว | ขนาด | unique IP | หน่วยพื้นที่ | ASN |
|---|---|---|---|---|---|---|
| `id` | อินโดนีเซีย | 367,247,163 | 19 GB | 19,956,896 | 34 จังหวัด | 2,577 |
| `ph` | ฟิลิปปินส์ | 262,110,845 | 14 GB | 16,773,991 | 80 จังหวัด (+17 region) | 581 |
| `th` | ไทย | 60,248,884 | 3.3 GB | 9,416,238 | 77 จังหวัด | 472 |
| `vn` | เวียดนาม | 24,667,548 | 1.2 GB | 2,538,560 | 63 จังหวัด | 290 |
| `my` | มาเลเซีย | 6,637,691 | 362 MB | 1,436,648 | 16 รัฐ | 309 |
| `mm` | พม่า | 2,115,739 | 95 MB | 144,576 | 14 รัฐ/ภาค | 141 |
| `kh` | กัมพูชา | 770,501 | 32 MB | 48,337 | 25 จังหวัด | 94 |
| `la` | ลาว | 139,693 | 5.6 MB | 13,668 | 17 แขวง | 34 |

**รวม 723,938,064 แถว** · ช่วงข้อมูล 2023-01-01 → 2025-12-31 ทุกประเทศ

> **ลาวใช้ code `la` และ folder `la`** — ต้นทางที่ `E:/ndt7` ใช้ folder ชื่อ `lao` แต่ในโปรเจกต์นี้
> normalize เป็น `la` หมดแล้ว พลาดกันบ่อย
>
> **หน่วยพื้นที่ = จำนวนที่ *มีจริงในข้อมูล*** ไม่ใช่จำนวนตามขอบเขตการปกครอง
> (PH boundary 81 แต่ Batanes ไม่มี test · MM boundary 15 มีจริง 14 · LA boundary 18 มีจริง 17)

### เปิดไฟล์

```python
import duckdb
con = duckdb.connect()
con.execute("SET memory_limit='10GB'")          # PH/ID ใหญ่ ต้องตั้ง

PARQ = {c: f"data/ndt7/{c}/mlab_{c}_clean.parquet"
        for c in ["id","ph","th","vn","my","mm","kh","la"]}

con.execute(f"SELECT * FROM read_parquet('{PARQ['th']}') LIMIT 5").df()

# ทุกประเทศรวมกัน (คอลัมน์ไม่เท่ากัน — PH มี region ประเทศอื่นไม่มี)
q = " UNION ALL BY NAME ".join(
    f"SELECT '{c}' AS country, * FROM read_parquet('{p}')" for c, p in PARQ.items())
```

> **อ่านเฉพาะคอลัมน์ที่ใช้เสมอ** — parquet เป็น columnar การ `SELECT` แค่ที่ต้องการเร็วกว่ามาก
> **อย่า `SELECT *` บน PH/ID** ถ้าไม่จำเป็น (14 GB / 19 GB) และอย่า `pd.read_parquet()` ทั้งก้อน

---

## Data Dictionary — 23 คอลัมน์ (PH 24)

| คอลัมน์ | ชนิด | ความหมาย |
|---|---|---|
| `id` | string | รหัสเฉพาะของการทดสอบ |
| `date` | date | วันที่ทดสอบ |
| `test_time` | timestamp | เวลาที่ทดสอบเต็ม |
| `year` / `month` / `hour` | int | derive จาก `test_time` |
| `type` | string | `download` / `upload` — **แต่ละแถวคือทิศทางเดียว** |
| `mean_throughput_mbps` | double | **ความเร็ว (Mbps) — ตัวแปรหลักของงาน** |
| `min_rtt` | double | latency ต่ำสุด (ms) ยิ่งน้อยยิ่งดี |
| `loss_rate` | double | อัตราสูญเสียแพ็กเก็ต (0–1) |
| `duration` | bigint | ระยะเวลาการทดสอบ |
| `client_ip` | string | IP ผู้ทดสอบ (IPv4/IPv6) |
| `city` | string | เมืองจาก M-Lab geo — **null ได้เยอะ** (ดูตารางล่าง) |
| `latitude` / `longitude` | double | พิกัดระดับเมือง — **null 0.00% ทุกประเทศ** |
| **`network_type`** | string | **`cellular` / `broadband` / `hosting` — ไม่ทับกัน** |
| `category` | string | `Mobile` / `Consumer Broadband` / `Hosting/Datacenter` — map 1:1 กับ `network_type` |
| **`asn`** | string | **คีย์สำหรับจัดกลุ่ม ISP ทุกกรณี** |
| `as_name` | string | ชื่อ AS จาก ip-api — ⚠️ เชื่อไม่ได้ ดู "กับดัก" |
| `isp` | string | ชื่อจาก M-Lab — ⚠️ **ห้ามใช้จัดกลุ่ม** |
| `operator` | string | ป้ายชื่อแบรนด์ · null ได้ · ⚠️ **ห้ามใช้จัดกลุ่ม** ใช้แสดงผลเท่านั้น |
| `label_source` | string | `block` / `census` — ที่มาของ label ตรวจย้อนกลับได้ทุกแถว |
| `province` | string | หน่วยพื้นที่ ADM1 — null ~0% (ID มี 6,896 แถว = 0.002% · ที่เหลือ 0) |
| `region` | string | **PH เท่านั้น** — 17 region derive จาก province |

> คอลัมน์ `description` และ `distance_from_server` ที่เคยมีใน TH v1 **ไม่มีแล้วใน v2**
> ถ้าโค้ดเก่าเรียกอยู่จะพัง

---

## ⭐ `network_type` — คอลัมน์สำคัญที่สุด

| network_type | category | คือ | ใช้ยังไง |
|---|---|---|---|
| `cellular` | Mobile | เน็ตมือถือ | เทียบมือถือ vs เน็ตบ้าน |
| `broadband` | Consumer Broadband | เน็ตบ้าน/ออฟฟิศ | ตัวหลักของการวัดคุณภาพเน็ตประเทศ |
| `hosting` | Hosting/Datacenter | server/CDN/cloud/VPN | **กรองออกก่อนวิเคราะห์ผู้ใช้จริง** |

```sql
WHERE network_type IN ('broadband','cellular')   -- EDA ผู้บริโภค ใช้อันนี้
```

### สัดส่วน v2 (ไว้ sanity-check ว่าโหลดถูกไฟล์)

| ประเทศ | broadband | cellular | hosting |
|---|---|---|---|
| ID | 64.6% | 25.6% | **9.8%** |
| PH | 71.0% | 26.5% | 2.5% |
| TH | 56.6% | **40.5%** | 2.9% |
| VN | 88.4% | 4.2% | 7.3% |
| MY | 63.2% | 31.9% | 5.0% |
| MM | 77.5% | 13.6% | 8.9% |
| KH | 62.5% | 33.2% | 4.3% |
| LA | 50.1% | 36.1% | **13.9%** |

> hosting ไม่ใช่ 2–5% เหมือนที่เอกสาร v1 เขียนไว้ — **LA 13.9% และ ID 9.8% สูงมาก**
> ถ้าลืมกรองออก ตัวเลขสองประเทศนี้จะเพี้ยนหนัก

---

## ความเร็ว median (ไว้ sanity-check)

median download / upload หน่วย Mbps · median `min_rtt` หน่วย ms

| ประเทศ | bb ↓ | bb ↑ | bb rtt | cell ↓ | cell ↑ | cell rtt |
|---|---|---|---|---|---|---|
| MY | 50.37 | 28.49 | 17.0 | 12.61 | 5.98 | 31.7 |
| VN | 42.39 | 22.51 | 108.0 | 19.96 | 8.63 | 77.5 |
| TH | 40.25 | 24.88 | 45.6 | 10.26 | 4.32 | 44.3 |
| PH | 32.03 | 18.81 | 46.3 | 8.19 | 1.98 | 55.0 |
| LA | 22.10 | 14.70 | 76.4 | 9.91 | 4.94 | 93.1 |
| KH | 17.83 | 15.01 | 50.3 | 11.39 | 5.77 | 77.3 |
| MM | 11.85 | 10.61 | 86.3 | 11.01 | 4.27 | 98.9 |
| ID | **9.80** | 6.54 | 20.0 | **11.93** | 5.19 | 26.6 |

> **ID กับ MM: cellular เร็วกว่าหรือเท่ากับ broadband** — ID cellular median 11.93 > broadband 9.80
> ไม่ใช่ bug แต่เป็นเรื่องที่ต้องอธิบายในเปเปอร์ (ฐาน broadband ของ ID กว้างและมีของถูกเยอะ)
>
> **mean สูงกว่า median มาก**ทุกประเทศ (TH broadband mean 100.5 vs median 40.3) เพราะ fiber
> ระดับ Gigabit ดึงหาง — **ใช้ median เสมอ** เว้นแต่มีเหตุผลเฉพาะ

---

## 🪤 กับดัก — อ่านก่อนเขียนโค้ด

**1. จัดกลุ่ม ISP ด้วย `asn` เท่านั้น ห้ามใช้ `isp` หรือ `operator`**
ip-api คืน**ชื่อองค์กรลูกค้า**สำหรับช่วง IP ที่เป็น leased line — AS4750 (CS Loxinfo) มีชื่อ `isp`
ถึง **420 ชื่อ** เช่น `dermatology`, `waterflow`, `kadokawa-ca` · และชื่อสะกดต่างของเจ้าเดียวกัน
ถูกนับแยก (`Globe Telecoms` vs `Globe Telecom Inc.`)

**2. `as_name` ก็เชื่อไม่ได้** — เป็นชื่อบริษัทที่เลิกใช้แล้วหรือข้อความโฆษณา:

| ASN | ip-api บอกว่า | ตัวจริง |
|---|---|---|
| 9534 | Binariang Berhad | **Maxis** |
| 9930 | TTNET | **TIME dotCom** |
| 38623 | `ISP/IXP IN CAMBODIA WITH THE BEST VERVICE IN THERE.` | **Metfone** |
| 132618 | Real Future Company Limited | **TrueMove H (True)** |
| 131445 | Advance Wireless Network | **AIS** |

**3. คัด ASN ต้องถ่วงน้ำหนักด้วย `test` ไม่ใช่ `address`**
CGNAT ทำให้ ASN มือถือมี test ต่อ address สูงกว่ามาก — Real Future เป็น ASN อันดับ 2 ของไทย
เมื่อวัดด้วย test (13.15%) แต่หลุดเกณฑ์ถ้าวัดด้วย address

**4. `asn` ในไฟล์นี้เป็น VARCHAR** แต่อ่านจาก CSV จะได้ BIGINT — cast ก่อน join/COALESCE

**5. DuckDB ทำงานกับ IP ต้อง `INSTALL inet; LOAD inet`** แล้วใช้
`network(CAST(ip || '/48' AS INET))` — **ห้ามตัดสตริงเอง** เพราะ IPv6 ของ ID ราว 19% เขียนแบบย่อ
(`::`) การตัดสตริงจะทำให้ /48 เดียวกันกลายเป็นคนละ key

**6. อ่าน CSV ที่มีชื่อ ISP ด้วย pandas ไม่ใช่ DuckDB** — ชื่อมี comma ในเครื่องหมายคำพูดและมี
quote ซ้อน (`"LLC ""SPUTNIK"""`) · ถ้าจำเป็นต้องใช้ DuckDB ต้องระบุ `quote='"', escape='"'`

**7. แต่ละแถว = ทิศทางเดียว** — download กับ upload เป็นคนละแถว เวลาเทียบความเร็ว
ต้อง filter `type` ให้ตรง ไม่งั้นจะได้ค่าปนกัน

**8. CGNAT — unique IP ≠ unique user** สัดส่วน address ≠ สัดส่วน test

---

## ข้อควรระวังเรื่อง null และการกระจายตัว

| ประเทศ | city null | isp null | operator null |
|---|---|---|---|
| ID | 12.0% | 12.1% | 25.6% |
| PH | 7.2% | 6.0% | 7.3% |
| TH | 5.4% | 0.2% | 4.6% |
| VN | 14.6% | 8.1% | 10.4% |
| MY | 9.5% | 0.8% | 6.4% |
| MM | **47.0%** | 5.1% | **56.2%** |
| KH | 27.1% | 2.9% | 28.1% |
| LA | 32.2% | 1.7% | 17.6% |

- **`province` และ `latitude`/`longitude` แทบไม่มี null** — มีแค่อินโดที่ `province` เป็น null 6,896 แถว
  (0.002%) ประเทศอื่นเป็น 0 ทั้งหมด · ใช้ `province` วิเคราะห์เชิงพื้นที่
  อย่าไป map เอาจาก `city` (city null เยอะและเป็นระดับเมือง ไม่ตรงจังหวัด)
- **`isp` null ได้ แต่แถวพวกนี้ยังมี `network_type` ครบ** (label มาจาก IP ไม่ใช่ชื่อ) — **อย่า drop**
- **`operator` null เยอะมากใน MM (56%)** เพราะยังไม่ได้แมป ASN เล็ก ๆ — ใช้แสดงผลเท่านั้น อย่าใช้กรอง

### ⚠️ ข้อมูลแต่ละปีไม่สมดุลอย่างหนัก — สำคัญกับ trend analysis

| ประเทศ | 2023 | 2024 | 2025 |
|---|---|---|---|
| VN | 1,263,325 | 3,895,740 | **19,508,483 (79%)** |
| MM | 137,378 | 760,233 | **1,218,128 (58%)** |
| LA | 20,737 | 53,591 | 65,365 |
| KH | 192,315 | 269,465 | 308,721 |
| MY | 805,540 | 2,462,114 | 3,370,037 |
| ID | 107,928,180 | 136,786,753 | 122,532,230 |
| PH | 80,015,809 | 82,850,274 | 99,244,762 |
| TH | 19,700,569 | 25,098,713 | 15,449,602 |

**VN มี 79% ของข้อมูลอยู่ในปี 2025 ปีเดียว** — การเทียบ trend ข้ามปีของ VN (และ MM)
เสี่ยงสะท้อนการเปลี่ยนแปลงของ*ฐานผู้ทดสอบ* มากกว่าการเปลี่ยนแปลงของ*ความเร็วจริง*
ส่วน TH กลับกัน ปี 2025 น้อยที่สุด · **เทียบข้ามประเทศให้ใช้ % หรือ median ไม่ใช่ count ดิบ**

---

## ที่มาของ label (สรุปสั้น)

ไม่ได้เดาจากชื่อ ISP แต่ตรวจ IP จริงผ่าน ip-api.com โดย probe 5 address ต่อบล็อก
(`/24` IPv4 · `/48` IPv6) แล้วแปะทั้งบล็อก — 50.4M address / 226,070 บล็อก / probe 1,001,120 ครั้ง
ยิงรวดเดียวจบใน 11.49 ชม. เพื่อให้เป็น snapshot เดียวกันทุกประเทศ

`label_source` บอกที่มาต่อแถว: `block` (จาก block verdict) หรือ `census` (ยิงราย address)
TH/PH มี census 0.1% ที่เหลือเป็น block เกือบ 100%

**ข้อจำกัดที่ต้องรู้:** ไม่มี ground truth — validate ได้แค่ความสม่ำเสมอภายในของ ip-api
เคลมได้แค่ *"ทำซ้ำคำตอบ ip-api ณ วันหนึ่งได้ซื่อตรง"* **ห้าม**เคลมว่า *"แยก fixed/mobile ถูก"*

รายละเอียดเต็ม → [`CLEANING_OVERVIEW.md`](CLEANING_OVERVIEW.md)
