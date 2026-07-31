# Code review — RQ3 peak-hour delivery (commit 06ab993)

Reviewed 2026-07-30: `scripts/build_peakhour.py`, `notebooks/comparison/rq3_peakhour.ipynb`.

**Verdict: sound work, results are real, safe to build the paper on.** Numbers reproduce independently.
Six issues to fix, one of which affects how the paper must describe the method.

Reproduction check — recomputed from raw exports rather than trusting the delivered summary:

| | delivered | recomputed |
|---|---|---|
| Thailand broadband busy/off | 0.893 | 0.889 |
| Thailand cellular busy/off | 0.556 | 0.561 |

Differences are rounding. The pipeline does what it says.

**What is done well:** correct UTC→local conversion with per-country offsets including Myanmar's +6:30;
hosting excluded; `throughput > 0` filter; the NDT7 4,294,967 ms RTT sentinel filtered rather than
clamped; DuckDB memory config appropriate for the 367M-row countries; weekday/weekend split; three
independent degradation measures; a bot diagnostic drawn from Lübben & Misfeld §3.2; and a
capital-vs-rest split. The busy hour resolves to 20:00–21:00 local in most countries, which is a human
evening peak and good evidence the data reflects real usage.

---

## 1. HIGH — `wmean` computes a weighted mean of medians, not a median

`rq3_peakhour.ipynb` cell 2:

```python
def wmean(country, nt, hours, col='med_mbps', typ='download'):
    p = prof(country, nt, typ).loc[hours].dropna(subset=[col,'n_tests'])
    return np.average(p[col], weights=p['n_tests'])
```

This averages four hourly *medians*, weighted by test count. A weighted mean of medians is not the
median of the pooled busy-hour distribution — quantiles do not compose that way. The quantity is a
perfectly reasonable summary and every number in the summary CSV is internally consistent, but it
**cannot be called "busy-hour median download"** in the paper, which is what the figure captions
currently imply.

Two ways out, either acceptable:
- Describe it accurately: "test-weighted mean of hourly median throughput across the busy window."
- Or compute the true pooled quantile in SQL over the whole 19–22h window instead of per hour.

This is the one issue that a reviewer familiar with quantiles will catch, so fix the wording at minimum.

## 2. HIGH — Vietnam fails the notebook's own plausibility check but is still reported

> **FIXED 2026-07-30** — `scripts/peakhour_flags.py` → `data/exports/ndt7_peakhour_flags.csv`.
> Rather than dropping Vietnam by hand, a country-segment now has to satisfy three conditions to be
> called demand-driven congestion: evening busy hour (18–23), throughput falls, **and RTT rises**.
> The third is what makes it a test rather than a description — throughput falling alone is explicable
> by a shifting user or ISP mix, but throughput down together with latency up is queueing at a
> bottleneck. Result: **13 of 18 country-segments qualify.** Excluded are Vietnam (both segments,
> busy hour 10–11:00, and RTT *falls* on broadband at 0.584), Cambodia broadband (busy hour 12:00),
> and Singapore (both segments — no congestion at all, which is a finding rather than a fault).
> Laos is *not* excluded: its apparent midday broadband peak was an artefact of pooling weekends into
> my own earlier check; weekday-only puts it at 20:00. The notebook still needs to read this file so
> its charts carry the flag.

The notebook builds a bot diagnostic explicitly to explain Vietnam's odd 11:00 peak, then includes
Vietnam unflagged in every summary table and chart. Vietnam shows three independent warning signs:

- busy hour is 10:00–11:00, not evening, in both segments
- lowest evening concentration of any country — 22.9% of broadband tests in 18–23h, below what a flat
  distribution would give
- **median RTT falls at the busy hour (ratio 0.54)** — the opposite of congestion

Whatever drives Vietnam's diurnal profile, it is not consumer demand. Its degradation ratio (0.650
broadband) should not be presented as congestion evidence. Cambodia and Laos have midday *broadband*
peaks too (12:00, 13:00), though their cellular peaks are properly evening and their cellular
degradation is the most severe in the set — so those two are usable on the cellular side.

Add an explicit exclusion or flag column rather than leaving the reader to notice.

## 3. MEDIUM — p10 is the least reliable statistic and carries the paper's most dramatic number

> **FIXED 2026-07-30** — `build_peakhour.py` now selects the quantile function per country
> (`EXACT_Q = {"kh","la","mm"}` → `quantile_cont`; the large countries keep `approx_quantile` for
> memory). Re-running those three changed p10 by up to **23.5% in Laos**, 9.7% in Myanmar, 5.6% in
> Cambodia — larger than the 7.94% my spot-check had suggested. Row counts are byte-identical
> before and after, so only the quantile columns moved. Two abstract figures were wrong as a result
> and have been corrected: the mobile range 0.23–0.70 → **0.23–0.73**, and the p10 minimum
> 0.11 → **0.12**.

Validated `approx_quantile` against exact `quantile_cont` on Laos:

| | max error |
|---|---|
| median | **0.80%** |
| p10 | **7.94%** |

The script's docstring claims ~1%, which holds for the median but not the tail. On the large countries
(≥10⁵ tests per cell) t-digest error will be far smaller, but Laos, Cambodia, and Myanmar are thin.

Laos is the worst: **152 of 192 cells hold under 1,000 tests, minimum 69.**

| country | min cell | median cell | cells <1000 |
|---|---|---|---|
| laos | 69 | 462 | 152 |
| myanmar | 231 | 5,306 | 19 |
| cambodia | 670 | 3,085 | 14 |
| vietnam | 1,121 | 28,833 | 0 |
| others | ≥3,118 | ≥26,772 | 0 |

**Cheap fix:** the kh/la/mm parquets are 32 MB, 5.6 MB, and 95 MB. Recompute those three with exact
`quantile_cont` instead of `approx_quantile` — seconds of work, and it removes the concern from the
abstract's "0.11" figure (Cambodia cellular p10) entirely.

## 4. MEDIUM — `emp_window` compares single hours with no sample guard

```python
bh = int(p['n_tests'].idxmax())
oh = int(night.idxmin())
return bh, oh, p.loc[bh,'med_mbps'] / p.loc[oh,'med_mbps']
```

One hour against one hour, no minimum-n check. For Laos the quiet hour may rest on ~69 tests. The
fixed-window measure (four hours vs three) is far more stable — prefer it for any headline claim, and
either widen this to a window or report n alongside each ratio.

## 5. LOW — busy hour is defined inconsistently between the summary and the analysis

`vol()` pools both network types *and* weekday+weekend to pick the busy hour reported in
`rq3_peakhour_summary.csv`, while degradation uses weekday-only per-segment profiles. For Thailand:

- pooled: 20:00 · weekday-only: 20:00 · weekday broadband only: **21:00**

Small, but the summary's `busy_hour` column and the `degr_emp` column are computed off different
definitions. Pick one.

## 6. LOW — the bot diagnostic double-counts IPs

`n_ips` comes from `approx_count_distinct` per cell. Summing it across hours counts an IP once per hour
it appears, so "tests per unique IP" computed that way is not a true ratio. Fine as a relative
diagnostic — and the conclusion holds, values are 1.4–6.3 with peak/median ratios ≤1.51, no automation
spikes — but do not quote it as an absolute figure.

## 7. Known, already flagged by the author: Indonesia timezone

Indonesia spans UTC+7/+8/+9; the script applies WIB (+7) nationally. The author documented this as a
limitation, which is the right call for now. Note it biases Indonesia's busy-hour placement
specifically. A per-province offset is possible since the `province` column exists, if it matters.

---

## What to do next, in order

### Blocking the 7 August full-paper deadline

1. **Write RQ3 into Sections 4–9.** Currently only the Abstract and two status notes mention it. This
   is the largest remaining task and it *changes* Section 8 rather than extending it: the Discussion
   currently argues the residual is mainly market structure because province-quarter averages are the
   wrong grain, and it explicitly claims tail behaviour is unmeasurable here. Both need rewriting —
   the tail is measurable and it is the worst signal in the dataset.
2. ~~Verify the Lübben & Misfeld (2022) citation.~~ **DONE 2026-07-30.** Retrieved and checked: all four
   thresholds match their Table 5 exactly. The citation itself was wrong twice over (initial "T." should be
   "N."; the title was a placeholder that does not exist) — both fixed in `paper_draft.md` and
   `citations.md`. Bonus: the paper is an M-Lab NDT study of Germany whose §4.2 busy-hour method is the
   one RQ3 already follows, so it now anchors RQ1 and RQ3 both.
3. **Fix the two bad citations in §1** — the unverifiable 64.65% ETDA figure, and the NBTC complaint
   numbers attributed to an article that does not contain them. Details in `docs/abstract_submission.md`.
4. **Scope the Thailand-vs-Vietnam claim.** §5.1 says Thailand's level stays second-highest behind
   Singapore. True through Q4 2025, but Ookla's live index (June 2026) now has Vietnam #8 at 307.36
   above Thailand #12 at 290.47. Add "within our study period" — our own catch-up finding predicted
   this, so it strengthens RQ2 rather than weakening it.
5. **Cut for length.** Was ~30% over at 9,800 words before RQ3; adding a fourth results section makes
   it worse. Candidates ranked in `paper_draft.md` Appendix A.1.
6. **Port to `docs/paper.tex`** — still a skeleton with the old Thailand-only title — and **anonymise
   it**, since AINTEC submission is anonymous.

### Code fixes (fast, do before writing RQ3 up)

7. Exact quantiles for kh/la/mm (issue 3) — minutes.
8. Flag or exclude Vietnam in the peak-hour outputs (issue 2).
9. Fix the method wording for `wmean`, or compute pooled quantiles (issue 1).
10. Apply the verified Vietnam province-name join fix in `rq_stats_crosscountry.ipynb` so §7.3's
    ρ = 0.967 matches the code (currently the draft is ahead of the notebook).
11. ~~Apply province-clustered standard errors as the headline OLS.~~ **DONE** — both models now use
    `cov_type='cluster'` grouped by province. Coefficients unchanged (clustering affects only standard
    errors); `log_gdp` SE 1.30 → 3.42, `log_density` 0.59 → 1.10. Every sign and significance holds.
12. ~~Rename the peak-hour notebook and figures.~~ **NOT NEEDED — the paper was renumbered instead.**
    Peak-hour is **RQ3** and ISP is **RQ4**, which is what the filenames already said. Renaming would
    have meant a 45-file swap plus 23 internal path rewrites plus regenerating every figure, against
    roughly fifty text edits in three documents. The resulting order is also the better one: RQ2
    measures change across years, RQ3 within the day, and RQ4 closes on market structure, the most
    novel claim. **No code was touched.**

### Admin

13. Author list — the peak-hour work is now a headline result, so this decision is more pressing.
14. PC conflicts on the HotCRP form — three Thai PC members are listed; confirm none is an advisor or
    recent collaborator.
15. `docs/Process.md` still carries the old RQ numbering and an unticked Sprint 2 checklist.
