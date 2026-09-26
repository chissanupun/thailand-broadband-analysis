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
problems. We analyze 990 million speed tests — 229.4M from Ookla Open Data
and 760.6M from M-Lab NDT7, Q1 2023 to Q4 2025 — across nine countries, and
score each country-quarter against the bandwidth requirements of voice, HD
video, UHD video and cloud gaming. Our preliminary results show that basic
connectivity is solved: voice and HD video succeed at 100% in every
country, every quarter of 2024–2025. That uniformity collapses at higher tiers. Fixed broadband stratifies
sharply by geography, with a 16x spread between the strongest and weakest
capital regions, and cloud-gaming success ranges from 100% in Singapore
to a peak of only 37% in Indonesia and 31% in Myanmar. Work is ongoing
on per-province modeling and on peak-hour behavior.

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
`poster_content.md`).
