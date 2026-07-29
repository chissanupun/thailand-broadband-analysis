# ที่มาของ `indonesia_reference.csv` + `indonesia_provinces.geojson`

สร้างเมื่อ 29 ก.ค. 2026 · สร้างตามแบบของประเทศอื่นใน `data/reference/` และ `data/geo/`
**ต้องเพิ่มลง `docs/citations.md` ด้วย** (Process.md ระบุว่าไฟล์นั้นยังไม่อัปเดตให้ครบ 8 ประเทศ)

---

## แหล่งข้อมูล

| คอลัมน์ | แหล่ง | ปีข้อมูล |
|---|---|---|
| `province_en` | ชื่อที่ตรงกับ `province` ใน `mlab_id_clean.parquet` | — |
| `province_th` | ชื่ออังกฤษของ geoBoundaries (**ไม่มีชื่อไทย** ใส่ชื่ออังกฤษแทน) | — |
| `region` | กลุ่มเกาะตาม Wikipedia *Provinces of Indonesia* (Java, Sumatra, Kalimantan, Sulawesi, Lesser Sunda Islands, Maluku Islands, Western New Guinea) | — |
| `area_km2` | Wikipedia *Provinces of Indonesia* → BPS | ล่าสุด |
| `pop_2024` | Wikipedia *Provinces of Indonesia* → BPS | ⚠️ **mid-2025** ดูข้อ 1 |
| `density_per_km2` | คำนวณเอง = `pop / area` (ไม่ได้ลอกจาก Wikipedia เพราะต้องคิดใหม่หลังยุบปาปัว) | — |
| `gdp_per_capita_raw_2021` | Wikipedia *List of Indonesian provinces by GDP per capita* ตาราง **"2021 Per Capita"** → BPS · หน่วย **USD nominal** | 2021 ✅ |
| `gdp_per_capita_usd_ppp_2021` | ตารางเดียวกัน คอลัมน์ PPP Int$ | 2021 ✅ |
| `gdp_per_capita_thb_2021` | คำนวณเอง = `usd_ppp × 32` | 2021 ✅ |
| `internet_tier` | คำนวณเอง = ควอร์ไทล์ของ GDP per capita ดูข้อ 3 | 2021 |

**geojson:** geoBoundaries `gbOpen` IDN ADM1
- `boundaryYearRepresented`: **2017** · `boundarySource`: OpenStreetMap, Wambacher
- **License: Open Data Commons Open Database License (ODbL) 1.0** — ต้อง cite
- เติม field `name` เข้าไปเอง (ให้ตรงกับ `province_en`) เหมือนที่ประเทศอื่นทำ
- แหล่งเดียวกับที่ประเทศอื่นใช้ (ตรวจแล้วทุกไฟล์มี schema `shapeISO`/`shapeGroup`/`shapeType`)

---

## ⚠️ ข้อควรระวัง 4 ข้อ — ต้องเขียนในเปเปอร์

### 1. `pop_2024` เป็นตัวเลข **mid-2025** ไม่ใช่ 2024

Wikipedia/BPS ให้ประชากรล่าสุดเป็น mid-2025 ไม่มีชุด 2024 ให้ในหน้าเดียวกัน
**คงชื่อคอลัมน์เป็น `pop_2024` ไว้เพราะ notebook ทุกเล่มอ้างชื่อนี้** ถ้าเปลี่ยนชื่อโค้ดจะพัง
→ ถ้าจะรายงานตัวเลขประชากรอินโดในเปเปอร์ ต้องเขียนว่าเป็น mid-2025

### 2. ยุบ 38 จังหวัดกลับเป็น 34

อินโดแยกปาปัวเพิ่มเป็น 38 จังหวัดช่วงปี 2022–24 แต่:
- `mlab_id_clean.parquet` มี **34** (join ด้วย GADM 4.1 = ข้อมูลปี 2022)
- geoBoundaries ADM1 มี **34** (ปี 2017)
- ตาราง GRDP "2021 Per Capita" มี **34** ✅ ตรงกันพอดี

เลยยุบเฉพาะ `area_km2` กับ `pop` จากหน้า Provinces (ที่มี 38) กลับเป็น 34:
```
Papua      = Papua + South Papua + Central Papua + Highland Papua
West Papua = West Papua + Southwest Papua
```
**ผลคือ ประชากร/พื้นที่ของ Papua กับ West Papua เป็นขอบเขตปี 2022 แต่ประชากรเป็น mid-2025**
(คนที่อยู่ในพื้นที่เดิม รวมกันแล้ว) — สอดคล้องกันเชิงพื้นที่ ไม่ได้นับซ้ำหรือขาด

### 3. `internet_tier` เป็นควอร์ไทล์ GDP **ไม่มีการปรับมือแบบไทย**

ตรวจสอบวิธีของไทยแล้วพบว่า tier ≈ ควอร์ไทล์ของ GDP per capita — เรียงตาม GDP ล้วน ๆ
แล้วตัดตามขนาดกลุ่มเดิม **ตรงกับของจริง 79.2%** และการใส่ `density` เข้าไปช่วยทำให้**แย่ลง**
ทุกน้ำหนัก (79% → 71% → 61%) แปลว่า density ไม่ใช่ตัวปรับ

16 จังหวัดไทยที่ไม่ตรงเป็นการปรับด้วยมือตามความรู้เชิงพื้นที่ (นนทบุรี/ปทุมธานี/ภูเก็ต/เชียงใหม่
ถูกดันขึ้น · ฉะเชิงเทรา/ชุมพร/นครปฐม ถูกกดลง · ยะลา/อุดรฯ/หนองคาย/เลย ถูกกดลง)

**ของอินโดใช้ควอร์ไทล์ตรง ๆ ไม่ปรับมือ** เพราะไม่มีเกณฑ์การปรับที่เขียนไว้ที่ไหน
→ **tier ของอินโดกับของไทยจึงไม่ได้สร้างด้วยวิธีเดียวกันเป๊ะ** ห้ามเทียบ tier ข้ามประเทศตรง ๆ
ได้กลุ่มละ 9/8/8/9 จังหวัด (tier 1 = รวยสุด)

### 4. `internet_tier` กับ `gdp_per_capita` มีความสัมพันธ์กันเอง (collinear)

หัวข้อ 8.5 ใส่ทั้ง `log_gdp` และ `C(internet_tier)` ในโมเดลเดียวกัน — ในเมื่อ tier สร้างจาก GDP
โดยตรง สองตัวนี้จึงซ้ำข้อมูลกัน ค่า coefficient ที่ออกมาตีความแยกกันไม่ได้
**เรื่องนี้เป็นของเดิมอยู่แล้ว ไม่ได้เกิดจากอินโด** (ไทย/เวียดนาม/ฟิลิปปินส์ ก็มีปัญหาเดียวกัน)
แต่พออินโดใช้ควอร์ไทล์ตรง ๆ ความซ้ำจะยิ่งสมบูรณ์

---

## ตรวจสอบแล้ว

- ชื่อจังหวัด **34 ตัวตรงกันครบทั้ง 3 ทาง** — parquet ↔ reference ↔ geojson ไม่มีตกหล่น
- join กับ parquet จริง: **0 แถวที่ join ไม่ติด**
- sanity: จำนวน test ไล่ตาม tier อย่างสมเหตุสมผล
  (tier 1 = 121.5M · tier 2 = 84.7M · tier 3 = 72.5M · tier 4 = 52.5M)
- Java มี 6 จังหวัด แต่กิน test ไป 267M จาก 331M (81%) — JakartaRaya จังหวัดเดียว 124M

## สร้างซ้ำได้ด้วย

`scratchpad/build_idn_ref.py` (มี assert ตรวจทุกขั้น ถ้า Wikipedia เปลี่ยนโครงสร้างจะ fail ทันที
ไม่เขียนไฟล์ผิด ๆ ออกมา)
