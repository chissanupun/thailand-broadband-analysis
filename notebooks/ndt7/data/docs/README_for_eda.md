# NDT7 Clean Data — คู่มือสำหรับทำ EDA

ข้อมูลความเร็วเน็ต (M-Lab NDT7 speed test) 5 ประเทศ ผ่านการ clean + จัดหมวดประเภทการเชื่อมต่อแล้ว
พร้อมนำไปทำ EDA / วิเคราะห์ต่อได้เลย ทุกไฟล์ **schema เหมือนกันเป๊ะ** เขียนโค้ดครั้งเดียวใช้ได้ทั้ง 5 ไฟล์

## ไฟล์ข้อมูล

| ประเทศ | path | แถว | ช่วงข้อมูล | หน่วยพื้นที่ |
|---|---|---|---|---|
| เวียดนาม | `data/vn/mlab_vn_clean.parquet` | 24,667,548 | 2023–2025 | 63 จังหวัด |
| มาเลเซีย | `data/my/mlab_my_clean.parquet` | 6,637,691 | 2023–2025 | 16 รัฐ |
| พม่า | `data/mm/mlab_mm_clean.parquet` | 2,115,739 | 2023–2025 | 13 รัฐ/ภาค |
| กัมพูชา | `data/kh/mlab_kh_clean.parquet` | 770,501 | 2023–2025 | 25 จังหวัด |
| ลาว | `data/lao/mlab_la_clean.parquet` | 139,693 | 2023–2025 | 17 แขวง |

> เป็นไฟล์ **parquet** อ่านด้วย `pd.read_parquet(path)` หรือ `duckdb` ก็ได้ (ไฟล์ VN ใหญ่ 1.2GB
> แนะนำใช้ duckdb query ตรง ๆ ไม่ต้องโหลดเข้า RAM ทั้งก้อน)

## Data Dictionary — 16 คอลัมน์

| คอลัมน์ | ชนิด | ความหมาย |
|---|---|---|
| `id` | string | รหัสเฉพาะของแต่ละการทดสอบ (unique, ไม่ซ้ำ) |
| `date` | date | วันที่ทดสอบ |
| `test_time` | timestamp | เวลาที่ทดสอบ (มีชั่วโมง/นาที) |
| `mean_throughput_mbps` | double | **ความเร็ว (Mbps)** — ตัวแปรหลักของงาน |
| `min_rtt` | double | ค่า latency ต่ำสุด (ms) — ยิ่งน้อยยิ่งดี |
| `loss_rate` | double | อัตราการสูญเสียแพ็กเก็ต (0–1) |
| `client_ip` | string | IP ผู้ทดสอบ |
| `duration` | bigint | ระยะเวลาการทดสอบ (ไมโครวินาที) |
| `type` | string | ทิศทางการวัด (download/upload) |
| `city` | string | เมือง (อาจ null ~15–30%) |
| `latitude` / `longitude` | double | พิกัด (geolocate ระดับเมือง) |
| `isp` | string | ชื่อผู้ให้บริการ (อาจ null — M-Lab ไม่มีชื่อให้ ~5–8%) |
| `network_type` | string | **ประเภทเครือข่าย** → `cellular` / `broadband` / `hosting` |
| `category` | string | **หมวดหมู่ (ใช้อันนี้เป็นหลัก)** → `Mobile` / `Consumer Broadband` / `Hosting/Datacenter` |
| `province` | string | หน่วยพื้นที่ระดับใหญ่สุด (จังหวัด/รัฐ/แขวง) — **ไม่มี null** |

## ⭐ `category` — คอลัมน์สำคัญที่สุด ต้องเข้าใจให้ตรง

แบ่งการเชื่อมต่อเป็น 3 กลุ่ม (`network_type` เป็นเวอร์ชันตัวพิมพ์เล็กของอันเดียวกัน):

| category | network_type | คือ | ใช้ยังไงใน EDA |
|---|---|---|---|
| **Mobile** | cellular | เน็ตมือถือ (4G/5G) | เทียบความเร็ว มือถือ vs บ้าน |
| **Consumer Broadband** | broadband | เน็ตบ้าน/ออฟฟิศ (fiber, DSL) | นี่คือ "เน็ตบ้าน" — ตัวหลักของการวัดคุณภาพเน็ตประเทศ |
| **Hosting/Datacenter** | hosting | server/CDN/cloud/VPN (Cloudflare, AWS, ฯลฯ) | **ควรกรองออกก่อนวิเคราะห์ผู้ใช้จริง** — ไม่ใช่คนใช้เน็ตทั่วไป |

> **สำคัญมาก:** `Hosting/Datacenter` ไม่ใช่ผู้ใช้จริง เป็นเครื่อง server ที่บังเอิญมารันเทสต์
> ถ้าจะวิเคราะห์ "คนใช้เน็ตในประเทศ" ให้ `WHERE category != 'Hosting/Datacenter'` ก่อนเสมอ
> (มีอยู่ราว 2.5–5% ของแต่ละประเทศ)

### สัดส่วนแต่ละหมวด (ไว้ sanity-check ว่าโหลดถูกไฟล์)

| ประเทศ | Consumer Broadband | Mobile | Hosting |
|---|---|---|---|
| เวียดนาม | 92.5% | 4.9% | 2.6% |
| มาเลเซีย | 49.7% | 46.3% | 4.0% |
| พม่า | 79.0% | 15.8% | 5.2% |
| กัมพูชา | 60.0% | 37.5% | 2.5% |
| ลาว | 52.0% | 45.3% | 2.7% |

## ที่มาของ `category` — จัดยังไง (เผื่อถูกถาม)

ไม่ได้เดาจากชื่อ ISP แต่**ตรวจ IP จริง**ผ่าน ip-api.com (ซึ่งบอกได้ว่า IP เป็น mobile/hosting):

1. **สุ่มตัวอย่าง (simple random sample)** IP ของแต่ละ ISP ตามสูตร Cochran → n=16,588 ต่อ ISP
   (99% confidence, ±1%) — ISP เล็กที่ IP ≤ 16,588 ตรวจครบทุกตัว
2. **ตัดสินต่อ ISP** ด้วย Wilson 99% CI เทียบเกณฑ์ความบริสุทธิ์ 99%:
   - ถ้าเกิน 99% เป็นทางเดียว → เหมาทั้ง ISP (mobile หรือ broadband)
   - ถ้าปน (mixed) → **ตรวจ IP ครบ 100%** แล้วติดป้ายราย IP
3. **hosting** แยกด้วย flag ของ ip-api + รายชื่อ CDN/cloud (Cloudflare, AWS, Akamai ฯลฯ)

รายละเอียดวิธี + การ validate อยู่ที่ `paper/methodology_isp_classification.md`

## ข้อควรระวังตอนทำ EDA

- **กรอง hosting ออกก่อน** ถ้าวิเคราะห์ผู้ใช้จริง (ดูด้านบน)
- **`isp` เป็น null ได้** (~5–8%) แต่ IP พวกนี้ยังมี `category` ครบ (ตรวจจาก IP ได้แม้ไม่มีชื่อ) — อย่า drop
- **พิกัดเป็นระดับเมือง** (M-Lab geolocate หยาบ) — 1 จังหวัดมีไม่กี่พิกัด ใช้ `province` วิเคราะห์เชิงพื้นที่ดีกว่า lat/long ดิบ
- **`type`** มีทั้ง download/upload — เวลาเทียบความเร็วอย่าลืมแยก หรือ filter ให้ตรงทิศทาง
- **ปริมาณข้อมูลไม่เท่ากันมาก** (VN 24.7M vs LA 0.14M) — เทียบข้ามประเทศให้ใช้ค่า % หรือ median ไม่ใช่ count ดิบ
- **median ความเร็ว** (ไว้ sanity-check): VN 30.4 / MY 23.4 / KH 13.5 / LA 12.2 / MM 11.1 Mbps

## ประเทศที่ยังไม่พร้อม

- **ฟิลิปปินส์ (ph)** — กำลัง fetch ข้อมูลเพิ่ม ยังไม่รวมในชุดนี้
- **ไทย (th)** — มี clean แยกต่างหาก (คนละ pipeline)
