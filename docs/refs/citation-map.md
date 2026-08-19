# Citation Map — which paper goes where

A working aid for drafting, not a finished bibliography. For each section of `paper_draft.md`,
this lists which of the 16 PDFs in `docs/` supports it and what claim it backs. Fill citations in
one slot at a time.

**Status of the pile:** 16 academic PDFs organised in `docs/01–05`. This is already a
journal-adequate related-work base — the task now is *placing* them, not finding more.
Two still missing (behind paywalls, request via library): none critical — every section is covered.

---

## By draft section

### §1 Introduction

| Claim in the text | Cite | File |
|---|---|---|
| Broadband raises GDP (10% penetration → 1–3% GDP) | Röller & Waverman 2001 · **Sridhar & Sridhar 2007** | `05-thailand-context/sridhar-2007-…` |
| "Ranked well but users complain" — the core contradiction | **Stocker & Whalley 2018** | `04-benchmarks-theory/stocker-whalley-2018-…` |
| Gap: no Thai study measures *quality* with real data | **Setthasuravich 2024** · Denfanapapol 2024 | `05-thailand-context/` |
| Cross-validation framework (Ookla vs NDT7) | **MacMillan 2023** | `03-cross-platform/macmillan-2023-…` |

> Röller-Waverman uses 21 OECD countries; **Sridhar 2007 uses developing countries** — closer to the
> Thai context, so cite it alongside or instead. Röller-Waverman itself is not in the folder (paywalled).

### §1.2 / §1.3 Hypotheses & scope

| Claim | Cite | File |
|---|---|---|
| Quality varies by area & network type, not one national answer | Stocker & Whalley 2018 | `04-…` |
| Prior Thai divide work is access-based, province/sub-district | Setthasuravich 2024 (sub-district) · Denfanapapol 2024 (province) | `05-…` |

### §2 Data

| Claim | Cite | File |
|---|---|---|
| Ookla open-data tiles used for Asia-Pacific analysis (precedent) | **'Ofa & Aparicio / ESCAP 2021** | `01-ookla/ofa-aparicio-2021-…` |
| M-Lab NDT7 platform description | **Gill 2022** (editorial, not peer-reviewed — cite for platform only) | `02-ndt7-mlab/gill-2022-…` |
| Per-country M-Lab EDA is an established design | Lübben & Misfeld 2022 (Germany) | `02-ndt7-mlab/lubben-misfeld-2022-…` |

### §3.2 Cross-country comparison

| Claim | Cite | File |
|---|---|---|
| Measuring spatial disparity in internet quality via speed tests | **Caldas / OECD 2023** | `01-ookla/caldas-2023-…` |
| Ookla for cross-region Asia-Pacific comparison | 'Ofa / ESCAP 2021 | `01-ookla/ofa-aparicio-2021-…` |

### §3.3 Ookla-vs-NDT7 cross-validation (the novelty)

| Claim | Cite | File |
|---|---|---|
| The two platforms differ in methodology & magnitude | **MacMillan 2023** (core reference) | `03-cross-platform/macmillan-2023-…` |
| Cross-platform speed-test validation is a real method | Lipphardt 2025 (M-Lab vs Cloudflare) | `03-cross-platform/lipphardt-2025-…` |
| Crowdsourced data needs bias correction | Lee 2023 | `01-ookla/lee-2023-…` |
| M-Lab big data can compare ISPs (like our Part 8) | Deng 2021 | `02-ndt7-mlab/deng-2021-…` |

> ⚠️ **FACT-CHECK BEFORE CITING.** Draft §3.3 (line 153) and §1.3 (line 36) claim NDT7 is a
> "passive/background test" and that MacMillan found NDT7 "underreports 12–56%". Both look wrong
> against the actual paper (NDT7 is *active* single-stream; the gap is mainly at high RTT). Read
> `macmillan-2023-ookla-vs-ndt7.pdf` and correct these two sentences before the citation goes in —
> otherwise a reviewer who knows the paper catches it.

### §3.6 Anomaly / divergence detection

| Claim | Cite | File |
|---|---|---|
| Performance inequity across users (divergence framing) | **Paul 2021** | `01-ookla/paul-2021-…` |
| Sampling-bias correction motivates `is_reliable` / weighting | Lee 2023 | `01-ookla/lee-2023-…` |

### Benchmarks — answering "good or bad" (Objective 4)

| Claim | Cite | File |
|---|---|---|
| "How much bandwidth is enough" — application thresholds | **Clark & Wedeman 2022** | `04-…/clark-wedeman-2022-…` |
| Current broadband definition = 100/20 Mbps, goal 1000/500 | **FCC 2024** (factsheet + §706 report) | `04-…/fcc-2024-…` |
| Speed alone ≠ good experience | Stocker & Whalley 2018 | `04-…/stocker-whalley-2018-…` |

---

## The 16 papers, by folder

- **01-ookla/** — Paul 2021 · Lee 2023 (bias-correction) · Caldas/OECD 2023 · 'Ofa/ESCAP 2021
- **02-ndt7-mlab/** — Gill 2022 (platform) · Lübben-Misfeld 2022 (Germany EDA) · Deng 2021 (ISP compare)
- **03-cross-platform/** — MacMillan 2023 (Ookla vs NDT7) · Lipphardt 2025 (M-Lab vs Cloudflare)
- **04-benchmarks-theory/** — Clark-Wedeman 2022 · Stocker-Whalley 2018 · FCC 2024 (×2)
- **05-thailand-context/** — Setthasuravich 2024 (sub-district) · Denfanapapol 2024 (province) · Sridhar 2007

## Still missing (not blocking)

- Röller & Waverman 2001 (AER, paywalled) — already cited in draft; Sridhar 2007 covers the same point.
- ITU Facts & Figures 2024 — cited in draft; it's an access/affordability source, **not** a speed
  threshold. Don't use it to justify a "good/bad" speed cutoff — use FCC / Clark-Wedeman for that.
