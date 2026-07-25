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

###  Sprint 1: เตรียมข้อมูลและขึ้นโครงสร้าง (8 - 14 มิ.ย.)

**เป้าหมาย:** ข้อมูลทั้ง Ookla และ NDT7 พร้อมวิเคราะห์ + โครงกระดูก Paper ครบ

- [x] จัดการ raw data ของ Ookla ให้อยู่ในระดับรายจังหวัด (master dataset)
- [x] ดึงและจัดการ raw data ของ NDT7 จาก M-Lab / BigQuery ให้อยู่ในระดับรายจังหวัดเช่นกัน
- [x] ลองพลอตกราฟ และดูค่า Correlation เบื้องต้นของทั้งสองชุดข้อมูล
- [x] เขียน Introduction + Methodology ใน paper.tex ไว้เป็น base

---

### Sprint 2: วิเคราะห์สถิติและหาข้อสรุป (15 - 21 ก.ค.)

**เป้าหมาย:** เปรียบเทียบ Ookla และ NDT7 ทางสถิติครบ + เขียนบท Results และ Discussion

- [x] RQ1 — "อินเทอร์เน็ตไทยดีหรือแย่?" เทียบกับ app-requirement thresholds (Ookla + NDT7) —
      `notebooks/comparison/rq1_thresholds_ookla.ipynb`, `rq1_thresholds_ndt7.ipynb`
- [x] RQ2 — เทรนด์รายไตรมาส (2023Q1-2025Q4), download/upload/latency, Ookla vs NDT7 fixed/mobile —
      `notebooks/comparison/rq2_trends.ipynb`. Headline: ทุก segment โต ไม่มีตัวไหนแย่ลง;
      Bangkok metro mobile ที่ RQ1 พบว่าแย่ (55-67% pooled) จริงๆ เป็นปัญหาปี 2023 (0-7%) ที่หายไปแล้วตั้งแต่ 2024-Q1 (100% ทุกไตรมาส)
- [ ] วิเคราะห์และเปรียบเทียบผลระหว่าง Ookla กับ NDT7 ในแต่ละจังหวัด/ภูมิภาค
- [ ] ทดสอบทางสถิติ (Correlation, ANOVA, OLS) และสรุปนัยสำคัญ
- [ ] ระบุจังหวัดที่มีพฤติกรรมผิดปกติ และอธิบายสาเหตุ
- [ ] Finalize รูปและแผนที่ทั้งหมด
- [ ] เขียนบท Results และ Discussion ใน paper.tex

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
