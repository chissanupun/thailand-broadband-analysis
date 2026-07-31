# -*- coding: utf-8 -*-
"""
RQ4 — congestion-plausibility flags ต่อ country x network_type

    python scripts/peakhour_flags.py

ปัญหาที่แก้: notebook เดิมสร้าง bot diagnostic ไว้อธิบายเวียดนาม (busy hour 11:00 ไม่ใช่เย็น)
แต่ยังรายงานเวียดนามปนใน summary ทุกตารางโดยไม่มีธง -> คนอ่านต้องมาสังเกตเอง

ที่นี่เปลี่ยนเป็น "เกณฑ์" ที่ตรวจซ้ำได้ ไม่ใช่การตัดประเทศทิ้งด้วยมือ
congestion ที่เกิดจาก demand จริงต้องเข้าเกณฑ์พร้อมกัน 3 ข้อ:

  1. busy hour อยู่ช่วงเย็น (18-23 local)   -> ตรงพฤติกรรมคนใช้จริง (L&M)
  2. throughput ตกตอน busy (degr < 1)       -> มี congestion
  3. RTT ขึ้นตอน busy (rtt_ratio > 1)        -> ยืนยันด้วยตัวแปรอิสระอีกตัว

ข้อ 3 สำคัญ: throughput ตกอย่างเดียวอธิบายได้หลายอย่าง (mix ของผู้ใช้เปลี่ยน, ISP เปลี่ยน)
แต่ถ้า RTT ขึ้นพร้อมกันด้วย = คิวที่ bottleneck = congestion จริง

**ทุกค่าใช้ weekday เท่านั้น** (is_weekend = False) ให้ตรงกับ notebook
(pool เสาร์อาทิตย์เข้าไปด้วยจะได้ตัวเลขต่างออกไป เช่น SG cellular 0.703 แทน 0.729)

output: data/exports/ndt7_peakhour_flags.csv
"""
import os
import glob
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORTS = os.path.join(ROOT, "data", "exports")

BUSY = [19, 20, 21, 22]     # หน้าต่าง busy คงที่ (L&M เยอรมนี 20-22)
OFF = [3, 4, 5]             # หน้าต่างเงียบคงที่ กลางดึก
EVENING = range(18, 24)     # ช่วงที่ถือว่าเป็น "เย็น" สำหรับเกณฑ์ข้อ 1


def wavg(g, hours, col):
    """ค่าเฉลี่ยถ่วง n_tests ของสถิติรายชั่วโมงในหน้าต่าง hours

    หมายเหตุ: นี่คือ *ค่าเฉลี่ยถ่วงน้ำหนักของ median รายชั่วโมง* ไม่ใช่ median ของทั้งหน้าต่าง
    (quantile รวมกันแบบนั้นไม่ได้) -> เวลาเขียนเปเปอร์ต้องเรียกชื่อให้ตรง
    """
    s = g.loc[hours]
    m = s[col].notna() & s["n_tests"].notna()
    return np.average(s.loc[m, col], weights=s.loc[m, "n_tests"]) if m.any() else np.nan


def analyse(path):
    country = os.path.basename(path)[len("ndt7_peakhour_"):-len(".csv")]
    d = pd.read_csv(path)
    out = []
    for nt in ("broadband", "cellular"):
        s = d[(d.network_type == nt) & (d.type == "download") & (~d.is_weekend)]
        if s.empty:
            continue
        g = s.set_index("hour_local").reindex(range(24))
        busy_hr = int(g["n_tests"].idxmax())
        degr = wavg(g, BUSY, "med_mbps") / wavg(g, OFF, "med_mbps")
        degr_p10 = wavg(g, BUSY, "p10_mbps") / wavg(g, OFF, "p10_mbps")
        rtt_ratio = wavg(g, BUSY, "med_rtt") / wavg(g, OFF, "med_rtt")
        evening_share = 100 * g.loc[list(EVENING), "n_tests"].sum() / g["n_tests"].sum()

        c1 = busy_hr in EVENING
        c2 = degr < 1
        c3 = rtt_ratio > 1
        if c1 and c2 and c3:
            verdict = "congestion"
        elif c1 and not (c2 and c3):
            verdict = "no-congestion"        # ช่วงเย็นคนใช้เยอะจริง แต่เครือข่ายไม่ตก
        else:
            verdict = "implausible-timing"   # busy hour ไม่ใช่เย็น -> ไม่ใช่ demand ของคน

        out.append(dict(
            country=country, network_type=nt, busy_hour=busy_hr,
            evening_share_pct=round(evening_share, 1),
            degr_med=round(degr, 3), degr_p10=round(degr_p10, 3),
            rtt_ratio=round(rtt_ratio, 3),
            evening_peak=c1, throughput_falls=c2, rtt_rises=c3,
            verdict=verdict,
            use_for_congestion_claim=(verdict == "congestion"),
        ))
    return out


def main():
    rows = []
    for p in sorted(glob.glob(os.path.join(EXPORTS, "ndt7_peakhour_*.csv"))):
        if os.path.basename(p).startswith("ndt7_peakhour_capital_"):
            continue
        if os.path.basename(p) == "ndt7_peakhour_flags.csv":
            continue
        rows += analyse(p)

    df = pd.DataFrame(rows).sort_values(["network_type", "degr_med"])
    out = os.path.join(EXPORTS, "ndt7_peakhour_flags.csv")
    df.to_csv(out, index=False)

    for nt in ("cellular", "broadband"):
        sub = df[df.network_type == nt]
        print(f"\n=== {nt} (weekday download) ===")
        print(sub[["country", "busy_hour", "evening_share_pct", "degr_med",
                   "degr_p10", "rtt_ratio", "verdict"]].to_string(index=False))

    bad = df[~df.use_for_congestion_claim]
    print(f"\n{len(df) - len(bad)}/{len(df)} country-segments qualify as demand-driven congestion.")
    if len(bad):
        print("EXCLUDED from congestion claims:")
        for _, r in bad.iterrows():
            why = []
            if not r.evening_peak:
                why.append(f"busy hour {r.busy_hour:02d}:00 not evening")
            if not r.throughput_falls:
                why.append(f"throughput rises (degr={r.degr_med})")
            if not r.rtt_rises:
                why.append(f"RTT falls (ratio={r.rtt_ratio})")
            print(f"  {r.country:12s} {r.network_type:10s} [{r.verdict}] — {'; '.join(why)}")
    print(f"\nsaved -> {out}")


if __name__ == "__main__":
    main()
