# สรุปข้อเสนอแก้ไข AINTEC '26 Paper #51 (ที่โดน Reject) — สำหรับอาจารย์

**บริบท:** Full paper ถูก AINTEC '26 ปฏิเสธ ผลรีวิว 3 คน: Reject / Weak reject / Weak accept
เอกสารนี้คือรายการสิ่งที่เจอและเสนอแก้ ยังไม่ถูก apply เข้าไฟล์จริง รอให้อาจารย์เลือกก่อน

---

## กลุ่ม A — จุดที่เป็นข้อผิดพลาดจริง 

### 1. ตัวชี้วัด "success rate" ที่ reviewer ทั้ง 3 คนติงตรงกัน
ของเดิมคำนวณ success rate จาก `min(ค่ามัธยฐานดาวน์โหลดต่อไตรมาส / threshold, 1) × 100`
ซึ่งเป็นอัตราส่วน ไม่ใช่อัตราการผ่านจริง และสำหรับ cloud gaming ใช้แค่ bandwidth
ไม่ได้เช็ค latency 25ms เลย ทั้งที่ตาราง requirement ของ paper เองระบุไว้

- Reviewer A: "the evaluation... appears to classify cloud-gaming success primarily using
  the 44 Mbps download threshold, without incorporating the stated latency requirement"
- Reviewer C: "is that per test? Or for the country-wide mean? I hope it is per-test"
  (คำตอบจริงคือไม่ใช่ทั้งสองอย่าง)

**ข้อเสนอ:** เปลี่ยนเป็นสัดส่วน (ถ่วงน้ำหนักตามจำนวน test) ของ province-quarter ที่ผ่าน
threshold จริง แยกทั้ง bandwidth และ latency คำนวณจากข้อมูลที่มีอยู่แล้วในโปรเจกต์
latency ใช้ค่าจาก Ookla ไม่ใช่ NDT7 เพราะ NDT7 ส่วนใหญ่วิ่งไป server ต่างประเทศ

ผลลัพธ์ใหม่ที่เจอ: cloud gaming ของ fixed broadband ในประเทศรายได้ต่ำ
(กัมพูชา/ลาว/เมียนมา) ติดปัญหาที่ bandwidth จริง แต่ mobile ของ 5 ประเทศ
(รวมสิงคโปร์) ผ่าน bandwidth เกือบหมดแต่ติดที่ latency แทน mobile ของสิงคโปร์เอง
ผ่าน latency แค่ 48.8%

### 2. Citation ที่ยังเป็น placeholder อยู่ในไฟล์ที่ส่งจริง
มีจุด `[CITATION NEEDED]` ค้างอยู่สองแห่งใน Related Work reference ที่ต้องใช้
(MacMillan et al. 2023, งานเทียบ Ookla กับ NDT7)

### 3. รูปที่ 1 ข้อมูลเก่า ขัดกับรูปที่ 2
Reviewer B ถาม: "ทำไม Indonesia หายไปจากรูปที่ 1?"
รูปเดิมเป็นแผนที่ยุคก่อนตัดสิงคโปร์ออก (8 ประเทศ) ตัวเลขในเนื้อหาก็เก่าตาม

**ข้อเสนอ:** ใช้รูปที่ regenerate ใหม่แล้ว (ครบ 9 ประเทศ อ่านจากข้อมูลจริง)
พร้อมแก้ตัวเลข: ช่องว่างระหว่างเมืองหลวงที่เร็วสุด/ช้าสุดคือ **16.4 เท่า**
(สิงคโปร์ 361.0 เทียบย่างกุ้ง 22.0 Mbps) ไม่ใช่ 12 เท่าตามที่เขียนไว้เดิม

### 4. ข้อความที่ผิดจากความจริง: "เมียนมาร์ดิ่งลงใกล้ 0 Mbps ช่วงปลายปี 2025"
ตรวจกับข้อมูลจริงแล้วเมียนมาร์โตขึ้นต่อเนื่องตลอด จาก ~21 Mbps (ต้นปี 2023)
เป็น ~44-54 Mbps (ปลายปี 2025) ไม่เคยตกใกล้ 0 เลย เป็นข้อความที่ผิดล้วนๆ

### 5. คำอธิบายวิธีการผิด: อ้างว่า "รวม" ข้อมูล Ookla กับ NDT7 เข้าด้วยกัน
Reviewer B: "ผู้เขียนอ้างว่ารวมชุดข้อมูล Ookla กับ MLab ใน Sec.4 แต่คำบรรยายรูปที่ 1
และ 2 บอกว่าใช้ Ookla อย่างเดียว"
ความจริงคือสองแหล่งข้อมูลไม่เคยถูกนำมารวมกันเลย วิเคราะห์แยกกันแล้วเทียบผล
เสนอแก้คำอธิบายให้ตรงกับสิ่งที่ pipeline ทำจริง

### 6. คำอธิบายการ "sample" ข้อมูล Indonesia ที่คลุมเครือ
Reviewer A: "ผู้เขียนบอกว่าทำ 'strategic sampling' แต่ให้รายละเอียดน้อยมาก"
ของเดิมพูดกำกวมว่า sample ข้อมูล NDT7 ของ Indonesia เพื่อประหยัดเวลา
แต่จริงๆ Indonesia ได้ข้อมูล NDT7 ครบทุกแถวเหมือนประเทศอื่น สิ่งที่ sample จริง
คือขั้นตอนตรวจสอบ mobile-flag ผ่าน ip-api (สุ่ม probe 5 IP ต่อ block แทนที่จะ
query ทุก IP ทำให้ใช้เวลา 11.5 ชั่วโมงแทนที่จะเป็น ~27 วัน) ซึ่งไม่กระทบข้อมูลหลักเลย

### 7. Ethics statement ผิด
ของเดิมบอกว่า "IP address ไม่ถูกเก็บไว้" แต่จริงๆ คอลัมน์ client IP
ยังอยู่ในไฟล์ข้อมูล NDT7 จริง (แค่ไม่เผยแพร่หรือระบุตัวตนย้อนกลับ)

### 8. "market share" ควรเป็น "test share"
Reviewer A: "ไม่ควรตีความปริมาณการวัดเป็นส่วนแบ่งตลาดหรือการใช้งานจริงโดยไม่มีหลักฐานเพิ่ม"
ตัวเลขในรูปเปรียบเทียบผู้ให้บริการมาจากสัดส่วน test ต่อ ASN ไม่ใช่ market share จริง
เสนอเปลี่ยนคำเรียกทั้งไฟล์ พร้อมเพิ่มประโยคเตือนสั้นๆ กำกับไว้

---

## กลุ่ม B — เนื้อหาที่เพิ่มใหม่  (ต้องอาจารย์ตัดสินใจว่าจะใส่มั้ยครับ)

### 9. ย่อหน้า Limitations & Representativeness
Reviewer C: "The paper should acknowledge that, because NDT results are
user-initiated, they are not necessarily representative. They may
over-represent problems (people measure when they have a problem), or
good cases (if an ISP had employees initiate tests from well provisioned
areas to boost their statistics). As far as I know we have NO way of
knowing how it relates to a uniform distribution. If you agree, please
acknowledge this limit. If you disagree, please explain how you
calibrate these measurements."

ของเดิมไม่มี section นี้เลย เสนอเขียนเพิ่มสั้นๆ ครอบคลุมเรื่อง bias ของกลุ่มตัวอย่าง
ช่องว่างของ coverage และข้อจำกัดของ latency ที่วัดได้

### 10. Reviewer A, B บอกว่างานวิเคราะห์ตื้นเกินไป ไม่มี takeaway — เสนอ เอา peak-hour (RQ3) + ISP (RQ4) กลับมาไหมครับ?
ข้อมูลทั้งสองเรื่องมีอยู่แล้วในโปรเจกต์ (คำนวณไว้แล้ว) แค่ไม่เคยถูกนำเข้า paper เท่านั้น
ถ้าใส่กลับเข้าไปจะได้ 2 finding เพิ่ม: (1) ช่วงเวลาเร่งด่วน เมืองหลวงเสื่อมสภาพหนักกว่าต่างจังหวัดใน
fixed broadband ถึง 6 ใน 8 ประเทศ ขัดกับความเข้าใจทั่วไป และ (2) ผู้ให้บริการที่คนใช้เยอะที่สุด
ไม่ใช่ตัวที่เร็วที่สุดใน 7 จาก 9 ประเทศ

### 11. ย่อหน้าเปรียบเทียบกับงานวิจัยอื่นด้าน Southeast Asia
Reviewer A บ่นว่า "the analysis does not produce a sufficiently novel
methodological contribution or a strong new scientific insight beyond
showing that Internet performance differs substantially across
countries" — งานเราแค่บอกว่าแต่ละประเทศเร็วช้าไม่เท่ากัน ซึ่งใครๆ ก็เดาได้อยู่แล้ว
ไม่มีอะไรใหม่

reference list ของอาจารย์มี 2 งานที่ทำเรื่องคล้ายกันอยู่แล้วแต่ไม่เคยถูกอ้างถึง
(Ofa2021 UN ESCAP, Caldas2023 OECD) เสนอเขียนย่อหน้าเทียบ 2 จุดต่างจากงานพวกนั้น:
งานเก่าใช้ Ookla อย่างเดียว เราใช้ Ookla + NDT7 สองแหล่งมาเช็คไขว้กัน (แหล่งนึง
server ในประเทศ อีกแหล่ง server ต่างประเทศ วัดคนละมุม) และงานเก่ารายงานแค่ความเร็ว
เฉลี่ยเทียบกันเฉยๆ เราเอาไปเทียบกับ threshold การใช้งานจริง (เช่น cloud gaming
ต้องการ 44 Mbps บวก latency 25ms ผ่านไหม) เพื่อบอก reviewer ล่วงหน้าว่างานนี้
ไม่ใช่แค่ทำซ้ำสิ่งที่มีคนทำไปแล้ว

---

## สิ่งที่ยังไม่ได้ทำ / รอข้อมูลเพิ่ม

- รูปแบบหน้าเอกสาร (copyright block, DOI) ยังเป็น placeholder รอ venue ใหม่ที่จะส่ง
- ยังไม่ตัดความยาวให้พอดีตาม page limit เพราะยังไม่รู้ว่าจะส่งที่ไหนต่อ
- ยังไม่ได้เพิ่มกราฟ CDF หรือตาราง threshold-sensitivity ที่ reviewer C แนะนำ

---

*หมายเหตุ: เอกสารนี้เป็นข้อเสนอ ไฟล์ `paper.tex` ปัจจุบันในระบบยังเป็นต้นฉบับของอาจารย์ 100%
ยังไม่มีการแก้ไขใดถูกนำเข้าไฟล์จริงจนกว่าอาจารย์จะเลือก*
