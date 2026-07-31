# Is Southeast Asian Broadband Good or Bad? A Nine-Country Assessment of Thresholds, Growth, and Market Structure

*Working draft for AINTEC '26. Structure and voice follow Rauf et al., "Ten Years of Event-Driven BGP Evolution in India and Bangladesh" (AINTEC '25) — see `docs/writing-style-refs/`. Section skeleton mirrors the ACM sigconf manuscript at `docs/paper.tex`, which is still a stub; content is drafted here first and ported once stable. `docs/Process.md` tracks sprint-level tasks.*

*Research-question numbering (settled 2026-07-30). **RQ3 = peak-hour/diurnal**, **RQ4 = ISP market structure** — both complete. An intermediate revision had these reversed, on the assumption that peak-hour would not be delivered; it since was, and the numbering reverted to the original plan, which also matches the analysis filenames (`rq3_peakhour.ipynb`, `rq4_isp.ipynb`). The ordering is deliberate: RQ2 measures change across years, RQ3 change within the day, and RQ4 closes on market structure, the paper's most novel claim.*


*Number provenance: every figure in Sections 4–7 was re-verified on 2026-07-30 against the current exports and notebook outputs, after the 2025-Q3 pipeline recovery and the addition of Indonesia as a ninth country. Numbers in earlier revisions of this draft predate both and should not be reused. Two open items are flagged inline: the Lübben & Misfeld citation (Section 3.4) and the Vietnam NDT7 reference-data join (Section 7.3).*

## Abstract

*Submission version, 188 words — inside acmart's 150–200 range with headroom. Self-contained: no section cross-references, no figure or table references, safe to paste into a submission form. Every number is verified against the current exports (2026-07-30). The longer exploratory abstract from earlier revisions is superseded.*

National broadband rankings are read as summaries of user experience. In Southeast Asia they contradict it: Ookla ranked Thai fixed broadband 13th worldwide in early 2025, while consumer-advocacy surveys and regulator records document persistent dissatisfaction. We test this tension across nine Southeast Asian countries over Q1 2023–Q4 2025, using province-aggregated Ookla Open Data and 760 million per-test M-Lab NDT7 records, judged against application-requirement thresholds rather than throughput alone. By those thresholds the region looks adequate: HD video is universally met and six of nine capitals pass everything. But a national average conceals three things at once. *Where*: failures fall almost entirely outside capital provinces. *When*: at the busy hour — evening in eight of nine countries — mobile throughput falls to between 0.23 and 0.73 of its overnight level, and the slowest tenth of sessions falls as low as 0.12, while fixed broadband degrades far less. *Whose*: in six of eight countries the highest-volume broadband operator is not the fastest major and in three it is the slowest, so test-weighted averages track a market's busiest networks rather than its best. Each axis is invisible in the statistic policy cites; together they account for the dissatisfaction rankings cannot.

**CCS Concepts:** • Networks → Network measurement; Public Internet • Social and professional topics → Regulation.

**Keywords:** broadband measurement, Ookla, M-Lab NDT7, Southeast Asia, digital divide, ISP market structure, cross-country comparison

---

## 1 Introduction

Broadband is treated as development infrastructure, and with reason: Röller and Waverman's
simultaneous-equations estimates place the return to telecommunications investment alongside other major
infrastructure. That framing gives national broadband rankings unusual weight in policy. They are among
the most widely cited statistics in telecommunications and among the least examined — a country's
position in a global index is one number derived from millions of user-initiated tests, routinely read
as a summary of what internet access is like for the people who live there. Whether it can bear that
reading is an empirical question, and in Southeast Asia the answer appears to be no.

The clearest documented case is Thailand, which serves as a motivating example rather than a subject of
deeper analysis — every country here receives identical treatment throughout. Ookla's Speedtest Global
Index placed Thai fixed broadband 13th worldwide in early 2025 at 237.05 Mbps, roughly double the global
figure, while placing Thai mobile 39th (Nation Thailand, 2025a; the index is revised monthly, so this is
a snapshot rather than a standing position). The gap between those two ranks is itself informative: the
answer already depends on access technology. Against that, a 2023 Foundation for Consumers survey of
2,924 respondents found **over 81% had encountered usage problems in the preceding six months**, mostly
slow speeds and dropped connections. The two figures are not strictly commensurable — a 2025 platform
ranking against a 2023 self-selected survey — and we do not treat their juxtaposition as a measurement.
What it establishes is weaker but sufficient: a high ranking and widespread dissatisfaction can coexist,
so the ranking is not by itself a description of what users experience. Explaining how both can be true
is the work of this paper.

The tension is not a Thai peculiarity. It is plausible wherever a national average is computed over a
market with uneven operators and uneven geography, which describes most of Southeast Asia, whose
economies span an unusually wide range of broadband maturity while sharing enough regulatory and
geographic context to make comparison meaningful. What has been missing is a like-for-like measurement
across the region able to separate the candidate explanations — that national averages are
geographically, temporally, or structurally misleading. Prior cross-platform work establishes that
measurement platforms disagree in magnitude, with MacMillan et al. reporting NDT7 underreporting
throughput relative to Ookla by 12–56%; prior single-country work characterises national infrastructure
in detail. To our knowledge no study has applied one unmodified pipeline across a region's provinces and
then tested all three explanations against each other.

We investigate the following research questions:

**RQ1: Is Southeast Asian broadband good or bad, and where does it fail?** Using application-requirement
thresholds for voice, HD, UHD, and cloud gaming, at what rate does each country clear each threshold at
province level, how does the capital compare to the periphery, and how does fixed compare to mobile?

**RQ2: How has quality changed over 2023–2025, and does the region show catch-up growth?**

**RQ3: Do peak-hour effects account for user-perceived degradation?** Does throughput fall and latency
rise during peak demand, how much worse is the slowest decile of sessions, and does this differ between
fixed and mobile?

**RQ4: Does ISP market structure explain the gap between national statistics and user experience?** How
concentrated is each market, how large is the gap between major operators, and is the operator carrying
the most traffic the one performing best?

Our contributions are:

1. **A symmetric nine-country comparison on one pipeline**, with no country treated as the reference
   case, so cross-country differences reflect measured variation rather than differing methodology.

2. **A decomposition of the ranking-versus-sentiment gap into three independent margins** — *where* a
   subscriber is, *when* they use the network, and *whose* network it is — with evidence that these
   cannot be collapsed into one. Capital provinces are the best served on the geographic margin and
   among the worst on the temporal one, so any single-mechanism account predicts the wrong sign for at
   least one result.

3. **A screening test for demand-driven congestion.** Peak-hour degradation is only evidence of
   congestion if throughput falls *and* latency rises during a genuinely human busy hour; applying all
   three conditions qualifies 13 of 18 country-segments and excludes one country whose diurnal profile
   is systematic but not demand-driven.

4. **A reliability threshold reported honestly, including where it does not bind.** We apply an explicit
   gate to both sources and report that it excludes nothing on the Ookla side at province granularity
   while materially shaping the NDT7 sample — a distinction similar studies leave implicit.

Section 2 reviews related work and Section 3 details data and methods. Sections 4 through 7 answer RQ1
to RQ4 in turn. Section 8 reports cross-country statistical validation and cross-source agreement,
Section 9 discusses implications and limitations, and Section 10 concludes.

---

## 2 Motivation & Background

A substantial literature measures broadband performance at national scale, and a smaller one asks whether the resulting numbers are trustworthy.

**Platform comparison.** MacMillan et al. conduct the closest methodological antecedent to our cross-source check, comparing Ookla Speedtest against M-Lab's NDT7 and finding that NDT7 underreports throughput by 12–56% depending on conditions. The mechanism is architectural rather than incidental: Ookla is an active, user-initiated test against a nearby server chosen for proximity, while NDT7 measurements are single-stream TCP transfers to a smaller server fleet. This means the two platforms cannot be pooled, but it does not prevent their *rankings* from being compared, which is how we use them.

**Application-requirement thresholds, and the closest antecedent to this study.** Absolute speed figures are difficult to interpret without a reference point, and percentile comparisons against other countries simply relocate the problem. Lübben and Misfeld ground assessment in what applications actually require, tabulating throughput and latency floors for voice, HD video, UHD video, and cloud gaming (their Table 5). This converts "is 60 Mbps good?" into "does 60 Mbps support the applications people use?", which is answerable, and we adopt their table as our RQ1 standard.

Their paper is more than a source of numbers for us: it is a study of the German Internet built on the same M-Lab NDT dataset we use, and it supplies the method for our RQ3 as well. Their Section 4.2 identifies *busy hours and days* from measurement volume and then asks whether achievable throughput falls during them — precisely the design we apply in Section 7, including their diagnostic for distinguishing automated test traffic from human usage. This paper can therefore be read as extending their single-country, single-source analysis in three directions: to nine countries rather than one, to a second measurement platform (Ookla) whose disagreement with NDT7 we can then quantify, and to sub-national geography and ISP market structure, neither of which their national-level treatment addresses.

**Sub-national divides.** Work on the digital divide has consistently found that national aggregates conceal internal variation, and that infrastructure investment tends to follow a capital-first pattern. This motivates our capital-versus-periphery decomposition in Section 4.2, but it also sets up a prediction that our data does not always confirm — Myanmar's and Singapore's capitals do not lead their countries, for different reasons.

**Market concentration.** Concentration is well studied in telecommunications economics, usually with price or investment as the outcome variable. It is less often connected to measured technical performance, and to our knowledge it has not been used to explain divergence between national broadband averages and user sentiment. Our RQ4 makes that connection: if a market's dominant operator is also a slower operator, then a test-weighted national average describes the market's better networks rather than its busiest ones. Ookla's own aggregates are test-weighted, so this bias is built into the statistic that policy cites.

Our work builds on these strands and extends them to a regional, structurally-oriented comparison: we take the threshold framework as our evaluative standard, the platform-comparison literature as our reason to treat cross-source agreement as a ranking question, and the concentration literature as the source of the mechanism we test in RQ4.

---

## 3 Data and Methodology

### 3.1 Datasets

**Ookla Open Data** supplies quarterly fixed and mobile performance tiles (Quadkey zoom 16, ~610×610 m),
each carrying mean download, upload, latency, and its underlying Speedtest submission count — twelve
complete quarters, Q1 2023–Q4 2025, all nine countries, both products, CC BY-NC-SA 4.0. An earlier
build of our pipeline dropped 2025-Q3 from every processed export although the quarter was present in
Ookla's raw source; the rebuild recovered it, and every figure here postdates that fix.

**M-Lab NDT7** supplies per-test records over the same range, retaining the timestamps and ISP
attribution that Ookla's tile aggregates discard — what makes RQ3 and RQ4 possible at all. NDT7 does
not distinguish fixed from mobile natively; network type is assigned by joining client IP against
ip-api's `mobile` flag, resolved per IP block. All nine countries were re-queried inside a single
11.49-hour window so the labels form one consistent snapshot, replacing an earlier labelling spread
across twelve days, which is not a defensible basis for cross-country comparison. Section 9.1 bounds
what this supports.

**Reference data.** Province population, density, and GDP per capita come from national statistical
agencies where sub-national series exist (e.g. the Department of Statistics Malaysia) and from World
Bank national figures where they do not — Cambodia's National Institute of Statistics publishes no
province-level GRDP, so one national value repeats across its provinces (Section 9.1). Boundaries are
geoBoundaries ADM1, except Thailand's national 77-province layer. Three boundary artefacts affect
specific results: geoBoundaries folds Naypyidaw into Mandalay Region, so Myanmar has no separate capital
province and we substitute Yangon; GADM 4.1 reflects 2022 boundaries, giving Indonesia 34 provinces
rather than today's 38; and Singapore has no capital province, so Central Region serves as a
central-business-district proxy.

**Table 1 — Data volume and coverage. Ookla figures are summed Speedtest submissions; NDT7 rows are
per-test records before filtering; reliable p-q is province-quarters passing the Section 3.2 gate.**

| Country | Prov. | Ookla fixed | Ookla mobile | NDT7 rows | Reliable p-q | RQ4 |
|---|---|---|---|---|---|---|
| Indonesia | 34 | 54.2M | 20.1M | 367.2M | 402 | ✓ |
| Philippines | 17 (80 raw) | 48.8M | 7.1M | 262.1M | 204 | ✓ |
| Vietnam | 63–64 | 25.9M | 3.5M | 24.7M | 698 | ✓ |
| Thailand | 77 | 20.8M | 10.5M | 60.2M | 872 | ✓ |
| Malaysia | 16 | 15.7M | 11.8M | 6.6M | 165 | ✓ |
| Singapore | 5 regions | 4.5M | 0.9M | 36.1M | 52 | ✗ no `asn` |
| Cambodia | 22–25 | 2.4M | 0.5M | 0.77M | 33 | ✓ |
| Myanmar | 14 | 1.75M | 0.25M | 2.12M | 76 | ✓ |
| Laos | 14–18 | 0.37M | 0.50M | 0.14M | 37 | ✓ |

NDT7 sample sizes are very uneven — Cambodia and Laos rest on 33 and 37 reliable province-quarters
against Thailand's 872 — which qualifies every NDT7 result reported later. Singapore's delivery predates
the ASN relabelling and has no `asn` column; rather than group its ISPs by name we exclude it from RQ4
wherever an RQ4 result appears. Province ranges reflect provinces with zero NDT7 volume being absent
from the NDT7 side only.

### 3.2 Aggregation and filtering

Ookla tiles are assigned to provinces by point-in-polygon on the tile centroid and aggregated to
province-quarter weighted by each tile's own test count, `Σ(tile_mean × tile_tests) / Σ(tile_tests)`.
The weighting is not optional: tile submission counts differ by orders of magnitude, and an unweighted
mean would give a sparsely-tested rural tile the same influence as a dense urban one. NDT7 aggregates
from per-test records directly, which we verified is equivalent to two-stage tile-binning (identical to
twelve decimal places on Malaysia).

Latency needs one asymmetric step. NDT7 carries sentinel round-trip values of 4,294,967 ms (2³²/1000)
that the cleaning stage missed because it filtered only negative values; twenty-one such rows inflate
Vientiane's mean latency from 116 to 539 ms. We discard `min_rtt ≥ 2000 ms` rather than clamping to it,
uniformly across all nine countries. **Ookla has no equivalent outlier step**, so the sources are not
perfectly symmetric here, which we note rather than conceal.

Every province-quarter is gated on measurement sufficiency before any statistic is computed:
`total_tests ≥ 100 AND n_tiles ≥ 5` for Ookla, `total_tests ≥ 100` alone for NDT7. The asymmetry is
deliberate. NDT7 coordinates come from MaxMind city centroids, so every test in a city collapses onto
one tile and `n_tiles` counts MaxMind cities per province rather than spatial spread — Laos has 139,693
rows at 33 distinct coordinates and a national maximum `n_tiles` of 3, making a `≥5` gate unsatisfiable
in principle rather than for want of data. Applying the Ookla gate unchanged would zero out Laos and
Cambodia entirely and cut Thailand from 1,225 reliable province-quarters to 564. We also report what
such studies usually leave unstated: **on the Ookla side the gate excludes nothing** — 3,222
province-quarters enter and 3,222 pass, on both fixed and mobile. It is a real constraint on NDT7 and a
formality on Ookla, and we claim it only where it binds.

### 3.3 Analysis methods

**Thresholds (RQ1).** Four application requirements are evaluated per province-quarter, taken from
Lübben and Misfeld's Table 5 and verified against the published paper. Their table is a compilation
whose sources differ in authority, which determines how much weight each result can bear:

| Application | Requirement | Primary source | Standing |
|---|---|---|---|
| Voice | ≤200 ms | ITU-T G.114 | International standard |
| HD video | ≥5 Mbps | Netflix recommendations | Vendor guidance |
| UHD video | ≥25 Mbps | Netflix recommendations | Vendor guidance, since revised |
| Cloud gaming | ≥44 Mbps **and** ≤25 ms | Di Domenico et al. (2021); Flinck Lindström et al. (2020) | Peer-reviewed |

A country's pass rate is the test-weighted share of province-quarters satisfying the threshold, so rates
reflect measured users rather than administrative units. We use the voice row's latency criterion only,
ignoring its 64 kbps rate, which every province-quarter clears by three orders of magnitude.

The Netflix-sourced rows are not stable — vendor guidance changes as codecs improve, and **Netflix now
publishes 15 Mbps for Ultra HD rather than the 25 Mbps in force when the table was compiled** — so we
report the sensitivity rather than leave a reader to discover it.

**Table 2 — UHD pass rate (%) at alternative thresholds, Ookla fixed, test-weighted.** Countries not
listed pass at 100.0% throughout.

| Country | ≥15 | ≥20 | ≥25 |
|---|---|---|---|
| Myanmar | 98.5 | 82.0 | **22.1** |
| Indonesia | 100.0 | 97.7 | **88.1** |
| Cambodia | 100.0 | 99.8 | 97.6 |
| Laos | 100.0 | 100.0 | 99.4 |

UHD is therefore **threshold-sensitive and cannot carry an argument alone**: at Netflix's current figure
the Myanmar and Indonesia shortfalls vanish. We retain 25 Mbps for comparability with Lübben and
Misfeld's German results and treat UHD as a descriptive tier boundary. **Cloud gaming carries RQ1
instead** — both criteria are peer-reviewed, it is the only threshold combining a throughput floor with
a latency ceiling, and Section 4 shows it is the only one that discriminates among these countries.

**Growth (RQ2)** is the percentage change in a country's median province download from 2023-Q1 to
2025-Q4, using the median across provinces rather than a test-weighted mean so growth is not dominated
by the capital, which would confound RQ2 with RQ1's geographic question. **Peak hour (RQ3)** is defined
in Section 6, alongside the screening procedure it requires.

**Market structure (RQ4).** ISPs are grouped by **ASN**, never by name. Name-based grouping fails badly
here: ip-api returns the *customer organisation* for leased-line ranges, so AS4750 alone carries 420
distinct "ISP" strings including `dermatology` and `waterflow`, and AS names are independently
unreliable — AS9534 is reported as "Binariang Berhad" but is Maxis. Displayed brand labels therefore
carry their ASN, since one brand can hold several (Thailand: True 2, AIS 3, NT 3, 3BB 2). We report
concentration as a Herfindahl-Hirschman Index over ASN shares of test volume on named ASNs only, define
a **major** as an operator holding ≥5% of a country-segment's tests, and measure the within-country gap
as the download ratio between best and worst major. Operators are not merged across corporate mergers
(dtac/True 2023, 3BB/AIS 2023, Celcom/Digi 2022): merging later is possible, un-merging is not.

**Statistical testing.** Cross-country differences are tested with a Kruskal-Wallis omnibus followed by
Holm-corrected pairwise Mann-Whitney tests, and province download is modelled as
`mean_dl ~ log(GDP per capita) + log(1 + density) + C(country)` by OLS with country fixed effects and
province-clustered standard errors. Section 8 reports these with the robustness checks they require.

---

## 4 RQ1: Are the Thresholds Met?

A pass rate is only interesting against a claim, and the claim under test is that this region's
broadband is good because its national averages are high. We take the national picture first, then
decompose it geographically and by access technology, which is where it breaks.

### 4.1 National pass rates, fixed broadband

**Table 3 — Fixed broadband threshold pass rates (%), test-weighted, Q1 2023–Q4 2025.**

| Country | HD | UHD | Cloud gaming | Voice | Tests |
|---|---|---|---|---|---|
| Vietnam | 100.0 | 100.0 | 100.0 | 100.0 | 25.9M |
| Singapore | 100.0 | 100.0 | 100.0 | 100.0 | 4.5M |
| Thailand | 100.0 | 100.0 | 99.5 | 100.0 | 20.8M |
| Malaysia | 100.0 | 100.0 | 97.6 | 100.0 | 15.7M |
| Philippines | 100.0 | 100.0 | 92.6 | 100.0 | 48.8M |
| Cambodia | 100.0 | 97.6 | 64.9 | 100.0 | 2.4M |
| Laos | 100.0 | 99.4 | 64.2 | 100.0 | 0.37M |
| Indonesia | 100.0 | **88.1** | **35.6** | 100.0 | 54.2M |
| Myanmar | 100.0 | **22.1** | **0.0** | 98.2 | 1.75M |

**HD video is not a constraint anywhere** — every province-quarter in every country clears 5 Mbps — and
**voice latency is effectively universal**, failing only marginally in Myanmar. Cloud gaming is the
discriminating threshold, pooling to 74.6% across the region, and it fails to reach 100% in **seven of
nine countries**.

The failures form a gradient rather than a tier. Five countries sit at or near ceiling (100% down to
Philippines at 92.6%), Cambodia and Laos form a middle band near 64%, Indonesia at 35.6% is a distinct
step below, and Myanmar at 0.0% stands alone — no Myanmar province-quarter in three years met 44 Mbps
and 25 ms simultaneously. UHD reproduces this ordering but does not establish it: as Section 3.3 sets
out, those figures depend on where the throughput line is drawn, and at Netflix's current 15 Mbps
recommendation every country clears UHD at 98.5% or better. **Cloud gaming separates these countries
because of its latency ceiling, not its bandwidth floor** — Myanmar's 0.0% is not a bandwidth story,
since 82.0% of its province-quarters exceed 20 Mbps.

Indonesia's placement matters because it is the region's largest market by test volume, at 54.2M fixed
submissions, and it performs second-worst. A narrative built on the original eight countries would have
described a clean upper tier against a lagging Myanmar/Cambodia/Laos tier; Indonesia replaces that with
a four-step gradient and puts the biggest market on the wrong side of it.

### 4.2 Capital versus periphery

If national averages are geographically misleading, restricting the same thresholds to capital provinces
should improve pass rates sharply. It does.

**Table 4 — Capital provinces: cloud-gaming pass rate and median download against the rest of the
country, fixed broadband. UHD is 100% in every capital except Yangon (3.2%).**

| Country | Capital | Cloud gaming % | Capital Mbps | Periphery Mbps | Gap |
|---|---|---|---|---|---|
| Philippines | NCR | 100.0 | 164.4 | 102.2 | **+62.2** |
| Thailand | Bangkok | 100.0 | 296.7 | 245.0 | +51.8 |
| Malaysia | Kuala Lumpur | 100.0 | 224.2 | 181.6 | +42.5 |
| Indonesia | Jakarta | 100.0 | 63.8 | 36.3 | +27.4 |
| Vietnam | Hà Nội | 100.0 | 150.7 | 127.5 | +23.3 |
| Cambodia | Phnom Penh | 66.8 | 60.5 | 45.3 | +15.2 |
| Laos | Vientiane | 77.6 | 54.4 | 43.0 | +11.4 |
| Myanmar | Yangon | 0.0 | 24.2 | 24.6 | **−0.4** |
| Singapore | Central Region | 100.0 | 320.5 | 366.1 | **−45.6** |

**Six of nine capitals clear every threshold at 100%.** Indonesia is the sharpest transition: a country
failing cloud gaming at 35.6% nationally passes at 100% in Jakarta. Laos and Cambodia improve on their
national figures without reaching full coverage. Only Myanmar fails in its capital, and it inverts the
expected pattern — Yangon's 3.2% UHD rate is *worse* than Myanmar's national 22.1%.

Seven of nine show the expected urban premium, from +11.4 Mbps in Laos to +62.2 in the Philippines. The
two exceptions are informative rather than anomalous. **Myanmar is flat**: Yangon tracks the national
median, so investment has not produced the capital-first concentration seen everywhere else.
**Singapore is negative**: its central-business-district proxy sits below every other planning region,
which is what one expects of a fully urban city-state whose newer residential fibre builds outperform
the commercial core. The "capital is best-connected" assumption requires a periphery to be true, and
Singapore has none.

Sections 4.1 and 4.2 together establish that threshold failures, where they exist, are overwhelmingly
peripheral. Note what this does *not* explain. Only Vietnam and Singapore clear every threshold
nationally, but Thailand and Malaysia miss by 0.5 and 2.4 percentage points, and Thailand's capital
passes everything — shortfalls far too small to account for the dissatisfaction that motivated this
study. Geography leaves a residual, which is what RQ3 and RQ4 take up.

### 4.3 Fixed versus mobile

Mobile is the access technology most users touch most often, and it behaves very differently.

**Table 5 — Mobile threshold pass rates (%) and the fixed–mobile cloud-gaming gap.**

| Country | UHD | Cloud gaming | Fixed CG | Gap (pp) | | Country | UHD | Cloud gaming | Fixed CG | Gap (pp) |
|---|---|---|---|---|---|---|---|---|---|---|
| Thailand | 100.0 | 21.6 | 99.5 | **77.9** | | Singapore | 100.0 | 48.8 | 100.0 | 51.2 |
| Vietnam | 100.0 | 27.9 | 100.0 | 72.1 | | Philippines | 99.6 | 43.2 | 92.6 | 49.4 |
| Malaysia | 100.0 | 33.5 | 97.6 | 64.1 | | Indonesia | 90.5 | 13.9 | 35.6 | 21.7 |
| Laos | 98.6 | 1.4 | 64.2 | 62.8 | | Myanmar | 68.8 | 0.0 | 0.0 | 0.0 |
| Cambodia | 87.7 | 10.5 | 64.9 | 54.4 | | | | | | |

**Mobile cloud gaming fails everywhere** — the region's best is Singapore at 48.8%, and Thailand reaches
only 21.6% despite a 99.5% fixed rate. The fixed–mobile gap exceeds 50 points in seven of nine
countries. Since cloud gaming is the only threshold pairing a throughput floor with a latency ceiling,
and mobile UHD passes at 100% in five countries, the binding constraint is latency.

Two countries invert the ordering: Myanmar's mobile UHD (68.8%) far exceeds its fixed rate (22.1%), and
Indonesia's is modestly above. Where fixed infrastructure is weakest mobile is not a substitute but the
better network, with direct implications for investment priority.

The capital-level mobile picture disrupts the geography of Section 4.2. Only the Philippines and
Malaysia reach 100% mobile cloud gaming in their capitals; Indonesia manages 58.9%, Thailand 51.3%,
Vietnam 38.1%, Cambodia 25.6%, Laos 7.4%, and **Singapore's Central Region reaches 0.0%**. Capital
status confers a large fixed-line advantage and very little mobile advantage — dense urban cores tax
cellular capacity in a way they do not tax fibre, which Section 6.4 takes up directly.

---

## 5 RQ2: Growth, 2023–2025

**Table 6 — Median province download growth, Ookla fixed, 2023-Q1 → 2025-Q4.**

| Country | 2023-Q1 | 2025-Q4 | Growth | | Country | 2023-Q1 | 2025-Q4 | Growth |
|---|---|---|---|---|---|---|---|---|
| Myanmar | 20.3 | 53.6 | +163.8% | | Laos | 32.0 | 62.2 | +94.4% |
| Cambodia | 25.3 | 61.7 | +144.1% | | Malaysia | 124.6 | 223.6 | +79.5% |
| Vietnam | 92.4 | 209.2 | +126.4% | | Thailand | 207.1 | 294.0 | +42.0% |
| Indonesia | 24.2 | 53.8 | +122.7% | | Philippines | 96.4 | 119.1 | +23.6% |
| Singapore | 282.0 | 553.8 | +96.4% | | | | | |

**Every country grew and no segment declined.** Seven of nine fit a catch-up pattern: the four
fastest-growing all start from a base of 20–92 Mbps, and the two slowest start high. Two do not fit,
and we flag rather than resolve them. Singapore starts above every other country at 282.0 Mbps and
still grows 96.4%, faster than five countries with far lower bases, so a high base does not
mechanically cap growth. Malaysia is the sharper case: at 124.6 Mbps it starts below Thailand's
207.1 Mbps yet grows nearly twice as fast, inverting the catch-up ordering for that pair. Both are
plausibly investment-cycle timing rather than diminishing returns, which Section 8's regression is
where to test. Mobile growth is faster throughout and reorders the table (Vietnam +209.1% to Myanmar
+13.8%), with Myanmar the reversal — fastest fixed growth in the region, slowest mobile.

Growth rate and attained level are distinct, and conflating them inverts the ranking: the two
slowest-growing countries, Thailand and the Philippines, end the period at opposite ends of the level
distribution, 294.0 against 119.1 Mbps. **The result that matters for this paper is negative.** No
country's quality fell over three years, so a trend argument cannot account for dissatisfaction
anywhere in the region, and one candidate explanation is closed off before Sections 6 and 7 take up the
others. Within countries the same catch-up appears — peripheral regions outgrow capital regions in
most of the nine — but Section 4.2 showed the absolute gaps remain large, so convergence is real,
incomplete, and slow enough that today's peripheral failures will persist for years.

NDT7 corroborates the direction but not the magnitude, agreeing that every country grew and on the
extremes (Vietnam fastest on both platforms, Thailand near the bottom on both) while disagreeing on the
middle ordering. Its per-country samples are very uneven (Table 1), so we read it as directional only.

---

## 6 RQ3: Peak-Hour Congestion

Sections 4 and 5 measure quality as if it were a property of a place. It is also a property of a time. A province-quarter average pools every hour of every day, so a network that is comfortable at 04:00 and saturated at 20:00 appears in Table 2 as its mean — adequate, and describing no hour anyone actually uses. This section asks whether that averaging conceals a systematic within-day pattern, following the busy-hour framework of Lübben and Misfeld (Section 2), whose German analysis this extends to nine countries.

We work from the per-test NDT7 records, which retain timestamps that the Ookla tile aggregates do not. Each test is converted to local time using a per-country offset, restricted to weekdays, and grouped by hour. Degradation is the ratio of throughput in a fixed evening busy window (19:00–22:00) to a fixed overnight quiet window (03:00–05:00); a ratio below 1 means the network is slower when more people use it. We report the ratio of hourly medians weighted by test count, which is a summary of the busy window rather than the median of the pooled window.

### 6.1 The busy hour is a human evening peak, not automated traffic

A diurnal pattern is evidence of demand-driven congestion only if the demand is human, and measurement
platforms attract automated and repeat testing, so we screen before interpreting. On mobile the busiest
hour falls in the evening (20:00–22:00 local) in **eight of nine countries**, the exception being
Vietnam at 10:00, and between 30% and 41% of each country's tests fall in the six evening hours against
the 25% a flat distribution would give. Tests per unique IP per hour sit between 1.4 and 6.3 with
peak-to-median ratios of 1.15–1.51, so no hour shows a small set of addresses generating
disproportionate volume — the signature of scripted testing.

We then require three conditions jointly: an evening busy hour, throughput that falls, **and latency
that rises**. The third does the real work, because falling throughput alone is explicable by a changing
mix of users or operators across the day, whereas throughput falling *while* latency rises is queueing
at a bottleneck, which a compositional shift does not produce. **Thirteen of eighteen country-segments
satisfy all three.**

The five that do not are excluded below and are informative in themselves. **Vietnam** fails on both
segments: a 10:00–11:00 busy hour, the region's lowest evening concentration (22.9% of broadband tests),
and broadband latency that *falls* under load (0.58) — whatever drives its diurnal profile is not
consumer demand, and we do not interpret it. **Cambodia's** broadband peaks at midday though its mobile
segment behaves normally. **Singapore** fails in the opposite direction: broadband *faster* in the
evening (1.25) with latency falling (0.83), i.e. no congestion at all, which for a fully-fibred
city-state is a plausible result rather than a defect.

### 6.2 Mobile networks degrade severely; fixed networks much less

**Table 7 — Peak-hour degradation, weekday download. Ratio of busy-hour (19–22h) to overnight (03–05h) throughput; below 1 means slower under load. Countries failing the Section 6.1 screen are marked †.**

| Country | Mobile ratio | Mobile p10 | Fixed ratio | Fixed p10 | Mobile RTT rise |
|---|---|---|---|---|---|
| Cambodia | **0.232** | **0.122** | 0.846† | 0.622† | 1.01× |
| Myanmar | 0.262 | 0.196 | 0.583 | 0.200 | 1.06× |
| Philippines | 0.304 | 0.175 | 0.464 | 0.203 | 1.20× |
| Laos | 0.320 | 0.281 | 0.596 | 0.437 | 1.04× |
| Indonesia | 0.398 | 0.242 | 0.732 | 0.541 | 1.08× |
| Malaysia | 0.420 | 0.190 | 0.673 | 0.397 | 1.12× |
| Vietnam† | 0.469 | 0.307 | 0.617† | 0.279† | 1.10× |
| Thailand | 0.556 | 0.543 | 0.893 | 0.544 | 1.09× |
| Singapore† | 0.729† | 0.346† | 1.253† | 0.514† | 0.99× |

The asymmetry between access technologies is the clearest result in this section. **Mobile throughput at the busy hour falls to between 0.23 and 0.73 of its overnight level; fixed broadband falls only to between 0.46 and 1.25.** In Cambodia a mobile connection delivers less than a quarter of its overnight throughput during the evening; in Myanmar and the Philippines, under a third. Every country degrades more on mobile than on fixed.

Latency corroborates this independently of throughput. Median round-trip time rises at the busy hour in eight of nine countries on mobile and six of nine on fixed, with the Philippines showing the largest fixed-line increase at 43%. Two measurements that would not move together under a compositional explanation move together here.

This finding also reframes Section 4.3, which reported that mobile cloud gaming fails almost everywhere while mobile UHD largely passes. That was measured on pooled data. The pooled figure understates the evening case: the same mobile networks that clear a 25 Mbps throughput bar on average are delivering a third or less of their capacity precisely when demand peaks.

### 6.3 The worst-served sessions degrade furthest

Averages describe the typical session, and complaints are rarely about typical sessions. We therefore repeat the measurement on the 10th percentile — the slowest tenth of sessions in each hour.

**The tail degrades more than the median in every country and on both access technologies, without exception.** Cambodia's slowest mobile decile falls to **0.122** of its overnight level, an eightfold reduction; the Philippines reaches 0.175 on mobile and 0.203 on fixed. Where the median user sees a network running at half speed, the worst-served tenth sees it at a fifth.

This bears directly on the question in Section 1. A province-quarter average cannot represent an experience that is this unevenly distributed across hours and across sessions, and the gap between a national statistic and a complaint is not evidence that one of them is wrong. They are measurements of different things: the statistic describes the average session, and dissatisfaction is generated by the tail of a distribution that is at its widest exactly when most people are online.

### 6.4 Capital cities degrade more, not less

Section 4.2 found that capital provinces clear application thresholds at higher rates than peripheries — six of nine capitals pass everything. Restricting the peak-hour analysis to the five countries with sufficient capital-level volume inverts that picture.

**Table 8 — Peak-hour degradation, capital versus rest of country, weekday download.**

| Country | Fixed: capital | Fixed: rest | Mobile: capital | Mobile: rest |
|---|---|---|---|---|
| Malaysia (Kuala Lumpur) | **0.581** | 0.774 | 0.428 | 0.404 |
| Thailand (Bangkok) | **0.804** | 0.956 | 0.556 | 0.566 |
| Indonesia (Jakarta) | **0.668** | 0.740 | **0.362** | 0.428 |
| Vietnam† (Hanoi) | 0.602† | 0.616† | 0.470† | 0.468† |
| Philippines (NCR) | 0.486 | 0.453 | **0.254** | 0.353 |

On fixed broadband the capital degrades more than the rest of the country in four of five cases, and the differences are substantial: Kuala Lumpur falls to 0.581 against 0.774 elsewhere in Malaysia, Bangkok to 0.804 against 0.956. On mobile, Jakarta and NCR degrade markedly more than their peripheries.

The two results are consistent once separated by grain. Capitals have better infrastructure, which is what threshold pass rates on pooled data measure, and they have far higher concurrent demand, which is what peak-hour degradation measures. **The capital advantage is an average-case advantage that narrows under load.** A Bangkok subscriber enjoys a network that clears every threshold in Table 3 and still loses a fifth of its throughput each evening, losing more of it than a subscriber in a province whose absolute speeds are lower. Geography and time are not competing explanations of dissatisfaction; they act on different margins, and the place best served on one is not best served on the other.

---

## 7 RQ4: Market Structure and the Median Subscriber

Sections 4 to 6 establish that the region's broadband is mostly adequate on average, improving
everywhere, failing mainly in peripheries, and degrading sharply in the evening. None of that explains
why users in countries with 100% pass rates complain. The mechanism proposed here does. National
averages are test-weighted, so they are dominated by whichever operators carry the most measured
traffic. If those are also the *better*-performing operators, the average describes the networks most
traffic crosses; if they are the *worse*-performing ones, the average is lifted by smaller, faster
operators carrying little of it, and the published figure describes a market's best networks rather
than its busiest. Which case obtains is an empirical question, and to our knowledge it has not been
asked of this region.

One inferential limit applies throughout, stated before the results rather than after. Our shares are
shares of **tests, not subscribers**. Treating them as subscriber shares would require test propensity
to be uniform across operators, which we cannot verify and have reason to doubt: carrier-grade NAT
compresses users behind addresses at operator-specific rates, and dissatisfied customers plausibly test
more often than satisfied ones — a bias running *against* our conclusion, since it would inflate a slow
incumbent's apparent share. We therefore frame everything in terms of measured traffic and the networks
carrying it. All results cover **eight countries; Singapore is excluded** for lack of ASN attribution
(Section 3.3).

### 7.1 Market concentration

**Table 9 — Herfindahl-Hirschman Index over ASN shares of test volume, named ASNs only.**

| Country | Broadband | Mobile | | Country | Broadband | Mobile |
|---|---|---|---|---|---|---|
| Laos | 3702 | 4427 | | Cambodia | 2010 | 5033 |
| Malaysia | 3006 | 2627 | | Thailand | 1679 | 2449 |
| Vietnam | 2797 | 3078 | | Myanmar | 687 | 2630 |
| Philippines | 2730 | 3374 | | | | |
| Indonesia | 2690 | 3288 | | | | |

Six of eight countries exceed the conventional 2500 threshold for a highly concentrated broadband
market, and Cambodia's mobile figure of 5033 is the most concentrated in the study, with Metfone at
66.4% share. Myanmar is the outlier in the opposite direction: a broadband HHI of 687 across six
operators above 5% share, which reflects the absence of a dominant national incumbent rather than
healthy competition — and it coexists with the worst measured performance in the region. Concentration
therefore does not predict performance on its own. What matters is not how concentrated a market is but
**which** operator is dominant, which is what the rest of this section measures.

### 7.2 The gap between major operators

Defining a **major** as an operator holding ≥5% of a country-segment's tests, the download ratio between
the best and worst major measures how much operator choice matters within a country.

**Table 10 — Best-versus-worst major operator, pooled 2023–2025. B = broadband, M = mobile.**

| Country | Seg | Worst major | Best major | Ratio | | Country | Seg | Worst major | Best major | Ratio |
|---|---|---|---|---|---|---|---|---|---|---|
| Malaysia | B | Celcom 44.1 | TIME dotCom 196.3 | **4.45×** | | Indonesia | M | Indosat 17.0 | Telkomsel 25.5 | 1.50× |
| Indonesia | B | Telkom 18.6 | Biznet 43.3 | 2.33× | | Philippines | M | Smart 20.8 | DITO 31.2 | 1.50× |
| Myanmar | B | Mytel 10.3 | Global Tech 22.9 | 2.23× | | Myanmar | M | Mytel 17.8 | Nine Comms 26.6 | 1.49× |
| Thailand | B | NT 65.9 | AIS 125.9 | 1.91× | | Philippines | B | PLDT 60.6 | Globe 90.0 | 1.48× |
| Laos | B | LTC 25.3 | Unitel 42.7 | 1.69× | | Malaysia | M | Digi 37.7 | Maxis 52.6 | 1.40× |
| Laos | M | ETL 13.3 | Unitel 22.2 | 1.68× | | Vietnam | M | VNPT 29.9 | Viettel 39.4 | 1.32× |
| Cambodia | B | EZECOM 19.4 | ANGKOR DATA 31.0 | 1.60× | | Cambodia | M | Metfone 19.0 | Smart 23.9 | 1.26× |
| Thailand | M | dtac 18.9 | AIS 29.4 | 1.55× | | Vietnam | B | VNPT 66.7 | Viettel 71.0 | **1.06×** |

The spread is wide enough to rival the cross-country variation the paper is built on. Malaysian
broadband majors differ by **4.45×**, from Celcom at 44.1 Mbps to TIME dotCom at 196.3. More
pointedly, Thailand's 1.91× operator gap exceeds its 1.21× capital-to-periphery ratio (Table 4): which
operator a Thai household buys from separates outcomes more than where in the country it lives. At the
other extreme Vietnam's broadband majors differ by only 1.06×, the narrowest in the region.

### 7.3 Most-used is not fastest

The decisive test is whether the operator carrying the most traffic is the one performing best. Table 11
locates each country's volume leader within its own market's range, 0% being the slowest major and 100%
the fastest. Every volume leader is itself a major, so the two populations coincide.

**Table 11 — Highest-volume versus fastest major operator, broadband.**

| Country | Most-used (share) | Mbps | Fastest major (share) | Mbps | Shortfall | Leader's position |
|---|---|---|---|---|---|---|
| Indonesia | Telkom Indonesia (49.7%) | 18.6 | Biznet (5.2%) | 43.3 | **2.3×** | **0% — slowest** |
| Myanmar | Mytel (15.4%) | 10.3 | Global Technology (6.4%) | 22.9 | 2.2× | **0% — slowest** |
| Philippines | PLDT (46.3%) | 60.6 | Globe (11.9%) | 90.0 | 1.5× | **0% — slowest** |
| Malaysia | TM (50.3%) | 113.1 | TIME dotCom (13.2%) | 196.3 | 1.7× | 45% — mid-market |
| Thailand | True (28.9%) | 114.5 | AIS (23.1%) | 125.9 | 1.1× | 81% |
| Cambodia | Metfone (40.9%) | 30.3 | ANGKOR DATA (11.5%) | 31.0 | 1.0× | 94% |
| Laos | Unitel (48.8%) | 42.7 | Unitel (48.8%) | 42.7 | — | 100% — fastest |
| Vietnam | Viettel (39.0%) | 71.0 | Viettel (39.0%) | 71.0 | — | 100% — fastest |

Two counts matter here and conflating them would overstate the result. **The most-used broadband
operator is not the fastest major in six of eight countries** — all but Laos and Vietnam. But the
mechanism requires the leader to be a *slower* operator, not merely not-the-fastest, and that holds in
**four of eight**: the leader is the outright slowest major in Indonesia, Myanmar, and the Philippines,
and sits at the midpoint in Malaysia. In Thailand (81%) and Cambodia (94%) the leader is near the top
of its market, so those are not cases of an average dragged down by its incumbent even though a faster
major exists.

Where it holds, it is severe. Indonesia is the extreme case: Telkom Indonesia carries **49.7% of
measured broadband traffic while being the slower of only two majors**, at 18.6 Mbps against Biznet's
43.3 — so the busiest network in the region's largest market delivers roughly 43% of what its fastest
major delivers. Myanmar and the Philippines have the same shape with more competitors. The mobile side
distributes differently: the leader is fastest in three of eight, and outright slowest in Cambodia,
where Metfone holds 66.4% of mobile tests — the largest share held by a slowest operator anywhere in
our data — and in the Philippines.

The national statistic is not wrong in these countries; it answers a different question than the one
policy asks of it. It reports the average measured speed, when what matters is how the network carrying
most of the traffic compares to the best that market has demonstrated it can build.

This also explains the residual left by Section 4.2. Thailand clears 99.5% nationally and 100% in
Bangkok, yet its slowest major delivers 65.9 Mbps against its fastest major's 125.9 — a spread no
province-level average can show, because both operators serve the same provinces. Geography and
operator choice are separate axes, and only the first is visible in province aggregates.

Vietnam is where every indicator lines up: the dominant operator is also the fastest, the operator gap
is the region's narrowest, and it is one of only two countries clearing every threshold nationally.
That is exactly what the mechanism predicts — where the leader performs well and operators differ
little, a test-weighted average is a fair summary and measured quality should not diverge from
sentiment. Laos also has a leader that is its fastest operator but a mid-range 1.69× gap, so leader
quality and market uniformity are separable properties rather than one underlying factor. The other
country clearing every threshold, Singapore, cannot be tested this way at all — it is the one country
without ASN attribution, so whether its market is uniform is unknown, and that gap is the most useful
target for future work.

---

## 8 Cross-Country Statistical Validation

Sections 4–7 are descriptive. This section establishes that the cross-country differences are
statistically real, that they survive the correction our data structure demands, and that they replicate
on an independent platform.

### 8.1 Omnibus and pairwise tests

Kruskal-Wallis on province-quarter download across the nine Ookla country groups rejects equal
distributions (H = 2810.07, p < 10⁻¹⁵, n = 3222), and Holm-corrected pairwise Mann-Whitney tests find
**35 of 36 country pairs differ significantly**. The sole exception is **Cambodia–Laos** (p = 0.82),
which Tables 3 and 6 anticipate: near-identical pass rates, near-identical growth, adjacent levels.
NDT7 reproduces the structure independently (H = 1605.25, n = 2539), again 35 of 36, again with
Cambodia–Laos the only exception (p = 0.19). Two platforms with different methodologies, different
sampling, and a known 12–56% magnitude offset agree on which single pair in the region is
indistinguishable.

### 8.2 Correcting for repeated measures

Each province contributes twelve province-quarter rows, so the tests above treat repeated measurements
of the same province as independent, inflating effective sample size roughly twelvefold; the OLS
Durbin-Watson of 0.613 confirms substantial positive autocorrelation. Collapsing to one row per province
reduces n from 3222 to 270, and Kruskal-Wallis remains decisive (H = 248.83, p = 3.1 × 10⁻⁴⁹) with
**35 of 36 pairs still significant and none lost**. Re-estimating with standard errors clustered by
province inflates them by 0.83–2.68× (log-GDP 1.30 → 3.42; Singapore's fixed effect 6.30 → 13.74) while
**every coefficient retains its sign and significance**. The conclusions are robust to
pseudo-replication; only the precision of the p-values was overstated. We report clustered standard
errors throughout and avoid quoting p-values below 10⁻¹⁵.

### 8.3 Regression and cross-source ranking agreement

Modelling province download on log GDP per capita, log density, and country fixed effects gives
R² = 0.870 on Ookla (n = 3222). Both covariates are positive and significant: **+15.51 Mbps per log-unit
of GDP per capita** (SE 3.42) and **+4.93 per log-unit of density** (SE 1.10). Country effects relative
to Cambodia are Singapore +275.3, Thailand +188.9, Malaysia +106.6, Vietnam +83.8, Philippines +55.0,
Laos +2.9 (n.s.), Myanmar −9.8, Indonesia −18.8. NDT7 gives the same qualitative picture independently
(n = 2539, R² = 0.653): log GDP +14.22, log density +3.39, Singapore +126.6, Malaysia +56.2, Thailand
+46.5, Philippines +28.9, Vietnam +19.4, Laos +2.4 (n.s.), Myanmar −4.6 (n.s.), Indonesia −12.4.

That GDP and density remain significant *after* absorbing country fixed effects means within-country
economic geography predicts broadband quality independently of national context. The coefficient is
however identified almost entirely off the five countries publishing sub-national GDP; for the other
four a single national value repeats across provinces (Section 9.1), so their fixed effects should be
read as absorbing GDP rather than isolating a GDP-independent residual.

Rank-correlating the two sets of country fixed effects gives **Spearman ρ = 0.967 (p = 2 × 10⁻⁵,
n = 9)**; an independent check on threshold pass rates rather than coefficients gives **ρ = 0.90
(p = 0.001)**. Two platforms disagreeing substantially on absolute magnitude produce near-identical
country orderings — the strongest available evidence that our country-level conclusions reflect the
networks rather than either platform's methodology.

**One methodological note, because an earlier version of this figure was wrong instructively.** Vietnam's
NDT7 export carried no GDP or density values: the files disagree on province spelling, the NDT7 side
stripping spaces (`AnGiang`) where the reference file does not (`An Giang`), giving **zero** exact
matches across 63 provinces while the Ookla side matched 64/64. Vietnam's 698 rows were dropped by the
model's `dropna`, and the baseline-recovery step — which inferred the reference country by set
difference against the input list — could not distinguish "reference level, coefficient 0 by
construction" from "dropped entirely", and assigned Vietnam 0.0. That fabricated point produced a
spurious ρ = 0.912. Both faults are fixed: a diacritic- and space-insensitive join key recovers all 698
rows with no collisions, and the baseline is now derived from the countries actually in the fitted
model, so a dropped country raises a warning instead of silently acquiring a zero. The failure mode is
general — any fixed-effects specification reconstructing an omitted baseline by set difference will
manufacture a spurious zero for a group lost to missing covariates, biased toward the baseline rather
than obviously broken.

---

## 9 Discussion

**A national average conceals three different things, and they act on different margins.** Our reading
of the ranking-versus-sentiment gap requires all three findings, not any one of them.

*Where.* Threshold failures concentrate in peripheral provinces, and six of nine capitals clear every
threshold (Section 4.2). Real but incomplete: only two countries fail to clear every threshold
nationally, and dissatisfaction is reported where the measured shortfall is a fraction of a percentage
point. Geography cannot carry that alone.

*When.* The same networks that clear thresholds on pooled data lose most of their capacity in the
evening (Section 6). Mobile throughput falls to between 0.23 and 0.73 of its overnight level, latency
rises alongside, and the slowest tenth of sessions degrades to 0.122 in Cambodia. A province-quarter
average is the mean of a distribution at its widest precisely when most people are online.

*Whose.* The operator carrying the most traffic is not the fastest major in six of eight countries, and
in four it sits at or below its market's midpoint (Section 7), so a test-weighted average is pulled
toward the incumbent while the market's demonstrated capability sits on a network carrying little
traffic.

Section 6.4 shows why these cannot be collapsed into one. Capitals are *better* on threshold pass rates
and *worse* on peak-hour degradation — Kuala Lumpur falls to 0.581 of its overnight throughput against
0.774 for the rest of Malaysia. A subscriber can be well served on the geographic margin and poorly
served on the temporal one at the same address, so any single-mechanism account predicts the wrong sign
for at least one result. The policy consequence is that the three margins need different instruments:
extending coverage addresses *where*, capacity provisioning at peak addresses *when*, and neither
touches *whose*, which concerns which operator holds the traffic rather than network reach. Published
aggregates make only the first visible, so a programme optimising the national average would rationally
under-invest in the other two.

**Three narrower findings follow.** Latency rather than bandwidth is the binding constraint on demanding
applications: mobile cloud gaming — the only threshold pairing a throughput floor with a latency ceiling
— fails everywhere, peaking at 48.8% in Singapore, so further investment in headline download speed will
not move it. Where fixed infrastructure is weakest, mobile is the better network: Myanmar's mobile UHD
pass rate (68.8%) far exceeds its fixed rate (22.1%), inverting the usual investment ordering. And
convergence is real but slow — peripheral regions outgrow cores in most countries while absolute gaps
remain large, up to +62.2 Mbps in the Philippines, so today's peripheral failures will persist for
years.

### 9.1 Limitations

**No ground truth for the cross-platform gap.** Any Ookla–NDT7 difference is confounded between genuine
network differences and active-versus-passive methodology. We use MacMillan et al.'s 12–56%
underreporting finding as prior context, never as a correction, and compare the platforms only on
rankings (Section 8.3), never by pooling.

**Mobile–fixed classification is a heuristic.** NDT7 network type derives from ip-api's per-block
`mobile` flag. Before the ASN relabelling whole operators were misfiled — `AIS SUPER WiFi`, a home-WiFi
brand, was 89% labelled cellular; Starlink 96%. The relabelling corrects this as of one 11.49-hour
window, but the label records what ip-api reported on that date, not verified truth, and some operators
genuinely sell both services (Philippine Globe runs AS4775 as 81% cellular and AS132199 as 60%
broadband), making their split approximate by construction. Every NDT7 mobile finding is
lower-confidence than its broadband equivalent, and mobile reliable-row counts are smaller throughout —
Vietnam passes the gate on only 26.3% of its mobile province-quarters, the lowest rate in the dataset.

**Test share is not subscriber share, which bounds RQ4.** Treating measured-test shares as subscriber
shares would require uniform test propensity across operators, and two mechanisms make that unlikely:
carrier-grade NAT compresses users behind addresses at operator-specific rates, and dissatisfied
customers plausibly test more often than satisfied ones. The second bias runs *against* our conclusion,
since it would inflate a slow incumbent's apparent share — the direction that would manufacture our
result. We therefore claim only what test-weighting supports. Converting it to a per-subscriber claim
needs operator subscriber counts, unavailable for most of these markets.

**GDP identification is degenerate for four countries.** Singapore, Cambodia, Myanmar, and Laos publish
no sub-national GDP series, so the regression's GDP coefficient is identified off the other five
(Section 8.3).

**NDT7 samples are uneven and not stable over time.** Cambodia and Laos rest on 33 and 37 reliable
province-quarters against Thailand's 872 (Table 1), and Vietnam's coverage decays from roughly 48% of
provinces in 2023-Q1 to 11% by 2025-Q4, so its later comparisons rest on a shrinking, non-random subset.

**Two structural gaps.** geoBoundaries folds Naypyidaw into Mandalay Region, so Myanmar's capital
analysis substitutes Yangon for the actual seat of government. And Singapore is absent from RQ4 entirely
for want of ASN attribution (Section 3.3) — the most consequential omission, since the mechanism in
Section 7.3 predicts that a market with a well-performing incumbent should show little
ranking-sentiment divergence, and Singapore is exactly that test case.

### 9.2 Future work

**Vietnam's diurnal profile is unexplained and is the most concrete open question.** It is the one
country whose peak-hour behaviour fails our screen on every criterion (Section 6.1): a mid-morning busy
hour, the region's lowest evening concentration of tests, and latency that *falls* under load. We
exclude it from the congestion claims rather than interpret it, but the pattern is systematic rather
than noisy and something is generating it — a measurement-infrastructure artefact, an unrepresentative
server or client population, or a genuinely different usage profile. Distinguishing these requires
per-server and per-ASN decomposition of the Vietnamese sample, which the current aggregation does not
support.

Three further extensions follow directly. Restoring Singapore to RQ4 would require ASN attribution for its NDT7 data and would test Section 7.3's mechanism on the region's strongest market. A dedicated study of Myanmar's rollout history would address the two anomalies it produces here — a capital that does not lead, and the region's least concentrated market coinciding with its worst performance. Finally, the methodology transfers to any region with tile-level Ookla coverage and per-test NDT7 data, and the market-structure result in particular is worth testing where incumbent dominance and measured performance can be jointly observed.

---

## 10 Conclusion

Across nine Southeast Asian countries measured on one consistent pipeline, fixed broadband clears
baseline video thresholds almost everywhere. The region's real failures are concentrated in
cloud-gaming-grade requirements — met fully only by Vietnam and Singapore, and missed substantially by
Cambodia, Laos, Indonesia, and Myanmar — and they fall overwhelmingly outside capital cities. Growth
over 2023–2025 was universal, so no country's quality declined and a trend argument cannot account for
dissatisfaction anywhere in the region.

Explaining why high national rankings coexist with widespread complaint requires three findings
together, not one. Failures are geographically concentrated in peripheries, yet six of nine capitals
clear every threshold and complaints persist there too. Measured quality is strongly time-dependent:
mobile throughput at the evening busy hour falls to between 0.23 and 0.73 of its overnight level, the
slowest tenth of sessions falls as far as 0.12, and latency rises alongside — a pattern averaging
erases entirely. And in six of eight countries the operator carrying the most traffic is not the fastest
major, so a test-weighted average describes a market's busiest networks rather than its best.

That these three cannot be collapsed is shown most directly by the capital cities, which are the
best-served places on the geographic margin and among the worst on the temporal one: Kuala Lumpur and
Bangkok clear every threshold and lose more of their throughput each evening than their own peripheries
do. A subscriber's experience is determined jointly by where they are, when they use the network, and
whose network it is, and a single national number is an average over all three at once.

The practical consequence is that published aggregates cannot support the questions asked of them.
They make coverage visible while concealing both peak-hour capacity and market composition, so a policy
programme optimising the national average would rationally under-invest in the two margins that our
results suggest matter most to users. Reporting a national broadband average without the market
structure and the demand cycle that produced it invites precisely the contradiction this paper set out
to explain.

## Acknowledgments

*TODO — collaborator contributions (Vietnam and Philippines NDT7 delivery, ip-api ASN relabelling) and advisor acknowledgements to be finalised.*

---

## References

- Röller, L.-H., & Waverman, L. (2001). *Telecommunications Infrastructure and Economic Development: A Simultaneous Approach*. The American Economic Review, 91(4), 909–923.
- Ookla. (2023). *Speedtest by Ookla Global Fixed and Mobile Network Performance Maps* [Dataset]. https://github.com/teamookla/ookla-open-data
- MacMillan, K., Mangla, T., Saxon, J., Marwell, N. P., & Feamster, N. (2023). *A Comparative Analysis of Ookla Speedtest and Measurement Lab's Network Diagnostic Test (NDT7)*. Proceedings of the ACM on Measurement and Analysis of Computing Systems, 7(1), Article 19. https://dl.acm.org/doi/epdf/10.1145/3579448
- Lübben, R., & Misfeld, N. (2022). *Exploring the Measurement Lab Open Dataset for Internet Performance Evaluation: The German Internet Landscape*. Electronics, 11(1), 162. https://doi.org/10.3390/electronics11010162 — thresholds taken from Table 5, "Exemplary application requirements"; busy-hour method from §4.2.
- International Telecommunication Union. (2003). *ITU-T Recommendation G.114: One-Way Transmission Time*. https://www.itu.int/rec/T-REC-G.114-200305-I/en — primary source for the 200 ms voice latency threshold.
- Di Domenico, A., Perna, G., Trevisan, M., Vassio, L., & Giordano, D. (2021). *A Network Analysis on Cloud Gaming: Stadia, GeForce Now and PSNow*. Network, 1(3), 247–260. https://doi.org/10.3390/network1030015 — primary source for the 44 Mbps cloud-gaming throughput requirement.
- Flinck Lindström, S., Wetterberg, M., & Carlsson, N. (2020). *Cloud Gaming: A QoE Study of Fast-paced Single-player and Multiplayer Gaming*. In Proceedings of the 2020 IEEE/ACM 13th International Conference on Utility and Cloud Computing (UCC), Leicester, UK, 7–10 December 2020, pp. 34–45. — primary source for the 25 ms cloud-gaming latency threshold.
- Netflix. *Netflix-recommended internet speeds* [Help Center]. https://help.netflix.com/en/node/306 — original source of the 5 Mbps HD and (at the time of Lübben & Misfeld's compilation) 25 Mbps UHD figures; now published as 15 Mbps for Ultra HD. See Section 3.4 and Table 2.
- Nation Thailand. (2025a, March 1). *Thailand ranks 13th in the world for fixed broadband speed*. https://www.nationthailand.com/business/tech/40046895
- Nation Thailand. (2025b, May 23). *Thai telecom outages expose duopoly flaws, experts call for fair competition*. https://www.nationthailand.com/business/tech/40050343
- Foundation for Consumers (มูลนิธิเพื่อผู้บริโภค). (2023). *Consumer impact survey following the True–dtac merger* (n = 2,924). Reported in Thai PBS, https://www.thaipbs.or.th/news/content/334937, and Thailand Consumers Council, https://www.tcc.or.th/true-dtac-merger-consumer/ — source of the 81% figure in Section 1. Self-selected respondents; not a representative national sample.
- geoBoundaries. (2023). *geoBoundaries Global Database of Political Administrative Boundaries* [Dataset]. https://www.geoboundaries.org
- Global Administrative Areas. (2022). *GADM database of Global Administrative Areas, version 4.1*. https://gadm.org
- World Bank. (2026). *GDP per capita (current US$) and GDP per capita, PPP (current international $)* [Dataset]. World Bank Open Data. https://data.worldbank.org
- Department of Statistics Malaysia (DOSM). (2022). *Gross Domestic Product (GDP) by State, 2021*. https://www.dosm.gov.my
- National Institute of Statistics, Ministry of Planning, Cambodia. *Statistical Yearbook* [confirms no province-level GRDP series currently published]. https://www.nis.gov.kh
- M-Lab. (2025). *Measurement Lab NDT7 Data*. https://www.measurementlab.net/data/docs/bq/quickstart/
- ip-api. (2026). *IP Geolocation API*. https://ip-api.com

---

## Appendix A — Open items before submission

| Item | Blocks | Status |
|---|---|---|
| **Cut ~30% of body text for the 9-page sigconf limit** | Camera-ready | See A.1 below |
| ~~Trim abstract to acmart's 150–200 words~~ | Abstract submission | **Done — 191 words, submission-ready** |
| ~~State the test-share vs subscriber-share limit~~ | RQ4 claim validity | **Done — §6 preamble and §8.1**; all "typical subscriber" phrasing removed from claims |
| ~~Verify Lübben & Misfeld (2022) citation~~ | — | **Done 2026-07-30 — all four thresholds match their Table 5; citation had wrong initial + fake title, both fixed** |
| ~~Fix Vietnam NDT7 province-name join~~ | — | **Done — applied + notebook re-run; ρ = 0.967, n = 2539, 9 countries** |
| ~~Port clustered standard errors into the notebook~~ | — | **Done — both models now `cov_type=cluster` by province** |
| Port this draft into `docs/paper.tex` (title, authors, abstract, sections, bibliography) | Camera-ready | `paper.tex` still a skeleton |
| Update `docs/citations.md` with non-Thai sources | Full paper | Not started |
| Update `docs/Process.md` — still has RQ4/RQ3 in the old order | Nothing | Not started |
| Add ASN attribution for Singapore NDT7 | §6 completeness | Blocked on data |
| ~~Integrate RQ3 peak-hour into the body~~ | — | **Done — Section 6 written; Discussion rebuilt around three mechanisms** |
| **Rename `rq3_peakhour.ipynb` → `rq3_peakhour.ipynb`** and relabel its `rq3_*` exports/figures | Consistency | Collaborator used the pre-swap numbering |

### A.1 Length

This draft is roughly 9,200 words with ten tables and no figures. ACM sigconf at 9 pages fits closer to 5,500–6,000 words of body text once tables and references are placed, so about 30% has to come out. The author's call, not a mechanical trim — candidates in order of how much they cost to lose:

1. **§5.2** names seven countries' regional growth rankings in prose; one table or two sentences would carry the same point.
2. **§2** runs four labelled subsections where the AINTEC style reference uses two paragraphs.
3. **§8.1** repeats several limitations already stated in §3 (reliability gate, latency filtering, boundary caveats) — cross-reference instead of restating.
4. **§4.3**'s capital-mobile paragraph duplicates §4.2's structure for a secondary result.

Several tables could also become figures, which is how the style reference spends its space and would read better for the growth and threshold comparisons.

### A.2 Number provenance notes

- **HHI values in §6.1 are recomputed in-repo** from `data/exports/ndt7_isp_*_quarterly.csv` (ASN shares of test volume, named ASNs only). They differ by 1–3% from the values in `HANDOFF.md` (e.g. Myanmar 687 here against 703 there; Thailand 1679 against 1700). The values here are reproducible from files in this repository and should not be "corrected" back to HANDOFF's.
- **§6.3's leader-position column** is derived from `rq4_leaders.csv` and `rq4_within_gap.csv`; it is not currently computed inside `rq4_isp.ipynb` and should be added there so the table is reproducible from the notebook alone.
- **Capital-versus-periphery figures in Table 4** compare the capital against non-capital provinces only. An earlier revision compared the capital against a country-wide median that included the capital itself, which understated every gap.
