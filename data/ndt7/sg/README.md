# mlab_sg_clean.parquet — คู่มือใช้งานข้อมูล

**ที่มา:** M-Lab NDT7 speed test, สิงคโปร์, ดึงมาจาก Google BigQuery
**ไฟล์:** `data/sg/mlab_sg_clean.parquet` (~1.9 GB)
**สร้างโดย:** `notebooks/sg/mlab_sg_clean.ipynb`

---

## ตัวเลขสำคัญ

| | |
|---|---|
| **จำนวน rows** | 36,107,112 |
| **จำนวน columns** | 21 |
| **Unique client IPs** | 2,435,572 |
| **ช่วงเวลา** | 2023-01-01 → 2025-12-31 |
| **ขนาดไฟล์** | ~1.9 GB |

เปิดด้วย DuckDB (เร็ว ไม่กิน RAM):
```python
import duckdb
df = duckdb.connect().execute("SELECT * FROM read_parquet('data/sg/mlab_sg_clean.parquet') LIMIT 5").df()
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
| `city` | string | เมืองของผู้ทดสอบจาก M-Lab geo — **มี NULL 30.6%** (ดูหมายเหตุ) |
| `province` | string | ภูมิภาค/โซน (5 planning regions: Central, East, West, North, North-East) — join จาก `latitude`/`longitude` แบบ point-in-polygon กับ nearest-fallback, coverage 100% |
| `latitude` | float | Latitude ของผู้ทดสอบ (ไม่มี NULL) |
| `longitude` | float | Longitude ของผู้ทดสอบ (ไม่มี NULL) |
| `isp` | string | ชื่อ ISP ดิบจาก M-Lab — **มี NULL 3.6%** |
| `network_type` | string | `broadband` / `cellular` / `hosting` — column หลักที่ใช้ filter (ไม่มี `unknown` แล้ว ดูหมายเหตุด้านล่าง) |
| `category` | string | หมวดย่อยละเอียดขึ้น (ดูด้านล่าง) |
| `description` | string | ป้ายชื่อแบบอ่านออก สำหรับ category |
| `distance_from_server` | float | ระยะทาง Haversine (km) ระหว่าง client กับ M-Lab server |

---

## column ที่สำคัญที่สุด: `network_type`

สิงคโปร์จะต่างจากไทยและเวียดนามอย่างเห็นได้ชัดตรงที่มี **Hosting/Cloud สูงถึง 41%** ซึ่งไม่ใช่ข้อผิดพลาดของข้อมูล แต่เป็นเพราะสิงคโปร์เป็นศูนย์กลาง Datacenter (Regional Hub) ของภูมิภาค

| `network_type` | Rows | % | ความหมาย |
|---|---|---|---|
| `hosting` | 15,006,471 | **41.6%** | DigitalOcean, Verizon, Zscaler, AWS, Cloudflare, ฯลฯ + enterprise/corporate networks (Traffic จาก Cloud/VPN/Datacenter/Corporate) |
| `broadband` | 14,589,117 | **40.4%** | เน็ตบ้าน/ออฟฟิศ (SingTel Magix, StarHub, MyRepublic, M1, Viewqwest, SingNet) |
| `cellular` | 6,511,524 | **18.0%** | มือถือ (M1/MobileOne, Singtel Mobile, TPG-Simba) |

**สำหรับวิเคราะห์เน็ตผู้บริโภค ให้ใช้ `WHERE network_type IN ('broadband', 'cellular')` — คิดเป็น 58.4% ของทั้งหมด**

**ไม่มี `unknown` ในไฟล์นี้แล้ว** — หลัง deep fetch 2 รอบ (StarHub conglomerate tail ~966k unique IPs รวม IPv6 resolve ครบ 100%) และจัดกลุ่ม 19 ชื่อบริษัท non-consumer ที่ตกหล่นจาก keyword matching (Elsevier, Adobe, SAP, DSO National Laboratories ฯลฯ) เข้า `hosting` แล้ว สิ่งที่เหลืออยู่ใน `unknown` คือกลุ่ม NaN-group ที่ไม่มีชื่อ ISP เลยและ resolve ไม่ได้จริงๆ (562,211 rows, 1.5% ของก่อนตัด) — **ถูกตัดออกจากไฟล์ parquet นี้แล้วตามคำขอ** ไม่ใช่ไปรวมกับ category ไหน หากต้องการ noise-floor นี้กลับมาต้อง rebuild จาก raw M-Lab data ใหม่ผ่าน `mlab_sg_clean.ipynb`

หากคุณต้องการวิเคราะห์เน็ตบ้านหรือมือถือจริง ๆ **จำเป็นต้องกรองเอา `hosting` ออกเสมอ** มิฉะนั้นสถิติความเร็วเฉลี่ยของสิงคโปร์จะพุ่งสูงเกินจริงจากความเร็วในระดับ Datacenter

---

## ภาพรวมความเร็ว (broadband + cellular เท่านั้น)

| network_type | type | Mean (Mbps) | Median (Mbps) | Std |
|---|---|---|---|---|
| broadband | download | 192.5 | 90.1 | 259.1 |
| broadband | upload | 153.0 | 56.2 | 255.2 |
| cellular | download | 144.0 | 49.2 | 246.7 |
| cellular | upload | 90.0 | 15.1 | 242.0 |

ความเร็วเฉลี่ยและกลางของสิงคโปร์สูงกว่าเพื่อนบ้านมากเนื่องจากระบบโครงสร้างพื้นฐานระดับชาติที่เป็นไฟเบอร์ทั้งหมด ค่า Std ที่ค่อนข้างสูงแปลว่ามีความต่างระหว่างโปรโมชั่นแพ็กเกจ (เช่น Gigabit vs Multi-Gigabit) ค่อนข้างมาก

---

## Top ISPs

| ISP | network_type | Rows |
|---|---|---|
| Starhub Internet, Singapore | broadband | 5,521,528 |
| SingTel Magix Hostmaster | broadband | 4,620,697 |
| DigitalOcean, LLC | hosting | 3,219,207 |
| MobileOne Ltd | cellular | 3,078,377 |
| MCI / Verizon Business | hosting | 1,719,506 |
| Singtel Mobile | cellular | 1,432,455 |
| Zscaler | hosting | 1,366,463 |
| MyRepublic Pte. Ltd. | broadband | 1,304,355 |
| TPG Telecom Limited | cellular | 936,537 |

หมายเหตุ: หลัง deep fetch สองรอบ, `Starhub Internet, Singapore` conglomerate IPs ถูก resolve ครบ 100% แล้ว — ไม่มี row ไหนเหลืออยู่ใน `unknown` อีกต่อไป

---

## ข้อมูลแยกตามปี

| ปี | Rows |
|---|---|
| 2023 | 11,648,190 |
| 2024 | 14,134,193 |
| 2025 | 10,324,729 |

การกระจายของข้อมูลค่อนข้างคงที่ในแต่ละปี

---

## หมายเหตุคุณภาพข้อมูล

- **`city` NULL 30.6%** — เนื่องจากสิงคโปร์เป็นนครรัฐ (City-State) ข้อมูลระดับเมืองจึงไม่มีความสำคัญนัก ให้ใช้ `province` ซึ่งแบ่งเป็นโซนภูมิภาค (Central, East, West, North, Northeast) แทนได้
- **`hosting` สูงถึง 41%** — เป็นพฤติกรรมจริงของข้อมูลสิงคโปร์ ต้องกรองออกเสมอในการวิเคราะห์เน็ตบ้าน/มือถือ
- **`isp` NULL 3.6%** — ส่วนนี้ได้รับการดึงข้อมูลย้อนกลับและจำแนกกลุ่มผ่าน ip-api แล้ว
- **`unknown` rows ถูกตัดออกจากไฟล์นี้แล้ว** (562,211 rows, ~1.5% ของข้อมูลหลัง classify) — เป็นการตัดสินใจเฉพาะสำหรับ SG เพราะ tail ที่เหลือหลัง deep fetch เล็กพอที่จะไม่กระทบตัวเลข broadband/cellular/hosting ใดๆ (ต่างจาก VN ที่ resolve ได้ครบ 100% ไม่มีอะไรให้ตัด) หากต้องการ raw signal กลับมาต้อง rebuild จาก raw M-Lab data
- **แต่ละ row = หนึ่งทิศทางเท่านั้น** — download กับ upload เป็นคนละ row แชร์ `id` เดียวกัน
- **`province`** — map ภูมิภาคให้สำหรับสิงคโปร์ เพื่อความสะดวกในการแบ่งเขตวิเคราะห์เชิงพื้นที่

---

## ขั้นตอนการ clean

1. **ลบ** 522,718 rows (1.4%) ที่ `mean_throughput_mbps <= 0` หรือ `duration <= 0` — ข้อมูลที่ผิดปกติ
2. **จำแนก `network_type`** ด้วย ip-api per-IP lookup สำหรับ StarHub (ใช้ IP block ร่วมกันทั้งมือถือและเน็ตบ้าน) คัดกรองคู่กับกลุ่มผู้ให้บริการทั่วไป รวมถึงคัดแยกกลุ่ม Hosting/CDN/VPN ด้วย keyword matching — deep fetch สองรอบครอบคลุม StarHub conglomerate tail ทั้งหมด (~966k unique IPs รวม IPv6) + curated list สำหรับ 19 ชื่อบริษัท non-consumer ที่ตกหล่นจาก keyword matching
3. **เพิ่ม derived columns** ได้แก่ `hour`, `year`, `month`, `distance_from_server`, `province` (point-in-polygon join จาก lat/long, coverage 100%)
4. **ตัด `network_type='unknown'` ออก** (562,211 rows) — genuinely-unresolvable no-ISP-label tail ที่เหลือหลัง classify, ตัดสินใจตัดออกเพราะเล็กพอที่จะไม่กระทบ metric ใดๆ (แตกต่างจากปกติของโปรเจกต์นี้ที่ปกติจะเก็บ `unknown` ไว้แล้ว filter ตอน query)
5. **ไม่มีการแก้ไขข้อมูลเดิม** — classification เป็น column ใหม่ทั้งหมด ตัวเลข measurement เดิมไม่ถูกแตะ (ยกเว้นการตัด unknown rows ในขั้นตอนที่ 4)
