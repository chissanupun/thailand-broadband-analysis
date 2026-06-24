# Dev Note — Internet Measurement

## Ookla Master Dataset (`data/ookla/processed/master_province_quarterly.parquet`)

**Shape:** 847 แถว (77 จังหวัด × 11 ไตรมาส)

| คอลัมน์                     | ความหมายแบบภาษาคน                                                                                            |
| --------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **name**                    | ชื่อจังหวัดภาษาอังกฤษ เช่น Bangkok, Chiang Mai                                                               |
| **province_th**             | ชื่อจังหวัดภาษาไทย เช่น กรุงเทพมหานคร, เชียงใหม่                                                             |
| **region**                  | ภูมิภาคที่จังหวัดนั้นอยู่ เช่น ภาคกลาง ภาคเหนือ ภาคอีสาน หรือกรุงเทพฯและปริมณฑล                              |
| **avg_d_mbps**              | ความเร็วอินเทอร์เน็ตขาเข้าหรือดาวน์โหลดเฉลี่ย (Mbps) ยิ่งมากยิ่งโหลดเว็บ ดู YouTube หรือดาวน์โหลดไฟล์ได้เร็ว |
| **avg_u_mbps**              | ความเร็วอินเทอร์เน็ตขาออกหรืออัปโหลดเฉลี่ย (Mbps) ยิ่งมากยิ่งส่งไฟล์ ไลฟ์สด หรือประชุมออนไลน์ได้ลื่น         |
| **avg_lat_ms_wt**           | ค่า Latency หรือความหน่วงเฉลี่ย (มิลลิวินาที) ยิ่งต่ำยิ่งดี เพราะข้อมูลตอบสนองเร็ว เหมาะกับเกมหรือวิดีโอคอล  |
| **total_tests**             | จำนวนครั้งที่มีการทดสอบความเร็วอินเทอร์เน็ต (Speedtest) ในจังหวัดนั้นช่วงไตรมาสนั้น                          |
| **total_devices**           | จำนวนอุปกรณ์ที่ไม่ซ้ำกันที่เข้ามาทดสอบ เช่น มือถือ คอมพิวเตอร์ แท็บเล็ต                                      |
| **n_tiles**                 | จำนวนพื้นที่ย่อย (tiles) ของ Ookla ที่ครอบคลุมจังหวัดนั้น ใช้บอกว่ามีการเก็บข้อมูลจากกี่บริเวณ               |
| **year**                    | ปีของข้อมูล เช่น 2023, 2024, 2025                                                                            |
| **quarter**                 | ไตรมาสของปี (1 = ม.ค.-มี.ค., 2 = เม.ย.-มิ.ย., 3 = ก.ค.-ก.ย., 4 = ต.ค.-ธ.ค.)                                  |
| **month**                   | เดือนเริ่มต้นของไตรมาส (1, 4, 7, 10)                                                                         |
| **period_start**            | วันที่เริ่มต้นของไตรมาส เช่น 2024-04-01                                                                      |
| **label**                   | ชื่อช่วงเวลาในรูปแบบอ่านง่าย เช่น "2024-Q2"                                                                  |
| **area_km2**                | พื้นที่ของจังหวัด หน่วยเป็นตารางกิโลเมตร                                                                     |
| **pop_2024**                | จำนวนประชากรของจังหวัด ณ สิ้นปี 2024                                                                         |
| **density_per_km2**         | ความหนาแน่นประชากร คือมีคนอาศัยกี่คนต่อ 1 ตารางกิโลเมตร ยิ่งมากยิ่งแออัด                                     |
| **gdp_per_capita_thb_2021** | GDP ต่อหัวของจังหวัดในปี 2021 (บาท/คน/ปี) ใช้ประมาณระดับเศรษฐกิจและรายได้เฉลี่ย                              |
| **internet_tier**           | ระดับคุณภาพอินเทอร์เน็ตที่ผู้วิจัยกำหนดไว้ 1–4 โดย **Tier 1 ดีที่สุด** และ Tier 4 ต่ำที่สุด                  |

---

## Ookla Notebook — Cell-by-Cell

### Cell 1 — ตั้งค่า path + โหลดแผนที่จังหวัด

```python
THAILAND_GEOJSON = '.../data/geo/thailand_provinces.geojson'
PROVINCE_COL = 'name'
perf_tiles_url = ".../data/ookla/raw/2023-Q1_performance_fixed_tiles.parquet"

thailand_provinces_gdf = gpd.read_file(THAILAND_GEOJSON).to_crs(4326)
state_bounds = thailand_provinces_gdf.total_bounds
```

**ทำอะไร:**
- กำหนด path ของไฟล์ 3 ตัว: แผนที่จังหวัด (GeoJSON), ชื่อ column ที่ระบุจังหวัด, และไฟล์ Ookla ไตรมาสแรก
- โหลด GeoJSON ขอบเขตจังหวัดไทยทั้ง 77 จังหวัดเข้า GeoDataFrame แล้ว convert ระบบพิกัดเป็น **EPSG:4326 (WGS84)** — ระบบเดียวกับ GPS / Ookla tiles
- `total_bounds` คือ bounding box รอบประเทศไทยทั้งหมด ได้ค่า `[min_lon, min_lat, max_lon, max_lat]`

**ทำไม:**
- Ookla raw data ครอบคลุมทั้งโลก (~6.3M tiles) — ถ้าโหลดทั้งหมดจะกินแรมมาก
- bounding box ใช้กรองเฉพาะ tiles ที่อยู่ในกรอบประเทศไทยก่อน (ทำใน Cell ถัดไป) ลดข้อมูลลงได้มาก

> **สั้นๆ:** โหลดแผนที่จังหวัดไทย → เอากรอบประเทศ → ใช้กรอง Ookla ให้เหลือแค่ tiles ในไทย ก่อน spatial join

---

### Cell 2 — เลือก metric ที่จะวิเคราะห์

```python
metric_name = 'avg_d_kbps'
```

**ทำอะไร:**
- กำหนดตัวแปรเก็บชื่อ column ที่จะใช้วิเคราะห์ — ในที่นี้คือ `avg_d_kbps` (ความเร็ว download เฉลี่ย หน่วย kbps)
- เป็น config ตัวเดียวที่ต้องเปลี่ยนถ้าอยากวิเคราะห์ metric อื่น เช่น `avg_u_kbps` (upload) หรือ `avg_lat_ms` (latency)

**ทำไม:**
- แทนที่จะ hard-code ชื่อ column กระจายไปทั่ว notebook → ตั้งชื่อไว้ที่เดียว แก้ที่เดียวได้เลย

> **สั้นๆ:** บอกว่า notebook นี้จะโฟกัสที่ download speed — เปลี่ยน 1 บรรทัดนี้ก็เปลี่ยน metric ได้ทั้ง notebook

---

### Cell 3 — สร้าง Bounding Box Filter

```python
bbox_filters = [('tile_y', '<=', state_bounds[3]), ('tile_y', '>=', state_bounds[1]),
                ('tile_x', '<=', state_bounds[2]), ('tile_x', '>=', state_bounds[0])]
```

**state_bounds คืออะไร:**
```
state_bounds = [min_lon, min_lat, max_lon, max_lat]
             =  [97.3,    5.6,    105.6,   20.5  ]
                  ↑        ↑        ↑        ↑
                west     south    east     north
                [0]      [1]      [2]      [3]
```

**filter แต่ละตัวหมายความว่า:**

| เงื่อนไข | ความหมาย |
|---|---|
| `tile_y >= state_bounds[1]` | lat ≥ 5.6°N → ไม่เอา tile ที่อยู่ใต้กว่าไทย |
| `tile_y <= state_bounds[3]` | lat ≤ 20.5°N → ไม่เอา tile ที่อยู่เหนือกว่าไทย |
| `tile_x >= state_bounds[0]` | lon ≥ 97.3°E → ไม่เอา tile ที่อยู่ตะวันตกกว่าไทย |
| `tile_x <= state_bounds[2]` | lon ≤ 105.6°E → ไม่เอา tile ที่อยู่ตะวันออกกว่าไทย |

**ทำไม:**
- filter นี้ไม่ได้รันใน Python — ส่งตรงให้ **PyArrow** (predicate pushdown) กรองตั้งแต่อ่านไฟล์เลย
- ไม่ต้องโหลด ~6M rows เข้า RAM ก่อนค่อยกรอง → ประหยัด RAM และเวลามาก

> **สั้นๆ:** สร้างกรอบสี่เหลี่ยมล้อมประเทศไทย แล้วบอก PyArrow ให้โหลดแค่ tiles ที่อยู่ในกรอบนี้ตั้งแต่แรก

---

### Cell 4 — แปลง tile coordinates → จุดบนแผนที่ + ล้าง null

```python
tiles_gdf = gpd.GeoDataFrame(
    tiles_df,
    geometry=gpd.points_from_xy(tiles_df.tile_x, tiles_df.tile_y),
    crs="EPSG:4326"
).drop(columns=["tile_x", "tile_y"])

tiles_gdf.dropna(subset=[metric_name], inplace=True)
```

**ทำอะไร:**

1. **แปลง tile_x, tile_y → Point geometry**
   ```
   ก่อน: tile_x=100.5, tile_y=13.7   (แค่ตัวเลข 2 column)
   หลัง: geometry=Point(100.5, 13.7) (จุดที่ geopandas ใช้ spatial join ได้)
   ```
   → drop `tile_x`, `tile_y` ทิ้ง เพราะข้อมูลถูกรวมเข้า geometry แล้ว

2. **drop แถวที่ metric เป็น null**
   - บาง tile ใน Ookla ไม่มีค่า download (`avg_d_kbps = NaN`)
   - ถ้าเอาไปทำ weighted average จะได้ผลผิด → ตัดออกก่อน

**ทำไม:**
- geopandas spatial join ต้องการ geometry column — ตัวเลข x,y ธรรมดาใช้ไม่ได้
- null ใน metric จะทำให้ `np.average(..., weights=...)` พัง

> **สั้นๆ:** เปลี่ยนพิกัด (x,y) เป็นจุดบนแผนที่ที่ geopandas เข้าใจ แล้วตัด tile ที่ไม่มีค่าความเร็วออก

---

### Cell 5 — Spatial Join: หาว่า tile ไหนอยู่จังหวัดไหน

```python
thailand_tiles_gdf = gpd.sjoin(
    tiles_gdf,
    thailand_provinces_gdf,
    how="inner",
    predicate="intersects"
)[[PROVINCE_COL, 'tests', metric_name]]
```

**ทำอะไร:**
- จับคู่ทุก tile (จุด) กับจังหวัด (polygon) — ถ้าจุดอยู่ในจังหวัดไหน ก็ได้ชื่อจังหวัดนั้นมา
- `how="inner"` → เอาแค่ tile ที่ match กับจังหวัดในไทย tile นอกไทยทิ้งหมด
- เอาแค่ 3 column: ชื่อจังหวัด, จำนวน tests, ค่าความเร็ว

**ทำไม bbox กรองไปแล้วยังต้อง inner join อีก:**
```
bbox = กรอบสี่เหลี่ยม → เกินขอบไทย มีบางส่วนของ พม่า/ลาว/กัมพูชา ติดมาด้วย
inner spatial join = ตัดที่เหลือออก เหลือแค่ tiles ที่อยู่ในขอบเขตจังหวัดไทยจริงๆ
```

**ผลลัพธ์:**
```
ก่อน: tiles_gdf → รู้แค่พิกัด (x,y) ไม่รู้ว่าอยู่จังหวัดไหน
หลัง: thailand_tiles_gdf → ทุก tile รู้แล้วว่าตัวเองอยู่จังหวัดไหน
```

> **สั้นๆ:** ถามว่า "tile นี้อยู่จังหวัดไหน" → ได้คำตอบทุก tile พร้อมตัดที่ไม่ใช่ไทยออก

---

### Cell 6 — Aggregate: คำนวณค่าเฉลี่ยความเร็วต่อจังหวัด

```python
province_stats = (
    thailand_tiles_gdf.groupby([PROVINCE_COL])
    .apply(lambda x: pd.Series({"avg_metric_wt": np.average(x[metric_name], weights=x["tests"])}))
    .reset_index()
)
province_stats['avg_metric_wt_mbps'] = province_stats['avg_metric_wt'] / 1000.0
province_data = thailand_provinces_gdf[[PROVINCE_COL, 'geometry']].merge(province_stats, on=PROVINCE_COL)
```

**ทำอะไร:**

**1. groupby + weighted average (ไม่ใช่ average ธรรมดา)**

| | tile A | tile B | ผลลัพธ์ |
|---|---|---|---|
| tests | 2 | 1,000 | — |
| ความเร็ว | 100 Mbps | 200 Mbps | — |
| average ธรรมดา | — | — | 150 Mbps ❌ |
| weighted average | — | — | ~199 Mbps ✅ |

tile ที่มีคนทดสอบเยอะกว่า → น้ำหนักมากกว่า → สะท้อนความจริงมากกว่า

**2. แปลง kbps → Mbps**
```
250,000 kbps ÷ 1000 = 250 Mbps  ← หน่วยที่คนอ่านออก
```

**3. re-merge geometry**
```
province_stats      = ชื่อจังหวัด + ความเร็ว  (ไม่มีรูปร่าง)
thailand_provinces  = ชื่อจังหวัด + polygon
          ↓ merge
province_data       = ชื่อ + ความเร็ว + polygon  → พร้อมพลอตแผนที่
```

> **สั้นๆ:** รวม tiles ทุกอันในจังหวัดเดียวกัน → ได้ความเร็วเฉลี่ยต่อจังหวัด 1 ค่า (ถ่วงน้ำหนักตามจำนวนคนทดสอบ) แล้วแปลงหน่วย + แนบ polygon เพื่อพลอตแผนที่

---

### Cell 7 — แบ่งกลุ่ม (bins) เพื่อพลอตแผนที่

```python
labels = ["0 to 50", "50 to 100", "100 to 200", "200 to 300", "300+"]
province_data['group'] = pd.cut(
    province_data['avg_metric_wt_mbps'],
    bins=(0, 50, 100, 200, 300, 10000),
    right=False,
    labels=labels
)
```

**ทำอะไร:**
- `pd.cut` แปลงค่าตัวเลขต่อเนื่อง → กลุ่ม (category)
  ```
  137 Mbps → "100 to 200"
  250 Mbps → "200 to 300"
  317 Mbps → "300+"
  ```

**`right=False`:**
```
[200, 300) → 200 รวม, 300 ไม่รวม
200 Mbps → "200 to 300" ✅
300 Mbps → "300+"        ✅

ถ้า right=True → 200 Mbps จะไปอยู่ "100 to 200" แทน ❌
```

**ทำไมต้องแบ่งกลุ่ม:**
- แผนที่ gradient สีต่อเนื่อง → ตาคนแยกยาก
- แบ่ง 5 กลุ่ม → สีแยกชัด → อ่านแผนที่ได้ทันที

> **สั้นๆ:** แปลงความเร็วเป็น 5 กลุ่มสี เพื่อพลอตแผนที่ให้อ่านง่าย

---

### Cell 8 — พลอตแผนที่ไทย (Choropleth Map)

```python
fig, ax = plt.subplots(1, figsize=(10, 8))
province_data.plot("group", ax=ax, legend=True, cmap="viridis",
                   legend_kwds={'title': "Avg Download (Mbps)", 'loc': 'lower right'})
ax.set_title("Weighted Average Fixed Broadband Download Speed by Province (2023 Q1)")
ax.set_axis_off()
plt.show()
```

**ทำอะไร:**

| บรรทัด | หมายถึง |
|---|---|
| `plt.subplots(1, figsize=(10,8))` | สร้างกรอบรูป ขนาด 10×8 นิ้ว |
| `.plot("group", ...)` | วาดแผนที่โดยระบายสีตาม column `group` |
| `cmap="viridis"` | palette: เหลือง = ช้า → เขียว → น้ำเงิน = เร็ว |
| `legend=True` | แสดง legend ว่าสีไหนคือ Mbps เท่าไร |
| `ax.set_axis_off()` | ซ่อน axis x,y — แผนที่ไม่ต้องการเส้นตาราง |

**output:** แผนที่ไทยระบายสีตามความเร็ว download ต่อจังหวัด (2023 Q1)

> **สั้นๆ:** เอา province_data ที่มีครบทั้งรูปร่างจังหวัด + กลุ่มสี → วาดแผนที่ choropleth ออกมา

---

## สรุป pipeline ทั้งหมด (Cell 1–8)

```
Cell 1  โหลดแผนที่จังหวัด → ได้กรอบประเทศไทย (bbox)
Cell 2  กำหนด metric = avg_d_kbps
Cell 3  สร้าง bbox_filters
Cell 4  โหลด Ookla parquet เฉพาะ tiles ในกรอบไทย
Cell 5  แปลง tile_x,tile_y → Point geometry + drop null
Cell 6  spatial join → ทุก tile รู้ว่าอยู่จังหวัดไหน
Cell 7  weighted average ต่อจังหวัด + kbps→Mbps + merge polygon
Cell 8  แบ่งกลุ่มสี
Cell 9  พลอตแผนที่
```

---

### Cell 9 — ดู Schema ของ Ookla Raw (ก่อนโหลดทั้งหมด)

```python
files = sorted([f for f in os.listdir(file_path) if f.endswith('.parquet')])
df = pd.read_parquet(os.path.join(file_path, files[0]), engine='pyarrow')
```

**จุดเปลี่ยน:** Cell 1–8 ทดสอบแค่ 1 ไฟล์ — Cell นี้เริ่มเตรียม Full EDA (11 ไตรมาส)

**ทำอะไร:**
- list ไฟล์ทั้งหมดใน raw/ → sort ให้เรียง 2023-Q1 → 2025-Q4
- โหลดแค่ไฟล์แรก (2023-Q1) เพื่อดู schema เท่านั้น

**ทำไมไม่โหลดทั้งหมดเลย:**
- 11 ไฟล์ รวมกัน ~3.7 GB → กิน RAM หมด
- schema ทุกไฟล์เหมือนกัน → ดูไฟล์เดียวพอ

> **สั้นๆ:** เช็ค schema ก่อน 1 ไฟล์ ไม่ได้โหลดทั้งหมด — Cell ถัดไปถึงจะ loop โหลดและ aggregate ทีละไตรมาส

---

### Cell 10 — โหลด Province Reference Data

```python
prov_ref = pd.read_csv(PROVINCE_REF_PATH)
prov_ref['gdp_per_capita_usd_2021'] = (prov_ref['gdp_per_capita_thb_2021'] / 31.0).round(0)
```

**ทำอะไร:**
- โหลด CSV ที่ผู้วิจัยรวบรวมเอง (ไม่ได้มาจาก Ookla) ประกอบด้วย: ประชากร, พื้นที่, ความหนาแน่น, GDP, internet_tier
- แปลง GDP จากบาท → USD (อัตรา 31 บาท/ดอลลาร์ ปี 2021) เพิ่มเป็น column ใหม่

**ทำไมต้องมี reference data แยก:**
- Ookla บอกแค่: tile อยู่ไหน + ความเร็วเท่าไร
- ไม่รู้ว่า: จังหวัดนี้ GDP เท่าไร คนเยอะแค่ไหน รวยหรือจน
- ต้อง merge prov_ref เข้ากับ Ookla เพื่อวิเคราะห์ว่า "ความเร็วสัมพันธ์กับ GDP / ความหนาแน่นประชากรไหม"

**print ท้าย cell:**
- ตรวจสอบว่าโหลดถูก — 77 จังหวัดครบ, region ถูกต้อง, ตัวเลขสมเหตุสมผล

> **สั้นๆ:** โหลดข้อมูลบริบทจังหวัด (GDP, ประชากร, tier) ที่ต้องใช้เปรียบเทียบกับความเร็ว Ookla

---

### Cell 11 — สรุป Reference Data ระดับภูมิภาค

```python
region_summary = prov_ref.groupby('region').agg(
    provinces=('province_en', 'count'),
    total_pop=('pop_2024', 'sum'),
    avg_density=('density_per_km2', 'mean'),
    avg_gdp_per_cap_thb=('gdp_per_capita_thb_2021', 'mean'),
    avg_gdp_per_cap_usd=('gdp_per_capita_usd_2021', 'mean'),
).sort_values('avg_gdp_per_cap_thb', ascending=False)
region_summary['total_pop_M'] = (region_summary['total_pop'] / 1e6).round(2)
```

**ทำอะไร:**
- groupby ภูมิภาค → สรุปตัวเลขรวม/เฉลี่ยต่อภูมิภาค
- `sort_values` เรียงจากภูมิภาคที่ GDP สูงสุด → ต่ำสุด
- `total_pop / 1e6` แปลง 5,000,000 → 5.0 (ล้านคน) อ่านง่ายขึ้น

**output ที่ได้:**
```
region               provinces  pop(M)  density  avg_gdp_thb
Bangkok & Vicinity       6       10.5    2,800     350,000
Eastern                  5        5.2      150     280,000
...
Northeastern            20       21.0       80      77,000
```

**ใช้ทำอะไร:** เป็น baseline ก่อน EDA — รู้ว่าภูมิภาคไหนรวย/จน/หนาแน่น เพื่อ interpret ผล Ookla ได้ถูกต้อง

> **สั้นๆ:** ดูภาพรวมก่อนว่าแต่ละภูมิภาคมีบริบทยังไง — ใช้เป็น reference ตอน interpret ความเร็วทีหลัง

---

### Cell 12 — พลอต GDP vs Density + GDP ต่อภูมิภาค

**กราฟซ้าย — Bubble Chart**

| element | หมายถึง |
|---|---|
| แกน x (log) | ความหนาแน่นประชากร (คน/km²) |
| แกน y | GDP ต่อหัว (พันบาท) |
| ขนาด bubble | ขนาดประชากรจังหวัด |
| สี | ภูมิภาค |
| annotate | label เฉพาะจังหวัดที่ GDP > 300k หรือจังหวัดที่น่าสนใจ |

**ทำไมแกน x ต้องเป็น log scale:**
```
BKK density = 5,000+ คน/km²
ชนบท        =    20  คน/km²
ต่างกัน 250× → linear scale ยุบทุกจังหวัดไปกองซ้าย อ่านไม่ออก
log scale    → กระจายสม่ำเสมอ อ่านออก
```

**กราฟขวา — Bar Chart GDP เฉลี่ยต่อภูมิภาค**
- เรียงจากน้อยสุด → มากสุด (ascending=True + barh)
- เส้นประดำ = ค่าเฉลี่ยประเทศ → ดูว่าภูมิภาคไหนสูง/ต่ำกว่าค่าเฉลี่ย

> **สั้นๆ:** visualize บริบทเศรษฐกิจ-ประชากร ก่อน EDA Ookla — ใช้ดูว่าจังหวัดไหนรวย/จน/หนาแน่นแค่ไหน เพื่อ interpret ความเร็วได้ถูกต้อง

---

### Cell 13 — แผนที่ Internet Tier (สมมติฐาน)

```python
geo_with_tier = thailand_gdf.merge(tier_map.rename(columns={'province_en':'name'}), on='name', how='left')
missing = geo_with_tier[geo_with_tier['internet_tier'].isna()]['name'].tolist()
geo_with_tier['tier_color'] = geo_with_tier['internet_tier'].map(tier_colors)
```

**ทำอะไร:**
- merge polygon จังหวัด + tier ที่ผู้วิจัยกำหนดเอง
- map tier → สี แล้วพลอตแผนที่

**tier_colors:**

| Tier | สี | หมายถึง |
|---|---|---|
| 1 | น้ำเงินเข้ม | คาดว่าเร็วสุด — BKK, EEC, ภูเก็ต |
| 2 | น้ำเงินกลาง | สูงกว่าค่าเฉลี่ย — เมืองท่องเที่ยว |
| 3 | ฟ้าอ่อน | ปานกลาง — เมืองจังหวัดทั่วไป |
| 4 | แดง | คาดว่าช้าสุด — อีสาน, ใต้ไกล, ชายแดน |

**`missing` check:**
- `how='left'` → ชื่อจังหวัดใน GeoJSON ≠ CSV → tier = NaN → จะเป็น lightgray บนแผนที่
- print ออกมาเพื่อรู้ว่าต้อง fix ชื่อไหน

**จุดประสงค์:**
- เป็น **สมมติฐาน** ก่อน EDA → "คาดว่าจังหวัดไหนจะเร็ว"
- หลัง EDA เปรียบเทียบว่า Ookla จริงๆ ตรงกับสมมติฐานไหม

> **สั้นๆ:** วาดแผนที่ tier ที่ตั้งสมมติฐานไว้ก่อน EDA — ใช้เปรียบเทียบกับผล Ookla จริงในภายหลัง

---

### Cell 14 — Top/Bottom 10 จังหวัดตาม GDP

```python
top10 = prov_ref.nlargest(10, 'gdp_per_capita_thb_2021')
bot10 = prov_ref.nsmallest(10, 'gdp_per_capita_thb_2021')
```

**ทำอะไร:** print ตารางจังหวัดที่รวยสุด 10 อันดับ และจนสุด 10 อันดับ

**ทำไม:**
- ตรวจสอบว่า tier ที่กำหนดสมเหตุสมผลไหม — ถ้า tier 4 โผล่ใน top 10 GDP แสดงว่า tier ผิด
- ใช้เป็น reference ตอน interpret ผล Ookla ว่า "จังหวัดรวยสุดได้เน็ตเร็วสุดไหม"

> **สั้นๆ:** sanity check tier + เตรียม context ก่อนเข้า EDA จริง

---

### Cell 15 — Build Master Dataset (loop ทุกไตรมาส) ⭐ Cell สำคัญสุด

```python
for fp in files:                          # loop 11 ไฟล์
    raw = pd.read_parquet(fp, columns=COLS, filters=bbox_filters)
    tiles_gdf = GeoDataFrame(... points_from_xy ...)
    joined = gpd.sjoin(tiles_gdf, thailand_gdf, how='inner', predicate='intersects')
    agg = joined.groupby('name').apply(weighted_average_per_province)
    records.append(agg)

master = pd.concat(records)               # รวมทุก quarter
master['avg_d_mbps'] = master['avg_d_kbps_wt'] / 1000   # kbps → Mbps
master = master.merge(prov_ref, on='name')               # แนบ GDP/ประชากร/tier
```

**pipeline เดิมแค่ทำซ้ำ 11 ครั้ง + เพิ่มสิ่งเหล่านี้:**

| สิ่งใหม่ | ทำไม |
|---|---|
| `COLS` = 7 columns | เพิ่ม `avg_u_kbps`, `avg_lat_ms`, `devices` — ไม่ได้วิเคราะห์แค่ DL แล้ว |
| `Q_TO_MONTH` | แปลง quarter → เดือน เพื่อสร้าง `period_start` datetime สำหรับกราฟ |
| `label = "2023-Q1"` | ใช้เป็น axis label |
| aggregate 6 metrics | DL, UL, latency, tests, devices, n_tiles ต่อจังหวัดต่อไตรมาส |
| merge prov_ref | master มีครบ: ความเร็ว + GDP + ประชากร + tier ใน table เดียว |

**output: `master` = 847 rows × 19 columns (77 จังหวัด × 11 ไตรมาส) — ใช้ทุก Cell ที่เหลือ**

> **สั้นๆ:** รัน pipeline (โหลด → กรอง → spatial join → aggregate) ซ้ำ 11 ครั้ง แล้วรวมออกมาเป็น master dataset ตัวเดียว

---

### Cell 16 — Data Quality Check

```python
# 1. นับ rows
expected = 77 * master['label'].nunique()  # 847

# 2. หา missing province-quarter
coverage_pivot = master.pivot_table(index='name', columns='label', values='total_tests')
missing_cells = [(p,q) for p in all_provinces for q in all_labels if NaN]

# 3. Low-test quarters
low_test = master[master['total_tests'] < 100]
```

**ตรวจ 3 อย่างก่อน EDA:**

| เช็ค | ถ้าผิดปกติหมายถึง |
|---|---|
| Actual rows = 847 | ครบ — ถ้าน้อยกว่า = บางจังหวัดหายไปบางไตรมาส |
| missing_cells | จังหวัด-ไตรมาสที่ไม่มี Ookla tile เลย |
| total_tests < 100 | มีข้อมูลแต่น้อยมาก → weighted average ไม่น่าเชื่อถือ → จะ flag เป็น LOW_COVERAGE ทีหลัง |

**ทำไมต้องเช็คก่อน EDA:**
- ไม่รู้ว่ามีรู → interpret กราฟผิดได้
- เช่น จังหวัดที่หายไป 1 ไตรมาส → growth chart เบี้ยว

> **สั้นๆ:** ตรวจความสมบูรณ์ของ master ก่อน — 847 rows ครบไหม มีรูโหว่ไหม ข้อมูลน้อยเกินไปไหม

---

### Cell 17 — Distribution ของทุก Metric (Histogram × 3)

```python
fig, axes = plt.subplots(1, 3, ...)
axes[0].hist(master['avg_d_mbps'], bins=60)   # download
axes[1].hist(master['avg_u_mbps'], bins=60)   # upload
axes[2].hist(master['avg_lat_ms_wt'], bins=60) # latency
# เส้นประ = median แต่ละ metric
print(master[...].describe())
```

**ทำอะไร:** ดูการกระจายตัวของทุก metric ในทุก province-quarter combos (847 จุด)

**`bins=60`:** แบ่งช่วงค่าออก 60 ช่อง — น้อยเกินไป = กราฟหยาบ, มากเกินไป = ขรุขระ

**เส้นประ = median (ไม่ใช่ mean):**
- outlier ดึง mean ให้เบี้ยวได้ → median บอกจุดกึ่งกลางที่แท้จริงกว่า

**`describe()` ท้าย cell:**
- ได้ min, max, mean, std, 25/50/75 percentile
- ใช้ตรวจว่ามี outlier สุดโต่งไหม เช่น latency 225ms

> **สั้นๆ:** EDA ขั้นแรก — ดูว่าข้อมูลกระจายตัวยังไง ก่อนแยก analyze ทีละจังหวัด/ภูมิภาค

---

### Cell 18 — Province Ranking Bar Chart → `01_province_ranking.png`

```python
prov_mean = master.groupby(['name','region']).agg(
    mean_dl=('avg_d_mbps','mean'), ...
).sort_values('mean_dl', ascending=True)

ax.barh(prov_mean['name'], prov_mean['mean_dl'], color=colors)
ax.axvline(national_mean, ls='--')
```

**`prov_mean` — เฉลี่ยข้าม 11 ไตรมาส:**
```
master (847 rows) → groupby จังหวัด → mean ทุก quarter → 77 rows
Bangkok: (290+295+...+310)/11 = ~300 Mbps
```

**`barh` = horizontal bar:**
- `ascending=True` → ช้าสุดล่าง เร็วสุดบน
- สีแท่ง = ภูมิภาค
- ตัวเลขข้างแท่ง = ค่า Mbps จริง (วาดด้วย `ax.text`)
- เส้นประดำ = ค่าเฉลี่ยประเทศ

> **สั้นๆ:** เฉลี่ยความเร็ว 11 ไตรมาสต่อจังหวัด → เรียง → วาด bar chart แนวนอน เห็นทันทีว่าจังหวัดไหนเร็ว/ช้าสุด

---

### Cell 19 — Heatmap Province × Quarter → `02_heatmap.png`

```python
pivot_dl = master.pivot_table(index='name', columns='period_start', values='avg_d_mbps')
# แปลง column เป็น "2023-Q1", "2023-Q2" ...
pivot_dl.columns = [strftime + quarter_number]
# เรียงจังหวัดตาม mean_dl (เร็วสุดบน)
pivot_dl = pivot_dl.loc[prov_mean.sort_values('mean_dl', ascending=False)['name']]

ax.imshow(pivot_dl.values, cmap='YlOrRd')
```

**`pivot_table` — long → wide:**
```
master (long 847 rows):       pivot_dl (wide 77×11):
name     | quarter | speed    name      | Q1  | Q2  | ...
Bangkok  | 2023-Q1 | 290  →   Bangkok   | 290 | 295 | ...
Bangkok  | 2023-Q2 | 295      Chiang Mai| 240 | ... | ...
```

**แปลง column label:**
```python
(month - 1) // 3 + 1
# เดือน 1 → Q1 | เดือน 4 → Q2 | เดือน 7 → Q3 | เดือน 10 → Q4
```

**`imshow` แทน plot:**
- รับ matrix ตัวเลข 77×11 → ระบายสีตามค่า
- `cmap='YlOrRd'` → เหลือง = ช้า, แดง = เร็ว

> **สั้นๆ:** แปลงข้อมูลเป็นตาราง 77×11 แล้วระบายสีตามความเร็ว → เห็นทั้ง ranking และ trend ตามเวลาในรูปเดียว

---

### Cell 20 — Regional Boxplot → `03_regional_boxplot.png`

```python
for ax, metric, label, color_key in [(axes[0],'avg_d_mbps',...), (axes[1],'avg_u_mbps',...), (axes[2],'avg_lat_ms_wt',...)]:
    data = [master[master['region']==r][metric].dropna().values for r in region_order]
    ax.boxplot(data, patch_artist=True, ...)
```

**boxplot อ่านยังไง:**
```
    ┌─────┐
────┤     ├────────○   ← outlier
    └─────┘
↑   ↑  ↑  ↑   ↑
min Q1 med Q3 max
     └─────┘
     IQR = 50% กลางของข้อมูล
```
- เส้นขาวกลางกล่อง = median
- กล่องกว้าง = ค่ากระจายเยอะ (จังหวัดในภูมิภาคไม่เท่ากัน)
- จุด ○ = outlier (ไกลจาก IQR มาก)

**data ต่อ 1 กล่อง:**
- ทุก province-quarter combo ในภูมิภาคนั้น
- Bangkok (6 จังหวัด × 11 ไตรมาส = 66 จุด) ต่อ 1 กล่อง

**loop 3 รอบ:** วาด boxplot เดิมซ้ำสำหรับ download / upload / latency แทนที่จะ copy code 3 รอบ

> **สั้นๆ:** เปรียบเทียบ distribution ความเร็วต่อภูมิภาค — เห็นทั้ง median, ความแปรปรวน และ outlier ในรูปเดียว

---

### Cell 21 — Time Series Trend (Top / Bottom / Hubs)

```python
groups = [
    ('Top 5 Fastest',        [...]),
    ('Bottom 5 Slowest',     [...]),
    ('Major Provincial Hubs',[...]),
]
for ax, (title, provinces, color) in zip(axes, groups):
    for prov in provinces:
        df_p = master[master['name']==prov].sort_values('label')
        ax.plot(df_p['period_start'], df_p['avg_d_mbps'], marker='o')
```

**ทำอะไร:** วาด line chart ความเร็ว download ตามเวลา แยก 3 กลุ่ม

**`sharex=True`:** ทั้ง 3 กราฟใช้แกน x เดียวกัน → เปรียบเทียบ trend ช่วงเวลาเดียวกันได้ทันที

**แต่ละเส้น = 1 จังหวัด** — x = ไตรมาส, y = ความเร็ว Mbps, จุด marker = 1 ไตรมาส

**ทำไมแบ่ง 3 กลุ่ม:**
- Top vs Bottom → เห็นว่า gap ขยายหรือแคบลงตามเวลา
- Provincial Hubs → เมืองใหญ่ที่น่าสนใจแต่ไม่ได้ top/bottom (ภูเก็ต เชียงใหม่ ขอนแก่น)

> **สั้นๆ:** ดู trend 11 ไตรมาสของจังหวัดที่เลือก — เห็นว่าเร็วขึ้น/ช้าลง/คงที่ และ gap ระหว่าง top กับ bottom เปลี่ยนยังไง

---

### Cell 22 — GDP & Density vs Speed (OLS Correlation) → `07_gdp_vs_speed.png`

```python
# กราฟซ้าย: GDP vs download (linear)
slope, intercept, r, p, _ = stats.linregress(x, y)

# กราฟขวา: log(density) vs download
s2,i2,r2,p2,_ = stats.linregress(np.log1p(x2), y2)
```

**ทำอะไร:** ทดสอบว่า "รวยกว่า/หนาแน่นกว่า = เน็ตเร็วกว่า" จริงไหม

**OLS คืออะไร:**
```
หาเส้นตรงที่ fit ข้อมูลได้ดีสุด
r    = ความสัมพันธ์ (-1 ถึง 1)
r²   = % ที่ตัวแปรนั้นอธิบายความเร็วได้
p    = นัยสำคัญทางสถิติ (p < 0.05 = ไม่ใช่แค่บังเอิญ)
```

**ทำไมกราฟขวาใช้ `log1p(density)` ไม่ใช่ density ตรงๆ:**
- density BKK 5,000+ vs ชนบท 20 → ต่างกัน 250× → linear ไม่ fit
- log ทำให้ความสัมพันธ์เป็นเส้นตรงมากขึ้น

**ผลสำคัญ (r=0.47, p<0.001):**
- GDP อธิบายความเร็วได้แค่ ~22% (r²=0.22)
- จังหวัดจนหลายอันได้เน็ตเร็วกว่าที่ GDP คาด → หลักฐานว่า FTTH rollout ทั่วถึง ไม่ได้กระจุกแค่จังหวัดรวย

> **สั้นๆ:** ทดสอบ GDP/density vs ความเร็ว — r=0.47 หมายถึงสัมพันธ์กันอ่อนๆ เท่านั้น → FTTH บีบ gap ลงได้มากกว่าที่ GDP จะบอก

**Pearson r คืออะไร:**
```
วัดว่าตัวแปร 2 ตัวเดินไปด้วยกันแค่ไหน ช่วง -1.0 ถึง +1.0

r = +1.0 → ขึ้นพร้อมกันสมบูรณ์
r =  0.0 → ไม่สัมพันธ์กันเลย
r = -1.0 → ตรงข้ามกันสมบูรณ์

0.0–0.3 = อ่อนมาก | 0.3–0.5 = อ่อน | 0.5–0.7 = ปานกลาง | 0.7+ = แรง
```

**ผลจริงจากกราฟ:**
- `r(GDP) = 0.475` → สัมพันธ์อ่อน — รวยกว่าเน็ตเร็วกว่านิดหน่อย แต่ไม่เสมอไป
- `r(density) = 0.629` → ปานกลาง — density ทำนายความเร็วได้ดีกว่า GDP

**outlier น่าสนใจจากกราฟ:**

| จังหวัด | สิ่งผิดปกติ |
|---|---|
| Rayong | GDP สูงสุด (~900k) แต่ความเร็วแค่ ~280 Mbps — รวยเพราะโรงงาน ไม่ใช่คนอยู่เยอะ ISP ไม่มีแรงจูงใจวางไฟเบอร์ dense |
| Nonthaburi/Pathum Thani | เร็วที่สุด (~310+ Mbps) แต่ GDP ไม่ได้สูงสุด |
| Phuket | density ปานกลาง แต่เร็วแค่ ~225 Mbps — เกาะ วางสาย fiber ยาก |
| Bangkok Metropolis | GDP + density สูงมาก แต่ไม่ได้เร็วที่สุด — ตึกเก่า สายเก่า |

---

### Cell 23 — UL/DL Ratio: หลักฐาน FTTH

```python
master['ul_dl_ratio'] = master['avg_u_mbps'] / master['avg_d_mbps']
ratio_mean = master.groupby('name')['ul_dl_ratio'].mean()
weird_ratio = ratio_mean[ratio_mean['ul_dl_ratio'] > 0.8]
```

**UL/DL ratio บอกอะไร:**
```
FTTH/GPON (ไฟเบอร์): ratio ≈ 0.9–1.0  ← upload เกือบเท่า download
HFC Cable:           ratio ≈ 0.2–0.5
ADSL:                ratio ≈ 0.1–0.2

ยิ่งใกล้ 1.0 = ยิ่งน่าจะเป็นไฟเบอร์
```

**เส้น 2 เส้นบนกราฟ:**
- เส้นแดงประ (1.0) = symmetric สมบูรณ์ upload = download
- เส้นดำจุด (~0.85) = ค่าเฉลี่ยประเทศ

**`weird_ratio > 0.8`:** จังหวัดที่ ratio สูงมาก = น่าจะใช้ไฟเบอร์แล้ว — ถ้าส่วนใหญ่เกิน 0.8 = หลักฐานว่า FTTH ทั่วถึงแล้วทั้งประเทศ

**ทำไมสำคัญ:** ใช้ยืนยัน hypothesis ว่า "ความเหลื่อมล้ำด้านเน็ตแคบลงเพราะ FTTH ขยายทั่วประเทศ ไม่ได้กระจุกแค่จังหวัดรวย"

> **สั้นๆ:** upload÷download ratio → ใช้เป็น proxy ว่าจังหวัดนั้น "ได้ไฟเบอร์แล้ว" หรือยัง — ค่าเฉลี่ยประเทศ ~0.85 = หลักฐาน FTTH กระจายทั่วถึง

---

### Cell 24 — Anomaly Detection (7 Flags) ⭐

```python
flags = {}  # { ชื่อจังหวัด: [list ของ flags] }
# แต่ละ flag: flags.setdefault(name, []).append(...)
```

**7 flags ที่ตรวจ:**

---

**A — LOW_COVERAGE**
- **วัดจาก:** `total_tests < 200` ในไตรมาสใดก็ตาม
- **ภาษาคน:** จังหวัดนี้มีคนกด Speedtest น้อยมากในบางไตรมาส → ค่าความเร็วอาจไม่ตรงความจริง ตัวอย่างน้อยเกินไป

---

**B — TIER1_UNDERPERFORM**
- **วัดจาก:** จังหวัด Tier 1 มี mean_dl ต่ำกว่า median ของจังหวัด Tier 3
- **ภาษาคน:** จังหวัดที่เราคาดว่าจะเร็วที่สุด (BKK, ชลบุรี ฯลฯ) แต่ผล Ookla จริงกลับช้ากว่าจังหวัดระดับกลาง — ผิดคาดมาก

---

**B — TIER4_OVERPERFORM**
- **วัดจาก:** จังหวัด Tier 4 มี mean_dl สูงกว่า median Tier 2 + 0.5×std ของประเทศ
- **ภาษาคน:** จังหวัดที่เราคาดว่าจะช้าที่สุด (อีสาน ชายแดน ฯลฯ) แต่กลับเร็วกว่าจังหวัดระดับดีกว่าอย่างชัดเจน — น่าแปลกใจ

---

**C — QoQ_SPIKE**
- **วัดจาก:** ความเร็วเปลี่ยนแปลง >50% ระหว่าง 2 ไตรมาสติดกัน `|dl[i] - dl[i-1]| / dl[i-1] > 0.50`
- **ภาษาคน:** ความเร็วกระโดดขึ้นหรือลงมากผิดปกติ เช่น Q1=200 Mbps แต่ Q2=320 Mbps — อาจมีการอัพเกรดสายหรือ data noise

---

**D — HIGH/LOW_UL_DL_RATIO**
- **วัดจาก:** z-score ของ ul_dl_ratio > +2.0 (สูงผิดปกติ) หรือ < -2.0 (ต่ำผิดปกติ) เทียบกับค่าเฉลี่ยประเทศ
- **ภาษาคน:** upload÷download ของจังหวัดนี้ผิดปกติมากเมื่อเทียบกับจังหวัดอื่นทั้งประเทศ — อาจใช้เทคโนโลยีต่างกัน หรือมี server พิเศษในพื้นที่

---

**E — REGIONAL_OUTLIER**
- **วัดจาก:** z-score ของ mean_dl > ±2.5 เมื่อเทียบกับจังหวัดอื่นในภูมิภาคเดียวกัน
- **ภาษาคน:** จังหวัดนี้เร็วหรือช้าผิดปกติมากเมื่อเทียบกับเพื่อนบ้านภูมิภาคเดียวกัน — ไม่ใช่แค่ต่ำกว่าค่าเฉลี่ยประเทศ แต่ผิดปกติในบริบทภูมิภาคด้วย

---

**F — ULTRA_LOW_LATENCY**
- **วัดจาก:** `mean_lat < 6 ms`
- **ภาษาคน:** latency ต่ำผิดปกติมาก (เน็ตบ้านไทยปกติควร 8–15ms อย่างน้อย) — แสดงว่า Ookla มี test server อยู่ใน datacenter ISP ในจังหวัดนั้นพอดี ทำให้ตัวเลขดีเกินจริง ไม่ใช่ความเร็วที่ผู้ใช้ทั่วไปจะได้รับ

---

**G — RAPID_GROWTH**
- **วัดจาก:** `(speed_2025Q4 - speed_2023Q1) / speed_2023Q1 > 0.35`
- **ภาษาคน:** ความเร็วเพิ่มขึ้นมากกว่า 35% ใน 3 ปี — แสดงว่ามีการวางสาย fiber ใหม่หรืออัพเกรด infrastructure ชัดเจนในช่วงนี้

---

**z-score คืออะไร:**
```
z = (ค่าจังหวัดนี้ - ค่าเฉลี่ย) ÷ ส่วนเบี่ยงเบนมาตรฐาน

z =  0.0 → ปกติ อยู่ตรงกลาง
z = +2.0 → สูงกว่าค่าเฉลี่ย 2 ช่วง = ผิดปกติพอที่จะ flag
z = -2.5 → ต่ำกว่าค่าเฉลี่ย 2.5 ช่วง = ผิดปกติชัดเจน
```

**output:** `flags` dict — จังหวัดที่มีหลาย flag = น่าสนใจที่สุด ใช้ใน deep dive Cell ถัดไป

> **สั้นๆ:** ตรวจหาจังหวัด "ผิดปกติ" 7 วิธีพร้อมกัน — ยิ่งมีหลาย flag ยิ่งน่าขุดลึก

---

### Cell 25 — Anomaly Map → `04_anomaly_map.png`

```python
geo_flags.plot('mean_dl', cmap='YlGnBu')        # layer 1: speed choropleth
geo_flagged.boundary.plot(color='red', lw=1.5)  # layer 2: ขอบแดงจังหวัด flagged
ax.annotate(f"{name}\n({flag_count}⚑)", xy=centroid)  # label
```

**2 layer บนแผนที่เดียว:**

| Layer | ทำอะไร |
|---|---|
| Base (YlGnBu) | ระบายสีตาม mean download — เหลือง=ช้า, น้ำเงิน=เร็ว |
| Overlay (red) | ขอบแดง + label เฉพาะจังหวัดที่มี flag |

**`.boundary.plot()`:** เอาแค่เส้นขอบ ไม่ fill → เห็น speed color ด้านล่างได้

**`map(flag_counts).fillna(0)`:** แปลงชื่อจังหวัด → จำนวน flags, จังหวัดที่ไม่มี flag = 0

**centroid:** จุดกึ่งกลาง polygon ของจังหวัด — ใช้เป็น xy สำหรับวาง label

> **สั้นๆ:** แผนที่ speed + ขอบแดงจังหวัดผิดปกติ — เห็นทั้งว่าเร็ว/ช้าและ flagged ในรูปเดียว

---

### Cell 26 — Full Province Summary Table

```python
summary = prov_mean + prov_ref + flag_counts + high_ratio
summary.sort_values('mean_dl', ascending=False)
print(summary[['name','region','tier','mean_dl','mean_ul','mean_lat','ul_dl_ratio','mean_tests','gdp','flag_count']])
```

**ทำอะไร:** merge ทุกอย่างที่คำนวณมาตลอด notebook เข้าตารางเดียว แล้ว print ครบ 77 จังหวัด

**ทำไมต้องมี:**
- ดูภาพรวมทุกจังหวัดในที่เดียวก่อน deep dive
- ตรวจว่า flag / ratio / GDP / tier สอดคล้องกัน
- ใช้อ้างอิงตอนเขียน paper ว่า "จังหวัด X มีค่า Y"

> **สั้นๆ:** ตารางสรุปปิดท้าย EDA — ทุก metric ทุกจังหวัดในที่เดียว

---

### Cell 27 — UL/DL Symmetry: หลักฐาน Nationwide Fiber

```python
axes[0].barh(ratio_sorted['name'], ratio_sorted['mean_ratio'])   # bar chart ratio ต่อจังหวัด
axes[1].scatter(density, ratio, ...)                              # density vs ratio
```

**กราฟซ้าย:** bar chart ratio ทุกจังหวัด — ดูว่าส่วนใหญ่เกิน 0.8 (ไฟเบอร์) ไหม

**กราฟขวา — สิ่งที่น่าสนใจสุด (density vs ratio):**
```
สมมติฐาน: เมืองหนาแน่น → ได้ไฟเบอร์ก่อน → ratio สูงกว่า

แต่ผลจริง: BKK ratio ต่ำกว่าชนบทบางจังหวัด

เหตุผล:
BKK    = ตึกเก่า 30-50 ปี ยังใช้สายเดิม + mix HFC/ADSL
ชนบท   = วางไฟเบอร์ใหม่ตั้งแต่ต้น ไม่มี legacy infrastructure
→ ชนบทบางจังหวัด ratio สูงกว่า BKK
```

**print ท้าย cell:**
- นับจังหวัดที่ ratio > 0.80 และ > 0.90
- เปรียบ BKK min ratio vs Northeastern max ratio
- ถ้า Northeastern max > BKK min = พิสูจน์ว่าชนบทบางจังหวัดได้ไฟเบอร์ดีกว่า BKK

> **สั้นๆ:** พิสูจน์ว่าไทยใช้ไฟเบอร์แพร่หลายแล้ว และพบ pattern ผิดคาด — ชนบทที่วางสายใหม่ ratio สูงกว่า BKK ที่ยังมี legacy infra ปนอยู่

> ⚠️ **ข้อจำกัด:** UL/DL ratio เป็นแค่ indirect proxy — Ookla ไม่มีข้อมูลว่าแต่ละการทดสอบใช้ fiber/cable/ADSL หรือบ้าน/มือถือ การสรุปว่า "จังหวัดนี้ใช้ FTTH" จึงเป็นการอนุมานจาก ratio เท่านั้น ไม่ใช่หลักฐานตรง ควรระบุใน paper ว่าเป็น "indirect evidence"

---

### Cell 28 — Growth Chart 2023-Q1 → 2025-Q4 → `06_growth_chart.png`

```python
growth = ((last - first) / first * 100)
# % เปลี่ยนแปลงตลอด 3 ปี
```

**ทำอะไร:** วัดว่าแต่ละจังหวัดความเร็วเพิ่มขึ้นกี่ % จากต้นปี 2023 ถึงปลายปี 2025

**2 เส้นบนกราฟ:**
- เส้นดำ (0%) = ไม่เปลี่ยนแปลง — จังหวัดซ้ายเส้นนี้ = ช้าลง
- เส้นแดง = ค่าเฉลี่ยการเติบโตของประเทศ — จังหวัดขวาเส้น = โตเร็วกว่าค่าเฉลี่ย

**pattern ที่คาดว่าจะเห็น:**
- Tier 4 (ชนบท) โตเร็วกว่า Tier 1 — Tier 1 ถึงเพดานแล้ว ชนบทเพิ่งได้ไฟเบอร์
- จังหวัดโตช้า = baseline สูงอยู่แล้ว หรือมีปัญหา infrastructure

**`f'{val:+.0f}%'`:** format บังคับแสดง sign → `+50%` หรือ `-5%` เห็นชัดว่าบวกหรือลบ

> **สั้นๆ:** เปรียบเทียบความเร็วปี 2023 vs 2025 ต่อจังหวัด — เห็นว่าใครโตเร็ว ใครหยุดนิ่ง และใครช้าลง

---

### Cell 29 — Deep Dive: 5 จังหวัดผิดปกติ → `05_deep_dive_weird.png`

```python
WEIRD = {
    'Mae Hong Son':             'ภูเขา/ชายแดน ช้าสุดในภาคเหนือ',
    'Satun':                    'เกาะ ภูมิศาสตร์จำกัด',
    'Ubon Ratchathani':         'Tier 4 แต่เร็วผิดคาด',
    'Phra Nakhon Si Ayutthaya': 'latency 5ms ต่ำผิดปกติ — Ookla server ใกล้ ISP DC',
    'Phuket':                   'Tier 1 แต่ช้าปี 2023 → ตามทัน 2025',
}
```

**ต่อ 1 จังหวัด วาด 2 กราฟ:**

| กราฟ | แสดง |
|---|---|
| ซ้าย | Download + Upload trend ตลอด 11 ไตรมาส |
| ขวา | Latency trend ตลอด 11 ไตรมาส |

**`fill_between`:** แรเงาใต้ line — ไม่ได้เพิ่มข้อมูลใหม่ แค่ทำให้เห็น magnitude ชัดขึ้น

**ทำไมเลือก 5 จังหวัดนี้:** แต่ละคนผิดปกติคนละแบบ ครอบคลุม flag type สำคัญ — ใช้เป็น case study ในบท Discussion ของ paper

> **สั้นๆ:** zoom เข้าดู 5 จังหวัดที่ผิดปกติที่สุด เห็น trend ทั้ง speed และ latency ตลอด 3 ปี

---

### Cell 30 — Setup Weirdness EDA (self-contained) ⭐ จุดเปลี่ยน section

```python
if 'master' not in dir() or master is None:
    master = pd.read_parquet(...)   # โหลดถ้ายังไม่มีใน memory

weird_df = master.groupby(['name','region']).agg(mean_dl, mean_ul, mean_lat, mean_tests)
temp_std = master.groupby('name')['avg_d_mbps'].std()
weird_df['cv_dl'] = weird_df['std_dl'] / weird_df['mean_dl']
weird_df['tests_per_1000_pop'] = mean_tests / pop_2024 * 1000
```

**ทำไม section นี้ไม่ใช้ `prov_mean` จาก cell ก่อน:**
- section นี้ออกแบบให้ run standalone ได้ — guard clause โหลดข้อมูลเองถ้าไม่มี

**2 column ใหม่ที่ไม่มีใน prov_mean:**

| Column | คำนวณจาก | หมายถึง |
|---|---|---|
| `std_dl` | std ของ download 11 ไตรมาส | ความสม่ำเสมอของความเร็ว |
| `cv_dl` | std_dl ÷ mean_dl | % ความแปรปรวน — สูง = ขึ้นๆลงๆผิดปกติ |
| `tests_per_1000_pop` | mean_tests ÷ pop × 1,000 | proxy ของ penetration rate + tech-savviness |

> **สั้นๆ:** สร้าง `weird_df` ใหม่ที่มี metric พิเศษสำหรับวิเคราะห์ความ "ผิดปกติ" โดยเฉพาะ — self-contained รัน standalone ได้

---

### Cell 31 — Composite Weirdness Score (7 Dimensions)

```python
weirdness_score = |tier_z| + |gdp_z| + |den_z| + |regional_z| + |ratio_z| + |lat_z| + |coverage_z|
```

**แนวคิด:** ไม่ได้วัดว่าเร็ว/ช้า แต่วัดว่า "ผิดคาดมากแค่ไหน" จาก 7 มุมพร้อมกัน

| Dim | วัดอะไร | วิธีคำนวณ |
|---|---|---|
| 1 `tier_residual_z` | เร็ว/ช้ากว่า tier ตัวเองแค่ไหน | (actual − median_tier) / median_tier → z |
| 2 `gdp_residual_z` | ผิดจากที่ GDP ทำนายไหม | OLS บน log-GDP → residual → z |
| 3 `den_residual_z` | ผิดจากที่ density ทำนายไหม | OLS บน log-density → residual → z |
| 4 `regional_z` | แปลกในภาคตัวเองไหม | z-score ภายใน region |
| 5 `ratio_z` | UL/DL ratio แปลกไหม | z-score ทั้งประเทศ |
| 6 `lat_regional_z` | latency ผิดปกติในภาคตัวเองไหม | z-score ภายใน region |
| 7 `coverage_z` | คน speedtest เยอะ/น้อยผิดปกติไหม | z-score ของ tests/1000 pop |

**ทำไมใช้ absolute value:** ผิดคาดทั้งสูงและต่ำนับเท่ากัน — เป้าหมายคือหาจังหวัด "ผิดปกติ" ไม่ใช่ "เร็วสุด"

**`np.log1p` vs `np.log`:**
- GDP → `np.log` (ไม่มีค่า 0)
- density → `np.log1p` = log(1+x) ป้องกัน log(0) ถ้า density น้อยมาก

> **สั้นๆ:** คำนวณ "Weirdness Score" จาก 7 z-score รวมกัน — จังหวัด score สูง = ผิดคาดจากหลายมุมพร้อมกัน ไม่ใช่แค่เร็วหรือช้า

---

### Cell 32 — Tier Expectation Gap Bar Chart

```python
tier_residual = (mean_dl - tier_expected) / tier_expected
# % ที่เร็วกว่า (+) หรือช้ากว่า (-) median ของ tier ตัวเอง
```

**ทำอะไร:** แสดงว่าแต่ละจังหวัด overperform/underperform tier ตัวเองกี่ %

**อ่านกราฟ:**
- 0% = เร็วตรงกับค่ากลางของ tier ตัวเอง (ปกติ)
- +50% = เร็วกว่า median tier ตัวเอง 50% (overperform)
- -30% = ช้ากว่า median tier ตัวเอง 30% (underperform)
- แดง (axvspan) = underperform รุนแรง | เขียว = overperform ชัดเจน
- ขวาสุด annotate tier bracket + median speed ของแต่ละ tier

**print ท้าย:** top 8 underperformer + top 8 overperformer vs tier median

> **สั้นๆ:** เห็นว่าจังหวัดใดโดดออกจาก tier ตัวเองมากสุด — overperform คือสัญญาณ catch-up growth, underperform คือสัญญาณ infrastructure gap

---

### Cell 33 — Ookla Test Coverage (tests per 1,000 pop)

```python
tests_per_1000_pop = mean_tests / pop_2024 * 1000
# กี่ครั้งต่อประชากร 1,000 คนต่อไตรมาส — สีตาม Tier
```

**ทำไม metric นี้สำคัญ:**
```
coverage ต่ำ = อาจหมายถึง
  1. penetration ต่ำ — เน็ตบ้านน้อยจริง (infrastructure gap)
  2. Ookla adoption ต่ำ — คนไม่ใช้แอป Speedtest (sampling bias)
→ แยกสองกรณีออกจากข้อมูลไม่ได้ 100%
```

**ทำไมสีเป็น Tier (ไม่ใช่ Region):**
- ตรวจว่า Tier 4 มี coverage ต่ำด้วยไหม → ถ้าใช่ = double disadvantage (จนทั้ง GDP + ถูก underrepresent ใน data)
- Tier 1 coverage สูง = data อาจ **bias** ในทิศที่ overstate ความเร็วจังหวัดดี

> ⚠️ **ข้อจำกัด:** จังหวัด tests/1000 ต่ำ = ค่าเฉลี่ยมาจากกลุ่มตัวอย่างน้อย → ความน่าเชื่อถือต่ำกว่า ควรระบุใน paper

> **สั้นๆ:** วัด sampling bias ของ Ookla — จังหวัดไหนถูก underrepresent ใน dataset เพราะคนกด Speedtest น้อย

---

### Cell 34 — Top 20 Weirdest Provinces: Bar + Heatmap

```python
# Layout: bar (1 unit) + heatmap (2 units) เป็น panel เดียว
gs = fig.add_gridspec(1, 2, width_ratios=[1, 2], wspace=0.08)
```

**กราฟซ้าย:** composite weirdness score bar — rank 1–20 บนลงล่าง, สีตาม region

**กราฟขวา — heatmap 20×7:**
- แดง = สูงกว่าคาด | น้ำเงิน = ต่ำกว่าคาด | intensity = ขนาด z-score
- `vmin=-4, vmax=4` — cap ไว้ที่ 4σ ไม่ให้ extreme outlier บีบ scale
- ตัวเลขสีขาว = |z| > 2.5 (contrast บน background เข้ม)
- ตัวหนา = |z| > 2

**อ่านผลรวม:**
- หลาย cell แดง = overperform หลายมิติพร้อมกัน
- mix แดง/น้ำเงิน = แปลกด้วยเหตุผลต่างกัน เช่น เร็วมากแต่ latency สูงด้วย

> **สั้นๆ:** ภาพรวม top 20 "จังหวัดแปลก" — เห็นทั้งอันดับและสาเหตุว่าแปลกด้านไหนบ้าง

---

### Cell 35 — Geographic Distribution: Weirdness + Speed Map

```python
geo_weird = thailand_gdf.merge(weird_df[['name','weirdness_score','mean_dl','internet_tier']], ...)
geo_weird['weirdness_score'] = geo_weird['weirdness_score'].fillna(0)
```

**2 แผนที่:**

| ซ้าย | ขวา |
|---|---|
| Weirdness score choropleth (YlOrRd — เหลือง→แดง) | Download speed choropleth (YlGnBu — เหลือง→น้ำเงิน) |
| annotate top 10 จังหวัดแปลกสุด | ขอบแดง = Tier 1, ขอบส้มประ = Tier 4 |

**`try/except` guard:** ถ้า `thailand_gdf` ไม่อยู่ใน memory → โหลดใหม่จาก path อัตโนมัติ

**`fillna(0)`:** จังหวัดที่ merge ไม่เจอ (ชื่อ mismatch) → score = 0 ไม่กลายเป็น lightgray

**ขอบ Tier บนแผนที่ขวา:** เห็นว่า Tier 4 บางจังหวัดสีเข้ม (เร็ว) = catch-up growth จริง ไม่ใช่แค่ทฤษฎี

> **สั้นๆ:** แผนที่ปิดท้าย Weirdness EDA — เห็นการกระจายเชิงพื้นที่ว่าจังหวัดแปลก/เร็ว/ช้าอยู่ตรงไหนของประเทศ

---

### Cell 36 — Final Styled Summary Table: ครบ 77 จังหวัด

```python
full_table['verdict'] = full_table.apply(make_verdict, axis=1)
display(styled)
```

**`make_verdict()` — แปลง z-score เป็นภาษาคน:**
```python
# เลือก signal ที่ |z| >= 1.0 → sort by magnitude → เอา top 3
signals = [(abs(r[d]), d, r[d]) for d in _DIM_ORDER if abs(r[d]) >= 1.0]
signals.sort(reverse=True)
→ "fast for GDP (+2.1σ) | overperforms Tier 4 (+1.8σ) | under-tested (-1.2σ)"
→ ถ้าไม่มี signal ≥1.0 → "unremarkable across all dimensions"
```

**Styling 4 ชั้น:**
| Column | Color |
|---|---|
| Score | YlOrRd — เหลือง→แดงตาม weirdness |
| z-columns (7 มิติ) | RdBu_r — น้ำเงิน=ต่ำกว่าคาด, แดง=สูงกว่าคาด |
| DL Mbps | YlGn — เหลือง→เขียวตามความเร็ว |
| Tier | background สี tier (แดง/ส้ม/เขียว/น้ำเงินอ่อน) |

**`display(styled)` ≠ `print`:** render HTML table จริงใน Jupyter — เห็น color gradient ได้

**print ท้าย:** นับจังหวัด |z|>2 / |z|>3 / unremarkable เพื่อ summarize ขนาดของ anomaly ในประเทศ

> **สั้นๆ:** ตาราง interactive ปิดท้าย notebook — ทุก metric ทุก z-score ทุกจังหวัด พร้อม verdict ภาษาคนอธิบายว่า "แปลกอย่างไร"

---

## NDT7 (M-Lab BigQuery)

ไม่มีไฟล์ local — ดึงข้อมูลจาก Google BigQuery โดยตรง

| คอลัมน์                | ความหมายแบบภาษาคน                                                                              |
| ---------------------- | ---------------------------------------------------------------------------------------------- |
| **MeanThroughputMbps** | ความเร็ว download หรือ upload เฉลี่ย (Mbps) วัดแบบ passive ทำงานอยู่เงียบๆ ในพื้นหลัง        |
| **MinRTT**             | ค่าความหน่วงต่ำสุด (ms) ใช้แทน latency — ยิ่งต่ำยิ่งดี                                        |
| **LossRate**           | อัตราการสูญหายของ packet (0–1) ยิ่งสูงยิ่งเน็ตไม่เสถียร                                       |
| **server_ip**          | IP ของ M-Lab server ที่ใช้ทดสอบ — ส่วนใหญ่อยู่ที่สิงคโปร์ (SG) และฮ่องกง (HK)               |
| **country_code**       | ประเทศของ server (SG / HK) — ไม่มี server ในไทย ทำให้ latency สูงกว่า Ookla                   |
| **distance_from_server** | ระยะทางจาก client ถึง server (km)                                                            |
| **duration**           | ระยะเวลาที่ใช้ทดสอบ (วินาที) — test ที่นานกว่ามักได้ throughput ต่ำกว่า (measurement artifact) |
| **ClientIP**           | IP ของ client — ใช้ map กลับไปหาจังหวัดผ่าน ip-api.com                                        |
| **type**               | ประเภทการเชื่อมต่อ: `broadband` (เน็ตบ้าน) หรือ `cellular` (เน็ตมือถือ) — อนุมานจากชื่อ ISP   |
| **province**           | จังหวัดที่ map ได้จาก IP lookup                                                                |
