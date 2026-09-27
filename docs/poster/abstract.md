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
problems (Thailand Consumer Council, 2023). Across nine countries, we
analyze 990 million speed tests — 229.4M from Ookla Open Data and 760.6M
from M-Lab NDT7, Q1 2023 to Q4 2025. Using Ookla province-quarter
aggregates, we compute the test-weighted share of province-quarters that
clear the bandwidth (and, for cloud gaming, latency) requirements of voice,
HD video, UHD video and cloud gaming. Both datasets are crowdsourced and
user-initiated rather than random samples. Voice and
HD video clear their bars in essentially every province-quarter across all
twelve quarters. Fixed broadband stratifies sharply by geography, with a
16x spread between the strongest and weakest capital regions. Against the
combined cloud-gaming bar, the binding constraint flips by market:
low-tier fixed broadband (Cambodia, Laos, Myanmar) fails mostly on
bandwidth, while five mobile networks — including Singapore, where only
48.8% of province-quarters meet the latency bound — clear bandwidth almost
universally yet fail mostly on latency. Work is ongoing on per-province
modeling and on peak-hour behavior.

## Keywords

Internet measurement, broadband performance, Southeast Asia, Ookla, M-Lab
NDT7, application requirements

**Updated:** 2026-09-27 — synchronized with `main/abstract.tex` after the
AINTEC full-paper reviews flagged the earlier median-ratio metric. The
abstract now reports the test-weighted share of province-quarters that
actually clear each threshold, with Ookla latency used for cloud gaming
because most NDT7 servers are offshore. The mobile latency result is
limited to the five markets where bandwidth clears almost universally;
the other four do not show that reversed-constraint pattern. The two-page
PDF and this text field should be checked together before submission.
