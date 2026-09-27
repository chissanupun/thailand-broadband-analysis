# AINTEC 2026 — poster track

## The poster lives in Figma. There is no LaTeX poster any more.

**https://www.figma.com/design/lEoSvJRQN6l3gaodEW3M6Q** — "AINTEC 2026 Poster — SEA Broadband", frame `3:2`.

The tikzposter build (`poster.tex`, `poster_v_dense.tex`, `poster.pdf`, `plan.md`, `assets/`) was deleted on 2026-09-24. It is in git history at **`b3bcd9a`** if it is ever needed; do not resurrect it in parallel with the Figma file, because two sources of the same poster is how the number drift in `poster_content.md` §0 happened the first time.

Frame is 1684×2384 px = **A1 at 72 dpi**. The frame carries export settings for **PNG @4×** (A1 at 288 dpi) and **PDF**. AINTEC requires A1 for the final poster.

## What is due when

Main abstract Overleaf project: **https://www.overleaf.com/project/6ab8f2d64f3863fedb8de8d2** — "AINTEC 2026 - Main Poster Abstract", created 2026-09-27 using the supplied ACM template. Current author order: Sukumal Kitisin, Chissanupun Athiwarikanon, Kunanont Malayanont, Pakkapon Pattanakul. Compiled PDF: two content pages, followed by a references-only third page.

| | What | When |
|---|---|---|
| **Now** | `main/abstract.tex` → `abstract.pdf`, ≤2 double-column ACM pages, non-anonymous | **2026-09-28 8pm EDT = 2026-09-29 07:00 Thai** (live HotCRP portal; ignore the CFP page's generic 23:59 AoE) |
| **Now** | The abstract text field on HotCRP — text in `abstract.md` | same |
| If accepted | The A1 poster, exported from Figma | notification **2026-10-09** |
| If accepted | 3-minute lightning talk (~400 words), not yet written | conference |

The CFP asks for an **abstract report**, not the designed poster. An earlier note in this repo said the opposite; the CFP page is the authority.

## Figures

Charts in the Figma file are **uploaded copies, not links**. Regenerating a figure in this repo does not update the poster — re-upload it.

- `scripts/build_poster_figs.py` → `outputs/poster_figs/` — poster type scale (font 17, ticks 15, dpi 200). **These are what the Figma poster uses.**
- `outputs/**` originals stay at paper type scale, because `docs/paper/paper.tex` and `main/abstract.tex` reference them.

The poster uses `05_fixed_vs_mobile.png` and `07_growth_trajectory.png` rather than the old `image4`/`image6`: same data, but script-generated from `data/exports` and therefore reproducible, which the `imageN.png` notebook exports are not.

## The other poster

The ISP / market-structure material was split into a second poster owned by **Kunanont Malayanont** on the advisor's instruction. Its content bank is `isp/content.md`. Nothing operator-layer belongs on this poster.

## Still to verify before printing

- Wording and numbers on the Figma sheet against `poster_content.md` — that file holds the provenance for every figure quoted.
- The 8-country paper prose vs the 9-country regenerated numbers (`poster_content.md` §0 item 2) is **still undecided**. The Figma poster uses the 9-country set throughout.
- Zoom test at real print size.
