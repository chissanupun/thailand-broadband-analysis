# -*- coding: utf-8 -*-
"""
รัน notebook แล้วเซฟ output กลับเข้าไฟล์เดิม

    python scripts/run_nb.py notebooks/ndt7/main/laos_ndt7_prep.ipynb [...]

- รันด้วย cwd = โฟลเดอร์ของ notebook (path ใน notebook เป็น relative)
- บังคับใช้ kernel `python3` เพราะ notebook บางเล่มระบุ `datasci` ซึ่งไม่ได้ลงทะเบียนบนเครื่องนี้
- ถ้า cell ไหน error จะหยุดเล่มนั้น แล้วรายงาน ไม่ลามไปเล่มอื่น
"""
import sys, os, time, traceback
import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

TIMEOUT = int(os.environ.get("NB_TIMEOUT", "7200"))   # ต่อ cell (วินาที)
KERNEL = os.environ.get("NB_KERNEL", "python3")


def run(path):
    path = os.path.abspath(path)
    d = os.path.dirname(path)
    name = os.path.basename(path)
    nb = nbformat.read(path, as_version=4)
    nb.metadata.setdefault("kernelspec", {})
    nb.metadata["kernelspec"]["name"] = KERNEL

    t0 = time.time()
    client = NotebookClient(nb, timeout=TIMEOUT, kernel_name=KERNEL,
                            resources={"metadata": {"path": d}},
                            allow_errors=False)
    try:
        client.execute()
        ok, err = True, None
    except CellExecutionError as e:
        ok, err = False, str(e)
    except Exception as e:
        ok, err = False, f"{type(e).__name__}: {e}"

    nbformat.write(nb, path)          # เซฟผลไม่ว่าจะสำเร็จหรือไม่ จะได้เห็นว่าตายตรงไหน
    dt = time.time() - t0
    print(f"{'OK  ' if ok else 'FAIL'} {name:32s} {dt/60:6.1f} นาที")
    if not ok:
        tail = "\n".join(err.strip().splitlines()[-12:])
        print("      " + tail.replace("\n", "\n      "))
    return ok


if __name__ == "__main__":
    targets = sys.argv[1:]
    if not targets:
        print(__doc__)
        sys.exit(1)
    results = [(t, run(t)) for t in targets]
    bad = [t for t, ok in results if not ok]
    print(f"\nสำเร็จ {len(results)-len(bad)}/{len(results)}")
    if bad:
        print("ล้มเหลว:")
        for b in bad:
            print("  -", b)
    sys.exit(1 if bad else 0)
