"""Generate HTML slide deck covering all 8 Ookla country EDAs + cross-country comparison.

Dark deck engine originally shared with build_slides.py (Thailand-only Thai deck),
removed 2026-08-08 — its numbered inputs stopped existing after the NDT7 refactor,
and a Thailand-only deck conflicts with the paper's equal-scope rule.
"""
import base64, pathlib

ROOT = pathlib.Path(__file__).parent.parent
OUTDIR = ROOT / 'outputs' / 'ookla'
NDT7_OUTDIR = ROOT / 'outputs' / 'ndt7'
COMPARISON_OUTDIR = ROOT / 'notebook_outputs' / 'comparison'
OUT_HTML = ROOT / 'slides' / 'slides_all_countries.html'
OUT_HTML.parent.mkdir(parents=True, exist_ok=True)


def img_b64(rel_path, base=OUTDIR):
    p = base / rel_path
    if not p.exists():
        return None
    data = base64.b64encode(p.read_bytes()).decode()
    return f"data:image/png;base64,{data}"


# country stats pulled directly from data/exports/*.csv (see conversation) -- not fabricated
COUNTRY_STATS = {
    'Thailand':    dict(n=77, mean=244, top='Nonthaburi (317 Mbps)', bottom='Mae Hong Son (137 Mbps)',
                         mmean=72, mtop='Nakhon Ratchasima (125 Mbps)', mbottom='Phichit (54 Mbps)'),
    'Singapore':   dict(n=5,  mean=376, top='North Region (389 Mbps)', bottom='Central Region (341 Mbps)',
                         mmean=194, mtop='North-East Region (212 Mbps)', mbottom='Central Region (172 Mbps)'),
    'Malaysia':    dict(n=16, mean=178, top='Kuala Lumpur (210 Mbps)', bottom='Kelantan (155 Mbps)',
                         mmean=171, mtop='Putrajaya (248 Mbps)', mbottom='Perlis (141 Mbps)'),
    'Vietnam':     dict(n=64, mean=135, top='Ho Chi Minh (178 Mbps)', bottom='Quảng Bình (109 Mbps)',
                         mmean=90, mtop='Đà Nẵng (133 Mbps)', mbottom='Côn Đảo (42 Mbps)'),
    'Philippines': dict(n=17, mean=106, top='NCR (159 Mbps)', bottom='ARMM (48 Mbps)',
                         mmean=57, mtop='NCR (101 Mbps)', mbottom='ARMM (23 Mbps)'),
    'Laos':        dict(n=18, mean=45,  top='Bokeo (60 Mbps)', bottom='Salavan (33 Mbps)',
                         mmean=39, mtop='Bokeo (72 Mbps)', mbottom='Houaphan (31 Mbps)'),
    'Cambodia':    dict(n=25, mean=44,  top='Svay Rieng (55 Mbps)', bottom='Stung Treng (36 Mbps)',
                         mmean=33, mtop='Phnom Penh (46 Mbps)', mbottom='Svay Rieng (25 Mbps)'),
    'Myanmar':     dict(n=14, mean=29,  top='Kayin (41 Mbps)', bottom='Rakhine (17 Mbps)',
                         mmean=27, mtop='Mandalay (36 Mbps)', mbottom='Rakhine (19 Mbps)'),
}

COUNTRY_ORDER = ['Thailand', 'Singapore', 'Malaysia', 'Vietnam', 'Philippines', 'Laos', 'Cambodia', 'Myanmar']
SLUGS = {'Thailand': 'thailand', 'Singapore': 'singapore', 'Malaysia': 'malaysia', 'Vietnam': 'vietnam',
         'Philippines': 'philippines', 'Laos': 'laos', 'Cambodia': 'cambodia', 'Myanmar': 'myanmar'}


# NDT7 stats pulled directly from the executed notebooks (describe()/summary-table output,
# see conversation) -- not fabricated. Cambodia has 0% reliable coverage under the same
# total_tests>=100 & n_tiles>=5 threshold used everywhere else in this study, so it has no
# numeric stats here -- see cambodia_slides_ndt7() below, which is text-only.
NDT7_STATS = {
    'Thailand': dict(
        n_ref=77, n_fixed=72, n_mobile=25,
        mean=83.17, top='Samut Sakhon (131.6 Mbps)', bottom='Chiang Rai (51.3 Mbps)', reliable_pct=57.0, reliable_n='517/907',
        mmean=43.12, mtop='Rayong (106.5 Mbps)', mbottom='Surin (9.6 Mbps)', mreliable_pct=15.4, mreliable_n='81/526',
    ),
    'Vietnam': dict(
        n_ref=64, n_fixed=42, n_mobile=1,
        mean=42.17, top='Đà Nẵng (68.9 Mbps)', bottom='Quảng Ninh (18.6 Mbps)', reliable_pct=28.6, reliable_n='210/733',
        mmean=39.29, mtop='Ho Chi Minh (39.3 Mbps)', mbottom='Ho Chi Minh (39.3 Mbps)', mreliable_pct=1.0, mreliable_n='4/396',
    ),
}
NDT7_ORDER = ['Thailand', 'Vietnam']
NDT7_SLUGS = {'Thailand': 'thailand', 'Vietnam': 'vietnam', 'Cambodia': 'cambodia'}


def ndt7_country_slides(country):
    slug = NDT7_SLUGS[country]
    s = NDT7_STATS[country]
    slides = []
    slides.append({
        'type': 'text',
        'title': f'{country} — NDT7 Broadband & Mobile Overview',
        'bullets': [
            f'<b>{s["n_ref"]} provinces in reference</b>, but reliability (total_tests≥100 & n_tiles≥5 — same bar as Ookla) only clears for '
            f'<b>{s["n_fixed"]} fixed</b> / <b>{s["n_mobile"]} mobile</b>',
            f'Fixed — {s["reliable_n"]} province-quarters reliable (<b>{s["reliable_pct"]}%</b>) · mean <b>{s["mean"]:.0f} Mbps</b> · fastest: <b>{s["top"]}</b> · slowest: <b>{s["bottom"]}</b>',
            f'Mobile — {s["mreliable_n"]} province-quarters reliable (<b>{s["mreliable_pct"]}%</b>) · mean <b>{s["mmean"]:.0f} Mbps</b> · fastest: <b>{s["mtop"]}</b> · slowest: <b>{s["mbottom"]}</b>',
        ] + ([f'<b>Mobile caveat:</b> only 1 province ({s["mtop"].split(" (")[0]}) clears the reliability bar at all — top/bottom are the same province, not a real ranking'] if s['n_mobile'] <= 1 else []),
    })
    slides.append({
        'type': 'image2',
        'base': NDT7_OUTDIR,
        'title': f'{country} — NDT7 Province Ranking, Fixed vs Mobile (Mean Download Speed)',
        'images': [
            ('Fixed Broadband', f'{slug}/12_province_ranking_mean.png'),
            ('Mobile/Cellular', f'{slug}/mobile/12_province_ranking_mean.png'),
        ],
        'metric': f'Weighted average download speed per reliable province-quarter (2023 Q1 - 2025 Q4). Fixed mean: {s["mean"]:.0f} Mbps ({s["n_fixed"]} provinces) · Mobile mean: {s["mmean"]:.0f} Mbps ({s["n_mobile"]} province{"s" if s["n_mobile"]!=1 else ""}).',
        'findings': [
            f'Fixed — fastest: {s["top"]} · slowest: {s["bottom"]}',
            f'Mobile — fastest: {s["mtop"]} · slowest: {s["mbottom"]}',
            'Only reliability-filtered province-quarters shown — bar chart is shorter than the Ookla equivalent since most provinces never clear the threshold',
        ],
    })
    slides.append({
        'type': 'image2',
        'base': NDT7_OUTDIR,
        'title': f'{country} — NDT7 GDP per Capita vs Download Speed, Fixed vs Mobile',
        'images': [
            ('Fixed Broadband', f'{slug}/16_gdp_speed_scatter.png'),
            ('Mobile/Cellular', f'{slug}/mobile/16_gdp_speed_scatter.png'),
        ],
        'metric': 'OLS regression of province mean download speed against GDP per capita and population density, fixed and mobile separately, reliability-filtered.',
        'findings': [
            'Bubble size = population',
            'Dashed line = OLS fit (r and p-value shown on chart)',
            'Cross-validates against the equivalent Ookla slide for the same country — same direction/strength expected if both platforms measure real signal',
        ],
    })
    return slides


def cambodia_slides_ndt7():
    """Cambodia NDT7: 0% of province-quarters clear the n_tiles>=5 reliability bar for both
    Fixed and Mobile (see cambodia_eda.ipynb intro) -- a structural volume/geolocation-coarseness
    problem, not a bug. No per-province numbers exist to show; this is a text-only finding slide."""
    return [{
        'type': 'text',
        'title': 'Cambodia — NDT7 Broadband & Mobile: 0% Reliable',
        'bullets': [
            '<b>0 of 151</b> Fixed and <b>0 of 43</b> Mobile province-quarters clear the same <b>total_tests≥100 & n_tiles≥5</b> bar used everywhere else in this study',
            'Not a bug: NDT7 geolocation here is <b>city-level</b> (one lat/lon per city, not per device) — raw points collapse into very few zoom-16 tiles regardless of test volume',
            'Cambodia has 750K raw NDT7 records but only <b>47 distinct tiles nationwide</b> across all 3 years (~2/province)',
            'Compare Vietnam: 22M raw records → 856 tiles — 48x Cambodia\'s volume — which is what let it clear the bar at all (28.6% fixed, 1.0% mobile)',
            'Threshold kept identical to every other country/source in this study rather than loosened for Cambodia alone — the 0% result is itself the finding',
        ],
    }]


def country_slides(country):
    slug = SLUGS[country]
    s = COUNTRY_STATS[country]
    slides = []
    slides.append({
        'type': 'text',
        'title': f'{country} — Fixed & Mobile Overview',
        'bullets': [
            f'<b>{s["n"]} provinces/states</b> covered, Ookla Fixed + Mobile, 2023 Q1 – 2025 Q4 (12 quarters)',
            f'Fixed — national mean: <b>{s["mean"]} Mbps</b> · fastest: <b>{s["top"]}</b> · slowest: <b>{s["bottom"]}</b>',
            f'Mobile — national mean: <b>{s["mmean"]} Mbps</b> · fastest: <b>{s["mtop"]}</b> · slowest: <b>{s["mbottom"]}</b>',
        ],
    })
    slides.append({
        'type': 'image2',
        'title': f'{country} — Province Ranking, Fixed vs Mobile (Mean Download Speed)',
        'images': [
            ('Fixed Broadband', f'{slug}/12_province_ranking_mean.png'),
            ('Mobile/Cellular', f'{slug}/mobile/12_province_ranking_mean.png'),
        ],
        'metric': f'Weighted average download speed per province, averaged across 12 quarters (2023 Q1 - 2025 Q4). Fixed mean: {s["mean"]} Mbps · Mobile mean: {s["mmean"]} Mbps.',
        'findings': [
            f'Fixed — fastest: {s["top"]} · slowest: {s["bottom"]}',
            f'Mobile — fastest: {s["mtop"]} · slowest: {s["mbottom"]}',
            'Color = region grouping (see legend on chart)',
        ],
    })
    slides.append({
        'type': 'image2',
        'title': f'{country} — GDP per Capita vs Download Speed, Fixed vs Mobile',
        'images': [
            ('Fixed Broadband', f'{slug}/16_gdp_speed_scatter.png'),
            ('Mobile/Cellular', f'{slug}/mobile/16_gdp_speed_scatter.png'),
        ],
        'metric': 'OLS regression of province mean download speed against GDP per capita and population density, fixed and mobile separately.',
        'findings': [
            'Bubble size = population',
            'Dashed line = OLS fit (r and p-value shown on chart)',
            'See notebook for full multivariate model (GDP + density + tier + region)',
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

# ── NDT7 (M-Lab) cross-validation section ────────────────────────────────────
SLIDES.append({
    'type': 'text',
    'title': 'NDT7 (M-Lab) Cross-Validation',
    'bullets': [
        'Independent second data source — M-Lab NDT7 speed tests, same province x quarter methodology, same reliability threshold (total_tests≥100 & n_tiles≥5)',
        'Currently covers <b>Thailand, Vietnam, Cambodia</b> — Philippines pending a collaborator delivery, Singapore/Malaysia/Myanmar/Laos not yet started',
        'NDT7 reliability varies hugely by country: it tracks raw test volume, not just country size — Thailand 57.0% reliable, Vietnam 28.6%, Cambodia 0%',
    ],
})
for c in NDT7_ORDER:
    SLIDES.extend(ndt7_country_slides(c))
SLIDES.extend(cambodia_slides_ndt7())

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

# ── RQ1 / RQ2 deep dive — Thailand-focused, from notebooks/comparison/ ──────
SLIDES.append({
    'type': 'text',
    'title': 'RQ1 — Is Thai Internet Good or Bad?',
    'bullets': [
        'Ookla Global Index ranks Thailand fixed broadband <b>#13 worldwide</b> (looks good) -- but ETDA / consumer-complaint surveys report frequent slow/dropped connections (looks bad)',
        'Instead of arguing from opinion: cross-validate <b>Ookla</b> (8-country SEA context) and <b>NDT7/M-Lab</b> (independent second data source) against real app-requirement thresholds',
        'Thresholds from Lübben &amp; Misfeld (2022), Table 5 -- Voice 64 kbps/200ms · HD 5 Mbps · UHD 25 Mbps · Cloud gaming 44 Mbps + ≤25ms',
        'Both platforms measure <b>province-quarter averages</b> -- a structural limitation kept in mind throughout (see Key Findings)',
    ],
})
SLIDES.append({
    'type': 'image',
    'base': COMPARISON_OUTDIR,
    'title': 'RQ1 — Threshold Pass Rate, 8-Country SEA Context (Ookla Fixed)',
    'image': 'rq1_thresholds_ookla/cell0010_out0.png',
    'metric': 'Test-weighted % of province-quarters clearing each app-requirement threshold, per country, Thailand highlighted.',
    'findings': [
        'HD (5 Mbps) is a non-issue everywhere -- all 8 countries at 100%, Thailand min province-quarter average ~157 Mbps (31x the bar)',
        'UHD (25 Mbps) is where cross-country variance shows up: Myanmar drops to 20.6%; Thailand stays 100% in every province/quarter',
        'Cloud-gaming latency is the only threshold with real within-Thailand variance',
    ],
})
SLIDES.append({
    'type': 'image',
    'base': COMPARISON_OUTDIR,
    'title': 'RQ1 — Thailand Cloud-Gaming Latency Failures by Province (Ookla Fixed)',
    'image': 'rq1_thresholds_ookla/cell0013_out0.png',
    'metric': '# of quarters (of 11) each province exceeds the 25ms cloud-gaming latency bar. Speed is never the bottleneck in any of these rows.',
    'findings': [
        '<b>Mae Hong Son</b> exceeds 25ms in 10/11 quarters (up to 219ms in 2024-Q2) -- a chronic outlier, not a blip',
        '<b>Nan</b> joins it in 6/11 quarters; Phrae and Phangnga each show one one-off quarter',
        'Reads as remote/upland last-mile geography (far from IX/server infra), not a broad national problem -- these 4 provinces account for ~all of Thailand\'s ~0.5% national gaming-threshold failure',
    ],
})
SLIDES.append({
    'type': 'image',
    'base': COMPARISON_OUTDIR,
    'title': 'RQ1 — Ookla Fixed vs NDT7 Fixed vs NDT7 Mobile, Thailand',
    'image': 'rq1_thresholds_ndt7/cell0010_out0.png',
    'metric': 'Same threshold rubric applied to NDT7 (M-Lab), cross-validated against the Ookla Thailand-fixed result.',
    'findings': [
        'NDT7 fixed looks almost as uniformly "good" as Ookla fixed -- HD and UHD both 100% across all 517 province-quarters',
        'NDT7 mobile is where the ETDA-complaint side of RQ1 finally becomes visible in the data',
        'Every NDT7 measurement (fixed and mobile) fails the 25ms cloud-gaming bar -- reads as an M-Lab server-placement artifact, not a real Thailand latency problem',
    ],
})
SLIDES.append({
    'type': 'image',
    'base': COMPARISON_OUTDIR,
    'title': 'RQ1 — NDT7 Mobile UHD Pass Rate by Province (Where Mobile Actually Degrades)',
    'image': 'rq1_thresholds_ndt7/cell0015_out0.png',
    'metric': '% of province-quarters clearing the 25 Mbps UHD threshold, NDT7 mobile, ranked by test volume.',
    'findings': [
        '<b>Bangkok metro cluster underperforms</b>: Bangkok Metropolis, Nonthaburi, Samut Prakan, Pathum Thani clear UHD only 55-67% of the time -- each on a solid multi-quarter sample',
        'Chiang Mai and Chon Buri (comparably large samples) sit at 100% -- inverts the usual "rural underserved" framing; the capital metro is where mobile degrades, plausibly congestion',
        'First result across both platforms that plausibly supports the "internet feels bad" side of the RQ1 tension',
    ],
})
SLIDES.append({
    'type': 'text',
    'title': 'RQ1 — Key Findings',
    'bullets': [
        '<b>Fixed broadband is genuinely good</b> on both Ookla and NDT7, by every speed threshold -- Ookla\'s "#13 worldwide" framing holds at province-average granularity',
        '<b>Mobile is where the two datasets start explaining the ETDA-complaint side</b> -- Bangkok metro mobile UHD pass rate (55-67%) is the strongest lead so far for resolving the Ookla-vs-ETDA tension',
        '<b>Methodological finding, not just a Thailand result:</b> province-quarter <i>averages</i> cannot see complaint-survey behavior at all -- a metric with zero variance across 847 province-quarters cannot explain "slow/dropped" complaints, which are almost certainly tail behavior or reliability/uptime, not average-quarter speed',
        '<b>NDT7 latency floor (34-40ms) is an infrastructure artifact</b> -- no in-country M-Lab server, unlike Ookla\'s ISP-hosted servers -- do not read as "Thailand fails gaming latency"',
        'Next step: per-test/percentile-level analysis (p10/p25 download, not mean) to resolve what province-quarter averages structurally cannot see',
    ],
})

SLIDES.append({
    'type': 'text',
    'title': 'RQ2 — What\'s the Trend?',
    'bullets': [
        'RQ1 is a snapshot; RQ2 asks the time dimension -- is it getting <b>better, worse, or flat</b> over 2023-Q1 to 2025-Q4 (12 quarters)?',
        'Method follows the <b>Fig. 7 template from Lübben &amp; Misfeld (2022)</b> -- median line with 25th/75th percentile band per quarter, per segment',
        'Four segments, Thailand only: Ookla fixed, Ookla mobile, NDT7 fixed (reliable), NDT7 mobile (reliable)',
        '<b>Coverage caveat:</b> Ookla fixed is missing 2025-Q3 (export gap); NDT7 mobile province coverage collapses from ~15/quarter in 2023 to 2-3/quarter from 2024-Q2 on -- read that line as indicative past 2024-Q1, not a population estimate',
    ],
})
SLIDES.append({
    'type': 'image',
    'base': COMPARISON_OUTDIR,
    'title': 'RQ2 — Quarterly Download Trend, Thailand 2023Q1-2025Q4',
    'image': 'rq2_trends/cell0007_out0.png',
    'metric': 'Median download (Mbps) per quarter, IQR shaded, 4 segments.',
    'findings': [
        'Ookla fixed: steady near-linear growth, 207 → 294 Mbps (+42%) -- the least-noisy series here',
        'Ookla mobile: flat through 2023 (~55-60), then a real inflection from 2024-Q2, reaching 91-104 Mbps by 2025 -- consistent with a 5G-rollout story',
        'NDT7 fixed tracks the same upward direction (+56%) despite a ~3x lower absolute level (single-TCP-stream, lower-bound methodology)',
    ],
})
SLIDES.append({
    'type': 'image',
    'base': COMPARISON_OUTDIR,
    'title': 'RQ2 — Quarterly Upload Trend, Thailand 2023Q1-2025Q4',
    'image': 'rq2_trends/cell0010_out0.png',
    'metric': 'Median upload (Mbps) per quarter, IQR shaded, 4 segments.',
    'findings': [
        'Same shape as download, smaller magnitude -- Ookla fixed +35%, NDT7 fixed +63%, both monotonically up',
        'Ookla mobile flat at ~17 Mbps through 2023-2024, then rises to 23-25 Mbps in 2025 -- echoes the download inflection, supports the 5G read',
        'NDT7 mobile upload is noisy with no trend (thin-sample segment)',
    ],
})
SLIDES.append({
    'type': 'image',
    'base': COMPARISON_OUTDIR,
    'title': 'RQ2 — Quarterly Latency Trend, Thailand 2023Q1-2025Q4',
    'image': 'rq2_trends/cell0013_out0.png',
    'metric': 'Median latency (ms) per quarter, IQR shaded, 25ms cloud-gaming ceiling marked.',
    'findings': [
        'Ookla fixed flat at 8-10ms the entire 3 years -- already far under the ceiling, nothing to improve',
        'Ookla mobile holds 30-36ms, hovering just above the ceiling, at most a marginal dip late 2025',
        'NDT7 (fixed and mobile) stays 60-120ms for all 12 quarters, <b>never once approaching 25ms</b> -- confirms RQ1\'s latency floor is a persistent M-Lab server-placement artifact, not a transient or improving last-mile issue',
    ],
})
SLIDES.append({
    'type': 'text',
    'title': 'RQ2 — Bangkok Metro Mobile: A 2023 Problem That Resolved',
    'bullets': [
        'RQ1\'s pooled 2023-2025 average (55-67% UHD pass rate for Bangkok metro) hid a sharp step change',
        '<b>2023 (all 4 quarters): 0-7%</b> UHD pass rate for Bangkok metro, on a solid 4-province sample, while the rest of Thailand was already at 65-100%',
        '<b>2024-Q1 onward: 100%</b> every single quarter through 2025-Q4 -- a clean, sudden recovery, not a gradual close',
        'RQ1\'s "Bangkok metro underperforms" framing is therefore a <b>resolved 2023 story</b>, not an ongoing problem, as of mid-2025',
        'Caveat: from 2024-Q3 on, both groups run on 1-3 provinces/quarter -- the 2023→2024-Q1 transition itself (4 vs 8-13 provinces) is the reliable part of this finding',
    ],
})
SLIDES.append({
    'type': 'image',
    'base': COMPARISON_OUTDIR,
    'title': 'RQ2 — SEA Context: Thailand\'s Download Growth vs 7 Neighbors (Ookla Fixed)',
    'image': 'rq2_trends/cell0020_out0.png',
    'metric': 'Median download (Mbps) per quarter, 8 countries, Thailand highlighted.',
    'findings': [
        'Thailand +42.0% (207 → 294 Mbps) is the <b>2nd-slowest</b> of 8 countries -- only the Philippines (+23.6%) grows slower',
        'Myanmar/Cambodia/Vietnam/Laos post +94-164% growth, but off a much lower 2023 base (20-92 Mbps) -- classic catch-up growth',
        'Thailand\'s <b>absolute level stays 2nd-highest of 8 throughout</b>, behind only Singapore -- slower %growth reflects a high starting point, not stagnation',
        'Open question for Discussion: Singapore (+96.4%) and Malaysia (+79.5% from a lower base than Thailand) both outgrow Thailand despite starting higher or comparable -- base effect alone doesn\'t fully explain it',
    ],
})
SLIDES.append({
    'type': 'text',
    'title': 'RQ2 — Key Findings',
    'bullets': [
        '<b>Getting better, on every metric with a usable sample</b> -- no segment shows a worsening trend anywhere in the 12 quarters',
        '<b>Download/upload:</b> monotonic growth on both fixed platforms and Ookla mobile (real 2024-2025 speed jump); NDT7 mobile too thin post-2024-Q1 to confirm independently',
        '<b>Latency:</b> Ookla stays flat and well under the 25ms ceiling throughout; NDT7\'s 60-120ms floor shows no convergence toward 25ms across 3 years -- structural, not transient',
        '<b>Bangkok metro mobile (RQ1 follow-up):</b> the underperformance RQ1 found was a resolved 2023 problem, not an ongoing one -- the single most important qualifier to add to the RQ1 write-up',
        'Open question: whether NDT7 mobile\'s sample recovers enough post-2024 to say anything with confidence at province level again',
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
        img_src = img_b64(s['image'], base=s.get('base', OUTDIR))
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

    if t == 'image2':
        panels = []
        for label, rel in s['images']:
            src = img_b64(rel, base=s.get('base', OUTDIR))
            tag = f'<img src="{src}" alt="{label}">' if src else '<div class="img-missing">image not found</div>'
            panels.append(f'<div class="img-panel"><div class="img-panel-label">{label}</div>{tag}</div>')
        items = ''.join(f'<li>{b}</li>' for b in s['findings'])
        return f"""
<section class="slide image-slide" id="slide-{idx}">
  <h2>{s['title']}</h2>
  <div class="slide-body">
    <div class="img-col img-col-dual">{''.join(panels)}</div>
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
.img-col-dual {{ gap: 16px; }}
.img-panel {{ flex: 1; min-width: 0; display: flex; flex-direction: column; align-items: center; gap: 8px; }}
.img-panel img {{ max-width: 100%; max-height: calc(100vh - 230px); object-fit: contain; border-radius: 6px; border: 1px solid #21262d; }}
.img-panel-label {{ font-size: 0.8rem; color: #8b949e; font-family: 'IBM Plex Mono', monospace; letter-spacing: 0.5px; text-transform: uppercase; }}
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
