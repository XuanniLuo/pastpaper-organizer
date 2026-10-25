# -*- coding: utf-8 -*-
"""
Build a Cambridge A-Level Physics 9702 **Paper 4 (A2)** question bank, grouped by
topic (12-25), covering 2024, 2025 and 2026. Each topic starts with its syllabus
requirements, followed by every Paper 4 question (oldest paper first), each
stamped with a header strip (paper · Q# · marks · syllabus codes).

Outputs (two separate books):
   9702_Paper4_2024-2026_ByTopic.pdf          — question book
   9702_Paper4_2024-2026_ByTopic_Answers.pdf  — mark-scheme answer key

Usage:
   python build_paper4_by_topic.py
"""
import json
import glob
import os
import re
import html as _html

import pymupdf
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter

W, H = A4                       # 595.27 x 841.89
PAGE_W = 595.0                  # normalise all pages to A4 width
NAVY = HexColor('#1f2a44')
GOLD = HexColor('#c9a24b')
GREY = HexColor('#5a6470')
INK = HexColor('#262626')

# ---------------------------------------------------------------------------
# fonts
# ---------------------------------------------------------------------------
try:
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
    CN = 'STSong-Light'
except Exception:
    CN = 'Helvetica'

try:
    import matplotlib
    _MT = os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data', 'fonts', 'ttf')
    pdfmetrics.registerFont(TTFont('DejaVu', os.path.join(_MT, 'DejaVuSans.ttf')))
    pdfmetrics.registerFont(TTFont('DejaVu-Bold', os.path.join(_MT, 'DejaVuSans-Bold.ttf')))
    MATH_FONT = 'DejaVu'
    MATH_FONT_B = 'DejaVu-Bold'
    DEJAVU_TTF = os.path.join(_MT, 'DejaVuSans.ttf')
    DEJAVU_BOLD_TTF = os.path.join(_MT, 'DejaVuSans-Bold.ttf')
except Exception:
    MATH_FONT = CN
    MATH_FONT_B = CN
    DEJAVU_TTF = None
    DEJAVU_BOLD_TTF = None

# ---------------------------------------------------------------------------
# topic titles (9702 A2, sections 12-25)
# ---------------------------------------------------------------------------
TOPICS = {
    12: 'Motion in a circle',
    13: 'Gravitational fields',
    14: 'Temperature',
    15: 'Ideal gases',
    16: 'Thermodynamics',
    17: 'Oscillations',
    18: 'Electric fields',
    19: 'Capacitance',
    20: 'Magnetic fields',
    21: 'Alternating currents',
    22: 'Quantum physics',
    23: 'Nuclear physics',
    24: 'Medical physics',
    25: 'Astronomy and cosmology',
}

DATA_DIRS = ['data2024', '_work/data2025', 'data2026']
SYLLABUS_PATH = 'data2024/syllabus_codes_a2_2026.txt'   # 2025-2027 syllabus (current)

# ---------------------------------------------------------------------------
# symbol / text cleaning
# ---------------------------------------------------------------------------
SYMBOL_MAP = {
    '×': '×', '÷': '÷', '•': '•',
    'Δ': 'Δ', 'θ': 'θ', 'λ': 'λ', 'ρ': 'ρ', 'μ': 'μ',
    'Ω': 'Ω', 'π': 'π', 'α': 'α', 'β': 'β', 'γ': 'γ',
    '∝': '∝', '°': '°', '±': '±', '≥': '≥', '≤': '≤',
}


def fix_symbols(text):
    # strip any PDF-Symbol private-use characters (U+F0xx) back to normal
    text = re.sub(r'[-]', '', text)
    text = re.sub(r'[   ]', ' ', text)   # thin spaces -> space
    text = re.sub(r'[ \t]+', ' ', text).strip()
    return text


def html_to_text(s):
    s = re.sub(r'<br\s*/?>', '\n', s, flags=re.I)
    s = re.sub(r'<[^>]+>', '', s)
    s = _html.unescape(s)
    return fix_symbols(s)


# ---------------------------------------------------------------------------
# data loading
# ---------------------------------------------------------------------------
def load_questions():
    qs = []
    for pat in ['data2024/9702_*qp_4*.json',
                '_work/data2025/9702_*qp_4*.json',
                'data2026/9702_*qp_4*.json']:
        for p in sorted(glob.glob(pat)):
            d = json.load(open(p, encoding='utf-8'))
            for q in d['questions']:
                q = dict(q)
                q['_paper'] = d['paper']
                q['_paper_full'] = d.get('paper_full', '')
                qs.append(q)
    return qs


def resolve_pdf(fn):
    for c in DATA_DIRS + ['.']:
        fp = os.path.join(c, fn)
        if os.path.exists(fp):
            return fp
    return None


def q_sort_key(q):
    # paper "9702/42/F/M/25" -> ['9702','42','F','M','25']
    t = q['_paper'].split('/')
    year = int(t[4])
    paper = int(t[1])
    sess = {'F': 0, 'M': 1, 'O': 2}.get(t[2], 9)
    qn = int(re.sub(r'\D', '', q.get('qnum', '0')) or 0)
    return (year, sess, paper, qn)


def q_codes(q):
    codes = []
    for p in q.get('parts', []):
        for c in p.get('codes', []):
            if c and c not in codes:
                codes.append(c)
    return codes


# ---------------------------------------------------------------------------
# syllabus (cleaned) — per topic, ordered list of (code, text)
# ---------------------------------------------------------------------------
MANUAL_FIX = {
    # kinetic theory of gases (OCR-damaged equations)
    '15.3.2': "explain how molecular movement causes the pressure exerted by a gas and hence deduce the relationship p = ⅓ρ⟨c²⟩",
    '15.3.3': "understand that the root-mean-square speed cᵣ.ₘ.ₛ. is given by √⟨c²⟩",
    '15.3.4': "compare pV = ⅓Nm⟨c²⟩ with pV = NkT to deduce that the average translational kinetic energy of a molecule is (3/2)kT, and recall and use this expression",
    # oscillations / quantum / nuclear (OCR-dropped points)
    '17.1.2': "recall and use ω = 2πf and ω = 2π/T",
    '17.2.2': "recall and use E = ½mω²x₀² for the total energy of a system undergoing simple harmonic motion",
    '22.2.2': "understand and use the terms threshold frequency and work function",
    '22.2.4': "recall and use hf = Φ + ½mv²max",
    '23.1.3': "understand the concept of mass defect, and that it is the difference between the total mass of a nucleus and the total mass of its constituent nucleons",
    '23.1.4': "understand the origin of nuclear binding energy and recall and use ΔE = Δmc²",
    '23.1.5': "understand that binding energy per nucleon is a measure of the stability of a nucleus",
    '23.1.6': "understand and interpret the graph of binding energy per nucleon against nucleon number",
    '23.1.7': "use the binding energy per nucleon curve to explain the release of energy in nuclear fission and nuclear fusion",
    '23.2.1': "understand that fluctuations in count rate provide evidence for the random nature of radioactive decay",
    '23.2.2': "understand that radioactive decay is both spontaneous and random",
}


def load_syllabus():
    txt = open(SYLLABUS_PATH, encoding='utf-8').read()
    # drop the running footer that OCR merged into some points
    txt = re.sub(r'Cambridge International AS & A Level Physics 9702 syllabus.*?cambridgeinternational\.org/alevel',
                 '', txt, flags=re.S)
    by_topic = {}
    for ln in txt.splitlines():
        ln = ln.strip()
        m = re.match(r'^(\d+)\.(\d+)\.(\d+)\s*—\s*(.*)$', ln)
        if not m:
            continue
        t = int(m.group(1))
        code = f'{m.group(1)}.{m.group(2)}.{m.group(3)}'
        body = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', m.group(4))
        body = re.sub(r'[   ]', ' ', body)
        body = re.sub(r'\s+', ' ', body).strip()
        if code in MANUAL_FIX:
            body = MANUAL_FIX[code]
        if body and len(body) > 1:
            by_topic.setdefault(t, []).append((code, body))
    # ensure MANUAL_FIX points that were absent from the file are inserted in order
    for t in TOPICS:
        pts = by_topic.setdefault(t, [])
        have = {c for c, _ in pts}
        for code, body in MANUAL_FIX.items():
            if code.startswith(f'{t}.') and code not in have:
                pts.append((code, body))
        by_topic[t] = sorted(pts, key=lambda x: tuple(map(int, x[0].split('.'))))
    return by_topic


# ---------------------------------------------------------------------------
# question page assembly (pymupdf): uniform A4 page, header strip on first page
# ---------------------------------------------------------------------------
HEADER_H = 40.0
CONTENT_MARGIN_X = 24.0
CONTENT_MARGIN_Y = 14.0


def question_pages(src_path, meta, idx):
    """Return a temp PDF path with the question rendered on uniform A4 pages."""
    src = pymupdf.open(src_path)
    out = pymupdf.open()
    n = src.page_count
    for i in range(n):
        page = src[i]
        pw, ph = page.rect.width, page.rect.height
        np = out.new_page(width=PAGE_W, height=H)
        top = HEADER_H if i == 0 else 0.0
        avail_w = PAGE_W - 2 * CONTENT_MARGIN_X
        avail_h = H - top - 2 * CONTENT_MARGIN_Y
        scale = min(avail_w / pw, avail_h / ph)
        dw, dh = pw * scale, ph * scale
        x = (PAGE_W - dw) / 2
        y = top + (H - top - dh) / 2
        if i == 0:
            _draw_header(np, meta)
        np.show_pdf_page(pymupdf.Rect(x, y, x + dw, y + dh), src, page.number)
    tmp = f'/tmp/_p4q_{idx}.pdf'
    out.save(tmp)
    out.close()
    src.close()
    return tmp


def _text_width(text, fontsize, bold=False):
    # codes are ASCII, so the built-in Helvetica metric is accurate enough
    return pymupdf.get_text_length(text, fontname='helv', fontsize=fontsize)


def _draw_header(page, meta):
    band = pymupdf.Rect(0, 0, PAGE_W, HEADER_H)
    page.draw_rect(band, color=None, fill=(0.122, 0.165, 0.267))
    page.draw_rect(pymupdf.Rect(0, HEADER_H - 2.5, PAGE_W, HEADER_H), color=None, fill=(0.788, 0.635, 0.294))
    left = f"{meta['paper']}   ·   {meta['qnum']}   ·   {meta['marks']} marks"
    page.insert_text((CONTENT_MARGIN_X + 12, 17), left, fontsize=10.5,
                     fontfile=DEJAVU_BOLD_TTF, color=(1, 1, 1))
    codes = '   ·   '.join(meta['codes']) if meta['codes'] else ''
    if codes:
        tw = _text_width(codes, 8.5)
        page.insert_text((PAGE_W - CONTENT_MARGIN_X - 12 - tw, 17), codes, fontsize=8.5,
                         fontfile=DEJAVU_TTF, color=(0.86, 0.80, 0.62))
    title = meta['title']
    page.insert_text((CONTENT_MARGIN_X + 12, 32), title, fontsize=8,
                     fontfile=DEJAVU_TTF, color=(0.80, 0.82, 0.86))


# ---------------------------------------------------------------------------
# reportlab page helpers (front matter + syllabus + answers)
# ---------------------------------------------------------------------------
def wrap(text, width=104):
    words = text.split()
    lines, cur = [], ''
    for w in words:
        if not cur:
            cur = w
        elif len(cur) + len(w) + 1 <= width:
            cur = cur + ' ' + w
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _fit(text, font, size, maxw):
    while size > 9 and stringWidth(text, font, size) > maxw:
        size -= 1
    return size


def cover(c, title, subtitle, footer):
    c.setFillColor(HexColor('#c6d1de')); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(NAVY); c.rect(0, H - 170, W, 170, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(0, H - 170, W, 5, fill=1, stroke=0)
    c.setFillColor(HexColor('#ffffff'))
    size = _fit(title, 'Helvetica-Bold', 30, W - 110)
    c.setFont('Helvetica-Bold', size)
    c.drawString(55, H - 100, title)
    c.setFont('Helvetica', 12); c.setFillColor(HexColor('#d7dee6'))
    c.drawString(55, H - 130, subtitle)
    c.setFont('Helvetica-Bold', 13); c.setFillColor(NAVY)
    c.drawString(55, H - 205, 'Name:')
    c.drawString(55, H - 250, 'Class:')
    c.setStrokeColor(HexColor('#8f9aa8')); c.setLineWidth(1)
    c.line(130, H - 210, 520, H - 210)
    c.line(130, H - 255, 520, H - 255)
    c.setFont('Helvetica', 10); c.setFillColor(HexColor('#4a5560'))
    c.drawString(55, 70, footer)
    c.setFont(CN, 13)
    c.drawString(55, 46, 'A-Level 物理 · Paper 4 习题集')


def topic_div(c, topic, title, nq, first_page_note):
    c.setFillColor(HexColor('#eef1f5')); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(NAVY); c.rect(0, H - 14, W, 14, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(0, H - 18, W, 4, fill=1, stroke=0)
    c.setFillColor(NAVY)
    text = f'{topic}  {title}'
    size = _fit(text, 'Helvetica-Bold', 30, W - 110)
    c.setFont('Helvetica-Bold', size)
    c.drawString(55, H - 160, text)
    c.setFont('Helvetica', 13); c.setFillColor(GREY)
    c.drawString(55, H - 195, f'{nq} questions · Paper 4 · 2024–2026')
    c.setFont(CN, 11); c.setFillColor(HexColor('#8a93a0'))
    c.drawString(55, H - 220, '考纲要求见下页 · 题目按年份排列（2024 → 2025 → 2026）')


def syllabus_page(c, topic, title, points):
    c.setFillColor(HexColor('#ffffff')); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(NAVY); c.rect(0, H - 60, W, 60, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(0, H - 60, W, 4, fill=1, stroke=0)
    c.setFillColor(HexColor('#ffffff')); c.setFont('Helvetica-Bold', 18)
    c.drawString(55, H - 38, f'Syllabus requirements · {topic}  {title}')
    c.setFont(CN, 11); c.setFillColor(HexColor('#e8d9b0'))
    c.drawString(55, H - 90, '考纲要求（9702 · 2025–2027 syllabus）')

    y = H - 124
    cur_sec = None
    for code, body in points:
        sec = code.rsplit('.', 1)[0]
        if sec != cur_sec:
            cur_sec = sec
            if y < 90:
                c.showPage(); y = H - 60
                _syl_continue_header(c, topic, title)
            c.setFont(MATH_FONT_B, 11.5); c.setFillColor(GOLD)
            c.drawString(55, y, sec)
            y -= 18
        lines = wrap(body, 96)
        c.setFont(MATH_FONT, 9.8); c.setFillColor(INK)
        c.setFont(MATH_FONT_B, 9.8); c.setFillColor(NAVY)
        tw = stringWidth(code, MATH_FONT_B, 9.8)
        c.drawString(55, y, code)
        c.setFont(MATH_FONT, 9.8); c.setFillColor(INK)
        for ln in lines:
            if y < 55:
                c.showPage(); y = H - 60
                _syl_continue_header(c, topic, title)
                c.setFont(MATH_FONT_B, 9.8); c.setFillColor(NAVY)
                c.drawString(55, y, code)
                c.setFont(MATH_FONT, 9.8); c.setFillColor(INK)
            c.drawString(55 + tw + 8, y, ln)
            y -= 14
        y -= 4
    c.showPage()


def _syl_continue_header(c, topic, title):
    c.setFillColor(HexColor('#ffffff')); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFont('Helvetica-Bold', 13); c.setFillColor(NAVY)
    c.drawString(55, H - 38, f'Syllabus requirements · {topic}  {title}  (continued)')
    c.setFillColor(GOLD); c.setLineWidth(2); c.line(55, H - 50, 120, H - 50)


def toc_page(c, entries):
    c.setFillColor(HexColor('#ffffff')); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(NAVY); c.setFont('Helvetica-Bold', 24)
    c.drawString(55, H - 60, 'Contents')
    c.setFont('Helvetica', 11); c.setFillColor(GREY)
    c.drawString(55, H - 84, 'Topic · questions · page')
    y = H - 120
    for topic, title, nq, pg in entries:
        if y < 60:
            c.showPage(); y = H - 60
        c.setFont('Helvetica-Bold', 13); c.setFillColor(NAVY)
        c.drawString(55, y, f'{topic}  {title}')
        c.setFont('Helvetica', 11); c.setFillColor(INK)
        c.drawString(55, y - 18, f'   {nq} questions')
        c.setFont('Helvetica-Bold', 12); c.setFillColor(NAVY)
        c.drawString(520, y, str(pg))
        y -= 42
    c.showPage()


# ---------------------------------------------------------------------------
# answer book
# ---------------------------------------------------------------------------
def ans_cover(c):
    c.setFillColor(NAVY); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(0, H - 10, W, 10, fill=1, stroke=0)
    c.setFillColor(HexColor('#ffffff')); c.setFont('Helvetica-Bold', 36)
    c.drawString(55, H - 180, 'Answer Key')
    c.setFont('Helvetica', 14); c.setFillColor(HexColor('#d7dee6'))
    c.drawString(55, H - 216, '9702 Physics · Paper 4 · 2024–2026 · By Topic')
    c.setFont(CN, 16); c.setFillColor(HexColor('#e8d9b0'))
    c.drawString(55, H - 256, '答案册（按 topic 分）')


def answers_page(c, topic, title, qs):
    y = H - 60
    c.setFillColor(NAVY); c.setFont('Helvetica-Bold', 16)
    c.drawString(55, y, f'{topic}  {title}')
    c.setFillColor(GOLD); c.setLineWidth(2); c.line(55, y - 8, 130, y - 8)
    y -= 30
    for q in sorted(qs, key=q_sort_key):
        head = f"{q['_paper']}   {q['qnum']}   —   {html_to_text(q.get('title', ''))}   [{q['marks']} marks]"
        for ln in wrap(head, 98):
            if y < 70:
                c.showPage(); y = H - 60
            c.setFont(MATH_FONT_B, 10); c.setFillColor(NAVY)
            c.drawString(55, y, ln)
            y -= 15
        c.setFont(MATH_FONT, 9.5); c.setFillColor(INK)
        for p in q.get('parts', []):
            label = p.get('label', '')
            marks = p.get('marks', '')
            ans = html_to_text(p.get('answer', '') or '')
            segs = ans.split('\n') or ['']
            labelstr = f'{label}  [{marks}]'
            lw = stringWidth(labelstr + '  ', MATH_FONT_B, 9.5)
            # first segment carries the bold label prefix
            for j, ln in enumerate(wrap(segs[0], 96)):
                if y < 60:
                    c.showPage(); y = H - 60
                if j == 0:
                    c.setFont(MATH_FONT_B, 9.5); c.setFillColor(HexColor('#8a6d1f'))
                    c.drawString(70, y, labelstr)
                    c.setFont(MATH_FONT, 9.5); c.setFillColor(INK)
                    c.drawString(70 + lw, y, ln)
                else:
                    c.setFont(MATH_FONT, 9.5); c.setFillColor(INK)
                    c.drawString(70 + lw, y, ln)
                y -= 13
            for seg in segs[1:]:
                for ln in wrap(seg, 96):
                    if y < 60:
                        c.showPage(); y = H - 60
                    c.setFont(MATH_FONT, 9.5); c.setFillColor(INK)
                    c.drawString(70, y, ln)
                    y -= 13
        y -= 6
    c.showPage()


# ---------------------------------------------------------------------------
# assembly
# ---------------------------------------------------------------------------
class Builder:
    def __init__(self):
        self.writer = PdfWriter()
        self.pages = 0

    def add_pdf(self, path):
        if not path or not os.path.exists(path):
            return
        for p in PdfReader(path).pages:
            self.writer.add_page(p)
            self.pages += 1

    def add_canvas(self, fn):
        c = rl_canvas.Canvas('/tmp/_wb_page.pdf', pagesize=A4)
        fn(c)
        c.save()
        for p in PdfReader('/tmp/_wb_page.pdf').pages:
            self.writer.add_page(p)
            self.pages += 1


def add_page_numbers(path):
    doc = pymupdf.open(path)
    for i, page in enumerate(doc):
        w = page.rect.width
        h = page.rect.height
        txt = str(i + 1)
        tw = pymupdf.get_text_length(txt, fontname='helv', fontsize=9)
        page.insert_text((w / 2 - tw / 2, h - 20), txt, fontsize=9, fontname='helv',
                         color=(0.42, 0.42, 0.42))
    doc.saveIncr()
    doc.close()


def main():
    questions = load_questions()
    syllabus = load_syllabus()

    # group + order
    by_topic = {}
    for q in questions:
        t = int(q['topic'])
        by_topic.setdefault(t, []).append(q)
    topic_order = sorted(by_topic.keys())
    missing = []

    # ---- question book body (per topic) ----
    body = Builder()
    toc_entries = []
    idx = 0
    for t in topic_order:
        qs = sorted(by_topic[t], key=q_sort_key)
        nq = len(qs)
        start_page = body.pages + 1
        toc_entries.append((t, TOPICS[t], nq, start_page))
        body.add_canvas(lambda c, t=t, title=TOPICS[t], nq=nq:
                        topic_div(c, t, title, nq, None))
        body.add_canvas(lambda c, t=t, title=TOPICS[t], pts=syllabus.get(t, []):
                        syllabus_page(c, t, title, pts))
        for q in qs:
            src = resolve_pdf(q['pdf'])
            if not src:
                missing.append((q['_paper'], q['qnum'], q['pdf']))
                continue
            meta = {
                'paper': q['_paper'],
                'qnum': q['qnum'],
                'marks': q.get('marks', 0),
                'title': html_to_text(q.get('title', '')),
                'codes': q_codes(q),
            }
            tmp = question_pages(src, meta, idx)
            idx += 1
            body.add_pdf(tmp)

    # ---- front matter ----
    front = Builder()
    front.add_canvas(lambda c: cover(
        c,
        '9702 Physics · Paper 4',
        'Structured questions by topic · 2024 · 2025 · 2026',
        'Cambridge International AS & A Level Physics 9702 — Paper 4 (A2)'))
    front.add_canvas(lambda c: toc_page(c, toc_entries))

    # ---- combine ----
    final = PdfWriter()
    for p in front.writer.pages:
        final.add_page(p)
    for p in body.writer.pages:
        final.add_page(p)

    qbook = '9702_Paper4_2024-2026_ByTopic.pdf'
    with open(qbook, 'wb') as f:
        final.write(f)
    add_page_numbers(qbook)

    # ---- answer book ----
    ans = Builder()
    ans.add_canvas(ans_cover)
    for t in topic_order:
        qs = sorted(by_topic[t], key=q_sort_key)
        ans.add_canvas(lambda c, t=t, title=TOPICS[t], qs=qs:
                       answers_page(c, t, title, qs))
    abook = '9702_Paper4_2024-2026_ByTopic_Answers.pdf'
    with open(abook, 'wb') as f:
        ans.writer.write(f)
    add_page_numbers(abook)

    print(f'question book : {qbook}  ({len(final.pages)} pages, {len(questions)} questions)')
    print(f'answer book   : {abook}  ({ans.pages} pages)')
    print(f'topics        : {topic_order}')
    if missing:
        print(f'\nWARNING {len(missing)} missing PDFs:')
        for m in missing:
            print('   ', m)
    else:
        print('no missing question PDFs')


if __name__ == '__main__':
    main()
