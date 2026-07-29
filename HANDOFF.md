# HANDOFF — สรุปสถานะข้อมูล NDT7 ทั้งหมด (29 ก.ค. 2026)

> ## 📍 อ่านก่อน — folder หลักย้ายแล้ว (29 ก.ค. 2026)
>
> **folder หลักคือ `E:\thailand-broadband-analysis\` ตั้งแต่นี้ไป**
> ไฟล์นี้ (ฉบับจริง) อยู่ที่ `E:\thailand-broadband-analysis\HANDOFF.md`
>
> **`E:\ndt7\` = แหล่งต้นทาง read-only เท่านั้น** ห้ามเขียนทับ ห้าม refactor อะไรในนั้น
> เก็บไว้เป็น pipeline ต้นทาง + artifact ดิบ (`data/labels/`, `ip_fetch/`, `docs/`)
>
> ### ข้อมูล copy เข้ามาในโปรเจกต์แล้ว — ไม่ต้องอ้าง path ข้าม drive อีก
>
> clean parquet ทั้ง 8 ประเทศถูก copy มาไว้ที่ `data/ndt7/<c>/mlab_<c>_clean.parquet` แล้ว
> (รวม ~40 GB · ตรวจแล้วขนาดตรงกับต้นทางทุกไฟล์ byte-for-byte)
> notebook ใน `notebooks/ndt7/main/` ที่ชี้ `../../../data/ndt7/<c>/...` อยู่แล้ว **จึงรันได้เลย**
>
> - **ลาวอยู่ใน `data/ndt7/la/` แล้ว** (ต้นทางใช้ folder `lao` — ตรงนี้ normalize ให้เป็น `la` หมดแล้ว)
> - parquet ถูก gitignore ไว้ (`data/ndt7/**/*.parquet`) — **ห้าม commit** ส่วน `.md`/`.csv` ยัง track ปกติ
> - ถ้าต้นทางที่ `E:/ndt7` มีการแก้ ต้อง copy ทับใหม่เอง ไม่มีอะไร sync อัตโนมัติ
>
> **⚠️ Memory ของ Claude ไม่ข้าม folder** — ผูกกับ path ของโปรเจกต์ ถ้าเปิด session ใน
> folder ใหม่ memory ชุดเดิมจะไม่ถูกโหลด ไฟล์นี้จึงเป็นตัวเดียวที่พาบริบทข้ามไปได้
> **เริ่ม session ใหม่:** บอกให้อ่าน `E:/thailand-broadband-analysis/HANDOFF.md` ก่อนทำอะไร
>
> **path ในเอกสารนี้:** ที่ขึ้นต้น `data/ndt7/...` = ในโปรเจกต์นี้ ·
> ที่เขียน `E:/ndt7/...` เต็ม ๆ = ต้นทาง read-only

> ลงรายละเอียดเชิงวิธีการที่ `E:/ndt7/docs/ndt7-pipeline-v2.md` ·
> สถานะการ fetch ที่ `E:/ndt7/ip_fetch/srs/RESUME.md`
>
> **บริบท:** งานที่เหลือคือ**เอาข้อมูลชุดนี้ไปใช้กับ notebook** ไม่ใช่แก้ pipeline อีก ·
> pipeline ข้อมูลถือว่าจบแล้ว

---

## 1. ข้อมูลตอนนี้เป็นยังไง

**8 ประเทศ · 723,938,064 แถว · ไม่มีแถวไหนที่ไม่มี label**

| ประเทศ | ไฟล์ (ในโปรเจกต์นี้) | แถว | cellular | broadband | hosting | หน่วยพื้นที่ |
|---|---|---|---|---|---|---|
| ID | `data/ndt7/id/mlab_id_clean.parquet` | 367,247,163 | 93,988,159 | 237,196,480 | 36,062,524 | 34 |
| PH | `data/ndt7/ph/mlab_ph_clean.parquet` | 262,110,845 | 69,366,703 | 186,204,755 | 6,539,387 | 80 (+17 region) |
| TH | `data/ndt7/th/mlab_th_clean.parquet` | 60,248,884 | 24,405,241 | 34,122,640 | 1,721,003 | 77 |
| VN | `data/ndt7/vn/mlab_vn_clean.parquet` | 24,667,548 | 1,047,714 | 21,817,334 | 1,802,500 | 63 |
| MY | `data/ndt7/my/mlab_my_clean.parquet` | 6,637,691 | 2,115,967 | 4,193,107 | 328,617 | 16 |
| MM | `data/ndt7/mm/mlab_mm_clean.parquet` | 2,115,739 | 287,992 | 1,639,687 | 188,060 | 14 |
| KH | `data/ndt7/kh/mlab_kh_clean.parquet` | 770,501 | 255,954 | 481,411 | 33,136 | 25 |
| LA | `data/ndt7/la/mlab_la_clean.parquet` | 139,693 | 50,387 | 69,925 | 19,381 | 17 |

> **ลาวใช้ `la` ทั้ง code และ folder ในโปรเจกต์นี้** (ต้นทาง `E:/ndt7` ใช้ folder `lao` — normalize แล้ว)
>
> **หน่วยพื้นที่ = จำนวนที่มีจริงในข้อมูล** ไม่ใช่จำนวนตามขอบเขตการปกครอง
> (PH boundary 81 แต่ Batanes ไม่มี test · MM boundary 15 มีจริง 14 · LA boundary 18 มีจริง 17)

### เปิดใช้

```python
import duckdb
con = duckdb.connect()
con.execute("SET memory_limit='10GB'")               # PH/ID ใหญ่ ต้องตั้ง
con.execute("SET temp_directory='.tmp/duckdb'")
con.execute("SET preserve_insertion_order=false")    # กัน OOM ตอน group by ที่ cardinality สูง

PARQ = {c: f"data/ndt7/{c}/mlab_{c}_clean.parquet"
        for c in ["id","ph","th","vn","my","mm","kh","la"]}

# ทุกประเทศรวมกัน (คอลัมน์ไม่เท่ากัน — PH มี region ประเทศอื่นไม่มี)
q = " UNION ALL BY NAME ".join(
    f"SELECT '{c}' AS country, * FROM read_parquet('{p}')" for c, p in PARQ.items())
```

> อ่านเฉพาะคอลัมน์ที่ใช้เสมอ · **อย่า `SELECT *` บน PH/ID** (14 GB / 19 GB)
> **อย่ารัน PH กับ ID พร้อมกัน** — เคยเจอ MemoryError (จอง 1.95 GiB สำหรับ 262M แถว)

### คอลัมน์

```
id, date, test_time, mean_throughput_mbps, min_rtt, loss_rate, client_ip, duration, type,
city, latitude, longitude, isp, asn, as_name, label_source, hour, year, month,
network_type, category, province, [region — PH เท่านั้น], operator
```

| คอลัมน์ | ความหมาย |
|---|---|
| `network_type` | `cellular` / `broadband` / `hosting` — ไม่ทับกัน |
| `category` | `Mobile` / `Consumer Broadband` / `Hosting/Datacenter` — map 1:1 กับ network_type |
| **`asn`** | **คีย์สำหรับจัดกลุ่ม ISP ทุกกรณี** (VARCHAR) |
| `as_name` | ชื่อ AS จาก ip-api — เชื่อไม่ได้ ดูข้อ 5 |
| `isp` | ชื่อจาก M-Lab — **ห้ามใช้จัดกลุ่ม** ดูข้อ 5 |
| `operator` | ป้ายชื่อแบรนด์จาก `ip_fetch/srs/asn_operator.csv` · NULL ได้ · **ห้ามใช้จัดกลุ่ม** |
| `label_source` | `block` หรือ `census` — ที่มาของ label ตรวจย้อนกลับได้ทุกแถว |

**สำหรับ EDA ผู้บริโภค:** `WHERE network_type IN ('broadband','cellular')` (ตัด hosting)

### แหล่ง label ดิบ

`data/labels/ip_label_<c>.parquet` — 50,456,244 address · 1 แถวต่อ address
เก็บ `mobile / hosting / proxy / asn / as_name / label_source` ต่อ address
**นี่คือ artifact ตัวจริง** ที่รอด refactor · clean parquet เป็นแค่ผลของการ join มันเข้ากับข้อมูลดิบ

---

## 2. 🚨 ตัวเลขเปลี่ยนจากเดิม — เรื่องสำคัญที่สุดในไฟล์นี้

**สัดส่วน cellular ลดลงทุกประเทศ** เพราะ ip-api แก้ฐานข้อมูลตัวเอง และเรา re-query ใหม่ทั้งหมดในหน้าต่างเดียว

| | v1 (เก่า) | v2 (ตอนนี้) | เปลี่ยน |
|---|---|---|---|
| MY | 46.3% | 31.9% | **−14.4 pp** |
| PH | 36.7% | 26.5% | **−10.2 pp** |
| LA | 45.3% | 36.1% | **−9.3 pp** |
| TH | 45.7% | 40.5% | −5.2 pp |
| KH | 37.5% | 33.2% | −4.3 pp |
| ID | 28.8% | 25.6% | −3.2 pp |
| MM | 15.8% | 13.6% | −2.2 pp |
| VN | 4.9% | 4.2% | −0.6 pp |

**อันดับประเทศสลับ ไม่ใช่แค่ตัวเลขขยับ:**
- v1: **MY** → TH → LA → KH → PH → ID → MM → VN
- v2: **TH** → LA → KH → **MY** → PH → ID → MM → VN

มาเลเซียตกจากอันดับ 1 ไปอันดับ 4

### ผลที่ตามมา

- **notebook วิเคราะห์ทุกเล่มถือตัวเลขเก่าอยู่** ต้อง re-run ทั้งหมด
- เล่มที่กระทบหนักสุด: `notebooks/ph/ndt7_ph_paper.ipynb` (มี pass-rate เทียบ Lübben & Misfeld 2022
  แยกตาม network_type)
- ประโยคใดๆ ที่อ้าง "ประเทศไหนใช้มือถือมากสุด" **เปลี่ยนคำตอบ**
- ถ้ารุ่นพี่/อาจารย์เคยเห็นตัวเลขชุดเก่า ต้องอธิบาย → ใช้ `docs/ndt7-pipeline-v2.md` §5.7 ที่เขียนไว้แล้ว

---

## 3. ทำไมถึงเชื่อชุดใหม่มากกว่า (สำหรับตอบ reviewer)

ตรวจแล้วว่าเจ้าที่เปลี่ยนสถานะเยอะเป็นใคร ผลออกมาเป็นระเบียบเกินกว่าจะเป็นความมั่ว:

**เจ้าที่หลุดจาก cellular = แบรนด์เน็ตบ้าน/ดาวเทียม/WiFi ล้วน**
Starlink (MY 96%) · AIS SUPER WiFi (89%) · Yes/YTL (69%) · Converge (64%) · TRUE INTERNET (64%) ·
AIS Fibre · 3BB · ดาวเทียมฟิลิปปินส์และลาว 100%

**มือถือแท้แทบไม่ขยับ**
Telkomsel 4.7% · XL Axiata 0.5% · Viettel 2.6% · VNPT 0.3% · MobiFone 1.4% · Maxis 2.6%

**ไทยเปลี่ยนสองทิศทาง — หลักฐานแข็งที่สุด** (TH เป็นประเทศเดียวที่ v1 ใช้ census ราย address
ด้วยกฎเดียวกับ v2 ตัวแปรจึงเหลือแค่วันที่ fetch):

```
TrueMove H  +847,625 → cellular      TRUE INTERNET   −945,903 → fixed
dtac        +641,295 → cellular      AIS Fibre       −674,162 → fixed
AWN/AIS     +486,481 → cellular      AIS SUPER WiFi  −361,100 → fixed
```

**2 เคสที่ต้องมี footnote** (ไม่ใช่ error แต่เป็นเจ้าที่มีสองธุรกิจจริง):
- **PH Globe** — AS4775 มือถือ (cellular 81%) · AS132199 Globe At Home (broadband 60%)
- **MY CelcomDigi** — Celcom cellular 63% · Digi broadband 60% (ทั้งคู่ขายทั้งมือถือและเน็ตบ้าน)

---

## 4. ข้อมูลมาจากไหน — วิธีย่อ

ip-api.com แก้ฐานข้อมูลทับที่เดิม และแต่ละประเทศเคย fetch คนละวัน (16–27 ก.ค.) label เดิมจึง
ไม่ใช่ snapshot เดียวกัน — ขัดกับข้ออ้างหลักของเปเปอร์

**แก้โดย re-query ทุกประเทศใน 11.49 ชม. เดียว (28 ก.ค. 22:45 → 29 ก.ค. 10:15)**

ทำได้เพราะ ip-api เก็บธง mobile **ต่อช่วง IP ไม่ใช่ต่อ IP** จึง probe แค่ 5 address ต่อบล็อก
(/24 สำหรับ IPv4, /48 สำหรับ IPv6) แล้วแปะทั้งบล็อก

| | |
|---|---|
| address ทั้งหมด | 50,456,244 |
| บล็อก | 226,070 |
| probe | 1,001,120 (แทนที่จะเป็น 50.4M = ~27 วัน) |
| บล็อกที่ probe ไม่ลงรอย | **44 (0.019%)** |
| address ที่ต้องยิงทีละตัว | 889 — ยืนยันว่าปนจริง **44/44 ไม่มี false positive** |
| error ที่คาดหวัง | 0.027% |

**การตรวจสอบที่ผ่าน:** address 379 ตัวที่อยู่ในข้อมูล 2–3 ประเทศ (สร้าง target แยกกัน สุ่ม probe
คนละตัว) ได้ label ตรงกันหมด **0 ขัดแย้ง**

---

## 5. 🪤 กับดัก — อ่านก่อนเขียนโค้ด

**1. จัดกลุ่ม ISP ด้วย `asn` เท่านั้น ห้ามใช้ `isp` หรือ `operator`**

ip-api คืน**ชื่อองค์กรลูกค้า**สำหรับช่วง IP ที่เป็น leased line — AS4750 (CS Loxinfo) มีชื่อ "isp"
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

ใช้ `operator` เป็นป้ายแสดงผลเท่านั้น (`ip_fetch/srs/asn_operator.csv` 79 แถว) แก้ได้แล้ว
`python ip_fetch/srs/patch_operator.py` โดยไม่ต้อง re-run notebook

**3. คัด ASN ต้องถ่วงน้ำหนักด้วย `test` ไม่ใช่ `address`**

CGNAT ทำให้ ASN มือถือมี test ต่อ address สูงกว่ามาก — Real Future เป็น ASN อันดับ 2 ของไทย
เมื่อวัดด้วย test (13.15%) แต่หลุดเกณฑ์ถ้าวัดด้วย address **ผมพลาดเรื่องนี้มาแล้วหนึ่งรอบ**

**4. DuckDB ต้อง `INSTALL inet; LOAD inet`** แล้วใช้
`network(CAST(ip || '/48' AS INET))` — ห้ามตัดสตริงเอง เพราะ IPv6 ของ ID ราว 19% เขียนแบบย่อ (`::`)
การตัดสตริงจะทำให้ /48 เดียวกันกลายเป็นคนละ key

**5. `asn` อ่านจาก CSV เป็น BIGINT แต่จาก regexp เป็น VARCHAR** — cast ก่อน join/COALESCE

**6. อ่าน CSV ที่มีชื่อ ISP ด้วย pandas ไม่ใช่ DuckDB** — ชื่อมี comma ใน quote และมี quote ซ้อน
(`"LLC ""SPUTNIK"""`) · ถ้าจำเป็นต้องใช้ DuckDB ต้องระบุ `quote='"', escape='"'`

**7. `0.019%` คือบล็อกที่ *ตรวจพบ* ว่าปน ไม่ใช่อัตราจริง** — k=5 จับ mixed block ได้ราว 58%
เขียนในเปเปอร์ว่า "detected" เสมอ

**8. ขอบเขตพื้นที่มาจากคนละแหล่ง**

| | แหล่ง | หมายเหตุ |
|---|---|---|
| TH | `thailand_provinces.geojson` 77 จังหวัด field `name` | **ไม่ใช่ GADM** |
| ID | GADM 4.1 IDN ADM1 = **34 จังหวัด** | ข้อมูลปี 2022 ก่อนแยกปาปัวเป็น 6 (2022–24) |
| PH | GADM ADM1 81 จังหวัด → derive 17 region | ข้อมูลจริงมี 80 (Batanes ไม่มี test) |
| อื่นๆ | GADM 4.1 ADM1 | |

GADM ฟรีสำหรับงานวิชาการ **ต้อง cite และห้ามแจก geometry ต่อ** — delivery zip ส่งแค่ parquet

---

## 6. เรื่องที่ตัดสินใจไปแล้ว — อย่ารื้อ

| | เหตุผล |
|---|---|
| **จัดกลุ่มด้วย ASN** ไม่ใช่ชื่อ ISP | ดูข้อ 5 |
| **ไม่ยุบรวมเจ้าที่ควบรวมกิจการ** (dtac/True มี.ค.2023 · 3BB/AIS ปลาย 2023 · Celcom/Digi 2022) | เก็บแยกเพื่อให้เทียบก่อน/หลังควบรวมได้ · ยุบทีหลังได้ แต่แยกกลับไม่ได้ |
| **ip-api ถูกหรือผิดไม่อยู่ในขอบเขต** | ไม่มีเวลาก่อนเดดไลน์ · เคลมได้แค่ *"ทำซ้ำคำตอบ ip-api ณ วันหนึ่งได้ซื่อตรง"* **ห้าม**เคลมว่า *"แยก fixed/mobile ถูก"* |
| **SRS + Wilson CI ถอดออกจากสายการผลิต** | v2 มี label ครบ 100% แล้ว ไม่มีอะไรให้ประมาณ · เหลือไว้เป็น held-out validation |
| k=5 ครบทุกบล็อก | เจ้าของงานเลือกเอง |
| Ookla-Indonesia ไม่ต้องทำ | รุ่นพี่ทำแล้ว |

---

## 7. สถานะงาน (อัปเดต 29 ก.ค. 2026 — รอบที่สอง)

### ✅ เสร็จแล้วรอบนี้

| | |
|---|---|
| **notebook วิเคราะห์ 8 ประเทศ** | รัน v2 ครบแล้วทั้ง prep + eda · export 16 ไฟล์ · กราฟ ~238 ใบ |
| **เพิ่ม MY + ID** | เดิมมีแค่ 6 ประเทศ ตอนนี้ครบ 8 (สร้าง `indonesia_*`, `malaysia_*` ใหม่) |
| **ชุดที่ 2: ASN × quarter** | `scripts/build_isp_quarterly.py` → `data/exports/ndt7_isp_<c>_quarterly.csv` ครบ 8 |
| **จัดกลุ่ม ISP ด้วย `asn`** | EDA §17/§18 เลิกใช้ `isp` แล้ว (ตรวจแล้วไม่เหลือ `GROUP BY isp`) |

### 🔴 ยังเหลือ

| | |
|---|---|
| `notebooks/comparison/rq1_thresholds_ndt7.ipynb` · `rq2_trends.ipynb` | **เจ้าของงานสั่งตัดออกจากคิวรอบนี้** ยังถือ export เก่าอยู่ ถ้าจะรันต้องรันหลัง prep เสมอ |
| `notebooks/ndt7/mlab_server.ipynb` | ยังไม่ได้ re-run |
| `docs/paper_draft.md` | ยังเขียนว่าครอบคลุม 2 ประเทศ (จริง 8) |
| `docs/citations.md` | ยังไม่มีแหล่งของอินโด — ดู `data/reference/indonesia_reference_PROVENANCE.md` |
| `mlab_servers_server_id.csv` | ขาดประเทศเดียว |
| **Ookla ↔ NDT7 cross-validation** | ไม่เคยทำ · ยังเป็นสิ่งเดียวที่อุดจุดอ่อน "ไม่มี ground truth" ได้ |
| **`la`/`mm` parquet ถูก track ใน git** | ต้อง `git rm --cached` ถ้าจะ untrack (เพื่อนจะไม่ได้ไฟล์ตอน pull) — **ยังไม่ได้ตัดสินใจ** |
| **ยังไม่ commit อะไรเลย** | working changes เยอะมาก |

---

## 7.1 🚨 การตัดสินใจเชิงวิธีการรอบนี้ — ต้องเขียนในเปเปอร์

### ก. ตัด `n_tiles` ออกจากเกณฑ์ reliability ของ NDT7

เดิม `is_reliable = total_tests>=100 AND n_tiles>=5` (ยืมจาก Ookla) **ตอนนี้ NDT7 ใช้
`total_tests >= 100` อย่างเดียว · Ookla ยังใช้ทั้งคู่เหมือนเดิม ไม่แตะ**

**เหตุผล:** NDT7 ได้พิกัดจาก MaxMind ซึ่งเป็น **city centroid** ทุก test ในเมืองเดียวกันตกลง tile
เดียวกัน `n_tiles` จึงวัด "จังหวัดนี้มีกี่เมืองใน MaxMind" ไม่ได้วัดการกระจายตัวของข้อมูล

หลักฐาน: ลาวทั้งประเทศ 139,693 แถว มีพิกัดต่างกัน **33 จุด** · `n_tiles` สูงสุด = 3 → เกณฑ์ ≥5
เป็นไปไม่ได้ · เทียบ Ookla ลาว: มัธยฐาน `n_tiles` = **150** (ต่ำสุด 50) ผ่านเกณฑ์ 216/216
· และในข้อมูล NDT7 พอ test เพิ่ม 100 เท่า `n_tiles` ขยับจาก 1.00 → แค่ 1.22 แล้วตัน
**ไม่ใช่ปัญหาข้อมูลน้อย แต่เป็นเพดานของ geolocation**

**ผลก่อน→หลัง:** ลาว 0→61 · กัมพูชา 0→57 · พม่า 9→103 · เวียดนาม 203→779 · ไทย 564→1225
(ฝั่ง mobile ถูกกดหนักที่สุด — ไทย cellular ผ่านแค่ 56/475 ก่อนแก้)

### ข. ทุกประเทศเฉลี่ยจาก province/region ตรง ๆ (เลิก tile-binning สองชั้น)

**พิสูจน์แล้วว่าให้ผลเท่ากันเป๊ะ** — `Σ(mean_tile × tests)/Σ(tests)` = ค่าเฉลี่ยรวมต่อ test
(ทดสอบมาเลเซีย: ต่างกัน 0.000000000000 Mbps) การหารด้วยขนาดกลุ่มถูกคูณกลับด้วยน้ำหนักพอดี
→ tile-binning เป็น **no-op** ที่เหลือผลข้างเคียงอย่างเดียวคือ `HAVING COUNT(*)>=3` ทิ้ง test 0.04%

**ยังเทียบ Ookla ได้เหมือนเดิม** — Ookla ใช้ `np.average(avg_d_kbps, weights=tests)` ซึ่งเป็น
ตัวประมาณค่าเดียวกัน (Ookla ต้องเขียนแบบนั้นเพราะข้อมูลดิบเป็น tile ไม่มีราย test)

### ค. latency ใช้สูตรเดียวกันทั้ง 8 ประเทศ

`AVG(CASE WHEN min_rtt < 2000 THEN min_rtt END)` = **ตัดค่าขยะทิ้ง**
เดิม 6 ประเทศใช้ `LEAST(min_rtt, 2000)` = นับค่าขยะเป็น 2000 ส่วน PH/ID ตัดทิ้งอยู่แล้ว
(NDT7 มีค่า sentinel แบบ **4,294,967 ms** = 2³²/1000 ที่ขั้น clean ไม่ได้กรองออก เพราะกรองแค่
`min_rtt < 0` — เวียงจันทน์ 21 แถวดัน avg จาก 116 เป็น 539 ms)

> **Ookla ไม่มีขั้นตัด outlier นี้เลย** ต้องเขียนใน methodology ว่า NDT7 มีขั้นเพิ่ม

### ง. `n_tiles` ยังคำนวณอยู่ แต่เป็นคอลัมน์วินิจฉัยเท่านั้น

`COUNT(DISTINCT tile)` ในคิวรีเดียวกัน · ครบทั้ง 8 ประเทศแล้ว (เดิม PH/ID เป็น NaN)
ใช้แสดงในตาราง "Data Quality" ของ EDA ไม่ได้เอาไปตัดสินอะไร

### จ. จัดกลุ่ม ISP ด้วย `asn` เท่านั้น — ป้ายชื่อต้องต่อรหัส ASN

`operator`/`as_name` ใช้เป็นป้ายแสดงผล **แต่ต้องต่อ `(ASxxxxx)` ท้ายป้าย** เพราะ 1 แบรนด์มีหลาย ASN
(ไทย: True 2 · AIS 3 · NT 3 · 3BB 2) ถ้าป้ายซ้ำ แกน categorical ของ matplotlib จะยุบแท่งทับกัน
และ `ax.text` จะลอยออกนอกกรอบ — **เคยพลาดมาแล้ว**

HHI ต้องหารด้วยฐาน**ที่มีชื่อเท่านั้น** (เดิมหารด้วยยอดที่รวม `(unknown)` ทำให้ต่ำกว่าจริง:
ลาว 3423 → ที่ถูกคือ 3641)

---

## 7.2 ตัวเลข v2 ล่าสุด (หลังแก้ทั้งหมด)

province/region × quarter ที่ผ่านเกณฑ์ `total_tests >= 100`:

| ประเทศ | broadband | mobile | | ประเทศ | broadband | mobile |
|---|---|---|---|---|---|---|
| thailand | 872 | 353 | | philippines | 204 | 151 |
| vietnam | 698 | 81 | | malaysia | 165 | 69 |
| indonesia | 402 | 361 | | myanmar | 76 | 37 |
| | | | | laos | 37 | 24 |
| | | | | cambodia | 33 | 24 |

HHI ฝั่ง broadband (จัดกลุ่มด้วย asn): พม่า 703 · ไทย 1700 · กัมพูชา 1953 · อินโด 2666 ·
PH 2749 · VN 2793 · MY 3064 · **ลาว 3641**

**เดดไลน์:** abstract **31 ก.ค. 2026** · full paper **7 ส.ค. 2026**

---

## 8. Limitation ที่ต้องเขียนในเปเปอร์

1. **ไม่มี ground truth** — validate แค่ความสม่ำเสมอภายในของ ip-api
2. **นิยาม "mobile" อาจเปลี่ยน** — ที่ ip-api แก้รอบล่าสุดคือย้าย FWA/ดาวเทียม/ไฟเบอร์ไปเป็น fixed
3. **GADM 4.1 = ข้อมูลปี 2022** — อินโดได้ 34 จังหวัด ไม่ใช่ 38
4. **CGNAT** — unique IP ≠ unique user · สัดส่วน address ≠ สัดส่วน test
5. **ISP ทับกลุ่มกันได้** — ip-api ส่ง `mobile`/`hosting`/`proxy` เป็น boolean อิสระ 3 ตัว
   การแบ่ง 3 กลุ่มเป็นผลของกฎลำดับ (cellular ชนะ hosting เสมอ) ไม่ใช่ธรรมชาติของข้อมูล
6. **TH ใช้ขอบเขตคนละแหล่ง** และ v1 ของ TH เคยใช้ 9 category ไม่มี hosting —
   TH เพิ่งเทียบกับประเทศอื่นได้เป็นครั้งแรกใน v2

---

## 9. แผนที่ไฟล์

### ในโปรเจกต์นี้ (`E:/thailand-broadband-analysis/`)

```
data/ndt7/
  CLEANING_OVERVIEW.md  README_for_eda.md   ← เอกสารฉบับจริง (ในโฟลเดอร์ประเทศเป็น stub)
  <c>/mlab_<c>_clean.parquet                ← 8 ประเทศ · gitignored
  <c>/README.md                             ← เรื่องเฉพาะประเทศ + เลข sanity-check
data/reference/
  <country>_reference.csv                   ← ประชากร/GDP/tier ต่อจังหวัด
  indonesia_reference_PROVENANCE.md         ← ที่มา + ข้อควรระวัง 4 ข้อของอินโด
data/geo/
  <country>_provinces.geojson               ← geoBoundaries ADM1 (ODbL)
  gadm41_PHL_1.geojson                      ← GADM 81 จังหวัด · gitignored (ห้ามแจกต่อ)
data/exports/
  ndt7_<country>_province_quarterly.csv           ← ชุด 1: พื้นที่ (broadband)
  ndt7_mobile_<country>_province_quarterly.csv    ← ชุด 1: พื้นที่ (mobile)
  ndt7_<bb|mobile>_<country>_reliable_*.csv       ← เฉพาะที่ผ่านเกณฑ์
  ndt7_isp_<country>_quarterly.csv                ← ชุด 2: ASN x quarter
notebooks/ndt7/
  main/<country>_ndt7_prep.ipynb + _eda.ipynb     ← 8 ประเทศ · แบน ไม่มี subfolder
  archive/                                        ← ของเก่า ไม่ใช้แล้ว (รวม bkk district)
  mlab_server.ipynb
notebooks/comparison/  rq1_thresholds_*.ipynb · rq2_trends.ipynb  ← ยังไม่ re-run
scripts/
  run_nb.py                 ← รัน notebook (บังคับ kernel python3 เพราะ `datasci` ไม่ได้ลงทะเบียน)
  build_isp_quarterly.py    ← สร้างชุด 2 ทั้ง 8 ประเทศ
  build_idn_ref.py          ← สร้าง reference + geojson ของอินโด (มี assert ทุกขั้น)
```

### คำสั่งที่ใช้บ่อย

```bash
python scripts/run_nb.py notebooks/ndt7/main/laos_ndt7_prep.ipynb notebooks/ndt7/main/laos_eda.ipynb
python scripts/build_isp_quarterly.py            # ทุกประเทศ (หรือใส่ code เฉพาะ เช่น la kh)
```

### ต้นทาง read-only (`E:/ndt7/`) — ห้ามเขียนทับ

```
E:/ndt7/
data/
  <c>/mlab_<c>_clean.parquet     ← ต้นทางของที่ copy มา (la อยู่ใน lao/)
  labels/ip_label_<c>.parquet    ← label ต่อ address · artifact ตัวจริง
ip_fetch/srs/
  RESUME.md                      ← สถานะการ fetch
  asn_operator.csv               ← ASN → ชื่อแบรนด์ (79 แถว)
  patch_operator.py              ← อัปเดต operator โดยไม่ต้อง re-run
  analyze_blocks.py              ← สรุป probe เป็น verdict ต่อบล็อก
  build_ip_labels.py             ← แปะ label ให้ทุก address
  run_block_refetch.py           ← ตัวยิง ip-api
  block_verdict_<c>.csv          ← verdict ต่อบล็อก
docs/
  ndt7-pipeline-v2.md            ← วิธีการฉบับเต็ม + §5.7 v1 vs v2 (เขียนไว้ให้ใช้ในเปเปอร์)
  ndt7-pipeline.md               ← v1 · ขั้น clean/province/save ยังใช้ได้ ที่เปลี่ยนคือ label
  th-ndt7-pipeline.md            ← v1 ของไทย (คนละ pipeline)
notebooks/
  build_clean_nb.py              ← generator ของ clean notebook ทั้ง 8 ประเทศ
  <c>/mlab_<c>_clean_v2.ipynb    ← notebook ที่ generate แล้วและรันไปแล้ว
```

### คำสั่งที่ใช้บ่อย

สร้าง clean notebook ใหม่แล้วรัน:
```bash
cd E:/ndt7/notebooks && python build_clean_nb.py <country> && python run_nb.py <dir>/mlab_<c>_clean_v2.ipynb
```

อัปเดตชื่อแบรนด์หลังแก้ `asn_operator.csv`:
```bash
cd E:/ndt7/ip_fetch/srs && python patch_operator.py
```
