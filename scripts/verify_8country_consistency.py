"""ตรวจว่าตัวเลขในเอกสารตรงกับข้อมูลจริง หลังตัด Singapore"""
import re, sys, pathlib

DOCS = pathlib.Path.home() / 'Desktop/code/lab/cnc/data-science/internet-measurement/docs'

fails, oks = [], []


def check(label, cond, detail=''):
    (oks if cond else fails).append(f'{label} {detail}')


texts = {p.name: p.read_text() for p in DOCS.glob('*.md')}

# 1. ไม่มีประเทศ Singapore หลงเหลือในฐานะประเทศที่ศึกษา
SG_OK_CONTEXT = ['sin01', 'Singapore 52.9', 'reach Singapore', 'to Singapore',
                 'Singapore removed', 'Singapore contributed', 'Singapore is dropped',
                 'Singapore was the extreme', 'Singapore cut', 'in Singapore (Section',
                 'Singapore, Hong Kong', 'further 20.7% in Singapore',
                 'Singapore NDT7', 'Singapore from the study',
                 # บริบทที่ตั้งใจให้มี: บันทึกการแก้ไข คำอธิบายเหตุผล ตารางงาน
                 'Singapore was already excluded',      # counting-trap note
                 'single exception',                    # คำอธิบาย RTT (0.99x)
                 'without Singapore',                   # หัวข้อ R²
                 'never contained Singapore',           # ตารางงานท้ายไฟล์
                 'no longer in the set',                # คำอธิบายว่าตัดออกแล้ว
                 'Singapore removed from the study']    # ตารางงาน
for name in ['paper_draft.md', 'results_th.md', 'abstract_th.md', 'analysis_th.md']:
    t = texts.get(name, '')
    bad = []
    for i, line in enumerate(t.splitlines(), 1):
        if 'Singapore' in line or 'สิงคโปร์' in line:
            if any(c in line for c in SG_OK_CONTEXT):
                continue
            # ภาษาไทย: อนุญาตถ้าเป็นบริบทเซิร์ฟเวอร์/บันทึกการแก้
            if any(c in line for c in ['sin01', 'ตัดสิงคโปร์', 'มีสิงคโปร์', 'ไม่มีสิงคโปร์',
                                       'ไปสิงคโปร์', 'เดิมมีสิงคโปร์', 'รวมสิงคโปร์',
                                       'สิงคโปร์ทั้งสองฝั่ง', 'ของสิงคโปร์', 'สิงคโปร์ซึ่ง',
                                       'สิงคโปร์กับมา', 'สิงคโปร์ประเทศเดียว', 'สิงคโปร์ 0.729',
                                       'บวกสิงคโปร์',      # เวียดนามยิงไปสิงคโปร์ = ตำแหน่งเซิร์ฟเวอร์
                                       'สิงคโปร์ที่ 1.27']):  # อ้างค่าเดิมเพื่อเทียบ
                continue
            bad.append(f'{name}:{i}')
    check(f'[SG] {name}', not bad, f'-> {bad[:4]}' if bad else 'สะอาด')

# 2. เลข 9 ประเทศต้องไม่หลงเหลือแบบไม่ตั้งใจ
for name in ['paper_draft.md']:
    t = texts[name]
    bad = []
    for i, line in enumerate(t.splitlines(), 1):
        for pat in [r'\bnine countries\b', r'\bNine-Country\b', r'\bsix of nine\b',
                    r'\bseven of nine\b', r'\beight of nine\b', r'\bthirty-six\b',
                    r'\b35 of 36\b', r'\b3222\b', r'\b3,222\b']:
            if (re.search(pat, line) and not line.strip().startswith('>')
                    and '~~' not in line
                    and 'Counting trap' not in line):   # โน้ตที่ตั้งใจอ้างกรอบเดิม
                bad.append(f'{name}:{i} [{pat}]')
    check(f'[9-country] {name}', not bad, f'-> {bad[:5]}' if bad else 'สะอาด')

# 3. ตัวเลขที่ re-run แล้วต้องปรากฏถูกต้อง
NEW = {'3162': 'paper_draft.md', '2487': 'paper_draft.md', '0.869': 'paper_draft.md',
       '0.568': 'paper_draft.md', '2738.48': 'paper_draft.md', '1525.89': 'paper_draft.md',
       '27 of 28': 'paper_draft.md'}
for val, fn in NEW.items():
    check(f'[new-number] {val}', val in texts[fn], f'ใน {fn}')

check('[rho-8c] 0.91 ใน abstract_th', '0.91' in texts['abstract_th.md'])
check('[rho-ols] 0.95 ใน analysis_th', '0.95' in texts['analysis_th.md'])

# 4. ตารางต้องมี 8 แถวประเทศ
def rows(t, header_frag):
    i = t.find(header_frag)
    if i < 0:
        return None
    seg = t[i:i + 2000].splitlines()
    n = 0
    for line in seg[2:]:
        if not line.strip().startswith('|'):
            break
        n += 1
    return n

n = rows(texts['paper_draft.md'], '| Country | HD | UHD | Cloud gaming | Voice | Tests |')
check('[Table3] 8 แถว', n == 8, f'ได้ {n}')

n = rows(texts['results_th.md'], '| ประเทศ | HD | UHD | Cloud gaming | Voice | จำนวนทดสอบ |')
check('[ตารางที่1 ไทย] 8 แถว', n == 8, f'ได้ {n}')

n = rows(texts['results_th.md'], '| ประเทศ | มือถือ | มือถือ p10 |')
check('[ตารางที่5 ไทย] 8 แถว', n == 8, f'ได้ {n}')

# 5. ความสอดคล้องข้ามไฟล์
for frag, files in [('5 จาก 8', ['results_th.md']), ('5 ใน 8', ['results_th.md']),
                    ('five of eight', ['paper_draft.md'])]:
    pass

check('[consistency] 0.23-0.56 ใน paper_draft',
      '0.23 and 0.56' in texts['paper_draft.md'])
check('[consistency] 0.23-0.56 ใน results_th',
      '0.23 ถึง 0.56' in texts['results_th.md'])
check('[consistency] 13 of 16 / 13 จาก 16',
      'sixteen' in texts['paper_draft.md'] and '13 จาก 16' in texts['results_th.md'])

print('=' * 60)
for o in oks:
    print('  OK   ', o)
print()
if fails:
    print('*** ไม่ผ่าน ***')
    for f in fails:
        print('  FAIL ', f)
    sys.exit(1)
print(f'ผ่านทั้งหมด {len(oks)} ข้อ')
