# ข้อเสนอแก้ไข paper.tex — สำหรับให้อาจารย์รีวิว

**สถานะ:** `docs/paper/paper.tex` ถูก revert กลับไปเป็นเวอร์ชันต้นฉบับของอาจารย์แล้ว (ตรงกับ
`AINTEC 2026-paper.docx` 100%) รายการด้านล่างคือสิ่งที่เคยแก้ไปวันนี้ แต่ยังไม่ apply กลับเข้าไฟล์
— รอให้อาจารย์เลือกว่าจะเอาข้อไหนบ้าง

บริบท: full paper (#51) โดน AINTEC '26 reject มา 3 reviewer (Reject / Weak reject / Weak
accept) รายการนี้แม็ปตรงกับ comment ที่ reviewer ให้มา ระบุว่าข้อไหนตอบ comment ตัวไหน

---

## กลุ่ม A — บั๊กจริง ควรแก้ไม่ว่าจะใช้สำนวนใคร (ตัวเลข/ข้อเท็จจริงผิด ไม่ใช่เรื่องสไตล์)

**1. Metric "success rate" ไม่ใช่ pass rate จริง — reviewer ทั้ง 3 คนติงจุดนี้**
- ของเดิม: `success rate = min(country's quarterly median download / threshold, 1) × 100` — เป็นอัตราส่วน ไม่ใช่ pass rate และ cloud gaming ใช้แค่ bandwidth ไม่เช็ค latency 25ms เลย ทั้งที่ Table 1 ของ paper เองมี latency requirement
- Reviewer A3: "the evaluation... appears to classify cloud-gaming success primarily using the 44 Mbps download threshold, without incorporating the stated latency requirement"
- Reviewer C: "is that per test? Or for the country-wide mean? I hope it is per-test." (คำตอบจริงคือ ไม่ใช่ทั้งคู่)
- ข้อเสนอ: เปลี่ยนเป็น test-weighted % ของ province-quarter ที่ผ่าน threshold จริง (bandwidth และ latency แยกกัน) คำนวณจาก `data/exports/ookla_*_province_quarterly.csv` ตรงตาม `notebooks/comparison/rq1_thresholds_ookla.ipynb` ที่มีอยู่แล้วในโปรเจกต์ latency ใช้ Ookla ไม่ใช่ NDT7 (NDT7 ส่วนใหญ่วิ่งไป server ต่างประเทศ)
- **ผลลัพธ์ใหม่ที่เจอ:** cloud gaming ที่ fixed broadband ประเทศรายได้ต่ำ (Cambodia/Laos/Myanmar) ติดที่ bandwidth จริง แต่ mobile ของ 5 ประเทศ (รวม Singapore) ผ่าน bandwidth เกือบหมดแต่ติด latency แทน — Singapore mobile latency ผ่านแค่ 48.8%

**2. `[CITATION NEEDED]` ยังอยู่ในไฟล์ที่ส่งจริง (2 จุด, Related Work §2.1)**
- Reviewer A1: "grammatical errors, inconsistent figure numbering, imprecise terminology, and apparent template artifacts"
- ข้อเสนอ: reference list มี MacMillan2023 (Ookla vs NDT7 comparison, POMACS 2023) อยู่แล้วแต่ไม่เคยถูก cite ในเนื้อหา — ใช้แทนสอง placeholder ได้เลย ไม่ต้องหา citation ใหม่

**3. Fig. 1 เก่า ขัดกับ Fig. 2 (Indonesia หายจาก Fig. 1)**
- Reviewer B: "Why is Indonesia missing in Fig. 1?"
- ของเดิม: `image1.png`/`image2.png` เป็นแผนที่ 8-ประเทศเก่า (ก่อน revert สิงคโปร์ 08-14), ตัวเลขในเนื้อหาก็เก่าตาม (SG 341, TH 244 national) ซึ่งมาจาก `scripts/build_slides_all_countries.py` ที่ hardcode ค่าไว้ ไม่ได้อ่านจาก data จริง
- ข้อเสนอ: สลับไปใช้รูปที่ regenerate แล้วใน `outputs/ookla/cross_country/01_all_country_fixed_dl.png` และ `03_capital_vs_national.png` (มี 9 ประเทศครบ อ่านจาก `data/exports/` จริง) พร้อมแก้ตัวเลขในเนื้อหา: capital spread จริงคือ **16.4×** (Singapore 361.0 vs Yangon 22.0) ไม่ใช่ 12× ที่เขียนไว้

**4. Claim เท็จ: "Myanmar briefly dropping near 0 Mbps at the end of 2025"**
- ตรวจกับข้อมูลจริง (`data/exports/ookla_myanmar_province_quarterly.csv`) แล้ว Myanmar โตขึ้นตลอด จาก ~21 Mbps (Q1 2023) เป็น ~44-54 Mbps (Q4 2025) ไม่เคยตกใกล้ 0 — เป็น claim ที่ผิดล้วนๆ ไม่เกี่ยวกับ Singapore cut เลย

**5. Methods §4: claim "merged" Ookla+NDT7 ไม่จริง**
- Reviewer B: "The authors claim that they merged the Ookla and MLab datasets in Sec.4, but the captions of Fig. 1 and 2 suggest Ookla only"
- จริงๆ ทั้งสอง source ไม่เคยถูก pool รวมกันเลย วิเคราะห์แยกแล้วเทียบกัน — ข้อเสนอ: แก้คำอธิบายให้ตรงกับสิ่งที่ pipeline ทำจริง

**6. "strategic sampling" ของ Indonesia อธิบายผิด**
- Reviewer A4: "The authors state that they performed 'strategic sampling'... but provide little detail"
- ของเดิมพูดกำกวมว่า sample ข้อมูล NDT7 ของ Indonesia เพื่อประหยัดเวลา — แต่จริงๆ Indonesia ได้ข้อมูล NDT7 ครบ 367.2M แถวเหมือนประเทศอื่น สิ่งที่ sample จริงคือขั้นตอน ip-api mobile-flag lookup (probe 5 IP ต่อ block แทนที่จะ query ทุก IP — 1.0M probe แทน 50.5M, ใช้เวลา 11.5 ชม.แทน ~27 วัน) ซึ่งไม่กระทบ record ข้อมูลเลย
- ข้อมูลอยู่ที่ `data/ndt7/CLEANING_OVERVIEW.md`

**7. Ethics statement ผิด**
- ของเดิมบอกว่า "IP addresses... are not retained" — แต่จริงๆ `client_ip` เป็น column ที่เก็บอยู่ใน NDT7 parquet จริง (`data/ndt7/README_for_eda.md`) แค่ไม่เผยแพร่/ไม่ re-identify

**8. "market share" ควรเป็น "test share"**
- Reviewer A4: "measurement volume should not be directly interpreted as ISP market share or national usage without additional evidence"
- ตัวเลขใน Fig. 6/7 มาจากสัดส่วน test ต่อ ASN ไม่ใช่ market share จริง — ข้อเสนอเปลี่ยนคำเรียกทั้งไฟล์ พร้อมเพิ่มประโยคเตือนสั้นๆ

---

## กลุ่ม B — เนื้อหาที่ "เพิ่มใหม่" ไม่มีในต้นฉบับอาจารย์เลย (ต้องอาจารย์ตัดสินใจว่าจะเอาไหม)

**9. Limitations & representativeness paragraph**
- Reviewer C ขอตรงๆ: "The paper should acknowledge that... they are not necessarily representative. ...If you agree, please acknowledge this limit."
- ของเดิมไม่มี section นี้เลย — เขียนเพิ่มสั้นๆ ครอบคลุม crowdsourced bias, coverage gap, Ookla latency เป็นแค่ lower bound

**10. RQ3 — Peak-Hour Congestion (subsection ใหม่)**
- ตอบ comment "shallow/no takeaway" ของ reviewer A2/B
- ข้อมูลมีอยู่แล้วใน `outputs/ndt7/comparison/rq3_*` (ไม่เคยถูกเอาเข้า paper) — busy/quiet throughput ratio ต่างกันมาก (Cambodia 0.23 ถึง Singapore 0.73), เมืองหลวงเสื่อมหนักกว่าต่างจังหวัดใน fixed broadband 6/8 ประเทศ (ขัดกับ intuition ทั่วไป)

**11. RQ4 — Market Structure (subsection ใหม่)**
- ตอบ comment เดียวกัน — most-tested operator ไม่ใช่ตัวเร็วที่สุดใน 7/9 ประเทศ (fixed), HHI concentration สัมพันธ์กับความเร็วบน mobile (ρ=-0.82) แต่ไม่สัมพันธ์บน fixed (ρ=0.12)

**12. Related Work: ย่อหน้าเทียบกับงานวิจัยอื่นด้าน SEA broadband**
- ตอบ reviewer A2 ("no novel contribution") — อ้างถึง Ofa2021 (UN ESCAP) และ Caldas2023 (OECD) ที่อยู่ใน reference list อยู่แล้วแต่ไม่เคยถูก cite ชี้ให้เห็นว่างานเราต่างจากพวกนั้นตรงไหน (รวม Ookla+NDT7 สองแหล่ง + threshold-based framing)

---

## สิ่งที่ไม่ได้แตะ / ยังไม่ verify เต็มที่

- หน้าตา/metadata (`\setcopyright`, `\acmDOI` placeholder) — ยังเป็น placeholder เดิม รอ venue ใหม่
- ยังไม่ตัดความยาวให้พอดี page limit ของ venue ที่จะ resubmit (ไม่รู้ venue เป้าหมาย ต้องรออาจารย์บอก)
- ไม่ได้เพิ่ม CDF figure หรือ threshold-sensitivity table ที่ reviewer C แนะนำ (ยังไม่ทำ ยังไม่มีใน list นี้)

---

*ไฟล์นี้เป็นข้อเสนอ ไม่ใช่สิ่งที่ apply ไปแล้ว — `paper.tex` ปัจจุบัน = ต้นฉบับอาจารย์ 100%*
