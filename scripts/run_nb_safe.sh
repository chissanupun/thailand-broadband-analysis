#!/usr/bin/env bash
# รัน run_nb.py ใน cgroup scope ที่จำกัด RAM ไว้ —
# เครื่องนี้มี RAM แค่ 7.5GB, notebook ID/PH (367M/262M แถว) เคยกิน RAM จน
# system-wide OOM-killer เลือกฆ่า process มั่ว (เคยลากเทอร์มินัลตายไปด้วย)
#
# ต่างจากการตั้ง memory_limit ใน duckdb เอง: ตรงนี้คุมทั้ง process รวม
# pandas/kernel overhead ด้วย และถ้าชนลิมิต cgroup จะฆ่าแค่ scope นี้
# ไม่ลามไปฆ่า process อื่นทั้งเครื่อง (เทอร์มินัลไม่ตาย)
#
# ใช้:
#   scripts/run_nb_safe.sh notebooks/ndt7/main/indonesia_ndt7_prep.ipynb
#   NB_MEM_MAX=3G scripts/run_nb_safe.sh notebooks/ndt7/main/philippines_ndt7_prep.ipynb
set -euo pipefail

MEM_MAX="${NB_MEM_MAX:-5G}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PY="$PROJECT_DIR/datasci/bin/python"   # venv โปรเจกต์ — มี duckdb/nbformat/nbclient

exec systemd-run --user --scope \
    -p MemoryMax="$MEM_MAX" \
    -p MemorySwapMax=1G \
    -- "$PY" "$SCRIPT_DIR/run_nb.py" "$@"
