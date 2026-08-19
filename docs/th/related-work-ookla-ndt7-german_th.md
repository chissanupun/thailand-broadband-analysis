# Related Work ฉบับร่าง — Ookla, NDT7, งานเยอรมนี

เอกสารนี้เป็นชิ้นส่วนของ Related Work (`paper_draft.md` §2 Motivation & Background) เรียบเรียงเป็นภาษาไทยก่อนตามธรรมเนียมของโปรเจกต์นี้ — Thai ก่อน English ทีหลัง คุมเฉพาะสามหัวข้อที่คุยกันรอบนี้คือ Ookla, NDT7, และงานของ Lübben & Misfeld (เยอรมนี) ส่วน digital divide กับ market concentration ที่เป็นอีกสองย่อหน้าใน §2 ฉบับอังกฤษยังไม่รวมเข้ามา รอบหน้าค่อยว่ากัน

Citation ทั้งหมดตรงกับ `citation-map-th.md` — อันไหนยังไม่มี full citation ในไฟล์นี้ วงเล็บกำกับไว้ว่า "รอเติมจาก PDF"

---

## Ookla คืออะไร

Ookla เป็นเจ้าของ Speedtest แอปและเว็บวัดความเร็วเน็ตที่คนทั่วไปรู้จักกันดี ตัวทดสอบเป็นแบบ active ต้องมีคนกดเริ่มเองถึงจะยิง traffic ออกไปวัด และเลือกเซิร์ฟเวอร์ปลายทางจากความใกล้ของผู้ใช้เป็นหลัก ผลที่ได้จึงเอียงไปทาง "ความเร็วสูงสุดที่เครือข่ายทำได้ในสภาพที่ดี" มากกว่าประสบการณ์เฉลี่ยของคนทั่วไปกลางวันธรรมดา

ข้อมูลที่งานนี้ใช้คือ **Ookla Open Data** ชุด tile รายไตรมาส ครอบคลุมทั้ง fixed และ mobile แบ่งพื้นที่เป็น Quadkey zoom 16 (ราว 610×610 เมตรต่อ tile) แต่ละ tile มีค่าเฉลี่ย download, upload, latency พร้อมจำนวนการทดสอบ (submission count) กำกับไว้ ดึงมาตั้งแต่ Q1 2023 ถึง Q4 2025 รวม 12 ไตรมาส ครบทั้ง 9 ประเทศทั้งสองผลิตภัณฑ์ เผยแพร่ภายใต้สัญญาอนุญาต CC BY-NC-SA 4.0

เอา Ookla tile มาทำงานวิเคราะห์ระดับภูมิภาคไม่ใช่เรื่องใหม่ 'Ofa และ Aparicio (ESCAP, 2021 — รอเติมจาก PDF) ใช้ชุดข้อมูลเดียวกันนี้เทียบทั่วเอเชียแปซิฟิก ส่วน Caldas (OECD, 2023 — รอเติมจาก PDF) ใช้วัดความเหลื่อมล้ำเชิงพื้นที่ในกลุ่มประเทศ OECD งานทั้งสองยืนยันว่า tile ระดับนี้เอาไปเทียบข้ามประเทศได้จริง แต่ทั้งคู่ไม่ได้แตะเรื่องช่วงเวลา (peak-hour) หรือโครงสร้างตลาดผู้ให้บริการ — ตรงนี้แหละที่งานนี้ไปต่อ

## NDT7 คืออะไร

NDT7 (Network Diagnostic Test เวอร์ชัน 7) เป็นแพลตฟอร์มวัดของ **Measurement Lab (M-Lab)** กลไกต่างจาก Ookla ตรงที่ NDT7 ยิง TCP stream เดี่ยว (single-stream) ไปยังเซิร์ฟเวอร์ในฟลีตของ M-Lab เอง ซึ่งมีจำนวนน้อยและกระจายตัวน้อยกว่าเซิร์ฟเวอร์ของ Ookla มาก ผู้ใช้จำนวนไม่น้อยจึงไม่ได้วัดกับเซิร์ฟเวอร์ในประเทศตัวเอง แต่วัดข้ามพรมแดนไปยังจุดที่ M-Lab มีเซิร์ฟเวอร์ตั้งอยู่

จุดนี้เจอเองตรง ๆ ในข้อมูลของงานนี้ — ไล่ log แล้วพบว่าไทย กัมพูชา มาเลเซีย วิ่งไปลง sin01 (สิงคโปร์) เป็นหลัก ลาวกับเวียดนามวิ่งไป hkg03 (ฮ่องกง) เมียนมาวิ่งไป maa01 (เจนไน) มีฟิลิปปินส์ประเทศเดียวที่วัดกับเซิร์ฟเวอร์ในประเทศตัวเองจริง (mnl01/mnl02 รวมกัน 94.6%) ระยะทางแสงไปสิงคโปร์อย่างเดียวก็กิน RTT ราว 20 ms แล้ว เกณฑ์ cloud-gaming latency ≤25 ms จึงวัดไม่ได้จริงจาก NDT7 ในประเทศส่วนใหญ่ของงานนี้ นี่คือเหตุผลที่ RQ1 ใช้ Ookla สำหรับตัวเลข cloud-gaming แทน

สิ่งที่ NDT7 ให้ได้แต่ Ookla ให้ไม่ได้คือ timestamp และ IP ของผู้ทดสอบระดับ per-test ไม่ใช่ค่าเฉลี่ยรายไตรมาสแบบ tile เอาไป join กับ ASN หา ISP ได้ (ผ่าน ip-api) ดูช่วงเวลาทดสอบได้ด้วย — ตรงนี้เองที่เปิดทาง RQ3 (peak-hour) และ RQ4 (โครงสร้างตลาด ISP) ซึ่ง Ookla tile แบบค่าเฉลี่ยไตรมาสทำไม่ได้เลย

งานที่เคยเอา M-Lab มาเทียบ ISP มาก่อนคือ Deng และคณะ (2021 — รอเติมจาก PDF) ส่วนคำอธิบายตัวแพลตฟอร์มเองอ้างจาก Gill (2022 — รอเติมจาก PDF) ซึ่งเป็นบทความ editorial ไม่ใช่ peer-reviewed จึงอ้างได้แค่ระดับอธิบายว่า platform คืออะไร ไม่ใช่ผลวิจัย

### เทียบสองแพลตฟอร์มเข้าด้วยกัน — MacMillan et al. (2023)

MacMillan และคณะ (2023) เป็นงานที่ใกล้เคียงวิธีของเราที่สุดในแง่การตรวจสอบข้ามแพลตฟอร์ม เขาเทียบ Ookla กับ NDT7 ตรง ๆ พบว่า NDT7 รายงานความเร็วต่ำกว่า Ookla อย่างสม่ำเสมอ ช่องว่างกว้างขึ้นเมื่อ RTT สูง ตรงกับกลไกที่อธิบายไว้ข้างต้นพอดี — Ookla เป็น active/proximity-based ส่วน NDT7 ยิงไป single-stream server fleet เล็ก ข้อสรุปที่ใช้ได้จากงานนี้คือ ตัวเลขดิบของสองแพลตฟอร์มเอามา pool กันตรง ๆ ไม่ได้ แต่**อันดับ** (ranking) ยังเทียบกันได้อยู่ นี่คือวิธีที่งานนี้ใช้ตรวจสอบความสอดคล้องข้ามแหล่งใน §8.3

## งานที่ใกล้เคียงที่สุด — Lübben & Misfeld (2022), เยอรมนี

ถ้าจะหางานเดียวที่ใกล้เคียงกับ paper นี้ที่สุด คืองานของ Ralf Lübben และ Nico Misfeld (Flensburg University of Applied Sciences) ตีพิมพ์ใน Electronics 2022, 11, 162 ชื่อ *Exploring the Measurement Lab Open Dataset for Internet Performance Evaluation: The German Internet Landscape* เขาใช้ M-Lab NDT ชุดเดียวกับที่งานนี้ใช้ วิเคราะห์เฉพาะเยอรมนีประเทศเดียว ช่วง ม.ค. 2019 – ส.ค. 2021 แต่ให้สองสิ่งที่งานนี้ยืมมาใช้ตรง ๆ

อย่างแรกคือ**เกณฑ์ตามการใช้งานจริง** (Table 5 ของเขา, หน้า 17) แทนที่จะถามว่า "60 Mbps เร็วหรือช้า" ซึ่งตอบไม่ได้ถ้าไม่มีจุดอ้างอิง เขาตั้งพื้นเกณฑ์ throughput และ latency ของแอปแต่ละประเภทไว้ล่วงหน้า:

| แอปพลิเคชัน | Data Rate ที่ต้องการ | Latency ที่ต้องการ |
|---|---|---|
| Voice (โทรศัพท์) | 64 kbps | 200 ms |
| Video streaming (HD) | 5 Mbps | ไม่กี่วินาที |
| Video streaming (UHD) | 25 Mbps | ไม่กี่วินาที |
| Cloud gaming | 44 Mbps | 25 ms |

แล้วถามแทนว่า "ความเร็วที่มี รองรับแอปที่คนใช้จริงได้ไหม" — งานนี้เอาตารางเดียวกันมาเป็นมาตรฐานของ RQ1 ทั้งหมด (ตัวเลข UHD ของ Netflix ที่เขาใช้คือ 25 Mbps ตอนตีพิมพ์ปี 2022 ปัจจุบัน Netflix ปรับเหลือ 15 Mbps แล้ว งานนี้บันทึกความต่างไว้ใน §3.4 และตารางที่ 2)

อย่างที่สองคือ**วิธีหา busy hour** จาก §4.2 ของเขา ใช้ปริมาณการทดสอบ (measurement volume) หาว่าชั่วโมงไหนเป็น peak แล้วถามว่าความเร็วที่วัดได้ตกลงในช่วงนั้นหรือไม่ พร้อม diagnostic แยกว่า traffic ที่เห็นเป็นคนใช้งานจริงหรือเป็น automated test (เยอรมนีใช้ TCP congestion-control protocol เป็นตัวแยก — BBR มี peak ชัดที่ 20:00–22:00 สะท้อนพฤติกรรมคนจริง ส่วน Cubic ไม่มี peak แต่ลดเป็นช่วง ๆ ทุก 6 ชั่วโมง เข้าเค้าว่าเป็นระบบทดสอบอัตโนมัติ) ออกแบบชุดนี้ถูกยกมาใช้ทั้งหมดใน RQ3 (§6) ของงานนี้ แม้ diagnostic ตัวช่วยแยกจะต่างกันเพราะ TCP protocol ของแต่ละประเทศไม่ได้ log ไว้ในข้อมูลชุดนี้

พูดได้ว่างานนี้เป็นการขยายงานของ Lübben & Misfeld ออกไปสามทาง จากหนึ่งประเทศเป็นเก้าประเทศ จากแพลตฟอร์มเดียว (NDT) เป็นสองแพลตฟอร์ม (เติม Ookla เข้ามาแล้ววัดว่าสองแหล่งเห็นต่างกันแค่ไหน ผ่านงานของ MacMillan et al. ข้างต้น) และจากภาพระดับประเทศ ขยายลงไปถึงระดับพื้นที่ย่อยกับโครงสร้างตลาดผู้ให้บริการ ซึ่งงานต้นทางที่มองแค่ระดับประเทศเดียวไม่ได้แตะ

---

## รายการอ้างอิง

- Ookla. (2023). *Speedtest by Ookla Global Fixed and Mobile Network Performance Maps* [Dataset]. https://github.com/teamookla/ookla-open-data
- M-Lab. (2025). *Measurement Lab NDT7 Data*. https://www.measurementlab.net/data/docs/bq/quickstart/
- MacMillan, K., Mangla, T., Saxon, J., Marwell, N. P., & Feamster, N. (2023). *A Comparative Analysis of Ookla Speedtest and Measurement Lab's Network Diagnostic Test (NDT7)*. Proceedings of the ACM on Measurement and Analysis of Computing Systems, 7(1), Article 19. https://dl.acm.org/doi/epdf/10.1145/3579448
- Lübben, R., & Misfeld, N. (2022). *Exploring the Measurement Lab Open Dataset for Internet Performance Evaluation: The German Internet Landscape*. Electronics, 11(1), 162. https://doi.org/10.3390/electronics11010162
- 'Ofa, S. V., & Aparicio, S. (2021). *Visualizing Broadband Speeds in Asia-Pacific* [ESCAP]. — full citation รอเติมจาก `docs/01-ookla/ofa-aparicio-2021-escap-visualizing-broadband-speeds-asiapacific.pdf`
- Caldas, ... (2023). *OECD Spatial Disparities in Speed Tests*. — full citation รอเติมจาก `docs/01-ookla/caldas-2023-oecd-spatial-disparities-speed-tests.pdf`
- Gill, ... (2022). *M-Lab Platform* [CCR]. — full citation รอเติมจาก `docs/02-ndt7-mlab/gill-2022-mlab-platform-ccr.pdf`
- Deng, ... (2021). *Comparing ISP Performance via M-Lab*. — full citation รอเติมจาก `docs/02-ndt7-mlab/deng-2021-comparing-isp-performance-mlab.pdf`

ยืนยันครบแล้ว: Ookla, M-Lab, MacMillan, Lübben-Misfeld — อยู่ใน References list ของ `paper_draft.md` อยู่แล้ว ตัวที่ยังไม่ครบ (Ofa, Caldas, Gill, Deng) ต้องเปิด PDF คัด author เต็ม/journal/หน้า ก่อนพอร์ตเข้า `paper.tex`
