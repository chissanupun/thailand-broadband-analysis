# Poster abstract — HotCRP text field

Kept in sync with `main/abstract.tex` — copy this verbatim into the HotCRP
abstract field, don't hand-edit numbers here independently of the PDF.

## Title

Beyond Speed Rankings: Application-Layer Broadband Performance in Nine
Southeast Asian Countries

## Abstract

Southeast Asian broadband is usually judged by headline speed-index
rankings, which say little about whether real applications work. Thailand
ranked 12th worldwide for fixed broadband in June 2026, yet a 2023 national
consumer survey found 81% of 2,924 respondents reporting connection
problems (Thailand Consumer Council, 2023). We analyze 990 million speed
tests — 229.4M from Ookla Open Data and 760.6M from M-Lab NDT7, Q1 2023 to
Q4 2025 — across nine countries, and compute the test-weighted share of
province-quarters that clear the bandwidth (and, for cloud gaming,
latency) requirements of voice, HD video, UHD video and cloud gaming (both
datasets are crowdsourced and user-initiated rather than a random sample).
Voice and HD video clear their bars in essentially every province-quarter
across all twelve quarters. Fixed broadband stratifies sharply by
geography, with a 16x spread between the strongest and weakest capital
regions. Against the combined cloud-gaming bar, the binding constraint
flips by market: low-tier fixed broadband (Cambodia, Laos, Myanmar) fails
mostly on bandwidth, while mobile networks in every single country —
including Singapore, at only 48.8% — fail mostly on latency. Work is
ongoing on per-province modeling and on peak-hour behavior.

## Keywords

Internet measurement, broadband performance, Southeast Asia, Ookla, M-Lab
NDT7, application requirements

**Updated:** 2026-09-26 — resynced to match `main/abstract.tex` (previous
09-15 draft used stale numbers: title varied, capital-gap figure said 12x,
verified figure is 16x). Same day, second pass: success-rate window
(2024–2025), Myanmar/Indonesia cloud-gaming bound, US spelling. Third
pass: "province-quarter" → "country-quarter" (the success rate is a national
median, per commit 64970b8), Singapore "roughly 100%" → "100%" (exactly
100.0 in all 8 quarters), "at most 37%/31%" → "a peak of only" (true values
37.1/31.2). Fourth pass: removed "on both fixed and mobile networks"
(CSV has no fixed/mobile split; open question for Pakkapon, see
`poster_content.md`). Fifth pass (2026-09-27, after AINTEC full-paper
rejection flagged the same metric as its most serious flaw): reworded
"succeed"/"connectivity is solved"/"success rate" language to make clear
the metric is median download speed as a capped percentage of a bandwidth
threshold, not a pass/fail rate; added one sentence stating the evaluation
is bandwidth-only (no latency) and both datasets are user-initiated, not a
random sample; added the missing TCC survey citation (`TCC2023` in
`references.bib`, sourced from tcc.or.th, 19 Dec 2023).

**Sixth pass (2026-09-27), after full-paper rejection — metric replaced,
not just reworded.** All three AINTEC reviewers of the rejected full paper
(#51) flagged the median-ratio metric itself, not just its labeling.
Replaced with the test-weighted % of province-quarters actually clearing
each threshold — bandwidth AND (for cloud gaming) Ookla latency <=25ms,
per อาจารย์'s 2026-08-13 ruling that cloud-gaming latency use Ookla, not
NDT7 (NDT7 mostly hits offshore servers). Every number independently
recomputed from `data/exports/ookla_*_province_quarterly.csv` — see
`main/abstract.tex`'s header comment for the exact method (matches
`notebooks/comparison/rq1_thresholds_ookla.ipynb`). New headline finding:
the binding constraint on cloud gaming flips by market and connection
type — bandwidth blocks low-tier fixed broadband, latency blocks mobile
*everywhere*, including Singapore (48.8% latency pass) and Malaysia/
Thailand (21.6-33.5%). Old "37% Indonesia / 31% Myanmar" framing is gone —
it was never a pass rate. PDF recompiled: 2 content pages + references,
clean.
