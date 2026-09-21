# AINTEC 2026 Poster — Plan

Fallback track if full paper rejected — poster acceptance still means Taiwan travel. Separate HotCRP site: `aintec2026-poster` (portal: cfp.wide.ad.jp/conferences/aintec2026poster). Reuses paper content, not new research.

## Confirmed facts
- **Deadline: Mon 2026-09-28, 8pm EDT = Tue 2026-09-29, 7am Thai time.**
- **Full paper decision: 22 Sept 2026** — 6-day gap before poster deadline. Submit regardless of paper outcome by 09-28; if paper is accepted later, decide then whether to withdraw the poster.
- **⚠️ Corrected 2026-09-15 (confirmed by user, overrides earlier CFP-text read): the "Submission PDF, max 20.5MB" field wants the actual designed poster PDF, not a text abstract.** The full poster (visual design, charts, layout) is due at this same deadline — no separate "abstract now, poster later" stage. The CFP boilerplate language about "ongoing work, preliminary results" describes the track's general framing, not a lighter submission requirement.
- Abstract text field is separate and still needed (short written abstract, distinct from the poster PDF).
- Not published in proceedings — protects right to submit as full paper elsewhere. Only poster title + author names appear on the conference webpage.
- Venue: Taiwan (National Taiwan University / GIS NTU Convention Center).

## Submission requirements (HotCRP form)
- Title
- **Submission PDF = the actual poster**, max 20.5MB
- Abstract (text field, separate from the poster PDF)
- Authors (anonymous to reviewers) — same as the paper's author list (decided 09-15), names not on disk, enter directly on HotCRP
- PC conflicts checked: Adisorn Lertsinsrubtavee, Kenjiro Cho (IIJ), Kun-Chan Lan (National Cheng Kung University), Marnel Peradilla (De La Salle University) — **confirmed 09-21, none are advisor/co-author, no conflicts.**

## Status
1. ✅ Author list decided (same as paper's)
2. ✅ Draft title + abstract text written — `docs/poster/abstract.md`, needs a title pick/edit
3. ✅ Poster .tex draft built — `docs/poster/poster.tex` (tikzposter, 3-column: universal basics / 12x urban-rural gap / application-tier divergence). **Not yet compiled or reviewed.** Upload to Overleaf to compile — no local LaTeX.
4. ⏳ **Open before submitting:**
   - ✅ **09-21: figure was stale, now fixed.** `build_cross_country_figs_8c.py` silently excluded Singapore from `FILES`/`CAPITALS` — regenerated with Singapore added (capital = Central Region). New numbers close to but not identical to paper text (Singapore 361/394.8 vs paper's 341/376, Bangkok 298.8/276.9 vs 295/244, etc.) — same ranking/direction, different data pull. **Flagged inline in poster.tex — confirm with paper author/อาจารย์ which numbers are current.**
   - ✅ **09-21: QR code added** — `\qrcode` to `github.com/chissanupun/thailand-broadband-analysis` (public repo, verified reachable), needs `qrcode` LaTeX package on Overleaf.
   - ✅ **09-21: author list filled with real names** — Chissanupun Athiwarikanon (chissanupun.a@ku.th), Kunanont Malayanont (kunanont.m@ku.th), Pakkapon Pattanakul (pakkapon.p@ku.th). Briefly tried anonymous (matching `paper.tex`'s `\author{Anonymous}`) to compile and compare — user reviewed the anonymous render and decided real names, no further CFP check needed.
   - Show อาจารย์, zoom-test at real size, outside "10-sec finding" check — needs you, not done here
   - ✅ **09-21: PC conflicts confirmed — none.**

## Draft title/abstract (for the Abstract text field — not the poster PDF)
Built from current `docs/paper/paper.tex` (Introduction/Data Analysis/Conclusion sections — more advanced than earlier vault notes, which still had the old RQ1-4 framing):

**Title options:**
1. "Beyond Speed Rankings: A Nine-Country Measurement Study of Southeast Asia's Application-Layer Digital Divide"
2. "Basic Access Is Universal, Application-Tier Access Isn't: Measuring Broadband in Southeast Asia"

**Abstract (~230 words)** — see chat log 2026-09-15, or regenerate from `paper.tex` §Introduction + §Conclusion (basic connectivity near-universal; fixed broadband urban-rural stratification up to 12×; UHD/cloud-gaming success diverges sharply, tier-one markets vs. <38% in developing markets).

## Phase — Poster design + build (now, not deferred)
- Pick 3 headline findings for 3-column layout: (1) universal basic connectivity (voice/HD ~100%), (2) urban-rural fixed-broadband stratification (up to 12×, invisible in national rankings), (3) application-tier divergence (UHD/cloud gaming: tier-one markets reliable, developing markets <38% success)
- One clean chart per column, pulled/simplified from `outputs/` figures — current 9-country versions, verify not stale 8-country regen
- Headline stat large, 1-2 sentence caption, minimal body text — skim-readable at 2m in 3 min (matches 3-min lightning talk format)
- QR code → paper repo/preprint
- Colorblind-safe palette, consistent style across columns
- Build: LaTeX `beamerposter` on Overleaf (no local LaTeX toolchain)
- Low-fidelity grayscale layout first, then fill content, then one typography/spacing polish pass
- Show อาจารย์ early — structure before polish
- Zoom-test PDF at real print size; one outside "state the finding in 10 sec" test

## Immediate next action
Poster design is now the blocking task, not a deferred nice-to-have — start the low-fidelity layout draft this week, given ~13 days to deadline and content/figures already exist from the paper.

**Created:** 2026-09-15
**Updated:** 2026-09-15 — corrected: submission PDF is the full poster, due at the same 09-28 deadline, not a lighter abstract-only stage.
**Updated:** 2026-09-21 — stale figure fixed (Singapore added back), QR code added, author list filled (real names, confirmed after comparing an anonymous draft), PC conflicts confirmed none, first local compile done (`pdflatex` works locally now, no Overleaf needed). Blocking: show อาจารย์, fix layout bugs found in first compile (title text overflows the header box; page is only ~half full, columns don't stretch to fill).

**Updated:** 2026-09-21 (late) — poster redesigned and compiles locally (`pdflatex poster.tex`, needs `qrcode` + `tikzposter`). Title overflow fixed (parbox), white bg, crimson stat band (990M / 9 / 4 / 16x), 5 charts (01 fixed ranking, voice, 03 capital-vs-national, cloud gaming, UHD), methodology table, QR block. Finding 2 text now quotes regenerated numbers (16x = Singapore capital 361.0 / Myanmar capital 22.0, not paper's 12x). Only 03 + 01 were regenerated; voice/cloud/UHD figures already had all 9 countries. Remaining: show อาจารย์, confirm 16x vs paper's 12x wording, zoom-test at print size.

**Updated:** 2026-09-21 (night) — user said content too thin; rebuilt with 5 findings + motivation/data/mobile/QR blocks, all text quoted from `paper.tex`, extra figures = paper's own `docs/paper/figures/image3/6/7.png`. Fits one A0 page. Dropped: top-5 provinces (image5), voice chart. Caveat: ISP chart (image7) labels are small at poster scale; Finding 2 numbers/16x still differ from paper prose (341/12x).

**Updated:** 2026-09-21 (night) — user will build the poster themselves. Content bank: `poster_content.md`; figures in `assets/`; last poster build kept as `poster_v_dense.tex`. Found: paper Figs 1–2 (image1/2) are 8-country (no Indonesia) yet paper text says nine — source of the 341/12x vs 361/16x mismatch.
