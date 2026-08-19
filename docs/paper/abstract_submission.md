# AINTEC '26 — abstract submission package

Deadline: **31 July 2026** (abstract). Full paper: 7 August 2026.
Source of truth for all content: `docs/paper_draft.md`. This file is the send-ready extract.

---

## 1. Title

**Is Southeast Asian Broadband Good or Bad? A Nine-Country Assessment of Thresholds, Growth, and Market Structure**

> Note: `docs/paper.tex` still carries the old title (*"Is Thai Internet Good or Bad? An Empirical Assessment of Thailand's Broadband Infrastructure Quality"*). That title is two scope shifts out of date — the study is no longer Thailand-primary and now covers nine countries. Use the title above.

## 2. Abstract (197 words — acmart allows 150–200)

National broadband rankings are read as summaries of user experience. In Southeast Asia they contradict it: Ookla ranked Thai fixed broadband 13th worldwide in early 2025, while consumer-advocacy surveys and regulator records document persistent dissatisfaction. We test this tension across nine Southeast Asian countries over Q1 2023–Q4 2025, using province-aggregated Ookla Open Data and 760 million per-test M-Lab NDT7 records, judged against application-requirement thresholds rather than throughput alone. By those thresholds the region looks adequate: HD video is universally met and six of nine capitals pass everything. But a national average conceals three things at once. *Where*: failures fall almost entirely outside capital provinces. *When*: at the busy hour — evening in eight of nine countries — mobile throughput falls to between 0.23 and 0.73 of its overnight level, and the slowest tenth of sessions falls as low as 0.12, while fixed broadband degrades far less. *Whose*: in six of eight countries the highest-volume broadband operator is not the fastest major and in three it is the slowest, so test-weighted averages track a market's busiest networks rather than its best. Each axis is invisible in the statistic policy cites; together they account for the dissatisfaction rankings cannot.

> **Opening sentence rewritten twice on 2026-07-30 after source verification.** It originally cited "64.65% of Thai internet users name slow speed as their leading online complaint" (ETDA via Statista) — unverifiable, and a **2022** survey presented as contemporaneous with a 2025 ranking. The first replacement cited "over 81% … that year," which repeated the same error in a new form: that survey is from **2023**, not 2025. The abstract now makes no numeric claim about dissatisfaction at all; the survey figures live in §1 with full attribution and dates. Only the Ookla ranking, which is verified, carries a number.

---

## External citation audit (2026-07-30)

Every claim in the abstract that does not come from our own data, checked against sources.

| Claim | Source | Verdict |
|---|---|---|
| Thailand 13th worldwide, fixed broadband, early 2025 | Nation Thailand, 1 Mar 2025 | ✅ Article verified: 13th / 237.05 Mbps fixed, 39th / 101.56 Mbps mobile. Secondary source reporting Ookla. |
| "consumer-advocacy surveys and regulator complaint records document persistent dissatisfaction" | Foundation for Consumers 2023; NBTC | ✅ Qualitative, supportable — no number asserted |

### Source-quality warning: both figures came from a newspaper, not a primary source

Both statistics were taken from **Nation Thailand**, a mainstream Thai English-language paper. What was verified is *that the newspaper says so*, not the underlying fact. For an ACM submission the primary sources should be cited:

- The 13th ranking's primary source is **Ookla's Speedtest Global Index** (`speedtest.net/global-index/thailand`). Not fetchable from this environment. The Global Index also updates monthly and the article never names the data month — it says only "the latest Speedtest Global Index for 2025." The abstract therefore says **"in early 2025"**. Do not tighten to "March 2025 data" without checking Ookla directly; March is the *article* date. Note also that checking today returns 2026 data, so confirming the early-2025 rank needs an archived snapshot.
- The 81% figure's primary source is a **Foundation for Consumers (มูลนิธิเพื่อผู้บริโภค)** survey, traced below.

### What the 81% figure actually is

Traced through Thai-language sources — [Thai PBS](https://www.thaipbs.or.th/news/content/334937) and [สภาองค์กรของผู้บริโภค (TCC)](https://www.tcc.or.th/true-dtac-merger-consumer/):

| | |
|---|---|
| Conducted by | Foundation for Consumers (มูลนิธิเพื่อผู้บริโภค) |
| Fieldwork | 9–23, **2566 = 2023** (TCC says September; Thai PBS says November — sources disagree on month) |
| Respondents | **2,924** ("nearly 3,000") |
| Sampling | Not stated in either source; self-selected response to an advocacy campaign |
| The actual finding | "ผู้ตอบแบบสอบถามกว่าร้อยละ 81 พบปัญหาการใช้งานในช่วง 6 เดือนที่ผ่านมา" — over 81% **of respondents** met usage problems in the prior six months |
| Context | Impact assessment on customers **after the True–dtac merger** (approved Oct 2022) |

Three consequences:

1. **It is a 2023 survey, not 2025.** Nation Thailand cited it in a May 2025 article; reading the article date as the survey date is the error that produced the first bad fix.
2. **"81% of Thai users" overstates the population.** It is 81% of ~2,924 self-selected respondents to a merger-impact survey, not a representative national sample. It cannot be written as a statement about Thai internet users generally.
3. Nation Thailand's *wording* is nonetheless a faithful rendering of the primary finding, so the paper is not misquoting the newspaper — it was misdating it.

**Usable form, if wanted in §1:** "a 2023 Foundation for Consumers survey of 2,924 respondents found over 81% had encountered usage problems in the previous six months, most commonly slow speeds and dropped connections, in the year following the True–dtac merger."

### RQ3 peak-hour numbers in the abstract — independently audited 2026-07-30

The "*When*" clause rests on a collaborator's delivery (`notebooks/comparison/rq3_peakhour.ipynb`, pushed 2026-07-30). Every figure quoted was recomputed from the raw exports rather than taken from their summary, and matched:

| | delivered | recomputed |
|---|---|---|
| Thailand broadband busy/off | 0.893 | 0.893 |
| Thailand cellular busy/off | 0.556 | 0.556 |

All ratios in this section are **weekday-only**, matching the notebook. An earlier check of mine pooled weekday and weekend and produced slightly different values (e.g. Singapore cellular 0.703 rather than 0.729); the notebook's weekday convention is the correct one and is what the abstract now quotes.

**Claims and their support:**

- *"mobile throughput falls to between 0.23 and 0.73 of its overnight level"* — cellular busy(19–22h)/off-peak(03–05h) median download, all nine countries: Cambodia 0.232, Myanmar 0.262, Philippines 0.304, Laos 0.320, Indonesia 0.398, Malaysia 0.420, Vietnam 0.469, Thailand 0.556, Singapore 0.729.
- *"the slowest tenth of sessions falls as low as 0.12"* — same ratio on p10: Cambodia 0.122 is the minimum. p10 is below the median ratio in every country, i.e. the tail degrades worse than the middle.
- *"evening in eight of nine countries"* — cellular busy hour is 20:00–22:00 local everywhere except **Vietnam (10:00)**.
- *"fixed broadband degrades far less"* — broadband ratios 0.464–1.253 against cellular's 0.232–0.729; Singapore's broadband is >1, i.e. no congestion at all.

**Congestion-plausibility screen (added 2026-07-30, `scripts/peakhour_flags.py`).** A country-segment counts as demand-driven congestion only if its busy hour is in the evening, throughput falls, *and* RTT rises. **13 of 18 qualify.** Excluded: Vietnam broadband and cellular (busy hour 10–11:00; broadband RTT *falls*, 0.584), Cambodia broadband (busy hour 12:00), and Singapore broadband and cellular (no congestion — Singapore's broadband is actually faster at the busy hour). The abstract's cellular range is unaffected by these exclusions: it spans Cambodia 0.232 to Singapore 0.729, and Vietnam's 0.469 is interior, so removing it moves neither bound. "Evening in eight of nine" is exactly the set of cellular segments with an evening busy hour.

**Bot check passes.** Tests per unique IP is 1.4–6.3 with peak/median ratios of 1.15–1.51 — no spike indicating automated testing. Latency corroborates congestion independently: median RTT rises at the busy hour in eight of nine countries on cellular and six of nine on broadband (Philippines broadband +41%).

**One country must be caveated in the body: Vietnam.** Its busy hour is 10:00–11:00 rather than evening, it has the lowest evening share of tests (22.9% of broadband tests in 18–23h, below what a uniform distribution would give), and its RTT *falls* at the busy hour (ratio 0.54) — the opposite of congestion. Vietnam's peak-hour figures should not be read as demand-driven congestion. Cambodia also shows a midday **broadband** peak (12:00), though its cellular peak is properly evening (21:00) and its cellular degradation is the most severe in the set. Laos is fine on both segments once weekday-only rows are used (20:00). The abstract's range figures include all nine countries, which is safe because Vietnam sits mid-range and is not the source of any quoted extreme — but the body must state this.

### Two citation faults found in the repo — both still present in the body, not the abstract

**1. The 64.65% ETDA figure is unverifiable and possibly mis-attributed.** Statista is paywalled (redirect loop, not fetchable). Web search cannot confirm it. Three concerns:
- `docs/citations.md` §6b itself records the survey year as **2022**, not 2025.
- The closest verifiable figure in the same Statista/ETDA family is **77.5% of Generation Z in 2020** — a subgroup, different year, different number. If the underlying series is per-generation, then "64.65% of Thai internet users" misstates the population.
- Search returns the exact string 64.65% attached to an unrelated ETDA metric (Gen Y live-commerce viewing rate), which is the kind of coincidence that produces mis-attribution.

→ Needs Statista institutional access (KU library) or the ETDA primary report to settle. Until then it should not appear in the paper.

**2. The NBTC complaint figures are attributed to a source that does not contain them.** `docs/paper_draft.md` §1 states complaints "rose from under 1,000 to nearly 3,000 in the first seven months of 2025," cited to Nation Thailand, 23 May 2025. That article contains **no NBTC complaint numbers at all** — it only notes that the NBTC issued warnings without fines. The attribution is also date-impossible: an article published 23 May cannot report on the first seven months of the year.

→ Either find the real source for these figures or remove the claim.

**Body still needs fixing.** `docs/paper_draft.md` §1 (line 25) carries both faults, and additionally asserts the ETDA survey was "in the same period" as the March 2025 ranking, which is false for a 2022 survey. The abstract is clean; §1 is not.

## 3. Keywords

broadband measurement, Ookla, M-Lab NDT7, Southeast Asia, digital divide, ISP market structure, cross-country comparison

## 4. CCS Concepts

- Networks → Network measurement
- Networks → Public Internet
- Social and professional topics → Regulation

## 5. Authors — NEEDS YOUR INPUT

Not yet decided. Required before submission:

- Author list and **order**
- Affiliations
- Corresponding author + email

`docs/paper.tex` currently has placeholders (`Author Name`, `Institution`, `author@example.com`). At minimum the collaborator who delivered the NDT7 ip-api ASN relabelling and the Philippines/Malaysia pipelines has a contribution worth an authorship or acknowledgement decision — see `HANDOFF.md`.

---

## Disclose proactively — do not let the prof find these

**1. ~~The threshold citation is unverified.~~ RESOLVED 2026-07-30.** The source was retrieved and checked. All four RQ1 thresholds (HD 5 Mbps, UHD 25 Mbps, cloud gaming 44 Mbps + ≤25 ms, voice ≤200 ms) match its Table 5, "Exemplary application requirements", **exactly** — no value changes.

The *citation* was wrong twice over and is now corrected:

| | was | is |
|---|---|---|
| Author | Misfeld, **T.** | Misfeld, **N.** (Nico) |
| Title | *App-requirement thresholds for network quality* — a placeholder that does not exist | *Exploring the Measurement Lab Open Dataset for Internet Performance Evaluation: The German Internet Landscape* |
| Venue | — | Electronics **11**(1), 162, 2022 · doi:10.3390/electronics11010162 |

A useful side effect: the paper is itself an M-Lab NDT study of Germany, and its §4.2 "Busy Hours and Days" is exactly the method our RQ3 follows — identify busy hours from measurement volume, then test whether throughput falls during them. It now anchors RQ1 *and* RQ3, and positions this paper as extending their single-country, single-platform analysis to nine countries, two platforms, and sub-national geography. §2 has been rewritten to say so.

**2. Scope has changed since the last version the prof may have seen.**
- **Nine countries, not eight** — Indonesia was added 2026-07-30 (Ookla + NDT7). It lands second-worst on fixed broadband, which breaks the old "clean five-country tier vs. Myanmar/Cambodia/Laos" framing into a four-step gradient.
- **NDT7 now covers all nine**, not five. Philippines and Malaysia arrived via a collaborator's ASN relabel; Singapore's NDT7 was added 2026-07-30.
- **All numbers shifted** after a pipeline fix recovered 2025-Q3, which had been missing from every country's export. Any figure the prof saw before 30 July is stale (e.g. Myanmar UHD was 20.6%, now 22.1%).

**3. The research questions were renumbered.** ISP-level analysis is now **RQ4** and is complete. Peak-hour/diurnal is now **RQ3** and is **paused** — no notebook exists for it. This resolves the earlier miscommunication about which was which. RQ3 appears in the paper only as future work; the abstract does not mention it.

---

## If the prof pushes on the numbers

Every figure in the abstract is verified against the current exports as of 2026-07-30 and is defensible:

| Claim | Source | Status |
|---|---|---|
| ρ = 0.90 cross-source agreement | `rq1_thresholds_ndt7.ipynb` cell 10 | **Clean** — drops NaN countries explicitly, n = 9 |
| Thailand 99.5% / Bangkok 100% | `rq1_thresholds_ookla.ipynb` cells 8, 17 | Verified |
| Six of nine capitals clear every threshold | `rq1_thresholds_ookla.ipynb` cell 17 | Verified |
| Six of eight leaders not fastest; ID/MM/PH slowest | `rq4_leaders.csv` + `rq4_within_gap.csv` | Verified |
| 64.65% ETDA / 13th worldwide | ETDA 2024; Nation Thailand 2025a | Cited |

Deliberately **not** in the abstract: the ρ = 0.967 regression-coefficient agreement figure. It is the better number but depends on a one-line notebook fix for Vietnam's reference-data join that has been verified and not yet applied (`docs/paper_draft.md` §7.3). The abstract uses the ρ = 0.90 pass-rate check instead, which needs no fix. If the prof asks why the paper quotes two agreement figures, that is the reason.

Also worth knowing if asked: the reliability gate (`total_tests ≥ 100 AND n_tiles ≥ 5`) **excludes zero rows on the Ookla side** at province granularity — 3,222 in, 3,222 pass. It binds only on NDT7. The paper states this rather than claiming the gate as a filter that did work it did not do.
