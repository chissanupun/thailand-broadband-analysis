# Ookla vs NDT7 Comparison Research — Thailand Open Dataset

## แนวคิด

เปรียบเทียบ Ookla Speedtest Intelligence กับ M-Lab NDT7 ในบริบทไทย โดยใช้ open dataset ทั้งคู่ ไม่ต้อง deploy hardware — ต่างจาก MacMillan et al. [3] ที่ใช้ paired test จาก Raspberry Pi 126 ครัวเรือนใน US

---

## สิ่งที่มีอยู่แล้ว

- **Ookla** — tile-level (~610m) fixed broadband, 11 ไตรมาส (2023Q1–2025Q3), 77 จังหวัด [2]
- **NDT7** — raw per-test, 30.6M records, 6 ไตรมาส (2023Q4–2025Q1), broadband + cellular [2]
- **Netrics dataset** — open longitudinal speed test data จาก University of Chicago deployment [1]

---

## Methodology ที่จะใช้

### 1. Spatial Matching
- Assign NDT7 test ทุกรายการเป็น zoom-16 tile ด้วย Web Mercator projection
- Match กับ Ookla tile ด้วย `tile_id` เดียวกัน
- Aggregate ทั้งคู่เป็น province × quarter

### 2. Temporal Alignment
- ใช้ช่วงเวลาที่ overlap: **2023Q4 – 2025Q1** (6 quarters)
- Aggregate ทั้งคู่ด้วย quarter boundary เดียวกัน

### 3. Statistical Comparison
- **Paired comparison** ระดับ province × quarter (ไม่ใช่ individual test)
- Wilcoxon signed-rank test หรือ paired t-test
- Effect size: Cohen's d
- Control: ISP tier, region, population density

### 4. Explanatory Analysis
- Province ไหนที่ gap ใหญ่ผิดปกติ → อธิบายด้วย latency, coverage density, ISP
- อ้าง MacMillan et al. [3]: high latency → NDT7 underreport 12–56%, อธิบาย gap ที่พบ

---

## ข้อจำกัดที่ต้อง declare

| ข้อจำกัด | เหตุผล |
|---|---|
| ไม่มี paired test | คนละ user, คนละเวลา, คนละ ISP |
| Ookla = pre-aggregated tile | ไม่เห็น raw per-test variance |
| Selection bias ต่างกัน | Ookla opt-in app users ≠ NDT7 browser users |
| NDT7 latency sensitivity | ตาม [3]: RTT >200ms → underreport มาก |
| NDT7 upload bug (historical) | ก่อน fix: AppInfo overestimate <10 Mbps — ใช้ TCPInfo จาก BigQuery |

---

## Contribution ที่ novel

- [ ] **Thailand-specific gap analysis** — Ookla vs NDT7 per province (ไม่เคยมีใครทำ)
- [ ] **Tier × gap interaction** — จังหวัด Tier 1 กับ Tier 4 gap ต่างกันไหม?
- [ ] **ISP-level comparison** — NDT7 มี ISP field, Ookla ไม่มี → cross-validate
- [ ] **Coverage bias** — จังหวัดที่ NDT7 test น้อย vs Ookla test มาก → ใครไม่ถูก represent

---

## ไม่สามารถ claim ได้

- NDT7 หรือ Ookla "แม่นกว่า" — ไม่มี ground truth
- Gap เกิดจาก network จริง 100% — อาจเป็น methodology difference ตาม [3]

---

## References

[1] Internet Innovation. *Netrics Data — Open Longitudinal Broadband Measurement Dataset.*
University of Chicago. https://github.com/internet-innovation/netrics-data

[2] Chissanupun A. *Thailand Broadband Analysis 2023–2025.*
Internet Measurement Project, CNC Data Science Lab.
file:///home/chissanupun/Desktop/code/lab/cnc/data-science/internet-measurement/outputs/slides.html

[3] MacMillan K., Mangla T., Saxon J., Marwell N.P., Feamster N. (2023).
*A Comparative Analysis of Ookla Speedtest and Measurement Labs Network Diagnostic Test (NDT7).*
Proc. ACM Meas. Anal. Comput. Syst., Vol. 7, No. 1, Article 19.
https://dl.acm.org/doi/epdf/10.1145/3579448
