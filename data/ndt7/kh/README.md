# กัมพูชา (`kh`) — NDT7 clean data

> **เอกสารฉบับจริงอยู่ที่ระดับบน ไม่ได้อยู่ในไฟล์นี้:**
> - วิธีทำข้อมูล → [`../CLEANING_OVERVIEW.md`](../CLEANING_OVERVIEW.md)
> - คู่มือ EDA + data dictionary → [`../README_for_eda.md`](../README_for_eda.md)
>
> ไฟล์นี้เก็บเฉพาะ**เรื่องที่เป็นของ kh โดยเฉพาะ** ตัวเลขกลางและ schema อยู่ในสองไฟล์ข้างบน
> (เดิม folder ประเทศเคยมีสำเนาเอกสารเต็มของตัวเอง แล้วมันหลุด sync จนเลขผิดหมด — เลยเลิกทำแบบนั้น)

**ไฟล์:** `data/ndt7/kh/mlab_kh_clean.parquet` · อัปเดต 29 ก.ค. 2026 (v2)

| | |
|---|---|
| แถว | 770,501 |
| unique client IP | 48,337 |
| ช่วงข้อมูล | 2023-01-01 → 2025-12-31 |
| หน่วยพื้นที่ | 25 จังหวัด |
| ASN | 94 |
| คอลัมน์ | 23 |

**สัดส่วนประเภทเน็ต** (ไว้ sanity-check ว่าโหลดถูกไฟล์)

| network_type | แถว | % |
|---|---|---|
| `broadband` | 481,411 | 62.5% |
| `cellular` | 255,954 | 33.2% |
| `hosting` | 33,136 | 4.3% |

**ความเร็ว median** (Mbps · sanity-check)

| network_type | download | upload | min_rtt (ms) |
|---|---|---|---|
| `broadband` | 17.83 | 15.01 | 50.3 |
| `cellular` | 11.39 | 5.77 | 77.3 |

## เรื่องเฉพาะของ กัมพูชา

- **AS38623 ชื่อใน ip-api เป็นข้อความโฆษณา** (`ISP/IXP IN CAMBODIA WITH THE BEST VERVICE IN THERE.`) ตัวจริงคือ **Metfone** — อย่าใช้ `as_name` เป็นชื่อแสดงผล

---

⚠️ **เลข v2 ไม่เท่า v1** — สัดส่วน cellular ลดลงทุกประเทศและอันดับประเทศสลับ
notebook เก่าที่ยังไม่ re-run ถือเลขผิดอยู่ · ดู [`../../HANDOFF.md`](../../HANDOFF.md)
