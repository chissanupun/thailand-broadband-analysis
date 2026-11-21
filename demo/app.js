'use strict';
// SEA Broadband Explorer: one static page, no build step. Data: data.json (speeds + pass rates),
// geo.json (simplified shapes), forecast.json (experimental model). Design = Figma "Web demo (v7)".

let D, G, F, Q = [];
const S = { lang: 'en', view: 'overview', net: 'fixed', qi: 0, ovTab: 'map', country: 'Thailand', prov: null,
  sort: { k: 'fixed', dir: -1 }, zoom: { c: null, vb: null }, fc: { c: 'Thailand', net: 'fixed', p: '__national__' } };
const PHONE = matchMedia('(max-width: 760px)');

// ---------- i18n ----------
const TH = {
  'Overview': 'ภาพรวม', 'Provinces': 'รายจังหวัด', 'Forecast': 'พยากรณ์', 'About the data': 'เกี่ยวกับข้อมูล', 'About': 'เกี่ยวกับ',
  'View the poster': 'ดูโปสเตอร์', 'beta': 'ทดลอง', 'Map': 'แผนที่', 'Line': 'กราฟเส้น', 'Table': 'ตาราง',
  'Country': 'ประเทศ', 'Network': 'เครือข่าย', 'Fixed broadband': 'อินเทอร์เน็ตบ้าน', 'Mobile': 'มือถือ',
  'fixed broadband': 'อินเทอร์เน็ตบ้าน', 'mobile': 'อินเทอร์เน็ตมือถือ',
  'Select a country to see its provinces': 'เลือกประเทศเพื่อดูรายจังหวัด', 'Select a row to see its provinces': 'เลือกแถวเพื่อดูรายจังหวัด',
  'Select a province': 'เลือกจังหวัด', 'Tap a province': 'แตะจังหวัด', 'Selected province': 'จังหวัดที่เลือก',
  'Singapore': 'สิงคโปร์', 'Thailand': 'ไทย', 'Malaysia': 'มาเลเซีย', 'Vietnam': 'เวียดนาม', 'Philippines': 'ฟิลิปปินส์',
  'Cambodia': 'กัมพูชา', 'Laos': 'ลาว', 'Indonesia': 'อินโดนีเซีย', 'Myanmar': 'เมียนมา', 'Yangon': 'ย่างกุ้ง',
  'Bangkok Metropolis': 'กรุงเทพมหานคร', 'Chiang Mai': 'เชียงใหม่',
  'Internet Landscape Study of Southeast Asian Countries': 'การศึกษาภูมิทัศน์อินเทอร์เน็ตของประเทศในเอเชียตะวันออกเฉียงใต้',
  'Significant digital divides emerge under higher-tier demands.': '<span class="nw">ยิ่งเกณฑ์การใช้งาน</span><wbr><span class="nw">แอปสูงขึ้น</span> <span class="nw">ความเหลื่อมล้ำ</span><wbr><span class="nw">ก็ยิ่งชัดเจน</span>',
  'The communication network quality of nine Southeast Asian countries, using test results from Q1 2023 to Q4 2025 from Ookla (229.4 million tests), compared against the bandwidth requirements of four popular application types.':
    'วิเคราะห์ 9 ประเทศในเอเชียตะวันออกเฉียงใต้ ตั้งแต่ Q1 2023 ถึง Q4 2025 ใช้ข้อมูลเปิดจาก Ookla Open Data (229.4 ล้านการทดสอบ) และตัดสินคุณภาพด้วยเกณฑ์การใช้งานแอป 4 ระดับ',
  'Mean download speed of {0}, {1} (Mbps)': 'ความเร็วดาวน์โหลดเฉลี่ยของ{0} {1} (Mbps)',
  'Mean download speed of {0} by country (Mbps)': 'ความเร็วดาวน์โหลดเฉลี่ยของ{0} รายประเทศ (Mbps)',
  "pass rate every quarter for voice and HD video streaming in nearly every country. The only departures are Thailand's brief dip to 99.8% in Q2 2024 and Myanmar's drop to 53.6% in Q2 2025, both driven by latency rather than bandwidth.":
    'คืออัตราการผ่านเกณฑ์ Voice และ Video streaming (HD) ทุกไตรมาสในเกือบทุกประเทศ ข้อยกเว้นมีแค่ไทยที่ตกลงเหลือ 99.8% ช่วงสั้น ๆ ใน Q2 2024 และเมียนมาที่ตกลงเหลือ 53.6% ใน Q2 2025 ทั้งสองกรณีเกิดจาก latency ไม่ใช่ bandwidth',
  "Myanmar's cloud-gaming pass rate. Myanmar fails to clear the combined threshold of 44 Mbps and 25 ms in any quarter of the study period.":
    'คืออัตราการผ่านเกณฑ์ Cloud gaming ของเมียนมา ตลอดช่วงที่ศึกษา เมียนมาไม่ผ่านเกณฑ์ 44 Mbps และ 25 ms เลยสักไตรมาส',
  'The fastest capital (Singapore, Central Region 361 Mbps) reaches speeds 16.4 times greater than the slowest capital (Yangon, 22 Mbps).':
    'เมืองหลวงที่เร็วที่สุด (สิงคโปร์ Central Region 361 Mbps) เร็วกว่าเมืองหลวงที่ช้าที่สุด (ย่างกุ้ง 22 Mbps) ถึง 16.4 เท่า',
  'Voice and HD video, Q1 2023 to Q4 2025': 'Voice และ Video streaming (HD), Q1 2023 ถึง Q4 2025',
  'Myanmar, cloud gaming, 12 quarters': 'เมียนมา, Cloud gaming, 12 ไตรมาส',
  'Cloud gaming pass rate': 'อัตราการผ่านเกณฑ์ Cloud gaming',
  'Mean download speed (Mbps) and cloud gaming pass rate (fixed broadband), {0}.': 'ความเร็วดาวน์โหลดเฉลี่ย (Mbps) และอัตราการผ่านเกณฑ์ Cloud gaming (อินเทอร์เน็ตบ้าน) {0}',
  'Top five fastest provinces': '5 จังหวัดที่เร็วที่สุด', '{0}, {1} provinces': '{0} {1} จังหวัด',
  'Rank {0} of {1}': 'อันดับ {0} จาก {1}', 'No data for {0}': 'ไม่มีข้อมูล {0}',
  'mean download speed, {0}': 'ความเร็วดาวน์โหลดเฉลี่ย {0}', 'national mean, {0}': 'ค่าเฉลี่ยทั้งประเทศ {0}',
  'National mean': 'ค่าเฉลี่ยทั้งประเทศ',
  'Evaluation results on the application requirements': 'ผลการประเมินตามเกณฑ์การใช้งานแอปพลิเคชัน',
  'National pass rate for fixed broadband: the test-weighted share of province-quarters meeting each requirement, {0}':
    'อัตราการผ่านเกณฑ์ระดับประเทศของอินเทอร์เน็ตบ้าน: สัดส่วนจังหวัด-ไตรมาสที่ผ่านแต่ละเกณฑ์ ถ่วงน้ำหนักตามจำนวนครั้งที่ทดสอบ {0}',
  'Required: 64 Kbps, 200 ms': 'เกณฑ์: 64 Kbps, 200 ms', 'Required: 5 Mbps': 'เกณฑ์: 5 Mbps', 'Required: 25 Mbps': 'เกณฑ์: 25 Mbps', 'Required: 44 Mbps, 25 ms': 'เกณฑ์: 44 Mbps, 25 ms',
  'Experimental forecast': 'การพยากรณ์ (ทดลอง)',
  'Trained on Q1 2023 to Q4 2024, tested on the four quarters of 2025, then used to project 2026.': 'ฝึกโมเดลด้วยข้อมูล Q1 2023 ถึง Q4 2024 ทดสอบกับ 4 ไตรมาสของปี 2025 แล้วจึงใช้คาดการณ์ปี 2026',
  'Experimental. Not part of the poster.': 'ส่วนทดลอง ไม่อยู่ในโปสเตอร์',
  "One gradient-boosting model trained on the Ookla province-quarters of all nine countries. Ookla tests are user-initiated and subject to sampling bias, and the forecast inherits it. The model cannot anticipate sudden changes: Vietnam's mobile mean download rose from 63 to 147 Mbps in Q4 2024 and the model missed it.":
    'ใช้โมเดล gradient boosting ตัวเดียว ฝึกด้วยข้อมูลจังหวัด-ไตรมาสของ Ookla จากทั้ง 9 ประเทศ ผลทดสอบของ Ookla มาจากผู้ใช้ที่กดทดสอบเอง จึงมี sampling bias และการพยากรณ์ก็รับ bias นี้มาด้วย โมเดลคาดการณ์การเปลี่ยนแปลงฉับพลันไม่ได้ เช่น ความเร็วดาวน์โหลดเฉลี่ยบนมือถือของเวียดนามพุ่งจาก 63 เป็น 147 Mbps ใน Q4 2024 ซึ่งโมเดลพลาดไป',
  '{0}, {1} mean download speed (Mbps)': '{0} ความเร็วดาวน์โหลดเฉลี่ยของ{1} (Mbps)',
  'Whole country': 'ทั้งประเทศ', 'Area': 'พื้นที่',
  'Model': 'โมเดล', 'Measured': 'ค่าจริง', '80% interval': 'ช่วง 80%', 'Projected, Q4 2026': 'คาดการณ์ Q4 2026',
  "80% interval {0} to {1} Mbps, from the model's errors on 2025.": 'ช่วง 80% อยู่ที่ {0} ถึง {1} Mbps คำนวณจากความคลาดเคลื่อนของโมเดลในปี 2025',
  'Median error on 2025': 'มัธยฐานความคลาดเคลื่อน ปี 2025', 'against {0}% for repeating the last value.': 'เทียบกับ {0}% ถ้าใช้ค่าล่าสุดซ้ำ',
  'Errors on the four quarters of 2025': 'ความคลาดเคลื่อนใน 4 ไตรมาสของปี 2025',
  'Method': 'วิธี', 'Median error': 'มัธยฐาน', 'Mean error': 'ค่าเฉลี่ย', 'One quarter ahead': 'ล่วงหน้า 1 ไตรมาส',
  'Straight-line trend': 'แนวโน้มเส้นตรง', 'Last value repeated': 'ใช้ค่าล่าสุดซ้ำ',
  'Absolute percentage error against the measured 2025 values, over {0} province-quarter forecasts. On mean error the three methods are about even; sudden changes hurt every method.':
    'ร้อยละความคลาดเคลื่อนสัมบูรณ์เทียบกับค่าจริงปี 2025 จากการพยากรณ์จังหวัด-ไตรมาส {0} รายการ ถ้าดูค่าเฉลี่ย ทั้ง 3 วิธีพอ ๆ กัน และการเปลี่ยนแปลงฉับพลันก็ทำให้ทุกวิธีพลาด',
  'The poster': 'โปสเตอร์', 'Contact': 'ติดต่อ', 'Questions about the data or the study? Email the first author.': 'มีคำถามเรื่องข้อมูลหรืองานวิจัย อีเมลหาผู้วิจัยหลักได้เลย', 'Poster preview': 'ตัวอย่างโปสเตอร์', 'Code': 'โค้ด', 'Datasets': 'ชุดข้อมูล',
  'Internet Landscape Study of Southeast Asian Countries. Poster, AINTEC 2026, Taipei.': 'Internet Landscape Study of Southeast Asian Countries โปสเตอร์ AINTEC 2026 ไทเป',
  'Download PDF': 'ดาวน์โหลด PDF', 'Open on GitHub': 'เปิดใน GitHub', 'Ookla Open Data': 'Ookla Open Data', 'M-Lab NDT7': 'M-Lab NDT7',
  'Data cleansing and preparation, and data analysis.': 'การทำความสะอาดและเตรียมข้อมูล และการวิเคราะห์ข้อมูล',
  'Ookla Open Data (global Parquet files on Amazon S3) and M-Lab NDT7 (BigQuery).': 'Ookla Open Data (ไฟล์ Parquet บน Amazon S3 แบบ global) และ M-Lab NDT7 (BigQuery)',
  'Data cleansing and preparation': 'การทำความสะอาดและเตรียมข้อมูล',
  "Ookla open data supplies quarterly internet-performance tiles split by connection type (fixed, mobile) at Quadkey zoom 16 (~600 × 600 m), each carrying mean download, upload, latency, and the underlying Speedtest submission count. We run point-in-polygon on the tiles to determine which province each point falls in, then compute a weighted average by each tile's test count. We filter only province-quarters with total_tests ≥ 100 and n_tiles ≥ 5. The bandwidth and latency requirements for different types of applications are adopted from Lübben and Misfeld.":
    'Ookla Open Data ให้ข้อมูลประสิทธิภาพอินเทอร์เน็ตรายไตรมาสในรูปแบบ tile แบ่งตามประเภทการเชื่อมต่อ (fixed, mobile) ที่ Quadkey zoom 16 (ขนาดราว 600 × 600 เมตร) แต่ละ tile มีค่าเฉลี่ย download, upload, latency พร้อมจำนวนครั้งที่ทดสอบ (Speedtest submission) กำกับมาด้วย tile ของ Ookla ถูกจับคู่เข้ากับจังหวัดด้วย point-in-polygon แล้วรวมเป็นระดับจังหวัด-ไตรมาสแบบถ่วงน้ำหนักตามจำนวนครั้งที่ทดสอบของแต่ละ tile ทุกจังหวัด-ไตรมาสต้องผ่านเกณฑ์ total_tests ≥ 100 และ n_tiles ≥ 5 ส่วนเกณฑ์ throughput และ latency สำหรับ application ประเภทต่าง ๆ มาจากงานของ Lübben และ Misfeld',
  'This site shows the Ookla dataset (229.4 million tests). The study also analyzes M-Lab NDT7 (760.6 million tests). We keep the two sources separate throughout and never pool their records.':
    'เว็บไซต์นี้แสดงชุดข้อมูล Ookla (229.4 ล้านการทดสอบ) งานวิจัยยังวิเคราะห์ M-Lab NDT7 (760.6 ล้านการทดสอบ) ด้วย ค่าความเร็วดิบจาก Ookla และ NDT7 ไม่ถูกนำมารวมกันโดยตรง เนื่องจากทั้งสองแพลตฟอร์มวัด network performance ภายใต้เงื่อนไขที่แตกต่างกัน',
  'Authors': 'ผู้วิจัย', 'Cite this work': 'อ้างอิงงานนี้',
  'Chissanupun Athiwarikanon, Kunanont Malayanont, Pakkapon Pattanakul and Sukumal Kitisin, Kasetsart University.':
    'Chissanupun Athiwarikanon, Kunanont Malayanont, Pakkapon Pattanakul และ Sukumal Kitisin มหาวิทยาลัยเกษตรศาสตร์',
  'Play quarters': 'เล่นทีละไตรมาส', 'Zoom in': 'ซูมเข้า', 'Zoom out': 'ซูมออก', 'Reset zoom': 'รีเซ็ตการซูม', 'Scroll or pinch to zoom': 'เลื่อนเมาส์หรือถ่างนิ้วเพื่อซูม', 'Pause': 'หยุด', 'Quarter': 'ไตรมาส', 'Language': 'ภาษา',
};
const t = (s, ...a) => (S.lang === 'th' && TH[s] != null ? TH[s] : s).replace(/\{(\d)\}/g, (_, i) => a[i]);
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
const nm = s => esc(S.lang === 'th' && TH[s] ? TH[s] : s); // place names: Thai where we have it
const ql = q => `${q.slice(5)} ${q.slice(0, 4)}`;
const netName = n => t(n === 'fixed' ? 'fixed broadband' : 'mobile');
const r0 = v => (v == null ? '–' : Math.round(v));

// ---------- colour ----------
const RAMP = [[0, '#e4e7f8'], [50, '#b6bcef'], [100, '#7f8ae0'], [200, '#4753c4'], [300, '#232a78']];
const col = v => { if (v == null) return '#f0f1f7'; let c = RAMP[0][1]; for (const [k, cc] of RAMP) if (v >= k) c = cc; return c; };
const DARK = new Set(['#4753c4', '#232a78']);
const ORANGE = '#e8763a', INDIGO = '#3f4bb8', MUTED = '#5a6190', INK = '#1b1f4b', LINE = '#e3e6f3';

// ---------- data access ----------
const q = () => Q[S.qi];
const nat = (c, net = S.net, qq = q()) => D[c][net].national[qq];
const prov = (c, p, net = S.net, qq = q()) => D[c][net].provinces[p]?.[qq];
const byNat = () => Object.keys(D).sort((a, b) => (nat(b) ?? -1) - (nat(a) ?? -1));

// ---------- geometry ----------
const pathCache = new Map();
function projector(ringsList, w, h, pad) {
  let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
  for (const rs of ringsList) for (const r of rs) for (const [x, y] of r) { x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); }
  const k = Math.cos((y0 + y1) / 2 * Math.PI / 180);
  const s = Math.min((w - 2 * pad) / ((x1 - x0) * k), (h - 2 * pad) / (y1 - y0));
  const ox = (w - (x1 - x0) * k * s) / 2, oy = (h - (y1 - y0) * s) / 2;
  return (lon, lat) => [ox + (lon - x0) * k * s, oy + (y1 - lat) * s];
}
const pathD = (rings, P) => rings.map(r => 'M' + r.map(p => P(...p).map(v => v.toFixed(1)).join(' ')).join('L') + 'Z').join('');
function aspect(ringsList) { // height/width of a lon/lat box after the cos(lat) squeeze
  let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
  for (const rs of ringsList) for (const r of rs) for (const [x, y] of r) { x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); }
  return (y1 - y0) / ((x1 - x0) * Math.cos((y0 + y1) / 2 * Math.PI / 180));
}
function seaGeom() {
  if (!pathCache.has('sea')) {
    const P = projector(Object.values(G).map(g => g.outline), 860, 560, 12);
    const paths = Object.fromEntries(Object.entries(G).map(([c, g]) => [c, pathD(g.outline, P)]));
    pathCache.set('sea', { P, paths });
  }
  return pathCache.get('sea');
}
function provGeom(c) {
  if (!pathCache.has(c)) {
    const rings = Object.values(G[c].provinces), w = 400, h = Math.round(Math.min(560, Math.max(280, w * aspect(rings) + 20)));
    const P = projector(rings, w, h, 10);
    const lab = {};
    for (const [n, rs] of Object.entries(G[c].provinces)) {
      let best = null, bestA = 0;
      for (const ring of rs) {
        const pts = ring.map(q => P(...q)); let a = 0, cx = 0, cy = 0;
        for (let i = 0, j = pts.length - 1; i < pts.length; j = i++) { const f = pts[j][0] * pts[i][1] - pts[i][0] * pts[j][1]; a += f; cx += (pts[j][0] + pts[i][0]) * f; cy += (pts[j][1] + pts[i][1]) * f; }
        if (Math.abs(a) > bestA) { bestA = Math.abs(a); const xs = pts.map(q => q[0]); best = { x: cx / (3 * a), y: cy / (3 * a), w: Math.max(...xs) - Math.min(...xs) }; }
      }
      if (best) lab[n] = best;
    }
    pathCache.set(c, { w, h, lab, paths: Object.fromEntries(Object.entries(G[c].provinces).map(([n, r]) => [n, pathD(r, P)])) });
  }
  return pathCache.get(c);
}

// ---------- small components ----------
const ICON = {
  tap: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 11V5a2 2 0 0 1 4 0v6m0-1a2 2 0 0 1 4 0v1m0 0a2 2 0 0 1 4 0v4a6 6 0 0 1-6 6h-2a6 6 0 0 1-5-3l-3-5a1.5 1.5 0 0 1 2.5-1.6L9 14"/></svg>',
  chev: '<svg class="chev" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>',
  play: '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M4 2.2v9.6a.6.6 0 0 0 .9.5l7.6-4.8a.6.6 0 0 0 0-1L4.9 1.7a.6.6 0 0 0-.9.5z" fill="currentColor"/></svg>',
  pause: '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><rect x="3" y="2" width="3" height="10" rx="1" fill="currentColor"/><rect x="8" y="2" width="3" height="10" rx="1" fill="currentColor"/></svg>',
};
const hint = s => `<span class="hint">${ICON.tap}${t(s)}</span>`;
const seg = () => `<div class="seg" role="group" aria-label="${t('Network')}">${['fixed', 'mobile'].map(n =>
  `<button type="button" data-net="${n}" aria-pressed="${S.net === n}">${t(n === 'fixed' ? 'Fixed broadband' : 'Mobile')}</button>`).join('')}</div>`;
const legend = () => `<div class="rl" style="width:min(240px,100%)"><div class="rlb">${RAMP.map(([, c]) => `<i style="background:${c}"></i>`).join('')}</div><div class="rlt">${RAMP.map(([k]) => `<span>${k}</span>`).join('')}<span>Mbps</span></div></div>`;
const PLAYER = '<div data-player></div>';
const NAV = [['overview', 'Overview', 'M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z'], ['provinces', 'Provinces', 'M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2z'],
  ['forecast', 'Forecast', 'M3 17l6-6 4 4 8-8'], ['about', 'About the data', 'M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18M12 8v.01M12 11v6']];

function chart({ w, h, series, labels, band, shade, marker, pad = [44, 16, 130, 30] }) {
  const [l, tp, r, b] = pad, n = labels.length, iw = w - l - r, ih = h - tp - b;
  const all = series.flatMap(s => s.vals).concat(band ? [...band.lo, ...band.hi] : []).filter(v => v != null);
  if (!all.length) all.push(0, 100);
  const raw = (Math.max(...all) - Math.min(...all)) / 4 || 10, p10 = 10 ** Math.floor(Math.log10(raw)), f = raw / p10;
  const step = (f <= 1 ? 1 : f <= 2 ? 2 : f <= 5 ? 5 : 10) * p10;
  const y0 = Math.max(0, Math.floor(Math.min(...all) / step) * step);
  let y1 = Math.ceil(Math.max(...all) / step) * step || step;
  if (y1 <= y0) y1 = y0 + step;
  const X = i => l + iw * i / (n - 1), Y = v => tp + ih * (1 - (v - y0) / (y1 - y0));
  const o = [`<svg viewBox="0 0 ${w} ${h}" style="width:100%;height:auto;display:block" role="img">`];
  for (let v = y0; v <= y1 + 1e-9; v += step)
    o.push(`<line x1="${l}" x2="${w - r}" y1="${Y(v).toFixed(1)}" y2="${Y(v).toFixed(1)}" stroke="${LINE}"/><text x="${l - 8}" y="${(Y(v) + 4).toFixed(1)}" text-anchor="end" font-size="12" fill="${MUTED}">${Math.round(v)}</text>`);
  labels.forEach((lab, i) => lab && o.push(`<text x="${X(i).toFixed(1)}" y="${h - 8}" text-anchor="middle" font-size="12" fill="${MUTED}">${lab}</text>`));
  if (shade) o.push(`<rect x="${X(shade[0]).toFixed(1)}" y="${tp}" width="${(X(shade[1]) - X(shade[0])).toFixed(1)}" height="${ih}" fill="#eef0fa"/><text x="${(X(shade[0]) + 8).toFixed(1)}" y="${tp + 16}" font-size="12" font-weight="600" fill="${MUTED}">${shade[2]}</text>`);
  if (marker != null) o.push(`<line x1="${X(marker).toFixed(1)}" x2="${X(marker).toFixed(1)}" y1="${tp}" y2="${tp + ih}" stroke="${ORANGE}" stroke-width="1" stroke-dasharray="3 4"/>`);
  if (band) {
    const pts = band.hi.map((v, i) => [X(band.s0 + i), Y(v)]).concat(band.lo.map((v, i) => [X(band.s0 + i), Y(v)]).reverse());
    o.push(`<path d="M${pts.map(p => p.map(v => v.toFixed(1)).join(' ')).join('L')}Z" fill="#ffad4a" fill-opacity=".28"/>`);
  }
  const ends = [];
  for (const s of series) {
    let d = '', pen = false;
    s.vals.forEach((v, i) => { if (v == null) { pen = false; return; } d += `${pen ? 'L' : 'M'}${X(s.s0 + i).toFixed(1)} ${Y(v).toFixed(1)}`; pen = true; });
    o.push(`<path d="${d}" fill="none" stroke="${s.color}" stroke-width="${s.wd}" stroke-linecap="round" stroke-linejoin="round"${s.dash ? ` stroke-dasharray="${s.dash}"` : ''}/>`);
    let li = s.vals.length - 1; while (li > 0 && s.vals[li] == null) li--;
    if (s.label && s.vals[li] != null) ends.push({ x: X(s.s0 + li), y: Y(s.vals[li]), ly: Y(s.vals[li]) + 4, s });
  }
  ends.sort((a, b) => a.ly - b.ly).forEach((e, i, a) => { if (i && e.ly < a[i - 1].ly + 15) e.ly = a[i - 1].ly + 15; });
  for (const e of ends) o.push(`<circle cx="${e.x.toFixed(1)}" cy="${e.y.toFixed(1)}" r="${e.s.dot ?? 4.5}" fill="${e.s.color}" stroke="#fff" stroke-width="2"/><text x="${(e.x + 10).toFixed(1)}" y="${e.ly.toFixed(1)}" font-size="12" font-weight="600" fill="${e.s.color === ORANGE ? '#b34f1a' : e.s.color}">${esc(e.s.label)}</text>`);
  o.push('</svg>');
  return o.join('');
}
const yearLabels = qs => qs.map(qq => (qq.endsWith('Q1') ? qq.slice(0, 4) : ''));

// ---------- maps ----------
const POS = { Myanmar: [96.0, 21.5], Thailand: [101.0, 15.6], Laos: [103.2, 19.6], Vietnam: [111.4, 15.2], Cambodia: [104.9, 12.7],
  Malaysia: [110.0, 4.2], Singapore: [106.9, 1.0], Indonesia: [117.0, -2.6], Philippines: [125.6, 13.5] };
function txt(x, y, s, size, weight, fill, num, halo) {
  const a = `x="${x.toFixed(0)}" y="${y.toFixed(0)}" text-anchor="middle" font-size="${size}" font-weight="${weight}"${num ? ' class="num"' : ''}`;
  return (halo ? `<text ${a} fill="#fff" stroke="#fff" stroke-width="4" stroke-opacity=".9" stroke-linejoin="round">${s}</text>` : '') + `<text ${a} fill="${fill}">${s}</text>`;
}
function seaMap() {
  const { P, paths } = seaGeom(), labels = !PHONE.matches, o = ['<svg class="map" viewBox="0 0 860 560" style="width:100%;height:auto;display:block">'];
  for (let lon = 90; lon < 135; lon += 5) { const [a, b] = P(lon, 30), [c, d] = P(lon, -12); o.push(`<line x1="${a.toFixed(1)}" y1="${b.toFixed(1)}" x2="${c.toFixed(1)}" y2="${d.toFixed(1)}" stroke="#dde1f3" stroke-dasharray="2 5"/>`); }
  for (let lat = -10; lat < 30; lat += 5) { const [a, b] = P(85, lat), [c, d] = P(140, lat); o.push(`<line x1="${a.toFixed(1)}" y1="${b.toFixed(1)}" x2="${c.toFixed(1)}" y2="${d.toFixed(1)}" stroke="#dde1f3" stroke-dasharray="2 5"/>`); }
  for (const c in paths) o.push(`<path d="${paths[c]}" transform="translate(0 6)" fill="#c3c9ec" opacity=".45"/>`);
  for (const c in paths) o.push(`<path class="hit" d="${paths[c]}" fill="${col(nat(c))}" stroke="#fff" stroke-width="1.6" stroke-linejoin="round" data-c="${c}" tabindex="0" role="button" aria-label="${nm(c)}, ${r0(nat(c))} Mbps"><title>${nm(c)}: ${r0(nat(c))} Mbps</title></path>`);
  const [sx, sy] = P(103.82, 1.35);
  o.push(`<circle class="hit" cx="${sx.toFixed(1)}" cy="${sy.toFixed(1)}" r="7" fill="${col(nat('Singapore'))}" stroke="${S.country === 'Singapore' ? ORANGE : '#fff'}" stroke-width="${S.country === 'Singapore' ? 3 : 2}" data-c="Singapore" tabindex="0" role="button" aria-label="${nm('Singapore')}, ${r0(nat('Singapore'))} Mbps"><title>${nm('Singapore')}: ${r0(nat('Singapore'))} Mbps</title></circle>`);
  o.push(`<path d="${paths[S.country]}" fill="none" stroke="${ORANGE}" stroke-width="3" stroke-linejoin="round" pointer-events="none"/>`);
  if (labels) {
    o.push('<g pointer-events="none">');
    for (const [c, [lon, lat]] of Object.entries(POS)) {
      const [x, y] = P(lon, lat), v = nat(c), name = nm(c);
      if (['Thailand', 'Laos', 'Cambodia', 'Myanmar'].includes(c) && DARK.has(col(v))) o.push(txt(x, y, name, 13, 600, '#fff') + txt(x, y + 19, r0(v), 17, 800, '#fff', 1));
      else if (['Myanmar', 'Laos', 'Cambodia'].includes(c)) o.push(txt(x, y, name, 13, 600, INK, 0, 1) + txt(x, y + 19, r0(v), 17, 800, INK, 1, 1));
      else {
        const cw = Math.max(name.length * 6.8, 30) + 18;
        o.push(`<rect x="${(x - cw / 2).toFixed(1)}" y="${(y - 15).toFixed(1)}" width="${cw.toFixed(1)}" height="38" rx="10" fill="#fff" stroke="${LINE}"/>` + txt(x, y, name, 11, 600, MUTED) + txt(x, y + 17, r0(v), 15, 800, INK, 1));
      }
    }
    o.push('</g>');
  }
  return o.join('') + '</svg>';
}
function provMap(c) {
  const { w, h, paths, lab } = provGeom(c), v = S.zoom.c === c ? S.zoom.vb : [0, 0, w, h];
  const o = [`<div class="mapwrap"><svg class="map pmap" viewBox="${v.join(' ')}" data-w="${w}" data-h="${h}" style="width:100%;height:auto;display:block;aspect-ratio:${w}/${h}">`];
  for (const p in paths) o.push(`<path d="${paths[p]}" transform="translate(0 5)" fill="#c3c9ec" opacity=".45"/>`);
  for (const p in paths) { const v = prov(c, p); o.push(`<path class="hit" d="${paths[p]}" fill="${col(v)}" stroke="#fff" stroke-width=".7" vector-effect="non-scaling-stroke" stroke-linejoin="round" data-p="${esc(p)}" tabindex="0" role="button" aria-label="${nm(p)}, ${r0(v)} Mbps"><title>${nm(p)}: ${r0(v)} Mbps</title></path>`); }
  if (S.prov && paths[S.prov]) o.push(`<path d="${paths[S.prov]}" fill="none" stroke="${ORANGE}" stroke-width="3" vector-effect="non-scaling-stroke" stroke-linejoin="round" pointer-events="none"/>`);
  o.push('<g class="plab" pointer-events="none">');
  for (const p in lab) { const v = prov(c, p), dark = DARK.has(col(v)); o.push(`<text x="${lab[p].x.toFixed(1)}" y="${lab[p].y.toFixed(1)}" data-p="${esc(p)}" data-w="${lab[p].w.toFixed(1)}" text-anchor="middle" dominant-baseline="middle" fill="${dark ? '#fff' : INK}" stroke="${dark ? '#161c4f' : '#fff'}" stroke-opacity=".55" paint-order="stroke" font-weight="600">${nm(p)}</text>`); }
  o.push('</g></svg>');
  o.push(`<div class="zctl"><button type="button" data-zoom="in" aria-label="${t('Zoom in')}">+</button><button type="button" data-zoom="out" aria-label="${t('Zoom out')}">−</button><button type="button" data-zoom="reset" aria-label="${t('Reset zoom')}"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg></button></div></div>`);
  return o.join('');
}

// ---------- province map zoom (viewBox pan/zoom; labels appear once zoomed and only where they fit) ----------
const ZMAX = 8, ZLABEL = 1.6;
function zoomApply(svg) {
  const W = +svg.dataset.w, H = +svg.dataset.h, [x, y, w, h] = S.zoom.vb, k = W / w;
  svg.setAttribute('viewBox', `${x} ${y} ${w} ${h}`);
  svg.style.touchAction = k > 1.01 ? 'none' : 'pan-y';
  const px = svg.getBoundingClientRect().width / w || 1, fs = 11 / px; // 11 screen px whatever the zoom
  for (const tx of svg.querySelectorAll('.plab text')) {
    const half = (tx.textContent.length * 3.2 + 4) / px, lx = +tx.getAttribute('x'), ly = +tx.getAttribute('y');
    const inView = lx - half > x && lx + half < x + w && ly - 8 / px > y && ly + 8 / px < y + h;
    const fits = k >= ZLABEL && inView && (tx.dataset.p === S.prov || +tx.dataset.w * px > tx.textContent.length * 6.4 + 6);
    tx.style.display = fits ? '' : 'none';
    if (fits) { tx.setAttribute('font-size', fs.toFixed(2)); tx.setAttribute('stroke-width', (3 / px).toFixed(2)); }
  }
}
function zoomBy(svg, f, ux, uy) {
  const W = +svg.dataset.w, H = +svg.dataset.h, [x, y, w, h] = S.zoom.vb;
  const nw = Math.min(W, Math.max(W / ZMAX, w / f)), nh = nw * H / W;
  if (ux == null) { ux = x + w / 2; uy = y + h / 2; }
  zoomPan(svg, ux - (ux - x) * nw / w, uy - (uy - y) * nh / h, nw, nh);
}
function zoomPan(svg, x, y, w, h) {
  const W = +svg.dataset.w, H = +svg.dataset.h;
  S.zoom.vb = [Math.min(Math.max(0, x), W - w), Math.min(Math.max(0, y), H - h), w, h];
  zoomApply(svg);
}
function zoomSetup() {
  const svg = app.querySelector('.pmap');
  if (!svg) return;
  if (S.zoom.c !== S.country) S.zoom = { c: S.country, vb: [0, 0, +svg.dataset.w, +svg.dataset.h] };
  zoomApply(svg);
  const toUnits = (cx, cy) => { const b = svg.getBoundingClientRect(), [x, y, w, h] = S.zoom.vb; return [x + (cx - b.left) / b.width * w, y + (cy - b.top) / b.height * h]; };
  svg.addEventListener('wheel', e => {
    const out = e.deltaY > 0;
    if (out && S.zoom.vb[2] >= +svg.dataset.w - 0.01) return; // fully out: let the page scroll
    e.preventDefault();
    zoomBy(svg, Math.exp(-e.deltaY * (e.deltaMode ? 0.05 : 0.0018)), ...toUnits(e.clientX, e.clientY));
  }, { passive: false });
  const pts = new Map(); let start = null, moved = false;
  const snap = () => { const a = [...pts.values()]; const cx = a.reduce((s, p) => s + p.x, 0) / a.length, cy = a.reduce((s, p) => s + p.y, 0) / a.length;
    return { cx, cy, d: a.length > 1 ? Math.hypot(a[0].x - a[1].x, a[0].y - a[1].y) : 0, vb: [...S.zoom.vb], n: a.length }; };
  svg.addEventListener('pointerdown', e => { pts.set(e.pointerId, { x: e.clientX, y: e.clientY }); start = snap(); moved = false; });
  svg.addEventListener('pointermove', e => {
    if (!pts.has(e.pointerId)) return;
    pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
    const now = snap(); if (now.n !== start.n) { start = now; return; }
    const b = svg.getBoundingClientRect(), [x, y, w, h] = start.vb, upp = w / b.width;
    if (!moved && Math.hypot(now.cx - start.cx, now.cy - start.cy) < 5 && Math.abs(now.d - start.d) < 5) return;
    if (!moved) { moved = true; try { svg.setPointerCapture(e.pointerId); } catch {} }
    if (now.n > 1 && start.d) { // pinch: zoom about the start midpoint, then follow the fingers
      const W = +svg.dataset.w, H = +svg.dataset.h, nw = Math.min(W, Math.max(W / ZMAX, w * start.d / now.d)), nh = nw * H / W;
      const ux = x + (start.cx - b.left) * upp, uy = y + (start.cy - b.top) * upp, nupp = nw / b.width;
      zoomPan(svg, ux - (now.cx - b.left) * nupp, uy - (now.cy - b.top) * nupp, nw, nh);
    } else if (w < +svg.dataset.w - 0.01) zoomPan(svg, x - (now.cx - start.cx) * upp, y - (now.cy - start.cy) * upp, w, h);
  });
  const end = e => { pts.delete(e.pointerId); start = pts.size ? snap() : null; };
  svg.addEventListener('pointerup', end); svg.addEventListener('pointercancel', end);
  svg.addEventListener('click', e => { if (moved) { e.stopPropagation(); moved = false; } }, true); // a drag is not a province click
}

// ---------- views ----------
function overview() {
  const order = byNat(), mx = nat(order[0]);
  const bars = order.map(c => `<button type="button" class="br" data-c="${c}"><span class="bn">${nm(c)}</span><span class="bw"><i style="width:${(nat(c) / mx * 100).toFixed(1)}%;background:${col(nat(c))}"></i></span><span class="bv">${r0(nat(c))}</span>${ICON.chev}</button>`).join('');
  let body;
  if (S.ovTab === 'map') body = seaMap();
  else if (S.ovTab === 'line') {
    const series = Object.keys(D).map(c => ({ s0: 0, vals: Q.map(qq => nat(c, S.net, qq)), color: c === S.country ? ORANGE : '#9aa3dc', wd: c === S.country ? 3 : 1.6, label: S.lang === 'th' && TH[c] ? TH[c] : c, dot: c === S.country ? 4.5 : 3 }));
    series.push(series.splice(Object.keys(D).indexOf(S.country), 1)[0]); // highlighted line on top
    body = `<div class="ctw"><h3 class="muted" style="margin:12px 0 4px">${t('Mean download speed of {0} by country (Mbps)', netName(S.net))}</h3>${chart({ w: PHONE.matches ? 380 : 820, h: PHONE.matches ? 340 : 470, series, labels: yearLabels(Q), marker: S.qi, pad: [40, 16, PHONE.matches ? 90 : 110, 30] })}</div>`;
  } else body = table();
  const vt = ['map', 'line', 'table'].map(k => `<button type="button" data-ov="${k}" aria-pressed="${S.ovTab === k}">${t(k[0].toUpperCase() + k.slice(1))}</button>`).join('');
  const sq = cls => `<div class="sq" aria-hidden="true">${`<i class="${cls}"></i>`.repeat(12)}</div>`;
  return `<section class="stage">
  <div>
    <p class="kicker">${t('Internet Landscape Study of Southeast Asian Countries')}</p>
    <h1>${t('Significant digital divides emerge under higher-tier demands.').replace('higher-tier', '<span class="nw">higher-tier</span>')}</h1>
    <p class="lede">${t('The communication network quality of nine Southeast Asian countries, using test results from Q1 2023 to Q4 2025 from Ookla (229.4 million tests), compared against the bandwidth requirements of four popular application types.')}</p>
    <div class="row">${seg()}${legend()}</div>
    <div class="bars"><h3>${t('Mean download speed of {0}, {1} (Mbps)', netName(S.net), ql(q()))}</h3>${bars}</div>
  </div>
  <div class="sm"><div class="smh"><div class="vt" role="group">${vt}</div>${hint(S.ovTab === 'table' ? 'Select a row to see its provinces' : 'Select a country to see its provinces')}</div>${body}${PLAYER}</div>
</section>
<section class="facts">
  <div class="fc"><div class="viz">${sq('on')}<small>${t('Voice and HD video, Q1 2023 to Q4 2025')}</small></div><b>100%</b><p>${t("pass rate every quarter for voice and HD video streaming in nearly every country. The only departures are Thailand's brief dip to 99.8% in Q2 2024 and Myanmar's drop to 53.6% in Q2 2025, both driven by latency rather than bandwidth.")}</p></div>
  <div class="fc"><div class="viz">${sq('off')}<small>${t('Myanmar, cloud gaming, 12 quarters')}</small></div><b>0%</b><p>${t("Myanmar's cloud-gaming pass rate. Myanmar fails to clear the combined threshold of 44 Mbps and 25 ms in any quarter of the study period.")}</p></div>
  <div class="fc"><div class="viz"><div class="cmp" aria-hidden="true"><span>${nm('Singapore')}</span><em><i style="width:100%"></i></em><span>361</span><span>${nm('Yangon')}</span><em><i class="lo" style="width:6.1%"></i></em><span>22</span></div></div><b>16.4×</b><p>${t('The fastest capital (Singapore, Central Region 361 Mbps) reaches speeds 16.4 times greater than the slowest capital (Yangon, 22 Mbps).')}</p></div>
</section>`;
}
function table() {
  const val = (c, k) => k === 'country' ? nm(c) : k === 'cloud' ? D[c].pass[q()]?.cloud : nat(c, k);
  const { k, dir } = S.sort;
  const rows = Object.keys(D).sort((a, b) => { const x = val(a, k), y = val(b, k); return (typeof x === 'string' ? x.localeCompare(y) : (x ?? -1) - (y ?? -1)) * dir; });
  const mx = Math.max(...Object.keys(D).map(c => nat(c, 'fixed')));
  const th = (key, label, n) => `<th class="${n ? 'n' : ''}"${k === key ? ` aria-sort="${dir < 0 ? 'descending' : 'ascending'}"` : ''}><button type="button" data-sort="${key}">${t(label)}${k === key ? (dir < 0 ? ' ▾' : ' ▴') : ''}</button></th>`;
  return `<div class="ctw"><table class="ct"><thead><tr>${th('country', 'Country')}${th('fixed', 'Fixed broadband', 1)}${th('mobile', 'Mobile', 1)}${th('cloud', 'Cloud gaming pass rate', 1)}</tr></thead><tbody>${rows.map(c => {
    const f = nat(c, 'fixed'), p = D[c].pass[q()]?.cloud;
    return `<tr data-c="${c}" tabindex="0"><td><i class="sw" style="background:${col(nat(c))}"></i>${nm(c)}</td><td class="n"><span class="tb"><i style="width:${(f / mx * 100).toFixed(1)}%"></i></span>${r0(f)}</td><td class="n">${r0(nat(c, 'mobile'))}</td><td class="n">${p == null ? '–' : Math.round(p) + '%'}</td></tr>`;
  }).join('')}</tbody></table><p class="ctn">${t('Mean download speed (Mbps) and cloud gaming pass rate (fixed broadband), {0}.', ql(q()))}</p></div>`;
}
function rankedProvinces(c) {
  return Object.keys(D[c][S.net].provinces).filter(p => prov(c, p) != null).sort((a, b) => prov(c, b) - prov(c, a));
}
function provinces() {
  const c = S.country, T = D[c], ranked = rankedProvinces(c), all = Object.keys(G[c].provinces);
  if (!S.prov || !(S.prov in T[S.net].provinces)) S.prov = (T.capital in T[S.net].provinces) ? T.capital : ranked[0];
  const p = S.prov, v = prov(c, p), rank = ranked.indexOf(p) + 1;
  const cl = byNat().map(x => `<button type="button" class="cc" data-c="${x}" aria-pressed="${x === c}">${nm(x)}<small>${r0(nat(x))}</small></button>`).join('');
  const top = ranked.slice(0, 5).map((x, i) => `<button type="button" class="tl" data-p="${esc(x)}"><span><em>${i + 1}</em>${nm(x)}</span><b>${r0(prov(c, x))}</b></button>`).join('');
  const opts = byNat().map(x => `<option value="${x}"${x === c ? ' selected' : ''}>${nm(x)} · ${r0(nat(x))} Mbps</option>`).join('');
  const series = [];
  if (p !== T.capital && T[S.net].provinces[T.capital]) series.push({ s0: 0, vals: Q.map(qq => prov(c, T.capital, S.net, qq)), color: '#9aa0c4', wd: 2, dash: '5 5', label: S.lang === 'th' && TH[T.capital] ? TH[T.capital] : T.capital });
  series.push({ s0: 0, vals: Q.map(qq => nat(c, S.net, qq)), color: INDIGO, wd: 2.5, label: t('National mean') });
  series.push({ s0: 0, vals: Q.map(qq => prov(c, p, S.net, qq)), color: ORANGE, wd: 3, label: S.lang === 'th' && TH[p] ? TH[p] : p });
  const P = T.pass[q()] || {};
  const meters = [['voice', 'Voice', 'Required: 64 Kbps, 200 ms'], ['hd', 'Video streaming (HD)', 'Required: 5 Mbps'], ['uhd', 'Video streaming (UHD)', 'Required: 25 Mbps'], ['cloud', 'Cloud gaming', 'Required: 44 Mbps, 25 ms']]
    .map(([k, n, req]) => `<div class="mtr"><div class="mh"><span>${n}</span><b>${P[k] == null ? '–' : Math.round(P[k]) + '%'}</b></div><div class="mb"><i style="width:${P[k] ?? 0}%"></i></div><small>${t(req)}</small></div>`).join('');
  return `<div class="app">
  <aside class="side">
    <div><h4>${t('Country')}</h4><div class="cclist">${cl}</div></div>
    <div><h4>${t('Network')}</h4>${seg()}</div>
    <div><h4>${t('Top five fastest provinces')}</h4>${top}</div>
  </aside>
  <div>
    <div class="csel"><select id="csel" aria-label="${t('Country')}">${opts}</select>${seg()}</div>
    <div class="main">
      <section class="pstage"><div class="psh"><h3>${t('{0}, {1} provinces', nm(c), all.length)}</h3>${hint(PHONE.matches ? 'Tap a province' : 'Select a province')}</div>${provMap(c)}<div style="margin-top:14px">${legend()}</div>${PLAYER}</section>
      <div class="col">
        <section class="det"><div class="dh"><div><p class="muted">${t('Selected province')}</p><h2>${nm(p)}</h2></div>${rank ? `<span class="rankb">${t('Rank {0} of {1}', rank, ranked.length)}</span>` : ''}</div>
          <div class="dg"><div><b>${r0(v)}<small> Mbps</small></b><span>${v == null ? t('No data for {0}', ql(q())) : t('mean download speed, {0}', ql(q()))}</span></div><div><b>${r0(nat(c))}<small> Mbps</small></b><span>${t('national mean, {0}', ql(q()))}</span></div></div>
          <div style="margin-top:12px">${chart({ w: PHONE.matches ? 380 : 640, h: PHONE.matches ? 230 : 240, series, labels: yearLabels(Q), marker: S.qi, pad: [40, 16, PHONE.matches ? 120 : 150, 30] })}</div></section>
        <section class="det"><h3>${t('Evaluation results on the application requirements')}</h3><p class="muted">${t('National pass rate for fixed broadband: the test-weighted share of province-quarters meeting each requirement, {0}', ql(q()))}</p><div class="mtrs">${meters}</div></section>
      </div>
    </div>
  </div>
</div>`;
}
function forecast() {
  const { c, net } = S.fc;
  if (!F.series[`${c}|${net}|${S.fc.p}`]) S.fc.p = '__national__';
  const p = S.fc.p, f = F.series[`${c}|${net}|${p}`], national = p === '__national__';
  const meas = Q.map(qq => national ? nat(c, net, qq) : prov(c, p, net, qq));
  let li = meas.length - 1; while (li > 0 && meas[li] == null) li--;
  const last = meas[li], allq = Q.concat(F.future_quarters), gap = Array(Q.length - 1 - li).fill(null);
  const area = national ? nm(c) : `${nm(p)}, ${nm(c)}`;
  const ch = chart({ w: PHONE.matches ? 380 : 900, h: PHONE.matches ? 280 : 360, labels: yearLabels(allq), shade: [Q.length, allq.length - 1, '2026'],
    series: [{ s0: 0, vals: meas, color: INDIGO, wd: 3 }, ...(last == null ? [] : [{ s0: li, vals: [last, ...gap, ...f.ml], color: ORANGE, wd: 3, dash: '7 5', label: t('Model') }])],
    band: last == null ? null : (gap.length ? { s0: Q.length, lo: f.lo, hi: f.hi } : { s0: li, lo: [last, ...f.lo], hi: [last, ...f.hi] }), pad: [40, 16, PHONE.matches ? 56 : 80, 30] });
  const S1 = F.summary, R1 = F.rolling_one_step;
  const provOpts = Object.keys(D[c][net].provinces).filter(x => F.series[`${c}|${net}|${x}`]).sort();
  const sel = (id, label, opts) => `<select id="${id}" aria-label="${t(label)}">${opts}</select>`;
  return `<div class="page">
  <h1 class="h1s">${t('Experimental forecast')}</h1>
  <p class="lede dk">${t('Trained on Q1 2023 to Q4 2024, tested on the four quarters of 2025, then used to project 2026.')}</p>
  <div class="fsel">${sel('fc-c', 'Country', byNat().map(x => `<option value="${x}"${x === c ? ' selected' : ''}>${nm(x)}</option>`).join(''))}
    ${sel('fc-n', 'Network', ['fixed', 'mobile'].map(n => `<option value="${n}"${n === net ? ' selected' : ''}>${t(n === 'fixed' ? 'Fixed broadband' : 'Mobile')}</option>`).join(''))}
    ${sel('fc-p', 'Area', `<option value="__national__">${t('Whole country')}</option>` + provOpts.map(x => `<option value="${esc(x)}"${x === p ? ' selected' : ''}>${nm(x)}</option>`).join(''))}</div>
  <div class="disc"><b>${t('Experimental. Not part of the poster.')}</b> ${t("One gradient-boosting model trained on the Ookla province-quarters of all nine countries. Ookla tests are user-initiated and subject to sampling bias, and the forecast inherits it. The model cannot anticipate sudden changes: Vietnam's mobile mean download rose from 63 to 147 Mbps in Q4 2024 and the model missed it.")}</div>
  <div class="fg">
    <section class="det"><h3>${t('{0}, {1} mean download speed (Mbps)', area, netName(net))}</h3>${ch}
      <div class="lg2"><span><i style="background:${INDIGO}"></i>${t('Measured')}</span><span><i style="background:${ORANGE}"></i>${t('Model')}</span><span><i class="bx"></i>${t('80% interval')}</span></div></section>
    <div class="col">
      <div class="kc"><span class="kl">${t('Projected, Q4 2026')}</span><b class="acc">${r0(f.ml.at(-1))}<small> Mbps</small></b><span>${t("80% interval {0} to {1} Mbps, from the model's errors on 2025.", r0(f.lo.at(-1)), r0(f.hi.at(-1)))}</span></div>
      <div class="kc"><span class="kl">${t('Median error on 2025')}</span><b>${S1.ml.median_ape.toFixed(1)}%</b><span>${t('against {0}% for repeating the last value.', S1.naive.median_ape.toFixed(1))}</span></div>
    </div>
  </div>
  <section class="det"><h3>${t('Errors on the four quarters of 2025')}</h3><div style="overflow-x:auto"><table class="mt"><tr><th>${t('Method')}</th><th>${t('Median error')}</th><th>${t('Mean error')}</th><th>${t('One quarter ahead')}</th></tr>
    ${[['ml', 'Model'], ['trend', 'Straight-line trend'], ['naive', 'Last value repeated']].map(([k, n]) => `<tr${k === 'ml' ? ' class="on"' : ''}><td>${t(n)}</td><td>${S1[k].median_ape.toFixed(1)}%</td><td>${S1[k].mape.toFixed(1)}%</td><td>${R1[k].mape.toFixed(1)}%</td></tr>`).join('')}</table></div>
    <p class="tn">${t('Absolute percentage error against the measured 2025 values, over {0} province-quarter forecasts. On mean error the three methods are about even; sudden changes hurt every method.', S1.ml.n.toLocaleString('en'))}</p></section>
</div>`;
}
function about() {
  const card = (h, p, links, img = '') => `<div class="rc${img ? ' rcp' : ''}">${img}<div class="rcb"><h3>${t(h)}</h3><p>${t(p)}</p>${links.map(([l, u]) => `<a class="lnk" href="${u}" target="_blank" rel="noopener">${t(l)}</a>`).join('')}</div></div>`;
  return `<div class="page"><h1 class="h1s">${t('About the data')}</h1>
  <div class="rcs">${card('The poster', 'Internet Landscape Study of Southeast Asian Countries. Poster, AINTEC 2026, Taipei.', [['Download PDF', 'poster.pdf']], `<a class="pthumb" href="poster.pdf" target="_blank" rel="noopener"><img src="poster.jpg" width="640" height="906" alt="${t('Poster preview')}" loading="lazy"></a>`)}
    ${card('Code', 'Data cleansing and preparation, and data analysis.', [['Open on GitHub', 'https://github.com/chissanupun/thailand-broadband-analysis']])}
    ${card('Datasets', 'Ookla Open Data (global Parquet files on Amazon S3) and M-Lab NDT7 (BigQuery).', [['Ookla Open Data', 'https://github.com/teamookla/ookla-open-data'], ['M-Lab NDT7', 'https://www.measurementlab.net/tests/ndt/ndt7/']])}
    ${card('Contact', 'Questions about the data or the study? Email the first author.', [['chissanupun.a@ku.th', 'mailto:chissanupun.a@ku.th']])}</div>
  <div class="ag"><section class="det"><h3>${t('Data cleansing and preparation')}</h3><p class="pp">${t("Ookla open data supplies quarterly internet-performance tiles split by connection type (fixed, mobile) at Quadkey zoom 16 (~600 × 600 m), each carrying mean download, upload, latency, and the underlying Speedtest submission count. We run point-in-polygon on the tiles to determine which province each point falls in, then compute a weighted average by each tile's test count. We filter only province-quarters with total_tests ≥ 100 and n_tiles ≥ 5. The bandwidth and latency requirements for different types of applications are adopted from Lübben and Misfeld.")}</p>
    <p class="pp mt16">${t('This site shows the Ookla dataset (229.4 million tests). The study also analyzes M-Lab NDT7 (760.6 million tests). We keep the two sources separate throughout and never pool their records.')}</p></section>
  <section class="det"><h3>${t('Authors')}</h3><p class="pp">${t('Chissanupun Athiwarikanon, Kunanont Malayanont, Pakkapon Pattanakul and Sukumal Kitisin, Kasetsart University.')}</p>
    <h3 class="mt16">${t('Cite this work')}</h3><p class="code">Athiwarikanon C., Malayanont K., Pattanakul P., Kitisin S. Internet Landscape Study of Southeast Asian Countries. AINTEC 2026.</p></section></div>
</div>`;
}

// ---------- player (kept as one live node so dragging survives re-renders) ----------
let timer = null;
const player = document.createElement('div');
player.className = 'pl';
player.innerHTML = `<button type="button" class="pb" data-play></button><div class="ptr"><input type="range" min="0" step="1"><div class="py"></div></div><span class="pq" aria-live="polite"></span>`;
const range = player.querySelector('input');
function syncPlayer() {
  range.max = Q.length - 1; range.value = S.qi; range.setAttribute('aria-label', t('Quarter')); range.setAttribute('aria-valuetext', ql(q()));
  range.style.setProperty('--p', `${S.qi / (Q.length - 1) * 100}%`);
  player.querySelector('.py').innerHTML = Q.map((qq, i) => qq.endsWith('Q1') ? `<span style="left:${(i / (Q.length - 1) * 100).toFixed(2)}%">${qq.slice(0, 4)}</span>` : '').join('');
  player.querySelector('.pq').textContent = ql(q());
  const b = player.querySelector('.pb'); b.innerHTML = timer ? ICON.pause : ICON.play; b.setAttribute('aria-label', t(timer ? 'Pause' : 'Play quarters'));
}
function stop() { clearInterval(timer); timer = null; }
function play() {
  if (timer) { stop(); return syncPlayer(); }
  if (S.qi === Q.length - 1) S.qi = 0;
  timer = setInterval(() => { S.qi++; if (S.qi >= Q.length - 1) { S.qi = Q.length - 1; stop(); } render(); }, 900);
  render();
}
// Re-rendering detaches the slider and kills a pointer drag, so while dragging only the label moves;
// the view redraws on release. Keyboard input redraws every step.
let dragging = false;
range.addEventListener('pointerdown', () => { dragging = true; });
addEventListener('pointerup', () => { if (dragging) { dragging = false; render(); } });
range.addEventListener('input', () => { stop(); S.qi = +range.value; if (dragging) syncPlayer(); else render(); });

// ---------- render + routing ----------
const app = document.getElementById('app');
function render() {
  document.documentElement.lang = S.lang;
  document.querySelectorAll('[data-lang]').forEach(b => b.setAttribute('aria-pressed', b.dataset.lang === S.lang));
  document.getElementById('paper-link').textContent = t('View the poster');
  const links = (withBeta, short) => NAV.map(([k, n, d]) => `<a href="#${k}"${S.view === k ? ' aria-current="page"' : ''}>${short ? `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="${d}"/></svg>` : ''}${t(short && k === 'about' ? 'About' : n)}${withBeta && k === 'forecast' ? ` <em class="beta">${t('beta')}</em>` : ''}</a>`).join('');
  document.getElementById('nav').innerHTML = links(true, false);
  document.getElementById('bbar').innerHTML = links(false, true);
  const sx = scrollX, sy = scrollY, inPlayer = player.contains(document.activeElement) ? document.activeElement : null, keep = inPlayer ? null : document.activeElement?.dataset;
  app.innerHTML = { overview, provinces, forecast, about }[S.view]();
  const slot = app.querySelector('[data-player]');
  zoomSetup();
  if (slot) { slot.replaceWith(player); syncPlayer(); inPlayer?.focus({ preventScroll: true }); }
  if (keep) { // put keyboard focus back on the same control after a re-render
    const k = ['c', 'p', 'net', 'ov', 'sort'].find(x => keep[x] != null);
    if (k) app.querySelector(`[data-${k}="${CSS.escape(keep[k])}"]`)?.focus({ preventScroll: true });
  }
  scrollTo(sx, sy);
}
function route() {
  if (!D) return;
  let parts; try { parts = location.hash.slice(1).split('/').map(decodeURIComponent); } catch { parts = []; }
  const [v, c, p] = parts;
  const view = NAV.some(([k]) => k === v) ? v : 'overview';
  if (view !== S.view) { stop(); scrollTo(0, 0); }
  S.view = view;
  if (view === 'provinces' && c && D[c]) { if (c !== S.country) S.prov = null; S.country = c; if (p) S.prov = p; }
  render();
}
const goProvinces = (c, p) => { location.hash = ['provinces', c, p].filter(Boolean).map(encodeURIComponent).join('/'); };

document.addEventListener('click', e => {
  const z = e.target.closest('[data-zoom]');
  if (z) { const svg = app.querySelector('.pmap'); if (z.dataset.zoom === 'reset') zoomPan(svg, 0, 0, +svg.dataset.w, +svg.dataset.h); else zoomBy(svg, z.dataset.zoom === 'in' ? 1.6 : 1 / 1.6); return; }
  const el = e.target.closest('[data-lang],[data-net],[data-ov],[data-sort],[data-play],[data-c],[data-p]');
  if (!el) return;
  const d = el.dataset;
  if (d.lang) { S.lang = d.lang; try { localStorage.setItem('lang', S.lang); } catch {} render(); }
  else if (d.net) { S.net = d.net; render(); }
  else if (d.ov) { S.ovTab = d.ov; render(); }
  else if (d.sort) { S.sort = { k: d.sort, dir: S.sort.k === d.sort ? -S.sort.dir : d.sort === 'country' ? 1 : -1 }; render(); }
  else if (d.play != null) play();
  else if (d.c) { if (S.view === 'provinces') goProvinces(d.c); else { S.country = d.c; goProvinces(d.c); } }
  else if (d.p) goProvinces(S.country, d.p);
});
document.addEventListener('keydown', e => {
  if ((e.key === 'Enter' || e.key === ' ') && e.target.matches('svg [data-c], svg [data-p], tr[data-c]')) { e.preventDefault(); e.target.dispatchEvent(new MouseEvent('click', { bubbles: true })); }
});
document.addEventListener('change', e => {
  const id = e.target.id, v = e.target.value;
  if (id === 'csel') goProvinces(v);
  else if (id === 'fc-c') { S.fc.c = v; S.fc.p = '__national__'; render(); }
  else if (id === 'fc-n') { S.fc.net = v; render(); }
  else if (id === 'fc-p') { S.fc.p = v; render(); }
});
addEventListener('hashchange', route);
PHONE.addEventListener('change', render);

(async () => {
  try { const l = localStorage.getItem('lang'); if (l === 'th' || l === 'en') S.lang = l; } catch {}
  try {
    [D, G, F] = await Promise.all(['data.json', 'geo.json', 'forecast.json'].map(f => fetch(f).then(r => { if (!r.ok) throw new Error(`${f}: HTTP ${r.status}`); return r.json(); })));
  } catch (err) {
    app.innerHTML = `<p class="loading">Could not load the data (${esc(err.message)}). Reload the page to try again.</p>`;
    return;
  }
  Q = Object.keys(D.Thailand.fixed.national);
  S.qi = Q.length - 1;
  route();
})();
