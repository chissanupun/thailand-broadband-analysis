"""Generate HTML slide deck covering all 8 Ookla country EDAs + cross-country comparison.
Modeled on outputs/build_slides.py (same dark deck engine); reference kept as-is for Thailand-only Thai deck.
"""
import base64, pathlib

OUTDIR = pathlib.Path(__file__).parent / 'ookla'
OUT_HTML = pathlib.Path(__file__).parent / 'slides_all_countries.html'


def img_b64(rel_path):
    p = OUTDIR / rel_path
    if not p.exists():
        return None
    data = base64.b64encode(p.read_bytes()).decode()
    return f"data:image/png;base64,{data}"


# country stats pulled directly from data/exports/*.csv (see conversation) -- not fabricated
COUNTRY_STATS = {
    'Thailand':    dict(n=77, mean=244, top='Nonthaburi (317 Mbps)', bottom='Mae Hong Son (137 Mbps)'),
    'Singapore':   dict(n=5,  mean=376, top='North Region (389 Mbps)', bottom='Central Region (341 Mbps)'),
    'Malaysia':    dict(n=16, mean=178, top='Kuala Lumpur (210 Mbps)', bottom='Kelantan (155 Mbps)'),
    'Vietnam':     dict(n=64, mean=135, top='Ho Chi Minh (178 Mbps)', bottom='Quảng Bình (109 Mbps)'),
    'Philippines': dict(n=17, mean=106, top='NCR (159 Mbps)', bottom='ARMM (48 Mbps)'),
    'Laos':        dict(n=18, mean=45,  top='Bokeo (60 Mbps)', bottom='Salavan (33 Mbps)'),
    'Cambodia':    dict(n=25, mean=44,  top='Svay Rieng (55 Mbps)', bottom='Stung Treng (36 Mbps)'),
    'Myanmar':     dict(n=14, mean=29,  top='Kayin (41 Mbps)', bottom='Rakhine (17 Mbps)'),
}

COUNTRY_ORDER = ['Thailand', 'Singapore', 'Malaysia', 'Vietnam', 'Philippines', 'Laos', 'Cambodia', 'Myanmar']
SLUGS = {'Thailand': 'thailand', 'Singapore': 'singapore', 'Malaysia': 'malaysia', 'Vietnam': 'vietnam',
         'Philippines': 'philippines', 'Laos': 'laos', 'Cambodia': 'cambodia', 'Myanmar': 'myanmar'}


def country_slides(country):
    slug = SLUGS[country]
    s = COUNTRY_STATS[country]
    slides = []
    slides.append({
        'type': 'text',
        'title': f'{country} — Fixed Broadband Overview',
        'bullets': [
            f'<b>{s["n"]} provinces/states</b> covered, Ookla Fixed Broadband, 2023 Q1 – 2025 Q4 (12 quarters)',
            f'National mean download speed: <b>{s["mean"]} Mbps</b>',
            f'Fastest: <b>{s["top"]}</b>',
            f'Slowest: <b>{s["bottom"]}</b>',
        ],
    })
    slides.append({
        'type': 'image',
        'title': f'{country} — Province Ranking (Mean Download Speed)',
        'image': f'{slug}/12_province_ranking_mean.png',
        'metric': f'Weighted average download speed per province, averaged across 12 quarters (2023 Q1 - 2025 Q4). National mean: {s["mean"]} Mbps.',
        'findings': [
            f'Fastest: {s["top"]}',
            f'Slowest: {s["bottom"]}',
            'Color = region grouping (see legend on chart)',
        ],
    })
    slides.append({
        'type': 'image',
        'title': f'{country} — GDP per Capita vs Download Speed',
        'image': f'{slug}/16_gdp_speed_scatter.png',
        'metric': 'OLS regression of province mean download speed against GDP per capita and population density.',
        'findings': [
            'Bubble size = population',
            'Dashed line = OLS fit (r and p-value shown on chart)',
            'See notebook for full multivariate model (GDP + density + tier + region)',
        ],
    })
    slides.append({
        'type': 'image',
        'title': f'{country} — Composite Divergence Map',
        'image': f'{slug}/27_divergence_map.png',
        'metric': 'Composite divergence score: sum of |z-scores| across 7 dimensions (tier gap, GDP gap, density gap, regional, UL/DL ratio, latency, coverage).',
        'findings': [
            'Left: divergence score choropleth (darker = more anomalous)',
            'Right: mean download speed choropleth with Tier 1 (red) / Tier 4 (dashed orange) borders',
        ],
    })
    return slides


SLIDES = [
    {
        'type': 'title',
        'title': 'Southeast Asia Broadband Analysis',
        'subtitle': 'Ookla Fixed Broadband — 8-Country Cross-Country Comparison',
        'meta': 'Data: Ookla Open Data (Fixed Broadband) · Thailand, Singapore, Malaysia, Vietnam, Philippines, Laos, Cambodia, Myanmar · 2023 Q1 - 2025 Q4',
    },
    {
        'type': 'text',
        'title': 'Scope & Data',
        'bullets': [
            '<b>Ookla Speedtest Intelligence</b> — tile-level fixed broadband data (~610x610m), aggregated to province/state',
            '<b>Coverage:</b> 8 countries, 236 provinces/states total, 12 quarters each (2023 Q1 - 2025 Q4)',
            '<b>New this round:</b> Cambodia, Myanmar, Laos, Malaysia added alongside existing Thailand/Singapore/Philippines/Vietnam',
            '<b>Reference data:</b> population, GDP per capita, density, region from national statistics offices / World Bank / Wikipedia',
            '<b>Limitation:</b> Cambodia/Laos/Myanmar have no published sub-national GDP -- national GDP repeated per province where noted',
        ],
    },
]

for c in COUNTRY_ORDER:
    SLIDES.extend(country_slides(c))

# ── Comparison section 1: every-country comparison ──────────────────────────
SLIDES.append({
    'type': 'text',
    'title': 'Comparison — Every Country',
    'bullets': ['Cross-country ranking on fixed and mobile broadband, using the same reliability-filtered methodology across all 8 countries.'],
})
SLIDES.append({
    'type': 'image',
    'title': 'Cross-Country Comparison — Fixed Broadband',
    'image': 'cross_country/01_all_country_fixed_dl.png',
    'metric': 'Mean download speed per country, reliability-filtered (total_tests>=100 & n_tiles>=5), averaged across all provinces and 12 quarters.',
    'findings': [
        'Singapore fastest (376 Mbps), Myanmar slowest (29 Mbps) -- a 13x gap',
        'Thailand ranks 2nd of 8, ahead of Malaysia/Vietnam/Philippines',
        'Mainland Southeast Asia (KH/MM/LA) lags city-states and Malaysia/Thailand substantially',
    ],
})
SLIDES.append({
    'type': 'image',
    'title': 'Cross-Country Comparison — Mobile/Cellular',
    'image': 'cross_country/02_all_country_mobile_dl.png',
    'metric': 'Mean mobile download speed per country, reliability-filtered, same methodology as fixed.',
    'findings': [
        'Singapore and Malaysia lead mobile too, but Vietnam moves ahead of Thailand on mobile (90 vs 72 Mbps)',
        'Thailand\'s fixed/mobile gap is wider than its neighbors -- fixed infrastructure investment outpaced mobile',
        'Myanmar lowest on both fixed and mobile',
    ],
})

# ── Comparison section 2: capital + top-5 city comparison ───────────────────
SLIDES.append({
    'type': 'text',
    'title': 'Comparison — Capital Cities & Top Provinces',
    'bullets': ['How much of each country\'s broadband performance is concentrated in the capital, and who the fastest provinces are nationally.'],
})
SLIDES.append({
    'type': 'image',
    'title': 'Capital City/Region vs National Average',
    'image': 'cross_country/03_capital_vs_national.png',
    'metric': 'Capital province/region mean download speed (bar) vs national average (diamond marker), fixed broadband.',
    'findings': [
        'NCR (Manila) has the largest capital premium: +50% over the Philippines national average',
        'Singapore and Myanmar are the only two where the capital/core region is actually BELOW the national average',
        'Cambodia (+23%) and Thailand (+21%) show the next-largest capital premiums',
    ],
})
SLIDES.append({
    'type': 'image',
    'title': 'Top 5 Fastest Provinces per Country',
    'image': 'cross_country/04_top5_provinces_per_country.png',
    'metric': 'Top 5 provinces/states by mean fixed broadband download speed, per country.',
    'findings': [
        'In most countries the capital is in the top 5, but rarely #1 (Nonthaburi > Bangkok in Thailand, Ho Chi Minh > Hanoi in Vietnam)',
        'Small/city-state geographies (Singapore) show the least spread between #1 and #5',
        'Wealthier non-capital provinces (special economic zones, border trade hubs) often outrank the capital',
    ],
})

SLIDES.append({
    'type': 'text',
    'title': 'Key Takeaways',
    'bullets': [
        '<b>Development tier explains most of the gap</b> -- Singapore/Malaysia/Thailand (upper-middle to high income) vs Cambodia/Laos/Myanmar (lower income)',
        '<b>Capital premium varies widely</b> -- from -9% (Singapore) to +50% (Philippines NCR)',
        '<b>Fixed vs mobile ranking flips</b> for several countries -- infrastructure investment strategy differs by country',
        '<b>The fastest province is not always the capital</b> -- secondary economic hubs often lead',
        '<b>Data quality caveat:</b> Cambodia/Laos/Myanmar have no official sub-national GDP; national GDP repeated as approximation',
    ],
})


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
        img_tag = f'<img src="{img_src}" alt="{s["title"]}">' if img_src else '<div class="img-missing">image not found</div>'
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
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Southeast Asia Broadband Analysis 2023-2025</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: 'IBM Plex Sans', 'Segoe UI', sans-serif;
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

.title-slide {{ background: #0d1117; text-align: center; }}
.title-content {{ max-width: 900px; }}
.title-slide h1 {{ font-size: 2.75rem; font-weight: 700; color: #f0f6fc; line-height: 1.25; margin-bottom: 24px; letter-spacing: -0.5px; }}
.title-slide .subtitle {{ font-size: 1.3rem; font-weight: 400; color: #8b949e; margin-bottom: 16px; }}
.title-slide .meta {{ font-size: 0.85rem; color: #484f58; font-family: 'IBM Plex Mono', monospace; }}
.title-slide::after {{ content: ''; display: block; width: 64px; height: 3px; background: #58a6ff; margin: 28px auto 0; }}

.text-slide {{ background: #0d1117; }}
.text-inner {{ width: 100%; max-width: 860px; }}
.text-slide h2 {{ font-size: 1.75rem; font-weight: 600; color: #f0f6fc; margin-bottom: 32px; padding-bottom: 12px; border-bottom: 1px solid #21262d; }}
.bullets {{ list-style: none; display: flex; flex-direction: column; gap: 14px; }}
.bullets li {{ font-size: 1.05rem; line-height: 1.65; color: #c9d1d9; padding: 14px 20px; background: #161b22; border: 1px solid #21262d; border-radius: 6px; }}

.image-slide {{ background: #0d1117; justify-content: flex-start; gap: 20px; align-items: stretch; }}
.image-slide h2 {{ font-size: 1.4rem; font-weight: 600; color: #f0f6fc; flex-shrink: 0; width: 100%; max-width: 1300px; align-self: center; padding-bottom: 12px; border-bottom: 1px solid #21262d; }}
.slide-body {{ display: flex; gap: 32px; flex: 1; min-height: 0; width: 100%; max-width: 1300px; align-self: center; }}
.img-col {{ flex: 1.6; min-width: 0; display: flex; align-items: center; justify-content: center; }}
.img-col img {{ max-width: 100%; max-height: calc(100vh - 200px); object-fit: contain; border-radius: 6px; border: 1px solid #21262d; }}
.img-missing {{ color: #484f58; font-size: 1rem; }}
.text-col {{ flex: 1; display: flex; flex-direction: column; gap: 16px; justify-content: flex-start; }}
.metric-badge {{ background: #161b22; border: 1px solid #30363d; border-left: 3px solid #58a6ff; border-radius: 0 6px 6px 0; padding: 12px 16px; font-size: 0.82rem; color: #8b949e; line-height: 1.6; font-family: 'IBM Plex Mono', monospace; }}
.findings {{ list-style: none; display: flex; flex-direction: column; gap: 10px; }}
.findings li {{ font-size: 0.95rem; line-height: 1.6; color: #c9d1d9; padding: 10px 14px; background: #161b22; border: 1px solid #21262d; border-radius: 6px; }}

.nav {{ position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%); display: flex; gap: 6px; align-items: center; z-index: 100; max-width: 90vw; flex-wrap: wrap; justify-content: center; }}
.dot {{ width: 7px; height: 7px; border-radius: 50%; border: none; background: #30363d; cursor: pointer; transition: all .2s; }}
.dot.active {{ background: #58a6ff; transform: scale(1.4); }}
.nav-btn {{ background: #161b22; border: 1px solid #30363d; color: #8b949e; font-size: 1.1rem; cursor: pointer; padding: 5px 14px; border-radius: 6px; transition: all .15s; }}
.nav-btn:hover {{ background: #21262d; color: #f0f6fc; }}
.slide-counter {{ position: fixed; top: 20px; right: 28px; font-size: 0.75rem; color: #484f58; font-family: 'IBM Plex Mono', monospace; }}
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
