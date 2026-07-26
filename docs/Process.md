## Progress Flow

## แผนการทำ Paper (8 มิ.ย. - 31 ก.ค.)

---

### หมายเหตุ — เปลี่ยนทิศทาง Paper (6 ก.ค.)

**เดิม:** วิเคราะห์ประสิทธิภาพบรอดแบนด์มีสาย (fixed only) ระดับจังหวัด เทียบกับ GDP/ความหนาแน่นประชากร (correlation study)

**ใหม่:** ตอบคำถาม **"อินเทอร์เน็ตไทยดีหรือแย่?"** — เหตุผล: ไทยไม่มีงานวิจัยเชิงระบบวัดคุณภาพเน็ตจากข้อมูลจริง มีแต่สถิติที่ขัดแย้งกัน (Ookla Global Index บอกว่า fixed ไทยอันดับ 13 โลก = ดี, แต่ ETDA/มูลนิธิผู้บริโภคสำรวจพบผู้ใช้ร้องเรียนเน็ตช้า/หลุดเยอะ = แย่ — ดูรายละเอียด citations.md §6) จึงใช้ Ookla (fixed + mobile) และ NDT7 มา cross-validate กันเพื่อหาคำตอบจริงแทนการเถียงกันด้วยความเห็น

**ผลกระทบต่อ scope:**
- เพิ่ม mobile (เดิมมีแค่ fixed) — ทั้งระดับ 77 จังหวัด และ district-level 8 จังหวัด (กทม. + โคราช/ขอนแก่น/เชียงใหม่/ภูเก็ต/ชลบุรี/สงขลา/ระยอง)
- GDP/density correlation ยังอยู่ แต่ลดบทบาทลงเป็น "ปัจจัยอธิบายส่วนต่าง" ไม่ใช่ objective หลักอีกต่อไป
- Introduction + Methodology ใน paper.tex เขียนใหม่แล้วตามทิศทางนี้ (ดู §1, §2.1 ใหม่)

---

### หมายเหตุ — ขยาย scope เป็น SEA 8 ประเทศ (20 ก.ค.)

**เดิม:** ตอบคำถาม "อินเทอร์เน็ตไทยดีหรือแย่?" แบบ standalone (ไทยอย่างเดียว)

**ใหม่:** ขยายเป็นคำถามเชิงเปรียบเทียบภูมิภาค — ไทยดีหรือแย่ **เทียบกับเพื่อนบ้าน SEA** (เวียดนาม ฟิลิปปินส์ สิงคโปร์ กัมพูชา เมียนมา ลาว มาเลเซีย) โดยไทยยังเป็น focus หลัก ประเทศอื่นเป็น benchmark/context ไม่ใช่ full cross-country study เท่ากัน

**ผลกระทบต่อ scope:**
- Ookla ฝั่งเดียว ขยายจาก 4 ประเทศ (ไทย/เวียดนาม/ฟิลิปปินส์/สิงคโปร์) เป็น 8 ประเทศ — เพิ่ม กัมพูชา/เมียนมา/ลาว/มาเลเซีย ใช้ pipeline เดียวกันทุกประเทศ (ดู `docs/paper_draft.md` §3.1)
- NDT7 **ยังคงจำกัดแค่ไทย + เวียดนาม** — ไม่ได้ขยายตามฝั่ง Ookla (กัมพูชาเก็บบางส่วนแต่ยังไม่ reliable ระดับจังหวัด, ฟิลิปปินส์รอ collaborator, สิงคโปร์/ลาว/มาเลเซีย/เมียนมา ไม่อยู่ใน scope)
- `docs/paper_draft.md` (draft ภาษาอังกฤษ) เขียนใหม่ตาม scope นี้แล้วครบ (Title, Intro, Objectives, Hypotheses, Scope, Data §2.1-2.4, Methodology §3.1-3.7) — **`paper.tex` (LaTeX ตัวจริง) ยังไม่ได้ port เนื้อหานี้เข้าไป**, title เก่ายังเป็น "Is Thai Internet Good or Bad?" ทุก section ยังเป็น `%% TODO`
- `README.md` อัปเดตแล้ว (26 ก.ค.) ให้ตรง scope 8 ประเทศ
- `docs/citations.md` / `citation-map.md` / `citation-map-th.md` **ยังไม่อัปเดต** — ยังอ้างอิงแหล่งข้อมูลไทยล้วน ต้องเพิ่มแหล่งของอีก 7 ประเทศ (DOSM มาเลเซีย, Cambodia HDI report, geoBoundaries ADM1, World Bank GDP กัมพูชา/เมียนมา/ลาว, VN NDT7 collaborator)
- โมเดล "divergence score" ผิดปกติรายจังหวัด (composite anomaly scoring, §3.6) **ถูก drop แล้ว (20 ก.ค.)** — ตัด anomaly-scoring layer ทิ้งจากทุก Ookla EDA notebook เหลือแค่วิเคราะห์ tier/GDP/density ตรงๆ (§3.2, §3.4) แทน — Sprint 2 checklist ข้อ "ระบุจังหวัดที่มีพฤติกรรมผิดปกติ" ด้านล่างจึงถือว่า **ตกไปแล้ว ไม่ต้องทำต่อ**

---

###  Sprint 1: เตรียมข้อมูลและขึ้นโครงสร้าง (8 - 14 มิ.ย.)

**เป้าหมาย:** ข้อมูลทั้ง Ookla และ NDT7 พร้อมวิเคราะห์ + โครงกระดูก Paper ครบ

- [x] จัดการ raw data ของ Ookla ให้อยู่ในระดับรายจังหวัด (master dataset)
- [x] ดึงและจัดการ raw data ของ NDT7 จาก M-Lab / BigQuery ให้อยู่ในระดับรายจังหวัดเช่นกัน
- [x] ลองพลอตกราฟ และดูค่า Correlation เบื้องต้นของทั้งสองชุดข้อมูล
- [x] เขียน Introduction + Methodology ใน paper.tex ไว้เป็น base

---

### Sprint 2: วิเคราะห์สถิติและหาข้อสรุป (15 - 21 ก.ค.)

**เป้าหมาย:** เปรียบเทียบ Ookla และ NDT7 ทางสถิติครบ + เขียนบท Results และ Discussion

- [x] RQ1 — "อินเทอร์เน็ตไทยดีหรือแย่?" เทียบกับ app-requirement thresholds (Ookla, ไทย + 7 ประเทศ SEA
      เป็น context) + NDT7 (ไทย/เวียดนาม) — `notebooks/comparison/rq1_thresholds_ookla.ipynb`,
      `rq1_thresholds_ndt7.ipynb`
- [x] RQ2 — เทรนด์รายไตรมาส (2023Q1-2025Q4), download/upload/latency, Ookla vs NDT7 fixed/mobile
      (ไทย deep-dive) + SEA growth-context เพิ่มเติม (26 ก.ค.: ไทยโต +42% ช้าเป็นอันดับ 2 จาก 8
      ประเทศ แต่ระดับสัมบูรณ์ยังสูงเป็นอันดับ 2 ตลอด — เพราะฐานเริ่มต้นสูงอยู่แล้ว ไม่ใช่ชะลอตัว) —
      `notebooks/comparison/rq2_trends.ipynb`. Headline เดิม: ทุก segment โต ไม่มีตัวไหนแย่ลง;
      Bangkok metro mobile ที่ RQ1 พบว่าแย่ (55-67% pooled) จริงๆ เป็นปัญหาปี 2023 (0-7%) ที่หายไปแล้วตั้งแต่ 2024-Q1 (100% ทุกไตรมาส)
- [ ] Ookla vs NDT7 province/quarter agreement (ไทย+เวียดนามเท่านั้น) — coverage comparison,
      Pearson/Spearman ranking agreement, Wilcoxon signed-rank magnitude gap (ดู `paper_draft.md`
      §3.3) — **ยังไม่มี notebook ทำเรื่องนี้เลย ณ วันนี้ (26 ก.ค.)**
- [ ] Cross-country stat tests (8 ประเทศ, Ookla): Kruskal-Wallis omnibus + Mann-Whitney pairwise
      (ไทย vs. แต่ละประเทศ) + OLS พร้อม country fixed-effect (ดู `paper_draft.md` §3.2 ข้อ 2-4) —
      notebook เก่า (`ookla_cross_country.ipynb`) ถูกลบไปแล้ว (คิดว่า superseded แต่จริงๆ ยังไม่มีอะไร
      มาแทน) **เป็นช่องว่างจริง ไม่ใช่แค่ยังไม่ tick checkbox**
- [ ] Within-country GDP/density correlation + OLS (ต่อประเทศ) — ทำแล้วบางส่วนใน
      `notebooks/ookla/*_eda.ipynb` (เช่น thailand_eda.ipynb มี `smf.ols` แล้ว) เช็คให้ครบทุกประเทศ
- ~~[ ] ระบุจังหวัดที่มีพฤติกรรมผิดปกติ และอธิบายสาเหตุ~~ — **drop แล้ว (20 ก.ค., ดูหมายเหตุด้านบน)**
      composite divergence score ถูกตัดทิ้ง ไม่ต้องทำต่อ
- [ ] Finalize รูปและแผนที่ทั้งหมด
- [ ] เขียนบท Results และ Discussion ใน paper.tex (ยังรอ paper_draft.md → paper.tex port ก่อน)

---

### Sprint 3: เก็บรายละเอียดและตกแต่งเล่ม (22 - 28 ก.ค.)

**เป้าหมาย:** Paper ร่างสมบูรณ์ทุกบท พร้อม compile เป็น PDF

- [ ] เขียน Abstract และ Conclusion
- [ ] ตรวจสอบ References ให้ครบและถูกต้องตาม primary source
- [ ] จัดหน้าและ format ใน LaTeX ให้เรียบร้อย
- [ ] Compile xelatex ผ่านโดยไม่มี error

---

### ช่วงเตรียมพร้อมสุดท้าย (29 - 31 ก.ค.)

**เป้าหมาย:** Paper พร้อมส่ง

- [ ] ตรวจทานตัวเลข ภาษา และความถูกต้องรอบสุดท้าย
- [ ] Export PDF และส่งงาน
