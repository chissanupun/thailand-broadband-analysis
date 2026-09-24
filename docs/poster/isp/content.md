# ISP poster — content bank

**Owner: Kunanont Malayanont (kunanont.m@ku.th).** Split off from the main poster on 2026-09-24 on อาจารย์'s instruction: the ISP / market-structure material comes out of `docs/poster/poster.tex` and becomes this second poster.

**Assumed target: AINTEC '26 poster track, PDF ≤ 20.5 MB + abstract text, due Mon 2026-09-28 8pm EDT = Tue 09-29 07:00 Thai. Not confirmed — check before building to that date.**

This file is the same shape as the main poster's `docs/poster/poster_content.md`: problems first, then paste-ready text, then a figure catalog, then what is still open. Everything here is either quoted from `docs/paper/paper.tex` or recomputed from `data/exports/ndt7_isp_*_quarterly.csv`; which one is marked on every number. Provenance and the recompute method are in the appendix.

---

## 0. Read first — five things that will bite

1. **Every ISP number on this poster is M-Lab NDT7, not Ookla.** The pipeline is `scripts/build_isp_quarterly.py` → `data/exports/ndt7_isp_<country>_quarterly.csv`. The main poster's geography and application-tier numbers are Ookla. **Do not mix the two on one panel**, and say "M-Lab NDT7" in the methods block so a reader can tell.
2. **This is 9 countries, Singapore included.** The old "Singapore has no ASN, RQ4 is 8 countries" limitation is **dead** — `build_isp_quarterly.py sg` ran on 2026-08-20, the CSV has 3,761 rows with real ASNs (12 `(unknown)` rows), and every `rq4_*.png` is dated 2026-08-20 and shows 9 countries. Verified by reading the figures on 2026-09-24. Do not reprint the 8-country caveat.
3. **Operators are pooled by name, ASNs are the grouping key underneath.** One operator can hold many ASNs (Thai NT has 12, AIS has 4, True has 2). The published charts pool a operator's ASNs and then test-weight. A per-ASN aggregation gives different numbers (True 128 per-ASN vs 115 pooled) — **use the pooled figures**, section 6 says how to reproduce them.
4. **No latency claims.** NDT7's servers are offshore for almost every country here (Thailand 52.9 % of tests land in Singapore, 0 % in-country; only the Philippines is domestic at 94.6 %). อาจารย์'s ruling 2026-08-13: NDT7 latency is not readable as domestic latency. Everything on this poster is **download throughput**.
5. **Market share here is share of NDT7 tests, not subscribers.** It is a measurement-side proxy. Label it that way on the poster; a reader who takes it as a regulatory market share will be wrong.

---

## 1. Why this is its own poster

The main poster answers *where* the speed is (geography, urban–rural) and *what breaks* (application tiers). This one answers **who sells it** — and the finding that motivates the split:

> **The fastest operator in a market is almost never the one people actually use.**

Singapore's fastest major fixed operator, MyRepublic, averages 300 Mbps on a 7 % share; the operator most people are on, Singtel Fibre, averages 176. Indonesia is the extreme: Biznet 43 Mbps at 5 % share against Telkom Indonesia at 19 Mbps with half the market. That gap is invisible in any national average, and it is a market-structure story, not a geography one.

**Title candidates**
1. Who Sells the Speed? Operator-Level Structure of Southeast Asian Broadband
2. The Fastest ISP Is Not the One You're On: Market Structure in Nine Southeast Asian Markets
3. (plain, paper-style) Operator-Level Performance and Market Concentration in Southeast Asia

**Tagline candidates**
- "Half a market on the slowest major operator."
- "300 Mbps at 7 % share. 19 Mbps at 50 %."

---

## 2. Big-number callouts

| Number | Label | Source |
|---|---|---|
| **13×** | fastest major fixed operator, best market vs worst (MyRepublic SG 300 → Global Technology MM 23 Mbps) | chart `rq4_fastest_major_compare.png` |
| **18×** | most-used fixed operator, best vs worst (Singtel Fibre 176 → Mytel MM 10 Mbps) | chart `rq4_leader_speed_compare.png` |
| **2.3×** | largest fastest-vs-most-used penalty (Indonesia fixed: Biznet 43 vs Telkom 19) | recomputed, §4 |
| **4.7×** | largest gap between two major operators in one market (Singapore cellular: Simba → Singtel Mobile) | chart `rq4_within_gap.png` |
| **5×** | cellular spread across the region, vs 13× for fixed (22 → 104 Mbps) | chart `rq4_fastest_major_compare.png` |
| **9** | countries, Q1 2023 – Q4 2025 | pipeline |
| **760.6M** | NDT7 tests behind the operator analysis | paper §Datasets |

---

## 3. Finding 1 — The fastest operator is not the one people use

Paste-ready:

> In seven of nine fixed-broadband markets the fastest major operator (≥ 5 % of tests) is **not** the most-used one. The penalty paid by the majority is largest in **Indonesia**, where Biznet averages 43 Mbps on a 5 % share while Telkom Indonesia carries half the market at 19 Mbps — a **2.3×** gap. **Myanmar** is nearly as wide (Global Technology 24 vs Mytel 10, **2.3×**), then **Malaysia** (TIME dotCom 196 vs TM 113, **1.7×**), **Singapore** (MyRepublic 300 vs Singtel Fibre 176, **1.7×**) and the **Philippines** (Globe 90 vs PLDT 61, **1.5×**). In **Laos** and **Vietnam** there is no penalty at all: the incumbent is both the largest and the fastest. **Cambodia** and **Thailand** have a different operator on top but a gap too small to matter (1.02× and 1.10×).

**Fixed broadband — most-used vs fastest major operator** *(recomputed; see §6)*

| Country | Most-used | Mbps | share | Fastest major | Mbps | share | Penalty |
|---|---|---:|---:|---|---:|---:|---:|
| Indonesia | Telkom Indonesia | 18.6 | 49.7 % | Biznet | 43.3 | 5.2 % | **2.33×** |
| Myanmar | Mytel | 10.3 | 15.4 % | Global Technology | 23.7 | 7.8 % | **2.30×** |
| Malaysia | TM | 113.4 | 50.0 % | TIME dotCom | 196.3 | 13.2 % | 1.73× |
| Singapore | Singtel Fibre | 176.3 | 25.4 % | MyRepublic | 300.1 | 7.4 % | 1.70× |
| Philippines | PLDT | 60.6 | 46.3 % | Globe | 90.0 | 11.9 % | 1.48× |
| Thailand | True | 114.5 | 28.9 % | AIS | 125.9 | 23.1 % | 1.10× |
| Cambodia | Metfone | 30.3 | 40.9 % | Angkor Data Comm. | 31.0 | 11.5 % | 1.02× |
| Laos | Unitel | 42.7 | 48.8 % | *(same)* | — | — | 1.00× |
| Vietnam | Viettel | 71.0 | 39.0 % | *(same)* | — | — | 1.00× |

Cellular flips several of these: Thailand 1.48× (True 20 → AIS 29), Philippines 1.50× (Smart 21 → DITO 31), Cambodia 1.26×, Malaysia 1.18×, Myanmar 1.08×; Singapore, Indonesia, Laos and Vietnam have none.

**Figures:** `rq4_leader_speed_compare.png` (most-used, both network types) and `rq4_fastest_major_compare.png` (fastest major, both). They are the paper's Figures `image8` and `image7`. Put them side by side — the shape of the two charts differing *is* the finding.

⚠ `image7`'s labels are small and go illegible at A0. Regenerate from the notebook at poster resolution or crop to fixed-only.

---

## 4. Finding 2 — Within a single market, majors differ up to 4.7×

Paste-ready:

> The spread is not only between countries. Inside one market, two operators both holding ≥ 5 % of tests can differ by **4.7×** (Singapore cellular: Simba 22 → Singtel Mobile 104 Mbps) and **4.4×** (Malaysia fixed: 45 → TIME dotCom 196). In those markets the spread between two major operators exceeds the spread between several national averages — Malaysia's slowest fixed major sits below Vietnam's national fixed mean. At the other end, Vietnam's two fixed majors differ by only **1.1×**, and its cellular majors by 1.3×: a uniform market, uniformly mid-tier.

⚠ The 4.4× row is labelled "Celcom" on the chart, in the **broadband** bucket. Celcom is a mobile brand; `network_type` comes from ip-api's mobile/hosting flags, which can misclassify fixed-wireless or unflagged ranges. Check what sits behind that ASN before printing the name — the ratio stands either way.

Rank order from `rq4_within_gap.png` (best-vs-worst major, pooled 2023–2025): SG cellular 4.7× · MY fixed 4.4× · SG fixed 2.4× · ID fixed 2.3× · MM fixed 2.2× · TH fixed 1.9× · LA fixed 1.7× · LA cellular 1.7× · KH fixed 1.6× · TH cellular 1.6× · ID cellular 1.5× · PH cellular 1.5× · MM cellular 1.5× · PH fixed 1.5× · MY cellular 1.4× · VN cellular 1.3× · KH cellular 1.3× · VN fixed 1.1×.

**Figure:** `rq4_within_gap.png` — a dumbbell chart, 18 rows (9 countries × fixed/cellular), already sorted by ratio and already labelled with both operator names. This is the single strongest chart available for this poster; give it a full column.

---

## 5. Finding 3 — Concentration bites mobile, not fixed

Paste-ready:

> Measured as share of NDT7 tests, every market in the region is concentrated, but the consequence differs by access type. Across fixed broadband there is **no relationship** between concentration and national speed (Spearman ρ = 0.15, p = 0.70, n = 9) — **Myanmar runs the region's least concentrated fixed market (HHI 706) and its slowest**, so fragmentation there means a long tail of small operators, not competition that delivers. On cellular the relationship is **negative and significant** (ρ = −0.78, p = 0.014, n = 9): the three most concentrated cellular markets — Cambodia (HHI 5,033), Laos (4,427) and the Philippines (4,214) — all sit at 18–23 Mbps, while the fastest, Singapore and Malaysia, are near the bottom of the concentration range.

⚠ n = 9 and this is an **association, not a cause** — a concentrated market can be concentrated *because* one operator built out. Print it as a correlation with its p-value, and do not write "competition raises speed" anywhere on the poster.

**Concentration, by market** *(recomputed; HHI on test-share, 0–10,000)*

| Country | Fixed HHI | Fixed CR3 | Fixed Mbps | Cellular HHI | Cellular CR3 | Cellular Mbps |
|---|---:|---:|---:|---:|---:|---:|
| Singapore | 1,573 | 62.9 % | 195.9 | 2,630 | 81.9 % | 77.4 |
| Malaysia | 2,966 | 76.5 % | 112.2 | 2,627 | 80.7 % | 46.5 |
| Thailand | 2,237 | 73.2 % | 100.5 | 3,247 | 96.2 % | 22.6 |
| Philippines | 2,817 | 80.9 % | 68.9 | 4,214 | 100 % | 23.1 |
| Vietnam | 3,239 | 94.3 % | 68.6 | 3,078 | 95.7 % | 33.4 |
| Laos | 3,640 | 91.6 % | 34.0 | 4,427 | 100 % | 18.1 |
| Cambodia | 2,094 | 66.0 % | 27.6 | 5,033 | 99.5 % | 20.5 |
| Indonesia | 2,564 | 59.1 % | 21.9 | 3,344 | 96.0 % | 20.5 |
| Myanmar | 706 | 36.4 % | 16.6 | 2,630 | 84.6 % | 22.4 |

Worth a caption line: **Myanmar is the only country whose cellular average (22.4) beats its fixed average (16.6)** — the hook back to the main poster's mobile-first observation.

**Figures:** the per-country donuts `rq4_marketshare_<country>_{broadband,cellular}.png` exist for all nine. Eighteen donuts will not fit. Either pick three contrasting markets (Singapore fragmented / Vietnam concentrated / Myanmar long-tail) or drop the donuts and let the table carry it.

---

## 6. Finding 4 — Fixed diverges, cellular converges *(optional fourth panel)*

> Fastest major fixed operators span **13×** across the region (23 → 300 Mbps). Fastest major cellular operators span **5×** (22 → 104), and with Singapore excluded the other eight markets fit inside **22–53 Mbps**. Mobile delivers a mediocre service uniformly; fixed delivers an excellent service to a few markets and a poor one to the rest.

This overlaps the main poster's fixed-vs-mobile block, so it is **cut-first** if space runs short. Figure: right-hand panel of `rq4_fastest_major_compare.png`.

---

## 7. Methods block (paste-ready)

> **Data.** M-Lab NDT7, 760.6 M single-stream tests, Q1 2023 – Q4 2025, nine Southeast Asian countries. Tests with non-positive throughput or duration are dropped; ip-api.com supplies the ASN and the mobile/hosting/proxy flags that separate broadband from cellular.
> **Grouping.** Operators are grouped by **ASN**, never by M-Lab's raw ISP-name string — one operator appears under hundreds of spellings, and for leased lines ip-api returns the customer's organisation rather than the carrier (AS4750 alone carries 420 distinct names). ASNs belonging to one operator are then pooled under that operator's most frequent label.
> **Weighting.** Averages are weighted by test count, not by address; carrier-grade NAT gives mobile ASNs far more tests per address. Operator quarters with fewer than 100 tests are flagged unreliable.
> **Market share** is an operator's share of tests within one network type and quarter — a measurement-side proxy for market position, not a subscriber count.
> **Throughput only.** NDT7 servers are off-net for eight of the nine countries, so absolute latency is not interpretable as domestic latency and no latency result is reported.

**Ethics line:** Only public, aggregated open data (M-Lab NDT7 via BigQuery). IP addresses are used transiently for ASN resolution via ip-api.com and are not retained.

---

## 8. Takeaway (paste-ready)

> National speed averages hide who is actually being served. In most Southeast Asian markets the operator carrying the largest share of traffic is not the fastest one available, and the gap reaches 2.3×; inside a single market, two operators of comparable size can differ by 4.7×. Concentration tracks poor performance on cellular but not on fixed, where Myanmar's fragmented market is also the region's slowest — so the policy lever is not competition count alone, but whether the operator the majority is on has invested. Measuring at the operator layer, not the national one, is what makes the difference visible.

---

## 9. Figure catalog

All under `outputs/ndt7/comparison/`, all generated 2026-08-20, all nine countries verified.

| File | Shows | Use |
|---|---|---|
| `rq4_within_gap.png` | Dumbbell, best vs worst major operator, 18 rows, ratio + names labelled | **Hero chart.** Full column |
| `rq4_fastest_major_compare.png` | Bars, fastest major operator per country, fixed \| cellular | Finding 1 + Finding 4. Labels too small at A0 — regenerate |
| `rq4_leader_speed_compare.png` | Bars, most-used operator per country with n, fixed \| cellular | Finding 1, pair with the above |
| `rq4_marketshare_<c>_broadband.png` | Per-country share donut, fixed (9 files) | Finding 3, pick ≤ 3 |
| `rq4_marketshare_<c>_cellular.png` | Per-country share donut, cellular (9 files) | Finding 3, pick ≤ 3 |
| `rq4_top5_<c>.png` | Top-5 operators per country, speed + share (9 files) | Backup / handout, too many for A0 |

Paper equivalents: `docs/paper/figures/image7.png` = `rq4_fastest_major_compare`, `image8.png` = `rq4_leader_speed_compare`. Same data, same pipeline.

---

## 10. Still open

- [ ] **Confirm the deadline and venue.** This file assumes AINTEC '26 poster track, 09-28 8pm EDT. Not verified with อาจารย์.
- [ ] **Author list and order.** The main poster carries all three names (Chissanupun Athiwarikanon, Kunanont Malayanont, Pakkapon Pattanakul). Whether this one keeps that list, or leads with its owner, is undecided.
- [ ] **Regenerate `rq4_fastest_major_compare` at poster resolution** — current labels are unreadable at A0.
- [ ] **Verify the Malaysia "Celcom" broadband row** (§4) before printing the operator name.
- [ ] **Which poster keeps the cellular band?** `poster.tex`'s Mobile block says "seven of nine markets, 22–39 Mbps"; §6 here says "22–53 across eight markets" off the same chart. Both are defensible readings, but the two posters must not print conflicting bands — pick one poster to carry it.
- [ ] **Myanmar's `Global Technology` share**: the chart labels 6 %, the recompute gives 7.8 %. Small, but the poster must not print both. Same for Philippines Globe (chart 12 % / 90 Mbps, recompute 11.9 % / 90.0).
- [ ] Zoom-test at real print size; show อาจารย์.

---

## Appendix — provenance

**Quoted from the published charts** (read directly from the PNGs, 2026-09-24): every ratio in §4, and the operator speeds and shares in §2 and §6.

**Quoted from `docs/paper/paper.tex`** (§Operator analysis, around the `fig:fastest-operator` and `fig:most-used-operator` blocks): the operator speed values also appearing in §3, and the 760.6 M test count.

**Recomputed on 2026-09-24** from `data/exports/ndt7_isp_*_quarterly.csv`: the penalty table in §3 and the whole concentration table in §5. Method — for each country and network type, label each ASN by `operator`, falling back to `as_name` then the ASN itself; sum `total_tests` per label across all quarters; take the test-weighted mean of `avg_d_mbps`; share = a label's tests over the network type's total; major = share ≥ 5 %; HHI = Σ share², CR3 = the top three shares. The two correlations in §5 are `scipy.stats.spearmanr` on the unrounded HHI against the test-weighted national mean, n = 9 (cellular ρ = −0.778, p = 0.0135; fixed ρ = 0.150, p = 0.700). This reproduces the published charts to within rounding (True 114.5 vs 115, AIS 125.9 vs 126, MyRepublic 300.1 vs 300, Globe 90.0 vs 90, Singtel Fibre 176.3 vs 176, TM 113.4 vs 113, PLDT 60.6 vs 61, Viettel 71.0 vs 71, Unitel 42.7 vs 43, Metfone 30.3 vs 30, Telkom 18.6 vs 19, Mytel 10.3 vs 10), which is what licenses mixing the two on one poster.

**Do not** aggregate per-ASN instead of per-operator — it silently changes the numbers (Thai True becomes 128.2 Mbps instead of 115, because True's second ASN averages 47 Mbps and gets dropped rather than pooled).

**Created:** 2026-09-24
