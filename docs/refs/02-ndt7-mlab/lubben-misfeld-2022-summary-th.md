# สรุปแปลไทย: Exploring the Measurement Lab Open Dataset for Internet Performance Evaluation: The German Internet Landscape

**ผู้เขียน:** Ralf Lübben, Nico Misfeld (Flensburg University of Applied Sciences, เยอรมนี)
**ตีพิมพ์:** Electronics 2022, 11, 162 — https://doi.org/10.3390/electronics11010162
**ไฟล์ต้นฉบับ:** `docs/02-ndt7-mlab/lubben-misfeld-2022-mlab-german-internet-landscape.pdf`

---

## บทคัดย่อ

Measurement Lab (MLab) เป็นชุดข้อมูลเปิดขนาดใหญ่สำหรับวัดประสิทธิภาพอินเทอร์เน็ต งานวิจัยนี้ใช้ข้อมูลจาก MLab วิเคราะห์สถานะอินเทอร์เน็ตเยอรมนีอย่างเป็นระบบ — หาช่วงเวลา/วันที่คนใช้เน็ตเยอะ (busy hours), ผลกระทบของตำแหน่ง server และ ISP, เปรียบเทียบผู้ให้บริการ และผลกระทบของ COVID-19 พบว่าอินเทอร์เน็ตเสื่อมประสิทธิภาพแค่บางส่วนช่วงต้น lockdown เท่านั้น และ protocol ควบคุมความคับคั่ง (congestion control) ที่พัฒนาขึ้นมาช่วยให้ประสิทธิภาพดีขึ้นจริง งานวิจัยเน้นช่วง "busy hours" เพราะเป็นช่วงที่ผู้ใช้สนใจที่สุด — ต้องรองรับงานหนักอย่าง video streaming หรือ cloud gaming ได้

---

## 1. ที่มาและปัญหา

ความต้องการอินเทอร์เน็ตความเร็วสูง-latency ต่ำเพิ่มขึ้นเรื่อยๆ ตามแอปพลิเคชันใหม่ๆ: การสนทนาด้วยเสียงต้องการ latency ต่ำกว่า 200ms, Netflix แนะนำ 5 Mbps สำหรับ HD และ 25 Mbps สำหรับ UHD, cloud gaming ต้องการทั้ง bandwidth สูง (44 Mbps) และ latency ต่ำ (~25ms) รัฐบาลหลายประเทศ (เช่น EU ปี 2013/2020) ตั้งเป้ามาตรฐาน broadband ระดับชาติ แต่ธรรมชาติของอินเทอร์เน็ตที่ผันผวนตามเวลาทำให้ตรวจสอบยาก

งานวิจัยนี้ใช้ MLab — แพลตฟอร์มเปิดที่เผยแพร่ทั้งผลวัดและซอฟต์แวร์ที่ใช้วัด — เพื่อดูสถานะอินเทอร์เน็ตเยอรมนี แต่ตั้งข้อสังเกตว่าการวิเคราะห์ MLab มีข้อควรระวัง (pitfall) เพราะเป็นข้อมูลจาก convenience sampling (ผู้ใช้เข้ามาทดสอบเอง ไม่ใช่การสุ่มตัวอย่างแบบสถิติ)

**คุณูปการหลักของงานวิจัย:**
- เสนอวิธี "confine" (จำกัดขอบเขต) ข้อมูลมหาศาลให้เหลือ subset ที่เป็นตัวแทนได้จริง — เลือกช่วงเวลา, ผู้ให้บริการ, congestion-control protocol
- วิเคราะห์ผลกระทบของ server/site/location ที่ MLab ตั้งอยู่ (ตำแหน่ง server ก็มีผลต่อผลวัด ไม่ใช่แค่ฝั่งลูกค้า)
- แสดงว่า congestion control protocol ที่พัฒนาในช่วงหลายปีที่ผ่านมาให้ผลลัพธ์ดีขึ้นจริงตามที่ออกแบบไว้
- ระบุผลกระทบของ COVID-19 lockdown ต่อประสิทธิภาพอินเทอร์เน็ต — พบว่าเสื่อมลงแค่บางส่วน ไม่ใช่ทั้งระบบ
- เปรียบเทียบ ISP และวิวัฒนาการช่วง busy hours

---

## 2. ข้อมูลและวิธีการ (Materials & Methods)

### 2.1 NDT คืออะไร
NDT (Network Diagnostic Test) มี 3 เวอร์ชัน: เวอร์ชันแรกใช้ web100 Linux kernel + TCP Reno (ก.พ. 2009 – พ.ย. 2019), NDT5 เริ่ม ก.ค. 2019 ใช้ TCP Cubic, NDT7 เริ่ม ก.พ. 2020 ใช้ TCP BBR เป็นค่าเริ่มต้น (ถ้าไม่มีจะ fallback เป็น Cubic) ทุกเวอร์ชันสร้าง TCP connection ระหว่าง MLab server กับ client วัดความเร็วเฉลี่ยและ latency (RTT) จากค่าสถิติภายใน TCP stack

**Congestion control protocols ที่เกี่ยวข้อง:**
- **TCP Reno** — protocol ดั้งเดิม
- **TCP Cubic** — พัฒนาเพื่อใช้ bandwidth ได้เต็มที่แม้ latency สูง (high-speed network)
- **TCP BBR** — เน้นลด queue/buffer ในเส้นทาง เพื่อลด delay (แก้ปัญหา "bufferbloat")

ข้อมูลที่ใช้มาจากตาราง BigQuery `measurement-lab.ndt.unified_downloads` ซึ่งกรองแล้ว: โอนข้อมูลอย่างน้อย 8KB, ทดสอบนาน 9-60 วินาที, ตรวจพบ congestion (ทดสอบเต็มความสามารถลิงก์จริง), ไม่รวม test ที่ผล NULL หรือมาจากเครื่องข่ายภายในของ MLab เอง

### 2.2 ตำแหน่ง server ในเยอรมนี
MLab มี server 2 ที่ในเยอรมนี: **Frankfurt** (6 sites ใน AS ต่างกัน — Telia, GTT, Vodafone, Level3, Tata, Telecom Italia Sparkle) และ **Hamburg** (1 site, Telia) แต่ละ site มีเครื่อง 4 ตัว (1 test + 3 production) เชื่อมด้วย 10G, 16 core

ขอบเขตการศึกษา: ผู้ใช้ในเยอรมนี ช่วง ม.ค. 2019 – ส.ค. 2021

### 2.3 Threats to Validity (ข้อจำกัดของวิธีวัด)
- ผลวัดสะท้อน**เส้นทางทั้งหมด** client→server ไม่ใช่แค่ access network เพียงอย่างเดียว — คอขวดอาจอยู่ที่ WiFi บ้าน หรือ transit network ก็ได้
- ผลเป็น **lower bound** เพราะ TCP connection เดียวอาจไม่ใช้ capacity เต็มที่ (โดยเฉพาะช่วง slow-start)
- ข้อมูลเป็น **convenience sampling** ไม่ใช่ random sample — คนที่สนใจเน็ตมักเป็นคนทดสอบบ่อย ต้องตีความอย่างระมัดระวัง

---

## 3. ผลการศึกษา (Results)

### 3.1 ISP ยอดนิยมในเยอรมนี
3 ผู้ให้บริการระดับประเทศ (Deutsche Telekom, Vodafone, Telefonica) ครองสัดส่วนวัด ~71-75% ของทั้งหมด ทั้งที่ Frankfurt และ Hamburg งานวิจัยจำกัดการวิเคราะห์ไว้ที่ 10 ISP ยอดนิยมต่อ location (ครอบคลุม ~90% ของการวัดทั้งหมด)

### 3.2 Busy Hours และ Busy Days
วิเคราะห์จำนวนการวัดและ IP ที่ active ต่อชั่วโมง พบรูปแบบชัดเจนสำหรับ **TCP BBR**: peak ที่ 20:00 น. (2 ทุ่ม) — งานวิจัยกำหนด busy hour = 20:00-22:00

ในทางกลับกัน **TCP Cubic** ไม่มี peak ชัดเจน แต่มีรูปแบบลดลงเป็นช่วงๆ ทุก 6 ชม. (ตี 1, 7 โมงเช้า, บ่ายโมง, 1 ทุ่ม) — ข้อสรุป: ผู้ใช้ TCP Cubic ส่วนใหญ่คือ**ระบบทดสอบอัตโนมัติ** (ยังใช้ NDT5 รุ่นเก่า) ไม่ใช่พฤติกรรมผู้ใช้จริงแบบ TCP BBR (มาจาก NDT7 ที่ end-user ใช้จริง)

พบว่า 1 IP อาจทำ measurement หลายครั้งในชั่วโมงเดียว (สูงสุด 175 ครั้งใน 1 ชม.!) — 50% ของการวัดทั้งหมดมาจาก IP ที่ทำซ้ำหลายครั้ง แต่พฤติกรรมนี้ใกล้เคียงกันทุก ISP จึงไม่ตัดออกจากการวิเคราะห์

**ผลต่อความเร็ว:** TCP Cubic เร็วกว่า TCP BBR อย่างชัดเจนในทุกชั่วโมง (~90 Mbps เทียบ ~25-30 Mbps) — แต่ TCP BBR มี RTT ต่ำกว่า (~15-17ms เทียบ Cubic ~14-25ms) เพราะ TCP Cubic วัดจากผู้ใช้กลุ่มน้อยที่ throughput สูงเป็นพิเศษ (ไม่ใช่ตัวแทนพฤติกรรมทั่วไป)

### 3.3 ตำแหน่ง MLab ในเยอรมนี — ผลกระทบ COVID-19
เปรียบเทียบ ม.ค. 2020 (ก่อน lockdown), มี.ค. 2020 (ต้น lockdown), มี.ค. 2021, ส.ค. 2021 พบว่า**เฉพาะ 2 sites ใน Frankfurt (fra04, fra05) เท่านั้น**ที่ประสิทธิภาพลดลงชัดเจนช่วง lockdown — throughput ตกฮวบ (บาง AS เหลือต่ำกว่า 5-8 Mbps) และ RTT เพิ่มขึ้นหลาย ms ปี 2021 ผลกระทบนี้หายไปแล้ว แสดงว่าเครือข่ายขยาย capacity ทันความต้องการ

**สรุป: ผลกระทบ COVID-19 มีจริงแต่เป็นแค่บางส่วน (partial) เฉพาะบาง AS ไม่ใช่ทั่วประเทศ**

### 3.4 วิวัฒนาการของ Congestion Control Protocol
TCP Reno ครองตลาดจนถึง พ.ย. 2019, ตามด้วย TCP Cubic, และ TCP BBR ตั้งแต่ ก.ค.-ส.ค. 2020 การเปลี่ยนจาก Reno→Cubic เพิ่ม throughput ชัดเจน (สอดคล้องเป้าหมายออกแบบของ Cubic) การเปลี่ยนจาก Cubic→BBR ทำให้ RTT ลดลง (สอดคล้องเป้าหมายของ BBR ที่ลด buffering) — **สรุป: protocol ทำงานตามที่ออกแบบไว้จริง เมื่อดูจากข้อมูลจริงในโลก (ไม่ใช่แค่ lab)**

### 3.5 เปรียบเทียบ ISP
6 ผู้ให้บริการที่พบทั้ง 2 location มีผลต่างกันมาก ISP ที่มี ASN 3209 ดีขึ้นชัดเจนที่สุด (throughput เพิ่ม ~3 เท่า, RTT ลดลงเกือบครึ่ง) ISP ที่ให้บริการ fiber-to-home อย่างเดียว (ASN 60294) มีประสิทธิภาพดีเด่น ส่วน ISP ที่มี RTT ต่ำสุด (ASN 15943) อาจเป็นเพราะพื้นที่ให้บริการอยู่ใกล้ Hamburg (ใกล้ server) มากกว่าปัจจัยด้านคุณภาพเครือข่ายจริง

---

## 4. เกณฑ์ "ดีพอหรือไม่" — ส่วนที่เกี่ยวข้องกับโปรเจกต์เรามากที่สุด

**Table 5 (หน้า 17): Exemplary application requirements**

| แอปพลิเคชัน | Data Rate ที่ต้องการ | Latency ที่ต้องการ |
|---|---|---|
| Voice (โทรศัพท์) | 64 kbps | 200 ms |
| Video streaming (HD) | 5 Mbps | ไม่กี่วินาที |
| Video streaming (UHD) | 25 Mbps | ไม่กี่วินาที |
| Cloud gaming | 44 Mbps | 25 ms |

ผู้เขียนนำผลวัดจริง (ส.ค. 2021) มาเทียบกับตารางนี้ พบว่า: **latency** (ประมาณจากครึ่งหนึ่งของ RTT) เพียงพอสำหรับทุกแอปพลิเคชันในกลุ่มตัวอย่าง 75th percentile — แต่ **throughput** ต่างออกไป: ราวครึ่งหนึ่งของการวัดผ่านเกณฑ์ 25 Mbps (UHD) น้อยกว่านั้นที่ผ่านเกณฑ์ cloud gaming แต่มากกว่า 75% ผ่านเกณฑ์ HD (5 Mbps)

ข้อควรระวังที่ผู้เขียนเน้นย้ำ: **RTT ที่วัดได้เป็นค่า TCP** แต่แอปพลิเคชัน real-time จริง (เสียง/เกม) มักใช้ UDP/RTP ไม่ใช่ TCP — ตัวเลขจาก NDT จึงเป็น**ค่าประมาณ**ของ propagation + processing delay เท่านั้น ไม่ใช่ latency จริงที่แอปนั้นๆ จะได้รับ

---

## 5. บทสรุปงานวิจัย (Conclusion)

- การวิเคราะห์ MLab ต้อง "confine" ข้อมูลอย่างเป็นระบบก่อน (เลือก ISP, ช่วงเวลา, congestion protocol) มิฉะนั้นจะได้ผลลัพธ์ที่บิดเบือน
- busy hour ของเยอรมนี = ช่วงเย็น (20:00-22:00), busy day = วันจันทร์
- ตำแหน่ง/AS ของ server มีผลเล็กน้อยต่อผลวัด ยกเว้นช่วง COVID lockdown ที่บาง AS กระทบหนักกว่า
- protocol congestion control ที่พัฒนาขึ้น (Reno→Cubic→BBR) ให้ผลตามที่ออกแบบไว้จริง
- ISP ที่ให้บริการ fiber ล้วนมีประสิทธิภาพเหนือกว่า ISP ที่ผสมเทคโนโลยี

**ข้อมูลเปิด:** สคริปต์และข้อมูลทั้งหมดอยู่ที่ https://gitlab.com/ralfluebben/mlab_germany_2021_data

---

## ทำไมบทความนี้เกี่ยวกับโปรเจกต์เรา

1. **Table 5** คือหนึ่งในเกณฑ์ "ดี/แย่" เชิงปริมาณที่ใช้อ้างอิงได้ — เทียบเท่ากับที่ Clark & Wedeman (2022) เสนอเป็น SSL framework และ FCC เสนอเป็น 100/20 Mbps benchmark
2. วิธี "confine ข้อมูลเป็น subset ตัวแทน" (เลือก busy hour, ISP ยอดนิยม, congestion protocol ที่ predominant ต่อช่วงเวลา) เป็นแนวทางที่ `vietnam_ndt7_prep.ipynb`/`cambodia_ndt7_prep.ipynb` เราเองก็ใช้หลักการคล้ายกัน (reliability threshold `total_tests>=100 & n_tiles>=5`)
3. เตือนเรื่อง **RTT จาก TCP ≠ latency จริงของแอป real-time** — ข้อควรระวังที่ควรใส่ใน Limitations section ของ `paper_draft.md` เช่นกัน ถ้าจะอ้างอิง latency ของเราไปเทียบกับ voice/gaming requirement
