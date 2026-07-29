# -*- coding: utf-8 -*-
"""สร้าง indonesia_reference.csv + indonesia_provinces.geojson ตามแบบประเทศอื่น"""
import json, re, sys
import pandas as pd

SCRATCH = r"C:\Users\user\AppData\Local\Temp\claude\E--ndt7\3efe3598-1bbf-4b09-b80f-0372835b2561\scratchpad"
OUT_REF = r"E:\thailand-broadband-analysis\data\reference\indonesia_reference.csv"
OUT_GEO = r"E:\thailand-broadband-analysis\data\geo\indonesia_provinces.geojson"

# ---------- 1. GRDP 2021 (ตารางใต้หัวข้อ "2021 Per Capita", 34 จังหวัด) ----------
t = json.load(open(f"{SCRATCH}/idn_grdp.json", encoding="utf-8"))["parse"]["wikitext"]
i = t.find("2021 Per Capita")
seg = t[i:t.find("\n{|", t.find("Per Capita data"))]  # ตัดก่อนตารางถัดไป
rows = re.findall(
    r"\|align=center\|\s*(\d+)\s*\n\|\{\{flag\|([^\}\|]+)\}\}\s*\n\|\[\[([^\]\|]+)[^\]]*\]\]\s*\n"
    r"\|align=right\|\s*([\d,]+)\s*\n\|align=right\|\s*([\d,]+)\s*\n\|align=right\|\s*([\d,]+)", seg)
grdp = pd.DataFrame(rows, columns=["rank", "name_en", "region", "rp_k", "usd_nom", "ppp_int"])
for c in ["rp_k", "usd_nom", "ppp_int"]:
    grdp[c] = grdp[c].str.replace(",", "").astype(float)
assert len(grdp) == 34, f"GRDP 2021 ต้องมี 34 แถว ได้ {len(grdp)}"

# ---------- 2. พื้นที่ + ประชากร (หน้า Provinces of Indonesia, 38 จังหวัด) ----------
t2 = json.load(open(f"{SCRATCH}/idn_wiki.json", encoding="utf-8"))["parse"]["wikitext"]
raw = re.findall(r"\|\s*\{\{code\|(\d+)\}\}(.*?)(?=\n\|-|\n\|\}|\Z)", t2, re.S)
recs = []
for code, body in raw:
    nums = re.search(r"\|\s*([\d,\.]+)\s*\|\|\s*([\d,]+)\s*\|\|\s*([\d,]+)", body)
    srt = re.search(r"\{\{sort\|([^\|]+)\|", body)
    names = [n for n in re.findall(r"\[\[([^\]\|]+?)(?:\|[^\]]*)?\]\]", body) if not n.startswith("File:")]
    nm = srt.group(1) if srt else (names[0] if names else "?")
    nm = re.sub(r"\s*\(province\)$", "", nm).strip()
    if not nums:
        continue
    recs.append(dict(code=code, name_en=nm,
                     area_km2=float(nums.group(1).replace(",", "")),
                     pop=int(nums.group(2).replace(",", ""))))
geo = pd.DataFrame(recs)
assert len(geo) == 38, f"หน้า provinces ต้องมี 38 แถว ได้ {len(geo)}"

# ยุบปาปัวกลับเป็นโครงสร้าง 34 จังหวัด (ให้ตรง parquet + geoBoundaries 2017)
MERGE = {"South Papua": "Papua", "Central Papua": "Papua", "Highland Papua": "Papua",
         "Southwest Papua": "West Papua"}
geo["name_en"] = geo["name_en"].replace(MERGE)
geo = geo.groupby("name_en", as_index=False).agg(area_km2=("area_km2", "sum"), pop=("pop", "sum"))
assert len(geo) == 34, f"หลังยุบต้องเหลือ 34 ได้ {len(geo)}"

# ---------- 3. ชื่อ: wiki -> geoBoundaries shapeName ----------
WIKI_TO_SHAPE = {
    "Bangka Belitung Islands": "Bangka-Belitung Islands",
    "Jakarta": "Jakarta Special Capital Region",
    "Yogyakarta": "Special Region of Yogyakarta",
}
for d in (grdp, geo):
    d["shape"] = d["name_en"].replace(WIKI_TO_SHAPE)

gj = json.load(open(f"{SCRATCH}/idn_adm1.geojson", encoding="utf-8"))
shapes = {f["properties"]["shapeName"] for f in gj["features"]}
for d, nm in ((grdp, "GRDP"), (geo, "area/pop")):
    miss = set(d["shape"]) - shapes
    assert not miss, f"{nm}: ชื่อไม่ตรง geoBoundaries -> {miss}"

# ---------- 4. shapeName -> ชื่อใน parquet ----------
SHAPE_TO_PARQUET = {
    "Aceh": "Aceh", "Bali": "Bali", "Bangka-Belitung Islands": "BangkaBelitung",
    "Banten": "Banten", "Bengkulu": "Bengkulu", "Central Java": "JawaTengah",
    "Central Kalimantan": "KalimantanTengah", "Central Sulawesi": "SulawesiTengah",
    "East Java": "JawaTimur", "East Kalimantan": "KalimantanTimur",
    "East Nusa Tenggara": "NusaTenggaraTimur", "Gorontalo": "Gorontalo",
    "Jakarta Special Capital Region": "JakartaRaya", "Jambi": "Jambi",
    "Lampung": "Lampung", "Maluku": "Maluku", "North Kalimantan": "KalimantanUtara",
    "North Maluku": "MalukuUtara", "North Sulawesi": "SulawesiUtara",
    "North Sumatra": "SumateraUtara", "Papua": "Papua", "Riau": "Riau",
    "Riau Islands": "KepulauanRiau", "South Kalimantan": "KalimantanSelatan",
    "South Sulawesi": "SulawesiSelatan", "South Sumatra": "SumateraSelatan",
    "Southeast Sulawesi": "SulawesiTenggara", "Special Region of Yogyakarta": "Yogyakarta",
    "West Java": "JawaBarat", "West Kalimantan": "KalimantanBarat",
    "West Nusa Tenggara": "NusaTenggaraBarat", "West Papua": "PapuaBarat",
    "West Sulawesi": "SulawesiBarat", "West Sumatra": "SumateraBarat",
}
assert set(SHAPE_TO_PARQUET) == shapes, "SHAPE_TO_PARQUET ไม่ครบ/ไม่ตรง"

# ---------- 5. ประกอบ ----------
df = grdp[["shape", "region", "usd_nom", "ppp_int"]].merge(
    geo[["shape", "area_km2", "pop"]], on="shape", how="outer", validate="1:1")
assert df.notna().all().all() and len(df) == 34

# ชื่อแสดงผล: ใช้ชื่ออังกฤษสั้นแบบอ่านง่าย (จะไปโผล่บนกราฟทุกใบ)
SHORT = {"Jakarta Special Capital Region": "Jakarta",
         "Special Region of Yogyakarta": "Yogyakarta",
         "Bangka-Belitung Islands": "Bangka Belitung"}
df["province_en"] = df["shape"].replace(SHORT)
# ไม่มีชื่อไทย -> ใส่ชื่ออินโดนีเซีย (แยกคำจากชื่อดิบใน parquet: JawaBarat -> Jawa Barat)
df["province_th"] = df["shape"].map(SHAPE_TO_PARQUET).str.replace(
    r"(?<=[a-z])(?=[A-Z])", " ", regex=True)
df["density_per_km2"] = (df["pop"] / df["area_km2"]).round(0).astype(int)
df["gdp_per_capita_raw_2021"] = df["usd_nom"]            # USD nominal (เหมือนประเทศอื่น)
df["gdp_per_capita_usd_ppp_2021"] = df["ppp_int"]
df["gdp_per_capita_thb_2021"] = (df["ppp_int"] * 32).round(2)   # สูตรเดียวกับประเทศอื่น

# internet_tier = ควอร์ไทล์ของ GDP per capita (สูงสุด = 1) ตามแบบไทย แต่ไม่มีการปรับมือ
df["internet_tier"] = pd.qcut(df["gdp_per_capita_raw_2021"].rank(method="first"),
                              4, labels=[4, 3, 2, 1]).astype(int)

df = df.rename(columns={"pop": "pop_2024"})
COLS = ["province_en", "province_th", "region", "area_km2", "pop_2024", "density_per_km2",
        "internet_tier", "gdp_per_capita_raw_2021", "gdp_per_capita_usd_ppp_2021",
        "gdp_per_capita_thb_2021"]
df[COLS].sort_values("province_en").to_csv(OUT_REF, index=False)
print(f"เขียน {OUT_REF}  ({len(df)} แถว)")

# ---------- 6. geojson: เติม field `name` ให้ตรงแบบประเทศอื่น ----------
SHAPE_TO_EN = dict(zip(df["shape"], df["province_en"]))
for f in gj["features"]:
    f["properties"]["name"] = SHAPE_TO_EN[f["properties"]["shapeName"]]
json.dump(gj, open(OUT_GEO, "w", encoding="utf-8"), ensure_ascii=False)
print(f"เขียน {OUT_GEO}  ({len(gj['features'])} features)")

print("\n--- ตัวอย่าง ---")
print(df[COLS].sort_values("gdp_per_capita_raw_2021", ascending=False).head(6).to_string(index=False))
print("\ntier:", df.groupby("internet_tier").size().to_dict())
