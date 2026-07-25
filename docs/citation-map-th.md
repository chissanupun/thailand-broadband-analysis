# แผนที่การอ้างอิง — paper ไหนใช้ตรงไหน (ฉบับภาษาไทย)

เอกสารช่วยตอนเขียน draft ไม่ใช่บรรณานุกรมฉบับสมบูรณ์ · สำหรับแต่ละ section ของ `paper_draft.md`
ไฟล์นี้บอกว่าใช้ PDF ฉบับไหนใน `docs/` หนุน และหนุนข้อความว่าอะไร · เติม citation ทีละช่องพอ
(ฉบับอังกฤษ: [`citation-map.md`](citation-map.md))

**สถานะกองเอกสาร:** มี paper วิชาการ 16 ฉบับจัดโฟลเดอร์ `docs/01–05` แล้ว — ถือว่า **related work
แข็งพอส่ง journal ได้** งานที่เหลือคือ *เอาไปวางให้ถูกที่* ไม่ใช่หาเพิ่ม · ที่ยังขาด 2 ฉบับ
(ติด paywall ขอผ่านห้องสมุด) ไม่มีอันไหนวิกฤต — ทุก section มีของอ้างครบ

---

## แยกตาม section ของ draft

### §1 บทนำ (Introduction)

| ข้อความในเนื้อหา | อ้าง | ไฟล์ |
|---|---|---|
| เน็ตดันเศรษฐกิจ (penetration 10% → GDP 1–3%) | Röller & Waverman 2001 · **Sridhar & Sridhar 2007** | `05-thailand-context/sridhar-2007-…` |
| "อันดับดีแต่คนบ่น" — ความขัดแย้งแกนหลักของ paper | **Stocker & Whalley 2018** | `04-benchmarks-theory/stocker-whalley-2018-…` |
| ช่องว่าง: ยังไม่มีงานไทยวัด *คุณภาพ* ด้วยข้อมูลจริง | **Setthasuravich 2024** · Denfanapapol 2024 | `05-thailand-context/` |
| framework เทียบ Ookla กับ NDT7 | **MacMillan 2023** | `03-cross-platform/macmillan-2023-…` |

> Röller-Waverman ใช้ 21 ประเทศ OECD · **Sridhar 2007 ใช้ประเทศกำลังพัฒนา** ใกล้บริบทไทยกว่า
> ใช้คู่กันหรือใช้แทนได้ · ตัว Röller-Waverman เองไม่มีในโฟลเดอร์ (ติด paywall)

### §1.2 / §1.3 สมมติฐาน & ขอบเขต

| ข้อความ | อ้าง | ไฟล์ |
|---|---|---|
| คุณภาพต่างตามพื้นที่/ประเภทเครือข่าย ไม่มีคำตอบเดียวทั้งประเทศ | Stocker & Whalley 2018 | `04-…` |
| งาน digital divide ไทยก่อนหน้า เน้น *การเข้าถึง* ระดับตำบล/จังหวัด | Setthasuravich 2024 (ตำบล) · Denfanapapol 2024 (จังหวัด) | `05-…` |

### §2 ข้อมูล (Data)

| ข้อความ | อ้าง | ไฟล์ |
|---|---|---|
| ใช้ Ookla tiles ทำงานวิเคราะห์เอเชียแปซิฟิก (precedent) | **'Ofa & Aparicio / ESCAP 2021** | `01-ookla/ofa-aparicio-2021-…` |
| คำอธิบาย platform M-Lab NDT7 | **Gill 2022** (เป็น editorial ไม่ peer-reviewed — อ้างได้เฉพาะตัว platform) | `02-ndt7-mlab/gill-2022-…` |
| EDA ด้วย M-Lab รายประเทศ เป็น design ที่มีคนทำแล้ว | Lübben & Misfeld 2022 (เยอรมนี) | `02-ndt7-mlab/lubben-misfeld-2022-…` |

### §3.2 การเปรียบเทียบข้ามประเทศ

| ข้อความ | อ้าง | ไฟล์ |
|---|---|---|
| วิธีวัดความเหลื่อมล้ำเชิงพื้นที่ด้วย speed test | **Caldas / OECD 2023** | `01-ookla/caldas-2023-…` |
| ใช้ Ookla เทียบข้ามภูมิภาคในเอเชียแปซิฟิก | 'Ofa / ESCAP 2021 | `01-ookla/ofa-aparicio-2021-…` |

### §3.3 Cross-validation Ookla กับ NDT7 (ตัว novelty)

| ข้อความ | อ้าง | ไฟล์ |
|---|---|---|
| สองแหล่งต่างกันทั้งวิธีวัดและขนาดค่า | **MacMillan 2023** (อ้างอิงหลัก) | `03-cross-platform/macmillan-2023-…` |
| การ validate ข้าม platform เป็นวิธีที่มีจริง | Lipphardt 2025 (M-Lab vs Cloudflare) | `03-cross-platform/lipphardt-2025-…` |
| ข้อมูล crowdsource ต้องแก้ bias | Lee 2023 | `01-ookla/lee-2023-…` |
| ใช้ M-Lab big data เทียบ ISP ได้ (เหมือน Part 8 ของเรา) | Deng 2021 | `02-ndt7-mlab/deng-2021-…` |

> ⚠️ **เช็คก่อนอ้าง** — draft §3.3 (บรรทัด 153) และ §1.3 (บรรทัด 36) เขียนว่า NDT7 เป็น
> "passive/background test" และ MacMillan พบว่า NDT7 "underreport 12–56%" · **ทั้งสองจุดดูจะผิด**
> เทียบกับ paper จริง (NDT7 เป็น *active* single-stream; ช่องว่างเกิดหลัก ๆ ตอน RTT สูง) ·
> อ่าน `macmillan-2023-ookla-vs-ndt7.pdf` แล้วแก้สองประโยคนี้ก่อนแปะ citation ไม่งั้น reviewer
> ที่รู้จัก paper นี้จับได้

### §3.6 การตรวจจับความผิดปกติ / divergence

| ข้อความ | อ้าง | ไฟล์ |
|---|---|---|
| ความเหลื่อมล้ำเชิงประสิทธิภาพระหว่างผู้ใช้ (กรอบ divergence) | **Paul 2021** | `01-ookla/paul-2021-…` |
| การแก้ sampling bias หนุนการใช้ `is_reliable` / ถ่วงน้ำหนัก | Lee 2023 | `01-ookla/lee-2023-…` |

### เกณฑ์ตัดสิน "good or bad" (Objective 4)

| ข้อความ | อ้าง | ไฟล์ |
|---|---|---|
| "แบนด์วิดท์เท่าไหร่ถึงพอ" — เกณฑ์ตามการใช้งาน | **Clark & Wedeman 2022** | `04-…/clark-wedeman-2022-…` |
| นิยาม broadband ปัจจุบัน = 100/20 Mbps เป้า 1000/500 | **FCC 2024** (factsheet + รายงาน §706) | `04-…/fcc-2024-…` |
| เร็วอย่างเดียวไม่เท่ากับประสบการณ์ดี | Stocker & Whalley 2018 | `04-…/stocker-whalley-2018-…` |

---

## 16 ฉบับ แยกตามโฟลเดอร์

- **01-ookla/** — Paul 2021 · Lee 2023 (bias-correction) · Caldas/OECD 2023 · 'Ofa/ESCAP 2021
- **02-ndt7-mlab/** — Gill 2022 (platform) · Lübben-Misfeld 2022 (EDA เยอรมนี) · Deng 2021 (เทียบ ISP)
- **03-cross-platform/** — MacMillan 2023 (Ookla vs NDT7) · Lipphardt 2025 (M-Lab vs Cloudflare)
- **04-benchmarks-theory/** — Clark-Wedeman 2022 · Stocker-Whalley 2018 · FCC 2024 (×2)
- **05-thailand-context/** — Setthasuravich 2024 (ตำบล) · Denfanapapol 2024 (จังหวัด) · Sridhar 2007

## ที่ยังขาด (ไม่บล็อกงาน)

- Röller & Waverman 2001 (AER, ติด paywall) — อ้างใน draft อยู่แล้ว · Sridhar 2007 หนุนประเด็นเดียวกัน
- ITU Facts & Figures 2024 — อ้างใน draft แล้ว · เป็นแหล่งเรื่องการเข้าถึง/ราคา **ไม่ใช่** เกณฑ์ความเร็ว
  อย่าเอาไปอ้างเป็นเส้นตัด "good/bad" ของความเร็ว — ใช้ FCC / Clark-Wedeman แทน
