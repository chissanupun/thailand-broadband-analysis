"""สร้างรูปชุด poster — ข้อมูลเดิม ตัวหนังสือใหญ่ขึ้น

    python scripts/build_poster_figs.py

ปัญหาที่แก้: รูปในกราฟชุดเดิมตั้ง font ไว้สำหรับหน้ากระดาษ A4 สองคอลัมน์
พอเอาไปวางบนโปสเตอร์ A1 กว้างคอลัมน์ละ ~13 ซม. ตัวเลขแกนเล็กจนอ่านไม่ออก

วิธี: ไม่แตะสคริปต์เดิมเลย แค่ตั้ง rcParams ให้ใหญ่ขึ้น แล้ว exec สคริปต์เดิม
โดย redirect savefig ไปที่ outputs/poster_figs/ รูปต้นฉบับใน outputs/ ไม่ถูกทับ
(paper.tex กับ abstract.tex ยังชี้ของเดิมอยู่ ต้องคงขนาดเดิมไว้)

output: outputs/poster_figs/*.png
"""
import runpy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / 'outputs' / 'poster_figs'
OUT.mkdir(parents=True, exist_ok=True)

# A1 poster, ~13 cm per column. Everything one step up from the paper defaults.
plt.rcParams.update({
    'font.size': 17,
    'axes.titlesize': 20,
    'axes.labelsize': 17,
    'xtick.labelsize': 15,
    'ytick.labelsize': 15,
    'legend.fontsize': 15,
    'figure.titlesize': 21,
    'lines.linewidth': 2.2,
    'lines.markersize': 7,
    'axes.linewidth': 1.3,
    'xtick.major.width': 1.3,
    'ytick.major.width': 1.3,
    'savefig.dpi': 200,
    'figure.dpi': 200,
})

_orig = Figure.savefig
written = []


def savefig(self, fname, *a, **kw):
    dest = OUT / Path(str(fname)).name
    kw['dpi'] = 200
    kw.setdefault('bbox_inches', 'tight')
    written.append(dest.name)
    return _orig(self, dest, *a, **kw)


Figure.savefig = savefig

for script in ('build_cross_country_figs_8c.py', 'build_extra_figs_8c.py', 'build_app_success_figs.py'):
    runpy.run_path(str(ROOT / script), run_name='__main__')
    plt.close('all')

Figure.savefig = _orig
print(f'{len(written)} figures -> {OUT}')
for n in sorted(written):
    print(' ', n)
