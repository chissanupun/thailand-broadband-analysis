"""Generate HTML slide deck from Ookla EDA outputs."""
import base64, pathlib

OUTDIR = pathlib.Path(__file__).parent / 'ookla'
OUT_HTML = pathlib.Path(__file__).parent / 'slides.html'

def img_b64(name):
    p = OUTDIR / name
    if not p.exists():
        return None
    data = base64.b64encode(p.read_bytes()).decode()
    return f"data:image/png;base64,{data}"

SLIDES = [
    {
        'type': 'title',
        'title': 'อินเทอร์เน็ตบรอดแบนด์ไทย',
        'subtitle': 'วิเคราะห์ระดับจังหวัด ปี 2023–2025',
        'meta': 'ข้อมูล: Ookla Open Data (Fixed Broadband) · 77 จังหวัด · 11 ไตรมาส',
    },
    {
        'type': 'text',
        'title': 'ข้อมูลที่ใช้',
        'bullets': [
            '<b>Ookla Speedtest Intelligence</b> — ข้อมูล Fixed Broadband ระดับ tile (~610×610 ม.)',
            '<b>ช่วงเวลา:</b> Q1 2023 – Q4 2025 (11 ไตรมาส)',
            '<b>ขอบเขต:</b> 77 จังหวัดทั่วประเทศไทย รวม 847 แถวข้อมูล',
            '<b>ตัวชี้วัดหลัก:</b> ความเร็ว Download/Upload (Mbps), Latency (ms), จำนวน Speedtest',
            '<b>ข้อจำกัด:</b> วัดจากคนที่กด Speedtest เท่านั้น — ไม่ครอบคลุมทุกครัวเรือน',
        ],
    },
    {
        'type': 'image',
        'title': 'อันดับความเร็ว Download ต่อจังหวัด',
        'image': '01_province_ranking.png',
        'metric': 'วัดจากค่าเฉลี่ย Download Speed (Mbps) ตลอด 11 ไตรมาส ถ่วงน้ำหนักตามจำนวน Speedtest',
        'findings': [
            'กทม.และปริมณฑล (แดง) ครอง Top 10 — infrastructure หนาแน่นสุด',
            'ภาคอีสาน (เทา) กระจายตัวกลาง — ไม่ได้ช้าทุกจังหวัด',
            'แม่ฮ่องสอนช้าสุด (~130 Mbps) — ภูเขา/ชายแดน ไม่มี server ใกล้',
        ],
    },
    {
        'type': 'image',
        'title': 'ความเร็วรายไตรมาส (Heatmap)',
        'image': '02_heatmap.png',
        'metric': 'วัดจาก Download Speed เฉลี่ยต่อจังหวัดต่อไตรมาส — สีเข้ม = เร็วกว่า',
        'findings': [
            'ทุกจังหวัดมีแนวโน้มเร็วขึ้นเรื่อยๆ (สีเข้มขึ้นจากซ้ายไปขวา)',
            'Q4 2024 – Q1 2025 เห็น jump ชัดเจนในหลายจังหวัด',
            'ช่องว่างระหว่างจังหวัดเร็ว/ช้าลดลงตามเวลา — fiber ขยายตัว',
        ],
    },
    {
        'type': 'image',
        'title': 'ความเร็วแยกตามภูมิภาค (Boxplot)',
        'image': '03_regional_boxplot.png',
        'metric': 'วัดจาก Distribution ของ Download Speed ทุกจังหวัดในภาค — กล่อง = 25th–75th percentile',
        'findings': [
            'กทม.และปริมณฑล median สูงสุด แต่ spread น้อย (จังหวัดใกล้เคียงกัน)',
            'ภาคเหนือมี outlier สูง (จังหวัดเติบโตเร็ว) และต่ำ (แม่ฮ่องสอน)',
            'ภาคอีสาน spread กว้าง — บางจังหวัดเร็วเทียบเท่า BKK ได้แล้ว',
        ],
    },
    {
        'type': 'image',
        'title': 'แผนที่จังหวัดผิดปกติ (Anomaly Map)',
        'image': '04_anomaly_map.png',
        'metric': 'วัดจากการเปรียบเทียบความเร็วและ latency ของแต่ละจังหวัดกับค่าเฉลี่ยประเทศ — ถ้าห่างจากค่าเฉลี่ยมากเกินไป (เร็วหรือช้าผิดปกติ, latency สูงผิดปกติ, หรือความเร็วตกฮวบระหว่างไตรมาส) จะถูก flag ว่าผิดปกติ',
        'findings': [
            'สีน้ำเงินเข้ม = เร็ว · สีอ่อน = ช้า · ขอบแดง = ผิดปกติทางสถิติ',
            'จังหวัดชายแดนภาคเหนือ/ใต้มักถูก flag latency สูงผิดปกติ',
            'บางจังหวัดถูก flag เพราะเร็วผิดคาดเทียบกับ GDP (ลงทุน fiber หนัก)',
        ],
    },
    {
        'type': 'image',
        'title': 'การเติบโต 3 ปี: ใครเร็วขึ้นมากสุด?',
        'image': '06_growth_chart.png',
        'metric': 'วัดจาก % การเปลี่ยนแปลงของ Download Speed จาก Q1 2023 ถึง Q4 2025',
        'findings': [
            'เส้นดำ (0%) = ไม่เปลี่ยน · เส้นแดง = ค่าเฉลี่ยประเทศ',
            'จังหวัดชนบท (Tier 4) หลายแห่งโตเร็วกว่าค่าเฉลี่ย — catch-up growth',
            'จังหวัดที่โตช้า = baseline สูงอยู่แล้ว หรือ infrastructure ยังไม่ลงทุนเพิ่ม',
        ],
    },
    {
        'type': 'image',
        'title': '5 จังหวัดที่ผิดปกติที่สุด',
        'image': '05_deep_dive_divergent.png',
        'metric': 'วัดจาก Download/Upload trend และ Latency trend ตลอด 11 ไตรมาส รายจังหวัด',
        'findings': [
            '<b>แม่ฮ่องสอน</b> — ช้าสุดในภาคเหนือ, latency พุ่งสูง (ภูเขา/ชายแดน)',
            '<b>อุบลราชธานี</b> — Tier 4 แต่เร็วผิดคาด (+19% vs tier median) — AIS/True ลงทุนหนัก',
            '<b>พระนครศรีอยุธยา</b> — latency ต่ำผิดปกติ (5ms) — Ookla server อยู่ใกล้ ISP datacenter',
        ],
    },
    {
        'type': 'image',
        'title': 'GDP กับความเร็วอินเทอร์เน็ต',
        'image': '07_gdp_vs_speed.png',
        'metric': 'วัดจากการถดถอยเชิงเส้น (OLS) ระหว่าง GDP per capita กับ Download Speed เฉลี่ย — ความสัมพันธ์ r = 0.55',
        'findings': [
            'GDP อธิบายความเร็วได้แค่ 31% — ที่เหลือมาจาก infrastructure investment',
            'จังหวัดอีสานหลายแห่งเร็วกว่าที่ GDP คาด — fiber rollout ไม่ขึ้นกับความรวยของจังหวัด',
            'แม่ฮ่องสอน/สตูล/ตาก อยู่ต่ำกว่าเส้นทำนาย — geography เป็น blocker หลัก',
        ],
    },
    {
        'type': 'image',
        'title': 'UL/DL Ratio — หลักฐาน Fiber ทั่วประเทศ',
        'image': '19_uldl_symmetry_ratio.png',
        'metric': 'วัดจาก Upload หารด้วย Download — ถ้าอัปโหลดกับดาวน์โหลดใกล้เคียงกัน (ratio ใกล้ 1.0) แสดงว่าน่าจะเป็น Fiber เพราะ Fiber ให้ความเร็วสองทางสมมาตร ต่างจาก ADSL ที่อัปโหลดช้ากว่าดาวน์โหลดมาก (ratio ประมาณ 0.1–0.3)',
        'findings': [
            'ค่าเฉลี่ยประเทศ ~0.85 — บ่งชี้ว่า fiber แพร่หลายแม้จังหวัดชนบท',
            '<b>ข้อจำกัดสำคัญ:</b> ratio เป็นแค่ indirect proxy — Ookla ไม่แยก fiber/cable/ADSL',
            'กทม. ratio ต่ำกว่าชนบทบางจังหวัด — legacy infra ปนอยู่ในตึกเก่า',
        ],
    },
    {
        'type': 'image',
        'title': 'Tier Expectation Gap — ใครโดดออกจาก tier ตัวเอง',
        'image': '22_tier_expectation_gap.png',
        'metric': 'วัดจาก (Download จริง − Median ของ Tier) หารด้วย Median × 100% — บวก = เร็วกว่าที่ tier คาด, ลบ = ช้ากว่า',
        'findings': [
            '0% = เป็นไปตามคาดของ tier · บวก = overperform · ลบ = underperform',
            'นครปฐม +20%, อุบลราชธานี +19% — โดดออกจาก tier ตัวเองมากสุด',
            'Tier 4 หลายจังหวัดอีสาน overperform — สัญญาณ catch-up growth ชัดเจน',
        ],
    },
    {
        'type': 'image',
        'title': 'แผนที่ความผิดปกติ — จังหวัดไหนผิดปกติที่สุด?',
        'image': '27_divergence_map.png',
        'metric': 'วัดจาก Composite Divergence Score — ผลรวมค่าเบี่ยงเบนจากค่าคาดการณ์ใน 7 มิติ (ความเร็ว, latency, GDP, density, tier, UL/DL ratio, coverage)',
        'findings': [
            'ซ้าย: แดงเข้ม = ผิดปกติมาก (ไม่ว่าจะเร็วหรือช้า) · ขวา: น้ำเงินเข้ม = เร็วมาก',
            'ภาคเหนือบางจังหวัดแปลกมากแต่ไม่จำเป็นต้องเร็ว — outlier เพราะ geography',
            'ขอบแดง (Tier 1) อยู่ในกลุ่มน้ำเงินเข้ม · ขอบส้ม (Tier 4) บางส่วนก็น้ำเงินเข้มแล้ว',
        ],
    },
    {
        'type': 'image',
        'title': 'Test Coverage — ใครถูก Underrepresent ใน Data?',
        'image': '25_test_coverage.png',
        'metric': 'วัดจากจำนวน Speedtest เฉลี่ยต่อไตรมาส หารด้วยจำนวนประชากร คูณ 1,000',
        'findings': [
            'coverage ต่ำ = อาจเป็นเพราะ (1) เน็ตบ้านน้อย หรือ (2) คนไม่ใช้ Ookla app',
            'จังหวัด coverage ต่ำ — ค่าเฉลี่ยมาจากกลุ่มตัวอย่างน้อย ความน่าเชื่อถือต่ำกว่า',
            'Ookla data มี sampling bias ตาม tier/พื้นที่ ควรระบุในงานวิจัย',
        ],
    },
    {
        'type': 'text',
        'title': 'สรุปข้อค้นพบหลัก',
        'bullets': [
            '<b>ความเร็วเพิ่มขึ้นทุกจังหวัด</b> — Fiber rollout แพร่หลาย แม้จังหวัดชนบท',
            '<b>Catch-up growth ชัดเจน</b> — Tier 4 (ชนบท) โตเร็วกว่าค่าเฉลี่ยในหลายจังหวัด',
            '<b>GDP ไม่ใช่ตัวทำนายที่ดี</b> — r=0.55, อธิบายได้แค่ 31% — infrastructure investment สำคัญกว่า',
            '<b>Geography เป็น blocker หลัก</b> — แม่ฮ่องสอน/สตูล/ตาก ช้าเพราะพื้นที่ ไม่ใช่เพราะจน',
            '<b>ข้อจำกัด Ookla</b> — ไม่รู้เทคโนโลยี (fiber/cable/ADSL), ไม่แยกมือถือ/บ้าน, sampling bias',
        ],
    },
]

def build_slide_html(s, idx):
    t = s['type']
    if t == 'title':
        return f"""
<section class="slide title-slide" id="slide-{idx}">
  <div class="title-content">
    <h1>{s['title']}</h1>
    <p class="subtitle">{s['subtitle']}</p>
    <p class="meta">{s['meta']}</p>
  </div>
</section>"""

    if t == 'text':
        items = ''.join(f'<li>{b}</li>' for b in s['bullets'])
        return f"""
<section class="slide text-slide" id="slide-{idx}">
  <div class="text-inner">
    <h2>{s['title']}</h2>
    <ul class="bullets">{items}</ul>
  </div>
</section>"""

    if t == 'image':
        img_src = img_b64(s['image'])
        img_tag = f'<img src="{img_src}" alt="{s["title"]}">' if img_src else '<div class="img-missing">ไม่พบรูป</div>'
        items = ''.join(f'<li>{b}</li>' for b in s['findings'])
        return f"""
<section class="slide image-slide" id="slide-{idx}">
  <h2>{s['title']}</h2>
  <div class="slide-body">
    <div class="img-col">{img_tag}</div>
    <div class="text-col">
      <div class="metric-badge">{s['metric']}</div>
      <ul class="findings">{items}</ul>
    </div>
  </div>
</section>"""

    return ''

slides_html = '\n'.join(build_slide_html(s, i) for i, s in enumerate(SLIDES))
nav_dots = ''.join(f'<button class="dot" onclick="goTo({i})" title="Slide {i+1}"></button>' for i in range(len(SLIDES)))

html = f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Thailand Broadband Analysis 2023–2025</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600;700&family=IBM+Plex+Mono&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: 'IBM Plex Sans Thai', 'Segoe UI', sans-serif;
  background: #0d1117;
  color: #e6edf3;
}}

.deck {{ width: 100vw; height: 100vh; overflow: hidden; position: relative; }}

.slide {{
  display: none;
  width: 100%; height: 100vh;
  padding: 48px 72px 72px;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  animation: fadeIn .2s ease;
}}
.slide.active {{ display: flex; }}
@keyframes fadeIn {{ from {{ opacity:0; transform:translateY(6px) }} to {{ opacity:1; transform:translateY(0) }} }}

/* Title */
.title-slide {{
  background: #0d1117;
  text-align: center;
}}
.title-content {{ max-width: 860px; }}
.title-slide h1 {{
  font-size: 3rem; font-weight: 700;
  color: #f0f6fc;
  line-height: 1.25; margin-bottom: 24px;
  letter-spacing: -0.5px;
}}
.title-slide .subtitle {{
  font-size: 1.4rem; font-weight: 400;
  color: #8b949e; margin-bottom: 16px;
}}
.title-slide .meta {{
  font-size: 0.9rem; color: #484f58;
  font-family: 'IBM Plex Mono', monospace;
}}
.title-slide::after {{
  content: '';
  display: block;
  width: 64px; height: 3px;
  background: #58a6ff;
  margin: 28px auto 0;
}}

/* Text slide */
.text-slide {{ background: #0d1117; }}
.text-inner {{ width: 100%; max-width: 820px; }}
.text-slide h2 {{
  font-size: 1.75rem; font-weight: 600;
  color: #f0f6fc; margin-bottom: 32px;
  padding-bottom: 12px;
  border-bottom: 1px solid #21262d;
}}
.bullets {{ list-style: none; display: flex; flex-direction: column; gap: 14px; }}
.bullets li {{
  font-size: 1.05rem; line-height: 1.65;
  color: #c9d1d9;
  padding: 14px 20px;
  background: #161b22;
  border: 1px solid #21262d;
  border-radius: 6px;
}}

/* Image slide */
.image-slide {{ background: #0d1117; justify-content: flex-start; gap: 20px; align-items: stretch; }}
.image-slide h2 {{
  font-size: 1.5rem; font-weight: 600;
  color: #f0f6fc;
  flex-shrink: 0;
  width: 100%; max-width: 1200px;
  align-self: center;
  padding-bottom: 12px;
  border-bottom: 1px solid #21262d;
}}
.slide-body {{
  display: flex; gap: 32px;
  flex: 1; min-height: 0;
  width: 100%; max-width: 1200px;
  align-self: center;
}}
.img-col {{
  flex: 1.6; min-width: 0;
  display: flex; align-items: center; justify-content: center;
}}
.img-col img {{
  max-width: 100%; max-height: calc(100vh - 200px);
  object-fit: contain;
  border-radius: 6px;
  border: 1px solid #21262d;
}}
.img-missing {{ color: #484f58; font-size: 1rem; }}
.text-col {{
  flex: 1; display: flex; flex-direction: column;
  gap: 16px; justify-content: flex-start;
}}
.metric-badge {{
  background: #161b22;
  border: 1px solid #30363d;
  border-left: 3px solid #58a6ff;
  border-radius: 0 6px 6px 0;
  padding: 12px 16px;
  font-size: 0.85rem; color: #8b949e;
  line-height: 1.6;
  font-family: 'IBM Plex Mono', monospace;
}}
.findings {{ list-style: none; display: flex; flex-direction: column; gap: 10px; }}
.findings li {{
  font-size: 0.97rem; line-height: 1.6;
  color: #c9d1d9;
  padding: 10px 14px;
  background: #161b22;
  border: 1px solid #21262d;
  border-radius: 6px;
}}

/* Nav */
.nav {{
  position: fixed; bottom: 24px;
  left: 50%; transform: translateX(-50%);
  display: flex; gap: 8px; align-items: center; z-index: 100;
}}
.dot {{
  width: 8px; height: 8px; border-radius: 50%;
  border: none; background: #30363d;
  cursor: pointer; transition: all .2s;
}}
.dot.active {{ background: #58a6ff; transform: scale(1.4); }}
.nav-btn {{
  background: #161b22; border: 1px solid #30363d;
  color: #8b949e; font-size: 1.1rem;
  cursor: pointer; padding: 5px 14px; border-radius: 6px;
  transition: all .15s;
}}
.nav-btn:hover {{ background: #21262d; color: #f0f6fc; }}
.slide-counter {{
  position: fixed; top: 20px; right: 28px;
  font-size: 0.75rem; color: #484f58;
  font-family: 'IBM Plex Mono', monospace;
}}
</style>
</head>
<body>
<div class="deck">
{slides_html}
</div>
<div class="nav">
  <button class="nav-btn" onclick="prev()">&#8592;</button>
  {nav_dots}
  <button class="nav-btn" onclick="next()">&#8594;</button>
</div>
<div class="slide-counter" id="counter"></div>
<script>
let cur = 0;
const slides = document.querySelectorAll('.slide');
const dots   = document.querySelectorAll('.dot');
const total  = slides.length;

function goTo(n) {{
  slides[cur].classList.remove('active');
  dots[cur].classList.remove('active');
  cur = (n + total) % total;
  slides[cur].classList.add('active');
  dots[cur].classList.add('active');
  document.getElementById('counter').textContent = (cur+1) + ' / ' + total;
}}
function next() {{ goTo(cur+1); }}
function prev() {{ goTo(cur-1); }}
document.addEventListener('keydown', e => {{
  if (e.key==='ArrowRight'||e.key===' ') next();
  if (e.key==='ArrowLeft') prev();
}});
goTo(0);
</script>
</body>
</html>"""

OUT_HTML.write_text(html, encoding='utf-8')
print(f"Saved: {OUT_HTML}")
print(f"Slides: {len(SLIDES)}")
