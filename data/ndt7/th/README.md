# ไทย (`th`) — NDT7 clean data

> **เอกสารฉบับจริงอยู่ที่ระดับบน ไม่ได้อยู่ในไฟล์นี้:**
> - วิธีทำข้อมูล → [`../CLEANING_OVERVIEW.md`](../CLEANING_OVERVIEW.md)
> - คู่มือ EDA + data dictionary → [`../README_for_eda.md`](../README_for_eda.md)
>
> ไฟล์นี้เก็บเฉพาะ**เรื่องที่เป็นของ th โดยเฉพาะ** ตัวเลขกลางและ schema อยู่ในสองไฟล์ข้างบน
> (เดิม folder ประเทศเคยมีสำเนาเอกสารเต็มของตัวเอง แล้วมันหลุด sync จนเลขผิดหมด — เลยเลิกทำแบบนั้น)

**ไฟล์:** `data/ndt7/th/mlab_th_clean.parquet` · อัปเดต 29 ก.ค. 2026 (v2)

| | |
|---|---|
| แถว | 60,248,884 |
| unique client IP | 9,416,238 |
| ช่วงข้อมูล | 2023-01-01 → 2025-12-31 |
| หน่วยพื้นที่ | 77 จังหวัด |
| ASN | 472 |
| คอลัมน์ | 23 |

**สัดส่วนประเภทเน็ต** (ไว้ sanity-check ว่าโหลดถูกไฟล์)

| network_type | แถว | % |
|---|---|---|
| `broadband` | 34,122,640 | 56.6% |
| `cellular` | 24,405,241 | 40.5% |
| `hosting` | 1,721,003 | 2.9% |

**ความเร็ว median** (Mbps · sanity-check)

| network_type | download | upload | min_rtt (ms) |
|---|---|---|---|
| `broadband` | 40.25 | 24.88 | 45.6 |
| `cellular` | 10.26 | 4.32 | 44.3 |

## เรื่องเฉพาะของ ไทย

- **ขอบเขตจังหวัดของไทยมาจากคนละแหล่งกับประเทศอื่น** — `data/geo/thailand_provinces.geojson` (77 จังหวัด, field `name`) ไม่ใช่ GADM
- **Bangkok Metropolis สัดส่วนสูงผิดปกติ** ส่วนหนึ่งมาจาก MaxMind fallback centroid (IP ที่ระบุตำแหน่งไม่แม่นตกมาที่ centroid สำรอง) ไม่ใช่ผู้ใช้กรุงเทพจริงทั้งหมด
- **`city` เป็นระดับเมือง ไม่ใช่จังหวัด** — เมืองใหญ่หลายเมืองแยกจากจังหวัดตัวเอง (Pattaya/Si Racha อยู่ใน Chon Buri · Hat Yai อยู่ใน Songkhla · Ko Samui อยู่ใน Surat Thani) ใช้ `province` ที่ join มาแล้ว อย่า map เอาจาก city
- **v1 ของไทยเคยใช้ 9 category และไม่มี hosting เลย** — v2 มี hosting 2.9% และเหลือ 3 กลุ่ม เท่าประเทศอื่น ไทยเพิ่งเทียบข้ามประเทศได้เป็นครั้งแรกใน v2
- **คอลัมน์ `description` และ `distance_from_server` ที่เคยมีใน v1 ไม่มีแล้ว** โค้ดเก่าที่เรียกจะพัง

---
