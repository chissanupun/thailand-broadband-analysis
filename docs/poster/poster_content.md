# Poster content bank — AINTEC 2026 poster track

Everything here is paste-ready. Text is quoted or condensed from `docs/paper/paper.tex` unless marked otherwise.
Figures are copied into `docs/poster/assets/` (see catalog in section 7). Previous poster draft: `poster_v_dense.tex` (compiles: `pdflatex poster_v_dense.tex`).

Deadline: poster PDF (max 20.5 MB) + abstract text due Mon 2026-09-28 8pm EDT = Tue 09-29 7am Thai.

---

## 0. Read first — problems found while building

1. **Paper's own Figure 1 and capital figure are 8-country (no Indonesia)** — `assets/image1.png` and `assets/image2.png` list Singapore, Thailand, Malaysia, Vietnam, Philippines, Laos, Cambodia, Myanmar only, while the paper text says "nine countries". The paper prose numbers (Singapore 376 national / 341 Central Region, Bangkok 295 vs 244, KL 210 vs 178, NCR 159 vs 106, Hanoi 153 vs 135, Phnom Penh 54 vs 44, Vientiane 53 vs 45, Yangon 27 vs 29, "12x") come from those two 8-country figures.
2. **Regenerated 9-country versions** (`assets/regen_fixed_dl.png`, `assets/regen_capital.png`; test-weighted, Indonesia included) give different numbers — see section 3, Finding 2. Same ranking and direction, different magnitudes. **Pick one set and use it consistently on the poster; ask อาจารย์ / the paper author which is current.**
3. Poster text next to a chart must quote that chart. Do not mix paper-prose numbers with regenerated charts (the previous draft caught this).
4. Cloud-gaming **latency** (25 ms) is not measured on NDT7 (M-Lab servers are offshore, latency inflated; อาจารย์'s ruling 2026-08-13). The paper's success rates use **download-speed thresholds**. Do not claim a latency result on the poster.
5. Anonymity: paper.tex is `\author{Anonymous}`. Poster currently uses real names (your call 09-21). The QR code / GitHub URL contains your username.
6. `paper.tex` still has `[CITATION NEEDED]` markers (Rajabiun & McKelvey, Feamster & Livingood). Do not cite them on the poster until resolved.

---

## 1. Title options
1. Beyond Speed Rankings: A Nine-Country Measurement Study of Southeast Asia's Application-Layer Digital Divide
2. Basic Access Is Universal, Application-Tier Access Isn't: Measuring Broadband in Southeast Asia
3. (short, paper's own) Internet Landscape Study of Southeast Asian Countries

Short tagline candidates:
- "Speed rankings say who is fastest. Applications say who is usable."
- "100% for HD video. Under 38% for cloud gaming."

## 2. Abstract (HotCRP text field, ~230 words — old draft from `abstract.md`)

Southeast Asia's broadband landscape is usually judged by headline speed-index rankings, which say little about whether real applications actually work for users. We analyze over 990 million speed tests (Ookla and M-Lab NDT7, Q1 2023 – Q4 2025) across nine countries — Thailand, Vietnam, Laos, Myanmar, Cambodia, Indonesia, the Philippines, Malaysia, and Singapore — and evaluate them against the bandwidth thresholds of four application classes: voice, HD video streaming, UHD video streaming, and cloud gaming.

We find that basic connectivity is a solved problem: voice and HD streaming succeed at essentially 100% across all nine countries, on both fixed and mobile networks. This uniformity collapses under higher-tier demand. Fixed broadband shows sharp urban-rural stratification — capital hubs reach speeds up to 12x their country's lower-tier regions, a gap invisible in national rankings. At the application layer, tier-one markets (Singapore, Thailand, Malaysia) sustain UHD streaming and cloud gaming reliably, while several developing markets fall below 38% success on the same thresholds, even though mobile networks offer a more geographically uniform baseline in countries like Myanmar, Laos, and Cambodia.

Our results argue that speed-index rankings obscure the digital divide that actually matters: not whether a country "has broadband," but whether that broadband survives contact with a real application. We use this framing to identify where infrastructure investment — fiber build-out, mobile-to-fixed migration, transport-layer optimization — would close real usage gaps rather than just index-ranking gaps.

(The "12x" here is the paper-prose number; see section 0 item 2.)

## 3. Text blocks (paste-ready)

### Big-number callouts
| Number | Label | Source |
|---|---|---|
| 990M | speed tests (Ookla 229.4M + NDT7 760.6M) | paper abstract |
| 9 | Southeast Asian countries | paper |
| 12 | quarters, Q1 2023 – Q4 2025 | paper §Datasets |
| 100% | HD-video success, every country, every quarter | paper §Analysis |
| <38% | cloud-gaming success in weakest markets (Indonesia <38%, Myanmar <31%) | paper |
| 3.2x | Thailand fixed vs mobile (largest gap) | paper |
| 12x (paper) / 16x (regen) | best capital vs worst capital | see section 0 |
| 300 vs 23 Mbps | fastest fixed ISP (MyRepublic SG) vs fastest in Myanmar | paper |
| 176 vs 10 Mbps | most-used fixed ISP: Singtel Fibre vs Mytel Myanmar | paper |
| 12th vs 81% | Thailand Ookla global rank vs consumers reporting problems | paper |

### Motivation
Speed-index rankings say little about whether real applications work. Thailand ranked 12th worldwide for fixed broadband (Ookla Speedtest Global Index, June 2026), yet a 2023 Thailand Consumer Council survey found 81% of 2,924 respondents had connection problems — mostly slow and dropping connections. The mismatch is not unique to Thailand.

Research question: how do nine Southeast Asian networks perform against the demands of real applications — voice, HD video, UHD video and cloud gaming?

### Data
- Ookla Open Data: 229,367,221 tests; quarterly tiles ~600 m x 600 m (Quadkey zoom 16); fixed and mobile; downloaded as Parquet from Amazon S3. Largest: Indonesia 74.2M; smallest: Laos 875,799.
- M-Lab NDT7: 760,607,387 tests; single-stream; largest Indonesia 367.2M; smallest Laos 139,693.
- Period: Q1 2023 – Q4 2025 (12 quarters), nine countries.
- Pipeline: clean throughput/duration <= 0; ip-api.com flags (mobile/hosting/proxy) and ASN; NDT7 points joined to province polygons (GeoPandas, `sjoin_nearest` for coastal points); Ookla tiles point-in-polygon on geoBoundaries ADM1; test-weighted province averages; keep province-quarters with >= 100 tests and >= 5 tiles.
- Operators grouped by ASN, not raw ISP-name strings (one operator can appear under hundreds of spellings).
- Known gaps: Vietnam and Cambodia mobile data missing for some small provinces/quarters. Indonesia NDT7 was sampled (27-day sample) because of volume.

### Application thresholds (paper Table 1, after Lübben & Misfeld 2022)
| Application | Data rate | Latency |
|---|---|---|
| Voice | 64 kbps | 200 ms |
| Video streaming (HD) | 5 Mbps | few seconds |
| Video streaming (UHD) | 25 Mbps | few seconds |
| Cloud gaming | 44 Mbps | 25 ms |

Success rate = national-level share meeting the **download-speed** threshold, per quarter (Q1 2024 – Q4 2025 in the paper's figures).

### Finding 1 — Basics are solved
Voice (>= 64 kbps) and HD video (>= 5 Mbps) succeed at 100% in every country, every quarter, on fixed and mobile networks (lines are offset a few pixels in the charts only so they stay visible). Even the lowest-tier broadband markets meet the basic floor.

### Finding 2 — Urban–rural stratification
**Version A — paper prose (8-country figure, `assets/image2.png`):**
Singapore leads the region overall, with its Central Region at 341 Mbps, slightly below its national baseline (376). Most other capital regions outperform their national benchmark: Bangkok Metropolis 295 (vs 244), Kuala Lumpur 210 (vs 178), NCR Philippines 159 (vs 106), Hanoi 153 (vs 135). Cambodia (Phnom Penh 54 vs 44) and Laos (Vientiane 53 vs 45) show modest capital premiums; Myanmar (Yangon 27) sits slightly below its national 29. Top capital hubs reach speeds more than 12 times higher than lower-tier regions.

**Version B — regenerated, 9 countries, test-weighted (`assets/regen_capital.png`):**
Capital vs national mean (Mbps): Singapore 361.0 vs 394.8 (only capital below its nation, besides Myanmar 22.0 vs 24.6); Thailand 298.8 vs 276.9; Malaysia 212.3 vs 194.8; Vietnam 161.4 vs 159.7; Philippines 159.6 vs 132.0; Cambodia 55.6 vs 53.0; Laos 55.6 vs 51.2; Indonesia 63.4 vs 41.2; Myanmar 22.0 vs 24.6. Best capital / worst capital = 361.0 / 22.0 = 16.4x.
National fixed means (regen, `assets/regen_fixed_dl.png`): Singapore 395, Thailand 277, Malaysia 195, Vietnam 160, Philippines 132, Cambodia 53, Laos 51, Indonesia 41, Myanmar 25 (16.1x spread).

### Finding 3 — The speed gap is widening
Singapore nearly doubled its median provincial fixed speed, from ~280 Mbps (early 2023) to ~550 Mbps (late 2025). Thailand grew steadily from ~200 to ~300. Malaysia and Vietnam form a middle tier; Vietnam accelerated to catch Malaysia at over 200 Mbps by Q4 2025. The Philippines moved from ~100 to ~120. Laos, Cambodia, Indonesia and Myanmar stayed flat below 60 Mbps for all three years (Myanmar briefly dipped near 0 at the end of 2025). Figure: `assets/image6.png`.

### Finding 4 — Application tiers diverge
**UHD video (>= 25 Mbps):** Malaysia, Singapore, Thailand, Philippines, Vietnam: 100% every quarter. Laos volatile: ~76% (Q1 2024) → 50% (Q4 2024) → 100% (Q1 2025) → ~92% (Q4 2025). Cambodia 67–86%. Indonesia ~36% → 65%. Myanmar 40–55%.

**Cloud gaming (>= 44 Mbps):** Singapore ~100% throughout. Thailand and Malaysia 87–100%. Philippines 58–93%. Vietnam from <50% (Q1 2024) to 100% (Q1 2025), settling ~94%. Cambodia 38–49%. Laos spikes to 85% in early 2025, back to ~52%. Indonesia <38%, Myanmar <31%.

Figures: `assets/fig_video_uhd_national.png`, `assets/fig_cloud_gaming_national.png` (and `_capital` variants for capital-only rates).

### Finding 5 — Fixed broadband varies far more than mobile
Fixed vs mobile mean download (`assets/image4.png` shows all nine with ratios): Singapore 2.1x (~400 vs ~190 Mbps), Thailand 3.2x (~275 vs ~85), Malaysia 1.1x, Vietnam 1.8x, Philippines 1.9x, Cambodia 1.4x, Laos 1.4x, Indonesia 1.1x, Myanmar 0.8x — the only country where mobile beats fixed (mobile-first). Mobile means (`assets/image3.png`): Singapore 190, Malaysia 173, Vietnam 88, Thailand 86, Philippines 71, Cambodia 39, Laos 38, Indonesia 36, Myanmar 32.

### Finding 6 — Who delivers the speed (operators)
**Fastest major ISP (>= 5% share), fixed** (`assets/image7.png`): MyRepublic (SG) 300 Mbps (7% share); TIME dotCom (MY) 196 (13%); AIS (TH) 126 (23%); Globe (PH) 90 (12%); Viettel (VN) 71 (39%); Biznet (ID) 43; Unitel (LA) 43; Angkor Data Communication (KH) 31; Global Technology (MM) 23.
**Fastest major ISP, cellular:** Singtel Mobile 104 Mbps (37%); Maxis (MY) 53 (27%); the other seven markets cluster at 22–39 Mbps (Viettel 39, DITO 31, Unitel 22 lowest).
**Most-used ISP by sample volume, fixed** (`assets/image8.png`): Singtel Fibre 176 Mbps (n=2.6M); True (TH) 115 (5.8M); TM (MY) 113 (1.1M); Viettel 71 (4.4M); PLDT (PH) 61 (48.6M); Unitel 43; Metfone (KH) 30; Telkom Indonesia 19 (67.2M); Mytel (MM) 10.
**Most-used, cellular:** Singtel Mobile 104 (n=841k); all others 19–45 (U Mobile MY 45, Viettel 39, Telkomsel 25, MPT 25, Unitel 22, Smart PH 21, True 20, Metfone 19).
Takeaway line: dominant fixed-broadband performance varies wildly by market, while cellular is far more uniform.

### Finding 7 — Where the speed is (top provinces)
Top five fastest provinces per country, hatched = provinces with <5% of national tests (`assets/image5.png`, large 2046x1705). Singapore >360 Mbps in every region (North Region 416). Thailand's top five are Bangkok-adjacent provinces >290 Mbps, all hatched (low sample). Malaysia and the Philippines concentrate in hubs (Kuala Lumpur 212, NCR 160) with significant samples. Emerging markets (Vietnam, Indonesia, Cambodia, Laos, Myanmar) top out below 200 Mbps (weaker ones <70) and rely on low-sample provinces to fill their top ranks.

### Takeaway / conclusion
Raw speed rankings hide the divide that matters: not whether a country "has broadband," but whether that broadband survives a real application. Basic needs (voice, HD video) are met everywhere; UHD video and cloud gaming expose the gap. Fixed broadband shows stark regional and urban–rural stratification, while mobile offers a more uniform but less capable baseline. This argues for targeted fiber deployment, regional infrastructure investment and transport-layer optimization to reach digital equity across Southeast Asia.

### Ethics (one line, if space)
Only public, aggregated/anonymized open datasets (Ookla Open Data, M-Lab NDT7 via BigQuery); IPs used transiently for ASN/geolocation via ip-api.com and not retained.

## 4. Extra "interesting" material (background from the paper — good for small text boxes)

- **Ookla vs M-Lab NDT7 — why both.** Ookla servers sit inside access ISPs and use many parallel TCP streams (measures last-mile capacity, higher throughput). NDT7 uses single-stream, off-net servers (closer to what a browsing/streaming flow sees). Ookla open data is spatial tiles (great for geography, no time-of-day); NDT7 is per-test records (peak-hour, protocol behavior). They are complementary. *(Rajabiun & McKelvey / Feamster & Livingood claims are still [CITATION NEEDED] in paper.tex.)*
- **NDT7 modernizations:** runs over WebSockets/TLS on ports 80/443 (no middlebox port filtering); integrates TCP BBR, reducing self-induced bufferbloat and giving lower, more accurate baseline latency.
- **Ookla sampling bias caveat (Deng et al. 2021):** user-initiated tests are biased and NAT multiplexing distorts them — motivates the filters above.
- **Threshold method (Lübben & Misfeld 2022):** Germany study on M-Lab NDT; isolate busy hours (8–10 p.m.), dedupe repeated IP measurements, control server location; judge services against application requirements. We adopt their thresholds.
- **Why NDT7 latency is unusable for cloud gaming here** (from repo notes `notebooks/ndt7/mlab_server.ipynb`, not in paper): most countries' tests hit Singapore/Hong Kong/Chennai servers (Thailand 52.9% Singapore, 0% in-country; Philippines 94.6% in-country Manila). Speed of light to Singapore alone ~20 ms RTT.

## 5. Old poster content (kept from earlier drafts)

**v1 (09-15) headline structure — 3 findings, 3 columns:** (1) basics solved, (2) urban–rural up to 12x, (3) application tiers diverge, <38%. Old Finding 2 body used paper-prose numbers; old caption said "Regenerated 09-21 ... confirm with paper author" (debug note, not for audience).

**Old takeaway text:** "Speed-index rankings obscure the digital divide that actually matters: not whether a country 'has broadband,' but whether that broadband survives contact with a real application. This argues for targeted fiber deployment, mobile-to-fixed migration, and transport-layer optimization aimed at closing usage gaps — not just ranking gaps."

**Old methodology paragraph (removed):** "Ookla Open Data and M-Lab NDT7 (round-trip latency, via Google BigQuery) ... Provinces below 5% of a country's national test volume are flagged as thin-data." — the "NDT7 latency" wording conflicted with the Ookla-only cloud-gaming ruling; the 5% thin-data rule comes from the repo's per-province analysis (`docs/figures_th.md`), not from the paper.

**Old methodology table (removed, partly wrong):** it said cloud gaming used "Ookla + M-Lab NDT7" — replaced by paper Table 1 above.

## 6. Layout notes from the previous build (tikzposter, A0 portrait, `poster_v_dense.tex`)
- tikzposter did not wrap `\\` in `\title` (2000 pt overfull box) — fix was `\title{\parbox{0.92\linewidth}{\centering ...}}`.
- `\usebackgroundstyle{Rays}` cut lines through text; plain white + crimson accent (`titlebgcolor`) read best.
- Content that fit one A0 page: title + 4-stat band + 3 columns (~5 charts, 1 table, QR). Adding the top-5 image (image5) overflowed the page.
- Low-res figures: `image7.png` (ISP bars) labels get tiny at poster scale; regenerate or crop before printing. `image3/4/9–12` are ~680 px wide (fine at half-column, soft if larger).
- `qrcode` LaTeX package needed for the QR (Overleaf has it; local texlive here has it).

## 7. Figure catalog (`docs/poster/assets/`)
| File | What it shows | 9-country? | Notes |
|---|---|---|---|
| `image1.png` | Ookla fixed mean download bar (376/244/178/135/106/45/44/29) | **No — 8, no Indonesia** | paper Fig; superseded by `regen_fixed_dl.png` |
| `image2.png` | Capital vs national average, fixed | **No — 8, no Indonesia** | matches paper prose (341/295/…); "12x" source |
| `regen_fixed_dl.png` | Fixed mean download by country, test-weighted | Yes | script `scripts/build_cross_country_figs_8c.py` (fixed 09-21 to include Singapore) |
| `regen_capital.png` | Capital vs national mean | Yes | same script; Finding 2 Version B |
| `image3.png` | Mobile mean download by country | Yes | 690x400 |
| `image4.png` | Fixed vs mobile bars with ratio labels | Yes | 680x376; best single "fixed vs mobile" chart |
| `image5.png` | Top-5 provinces per country (hatched = low sample) | Yes | 2046x1705, high res |
| `image6.png` | Growth of median provincial fixed speed, Q1 2023–Q4 2025 | Yes | 1115x615 |
| `image7.png` | Fastest major ISP (>=5% share) fixed + cellular | Yes | small labels |
| `image8.png` | Most-used ISP fixed + cellular (n shown) | Yes | 1233x445 |
| `image9.png` | Voice success rate national (paper version) | Yes | flat 100% line |
| `image10–12.png` | HD / UHD / cloud-gaming success (paper versions) | Yes | 616–673 px wide |
| `fig_voice_national.png`, `fig_video_hd_national.png`, `fig_video_uhd_national.png`, `fig_cloud_gaming_national.png` | Regenerated national success-rate charts (offsets on flat lines) | Yes | 11x5 in |
| `fig_*_capital.png` | Same four metrics, capital provinces only | Yes | not used in paper/poster yet — possible extra panel |

## 8. Ideas not yet used (verify before putting on a poster)
- **Capital-only success rates** (`fig_*_capital.png`): would let you say "even capitals fail cloud gaming in X". No numbers verified yet — read the chart before quoting.
- **Per-country market share charts:** `outputs/ndt7/comparison/rq4_marketshare_<country>_{broadband,cellular}.png`, `rq4_top5_<country>.png`, `rq4_within_gap.png`, `rq4_leader_speed_compare.png` — ISP structure. **Moved to the separate ISP poster, 2026-09-24 (อาจารย์'s call); see `docs/poster/isp/content.md`.** The old "Singapore ASN blocked, RQ4 is 8 countries" caveat is resolved — `build_isp_quarterly.py sg` ran 08-20, all `rq4_*` figures are 9 countries (verified 09-24).
- **Peak-hour (RQ3) figures:** `outputs/ndt7/comparison/rq3_*.png` (busy-hour degradation, diurnal RTT/throughput, capital vs rest). Not in the current `paper.tex`. Notes from earlier drafts: NDT7 absolute RTT is unreadable as domestic latency (offshore servers), busy/quiet ratios are the defensible part; Vietnam's odd diurnal profile is likely Hong Kong transit. Treat as unverified for the poster.
- **Server geography:** `outputs/ndt7/mlab_server/01_top8_server_share_by_country.png` — good "why not NDT7 latency" visual.
- **Growth vs base / catch-up, provincial spread, capital vs top-5:** `outputs/ookla/cross_country/05–09_*.png` — built in the 8-country era, some contaminated (see repo note); regenerate before use.
- **Country deep-dives** (`outputs/ookla/<country>/`, `outputs/ndt7/<country>/`): choropleths, heatmaps, GDP vs speed scatter, upload/download symmetry — per-country only; equal-scope rule says no country gets deeper treatment than others, so avoid a single-country panel.
- **Thai-language framing** (for a lay caption): "อันดับ 12 ของโลก แต่ผู้บริโภค 81% เจอปัญหา" — the mismatch is the story.

## 9. Still open (yours)
- Show อาจารย์; zoom-test at real print size; outside "state the finding in 10 seconds" test.
- Decide Finding 2 numbers (paper prose 8-country vs regenerated 9-country) — and whether to correct paper Figures 1–2 (currently missing Indonesia).
- Decide anonymity of the PDF / QR link.
- HotCRP form: title, poster PDF (<= 20.5 MB), abstract, authors (Chissanupun Athiwarikanon chissanupun.a@ku.th; Kunanont Malayanont kunanont.m@ku.th; Pakkapon Pattanakul pakkapon.p@ku.th), PC conflicts (none — Adisorn Lertsinsrubtavee, Kenjiro Cho, Kun-Chan Lan, Marnel Peradilla).
