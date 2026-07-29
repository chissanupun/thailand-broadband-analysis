# ฟิลิปปินส์ (`ph`) — NDT7 clean data

> **เอกสารฉบับจริงอยู่ที่ระดับบน ไม่ได้อยู่ในไฟล์นี้:**
> - วิธีทำข้อมูล → [`../CLEANING_OVERVIEW.md`](../CLEANING_OVERVIEW.md)
> - คู่มือ EDA + data dictionary → [`../README_for_eda.md`](../README_for_eda.md)
>
> ไฟล์นี้เก็บเฉพาะ**เรื่องที่เป็นของ ph โดยเฉพาะ** ตัวเลขกลางและ schema อยู่ในสองไฟล์ข้างบน
> (เดิม folder ประเทศเคยมีสำเนาเอกสารเต็มของตัวเอง แล้วมันหลุด sync จนเลขผิดหมด — เลยเลิกทำแบบนั้น)

**ไฟล์:** `data/ndt7/ph/mlab_ph_clean.parquet` · อัปเดต 29 ก.ค. 2026 (v2)

| | |
|---|---|
| แถว | 262,110,845 |
| unique client IP | 16,773,991 |
| ช่วงข้อมูล | 2023-01-01 → 2025-12-31 |
| หน่วยพื้นที่ | 80 จังหวัด |
| ASN | 581 |
| คอลัมน์ | 24 |

**สัดส่วนประเภทเน็ต** (ไว้ sanity-check ว่าโหลดถูกไฟล์)

| network_type | แถว | % |
|---|---|---|
| `broadband` | 186,204,755 | 71.0% |
| `cellular` | 69,366,703 | 26.5% |
| `hosting` | 6,539,387 | 2.5% |

**ความเร็ว median** (Mbps · sanity-check)

| network_type | download | upload | min_rtt (ms) |
|---|---|---|---|
| `broadband` | 32.03 | 18.81 | 46.3 |
| `cellular` | 8.19 | 1.98 | 55.0 |

## เรื่องเฉพาะของ ฟิลิปปินส์

- **มี `region` เพิ่มมา 1 คอลัมน์** (17 region derive จาก province) — ประเทศอื่นไม่มี เวลา UNION ข้ามประเทศต้องใช้ `UNION ALL BY NAME`
- **boundary มี 81 จังหวัด แต่ข้อมูลมี 80** — Batanes ไม่มี test เลย
- **Globe มีสอง ASN คนละธุรกิจ** — AS4775 มือถือ (cellular 81%) · AS132199 Globe At Home (broadband 60%) ต้องมี footnote ถ้าจะรวมเป็นเจ้าเดียว
- ไฟล์ใหญ่ 14 GB — **อย่า `SELECT *`** และตั้ง `SET memory_limit` ก่อนเสมอ

---

