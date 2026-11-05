# -*- coding: utf-8 -*-
"""
Build a 5-question A2 mid-term paper (100 marks) from 2022/2023 9702 Paper 4
questions on topics 12/13/17, plus a mark scheme from screenshots of the
original mark schemes.

Every page carries the DEPU letterhead logo; the original paper headers and
question-source info are removed; marks are redistributed so the paper totals
100.

Outputs:
  A2-Midterm_Physics_9702_Paper4_2022-23.pdf
  A2-Midterm_Physics_9702_Paper4_2022-23_MarkScheme.pdf
"""
import os
import re
import pymupdf
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, 'depu_logo.png')

DPI = 150
A4_PT = (595.27, 841.89)
A4_PX = (int(A4_PT[0] * DPI / 72), int(A4_PT[1] * DPI / 72))
LOGO_W_PX = A4_PX[0] - 2 * int(40 * DPI / 72)          # 40pt side margins
LOGO_H_PX = int(LOGO_W_PX * 147 / 1943)
CROP_TOP_PX = int(64 * DPI / 72)                        # header + question number

NAVY = (0x1f, 0x2a, 0x44)
GOLD = (0xc9, 0xa2, 0x4b)
GREY = (0x35, 0x39, 0x44)

try:
    import matplotlib
    MT = os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data', 'fonts', 'ttf')
    FONT = os.path.join(MT, 'DejaVuSans.ttf')
    FONT_B = os.path.join(MT, 'DejaVuSans-Bold.ttf')
except Exception:
    FONT = FONT_B = None

QUESTIONS = [
    {'num': 1, 'topic': 'Motion in a circle', 'marks': 20,
     'title': "Circular motion of a clock's minute hand",
     'slice': '9702_w23_qp_42_Q1_Motion_in_a_circle.pdf',
     'new_parts': [2, 4, 2, 4, 4, 4], 'old_total': 10,
     'ms': '9702_w23_ms_42.pdf', 'ms_pages': [6]},
    {'num': 2, 'topic': 'Gravitational fields', 'marks': 20,
     'title': 'Gravitational potential of a planet — surface g & satellite orbit period',
     'slice': '9702_m23_qp_42_Q1_Gravitational_fields.pdf',
     'new_parts': [3, 2, 2, 3, 7, 3], 'old_total': 12,
     'ms': '9702_m23_ms_42.pdf', 'ms_pages': [6, 7]},
    {'num': 3, 'topic': 'Gravitational fields', 'marks': 20,
     'title': "Gravitational potential & escape speed — the Moon's field & hydrogen atmosphere",
     'slice': '9702_w23_qp_42_Q2_Gravitational_fields.pdf',
     'new_parts': [3, 3, 2, 3, 2, 5, 2], 'old_total': 12,
     'ms': '9702_w23_ms_42.pdf', 'ms_pages': [7]},
    {'num': 4, 'topic': 'Oscillations', 'marks': 20,
     'title': 'Oscillating mass on a spring — energy lines, period & damping',
     'slice': '9702_m23_qp_42_Q3_Oscillations.pdf',
     'new_parts': [4, 8, 2, 4, 2], 'old_total': 10,
     'ms': '9702_m23_ms_42.pdf', 'ms_pages': [9]},
    {'num': 5, 'topic': 'Oscillations', 'marks': 20,
     'title': 'Simple harmonic motion — defining equation, energy & damping',
     'slice': '9702_w22_qp_41_Q3_Oscillations.pdf',
     'new_parts': [4, 2, 3, 3, 4, 4], 'old_total': 11,
     'ms': '9702_w22_ms_41.pdf', 'ms_pages': [8]},
]


# ---------------------------------------------------------------------------
# mark editing (pymupdf redaction, text layer preserved)
# ---------------------------------------------------------------------------
def edit_marks(src_pdf, new_parts, old_total, out_pdf):
    doc = pymupdf.open(src_pdf)
    # collect all part marks + the total, in reading order (top-origin: small y = top)
    marks = []
    for i in range(doc.page_count):
        for n in range(1, 10):
            for r in doc[i].search_for('[%d]' % n):
                marks.append((i, r.y1, n, r))
        for r in doc[i].search_for('[Total: %d]' % old_total):
            marks.append((i, r.y1, -1, r))
    marks.sort(key=lambda m: (m[0], m[1]))   # page, then top-to-bottom
    # first N are part marks, last is the total
    part_marks = [m for m in marks if m[2] != -1]
    total_marks = [m for m in marks if m[2] == -1]
    assert len(part_marks) == len(new_parts), (src_pdf, len(part_marks), len(new_parts))
    for m, new in zip(part_marks, new_parts):
        page = doc[m[0]]
        page.add_redact_annot(m[3], text='[%d]' % new, fontname='helv',
                              fontsize=11, text_color=(0, 0, 0))
    for m in total_marks:
        page = doc[m[0]]
        page.add_redact_annot(m[3], text='[Total: 20]', fontname='helv',
                              fontsize=11, text_color=(0, 0, 0))
    for i in range(doc.page_count):
        doc[i].apply_redactions()
    doc.save(out_pdf)
    doc.close()
    return out_pdf


# ---------------------------------------------------------------------------
# page composition (PIL): crop header, add logo + strip
# ---------------------------------------------------------------------------
def _font(size, bold=False):
    p = FONT_B if bold else FONT
    return ImageFont.truetype(p, size) if p else ImageFont.load_default()


CN_FONT = '/System/Library/Fonts/STHeiti Light.ttc'


def _cn(size):
    return ImageFont.truetype(CN_FONT, size)


def raster_page(pdf, pno):
    doc = pymupdf.open(pdf)
    pix = doc[pno].get_pixmap(dpi=DPI)
    png = '/tmp/_pg_%d.png' % pno
    pix.save(png)
    doc.close()
    return png


def compose_question_page(slice_pdf, pno, q, first):
    img = Image.open(raster_page(slice_pdf, pno)).convert('RGB')
    img = img.crop((0, CROP_TOP_PX, img.width, img.height))
    page = Image.new('RGB', A4_PX, 'white')
    # logo
    logo = Image.open(LOGO).convert('RGB').resize((LOGO_W_PX, LOGO_H_PX))
    lx = (A4_PX[0] - LOGO_W_PX) // 2
    ly = int(12 * DPI / 72)
    page.paste(logo, (lx, ly))
    d = ImageDraw.Draw(page)
    if first:
        sy = ly + LOGO_H_PX + int(16 * DPI / 72)
        d.text((int(40 * DPI / 72), sy),
               'Question %d  ·  %s  ·  %d marks' % (q['num'], q['topic'], q['marks']),
               font=_font(int(15 * DPI / 72), bold=True), fill=NAVY)
        d.text((int(40 * DPI / 72), sy + int(18 * DPI / 72)),
               q['title'], font=_font(int(11 * DPI / 72)), fill=GREY)
        content_top = sy + int(38 * DPI / 72)
    else:
        content_top = ly + LOGO_H_PX + int(14 * DPI / 72)
    # scale content to fit below
    cw, ch = img.size
    avail_w = A4_PX[0] - 2 * int(24 * DPI / 72)
    avail_h = A4_PX[1] - content_top - int(14 * DPI / 72)
    scale = min(avail_w / cw, avail_h / ch)
    nw, nh = int(cw * scale), int(ch * scale)
    img = img.resize((nw, nh))
    px = (A4_PX[0] - nw) // 2
    page.paste(img, (px, content_top))
    return page


def compose_ms_page(ms_pdf, pno, q):
    img = Image.open(raster_page(ms_pdf, pno)).convert('RGB')
    img = img.crop((0, int(40 * DPI / 72), img.width, img.height))
    page = Image.new('RGB', A4_PX, 'white')
    logo = Image.open(LOGO).convert('RGB').resize((LOGO_W_PX, LOGO_H_PX))
    lx = (A4_PX[0] - LOGO_W_PX) // 2
    ly = int(12 * DPI / 72)
    page.paste(logo, (lx, ly))
    d = ImageDraw.Draw(page)
    sy = ly + LOGO_H_PX + int(14 * DPI / 72)
    d.text((int(40 * DPI / 72), sy),
           'Mark scheme — Question %d' % q['num'],
           font=_font(int(14 * DPI / 72), bold=True), fill=NAVY)
    content_top = sy + int(24 * DPI / 72)
    cw, ch = img.size
    avail_w = A4_PX[0] - 2 * int(24 * DPI / 72)
    avail_h = A4_PX[1] - content_top - int(14 * DPI / 72)
    scale = min(avail_w / cw, avail_h / ch)
    nw, nh = int(cw * scale), int(ch * scale)
    img = img.resize((nw, nh))
    px = (A4_PX[0] - nw) // 2
    page.paste(img, (px, content_top))
    return page


DARK = (0x26, 0x26, 0x26)


def _pt(v):
    return int(v * DPI / 72)


def _wrap(text, font, max_pt):
    words = text.split()
    lines, cur = [], ''
    for w in words:
        test = (cur + ' ' + w).strip()
        if font.getlength(test) <= max_pt:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def build_cover():
    page = Image.new('RGB', A4_PX, 'white')
    logo = Image.open(LOGO).convert('RGB').resize((LOGO_W_PX, LOGO_H_PX))
    page.paste(logo, ((A4_PX[0] - LOGO_W_PX) // 2, _pt(16)))
    d = ImageDraw.Draw(page)
    ML = _pt(55)

    d.text((ML, _pt(82)), 'Mid-term Examination', font=_font(_pt(24), bold=True), fill=NAVY)
    d.text((ML, _pt(110)), 'PHYSICS · Paper 4 (A2)', font=_font(_pt(13)), fill=GREY)
    d.text((_pt(340), _pt(78)), 'A卷', font=_cn(_pt(30)), fill=NAVY)
    d.line([(ML, _pt(128)), (_pt(300), _pt(128))], fill=GOLD, width=3)

    # candidate info (two columns)
    y = _pt(152)
    d.text((ML, y), 'Centre No.: _________________', font=_font(_pt(12), bold=True), fill=DARK)
    d.text((_pt(330), y), 'Class: _________________', font=_font(_pt(12), bold=True), fill=DARK)
    y += _pt(26)
    d.text((ML, y), 'Candidate No.: _________________', font=_font(_pt(12), bold=True), fill=DARK)
    d.text((_pt(330), y), 'Candidate name: _________________', font=_font(_pt(12), bold=True), fill=DARK)

    y += _pt(34)
    d.text((ML, y), 'Exam Duration: 60 mins', font=_font(_pt(12), bold=True), fill=DARK)
    y += _pt(24)
    d.text((ML, y), 'Additional Materials: Answer Booklet/Paper', font=_font(_pt(12), bold=True), fill=DARK)
    y += _pt(20)
    d.text((ML, y), 'Graph Paper · List of Formulae', font=_font(_pt(11)), fill=DARK)

    y += _pt(36)
    d.text((ML, y), 'READ THESE INSTRUCTIONS FIRST', font=_font(_pt(14), bold=True), fill=NAVY)
    y += _pt(26)
    instr = [
        'If you have been given an Answer Booklet, follow the instructions on the front cover of the Booklet.',
        'Write your Centre number, Candidate number and name on all the work you hand in.',
        'Write in dark blue or black pen. You may use an HB pencil for any diagrams or graphs.',
        'Do not use staples, paper clips, glue or correction fluid.',
        'Answer all questions.',
        'Give non-exact numerical answers correct to 3 significant figures, unless a different level of accuracy is specified in the question.',
        'The use of an electronic calculator is expected, where appropriate.',
        'You are reminded of the need for clear presentation in your answers.',
        'At the end of the examination, fasten all your work securely together.',
        'The number of marks is given in brackets [ ] at the end of each question or part question.',
        'The total number of marks for this paper is 100.',
    ]
    ifont = _font(_pt(10.5))
    max_w = (A4_PT[0] - 62 - 28) * DPI / 72
    for line in instr:
        for wl in _wrap(line, ifont, max_w):
            d.text((_pt(62), y), wl, font=ifont, fill=DARK)
            y += _pt(17)
        y += _pt(4)

    y += _pt(12)
    d.text((ML, y), 'Topics: Motion in a circle · Gravitational fields · Oscillations',
           font=_font(_pt(12.5), bold=True), fill=NAVY)
    y += _pt(22)
    d.text((ML, y), '5 questions · 100 marks', font=_font(_pt(12)), fill=GOLD)

    # footer
    d.rectangle([0, A4_PX[1] - _pt(34), A4_PX[0], A4_PX[1]], fill=NAVY)
    d.text((ML, A4_PX[1] - _pt(24)),
           'DEPU International Senior Department', font=_font(_pt(14), bold=True), fill=(255, 255, 255))
    return page


def build_markscheme_cover():
    page = Image.new('RGB', A4_PX, 'white')
    logo = Image.open(LOGO).convert('RGB').resize((LOGO_W_PX, LOGO_H_PX))
    lx = (A4_PX[0] - LOGO_W_PX) // 2
    ly = int(16 * DPI / 72)
    page.paste(logo, (lx, ly))
    d = ImageDraw.Draw(page)
    d.text((int(55 * DPI / 72), int(88 * DPI / 72)), 'Mark Scheme',
           font=_font(int(26 * DPI / 72), bold=True), fill=NAVY)
    d.text((int(55 * DPI / 72), int(112 * DPI / 72)), 'PHYSICS · Paper 4 (A2)',
           font=_font(int(15 * DPI / 72)), fill=GREY)
    d.text((int(340 * DPI / 72), int(84 * DPI / 72)), 'A卷', font=_cn(int(30 * DPI / 72)), fill=NAVY)
    d.line([(int(55 * DPI / 72), int(128 * DPI / 72)),
            (int(300 * DPI / 72), int(128 * DPI / 72))], fill=GOLD, width=3)
    d.text((int(55 * DPI / 72), int(150 * DPI / 72)),
           'A2 Mid-term Examination — 5 questions · 100 marks',
           font=_font(int(14 * DPI / 72)), fill=(0x26, 0x26, 0x26))
    return page


def main():
    paper_pages = [build_cover()]
    for q in QUESTIONS:
        edited = edit_marks(os.path.join(HERE, q['slice']), q['new_parts'],
                            q['old_total'], '/tmp/_edited_%d.pdf' % q['num'])
        n = pymupdf.open(edited).page_count
        for i in range(n):
            paper_pages.append(compose_question_page(edited, i, q, first=(i == 0)))

    paper_pages[0].save(os.path.join(HERE, 'A2-Midterm-A.pdf'),
                        save_all=True, append_images=paper_pages[1:], resolution=DPI)

    ms_pages = [build_markscheme_cover()]
    for q in QUESTIONS:
        for p in q['ms_pages']:
            ms_pages.append(compose_ms_page(os.path.join(HERE, q['ms']), p - 1, q))
    ms_pages[0].save(os.path.join(HERE, 'A2-Midterm-A_MarkScheme.pdf'),
                     save_all=True, append_images=ms_pages[1:], resolution=DPI)

    print('paper: A2-Midterm-A.pdf  (%d pages, 100 marks)' % len(paper_pages))
    print('mark scheme: A2-Midterm-A_MarkScheme.pdf  (%d pages)' % len(ms_pages))


if __name__ == '__main__':
    main()
