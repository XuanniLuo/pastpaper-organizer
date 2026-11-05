# -*- coding: utf-8 -*-
"""
Build a 40-minute IGCSE 0625 Thermal Physics quiz paper from past-paper questions.
Cover is "quiz 叁 6Nov". Section A = 15 multiple-choice, Section B = 2 structured.
Compact layout: 3 MCQ per page, small section bands, no logo on question pages.
"""
import os
import pymupdf
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, 'depu_logo.png')

DPI = 150
A4_PT = (595.27, 841.89)
A4_PX = (int(A4_PT[0] * DPI / 72), int(A4_PT[1] * DPI / 72))
LOGO_W_PX = A4_PX[0] - 2 * int(40 * DPI / 72)
LOGO_H_PX = int(LOGO_W_PX * 147 / 1943)

NAVY = (0x1f, 0x2a, 0x44)
GOLD = (0xc9, 0xa2, 0x4b)
GREY = (0x35, 0x39, 0x44)
DARK = (0x26, 0x26, 0x26)

try:
    import matplotlib
    MT = os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data', 'fonts', 'ttf')
    FONT = os.path.join(MT, 'DejaVuSans.ttf')
    FONT_B = os.path.join(MT, 'DejaVuSans-Bold.ttf')
except Exception:
    FONT = FONT_B = None

CN_FONT = '/System/Library/Fonts/STHeiti Light.ttc'


def _pt(v):
    return int(v * DPI / 72)


def _font(size, bold=False):
    p = FONT_B if bold else FONT
    return ImageFont.truetype(p, size) if p else ImageFont.load_default()


def _cn(size):
    return ImageFont.truetype(CN_FONT, size)


def _wrap(text, font, max_pt):
    words = text.split()
    lines, cur = [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if font.getlength(t) <= max_pt:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


MCQ = [
    '0625_s26_qp_21_Q10.pdf',  # 2.1 gas arrangement
    '0625_s26_qp_22_Q11.pdf',  # 2.1 gas pressure (particles)
    '0625_s26_qp_23_Q12.pdf',  # 2.1 p–V graph
    '0625_w23_qp_22_Q12.pdf',  # 2.1 Brownian motion
    '0625_s26_qp_22_Q13.pdf',  # 2.2 specific heat capacity
    '0625_s26_qp_22_Q14.pdf',  # 2.2 evaporation
    '0625_s26_qp_23_Q13.pdf',  # 2.2 thermal expansion
    '0625_s26_qp_22_Q16.pdf',  # 2.3 radiation (emission)
    '0625_s26_qp_23_Q14.pdf',  # 2.3 convection
    '0625_s26_qp_21_Q16.pdf',  # 2.3 radiation (vacuum)
    '0625_s26_qp_21_Q11.pdf',  # 2.1 gas pressure (volume/temperature)
    '0625_s26_qp_23_Q10.pdf',  # 2.1 gas compression (KE, collision rate)
    '0625_s26_qp_22_Q15.pdf',  # 2.2 evaporation vs boiling
    '0625_s26_qp_21_Q14.pdf',  # 2.3 conduction (metal vs plastic)
    '0625_s26_qp_23_Q15.pdf',  # 2.3 radiation through space
]

STRUCTURED = [
    ('0625_m26_qp_42_Q05.pdf', 8, 'Air in a car tyre — gas pressure and particle structure'),
    ('0625_s24_qp_43_Q04.pdf', 9, 'Heating water in a saucepan — specific heat capacity'),
]


def build_cover():
    page = Image.new('RGB', A4_PX, 'white')
    logo = Image.open(LOGO).convert('RGB').resize((LOGO_W_PX, LOGO_H_PX))
    page.paste(logo, ((A4_PX[0] - LOGO_W_PX) // 2, _pt(16)))
    d = ImageDraw.Draw(page)
    ML = _pt(55)

    d.text((ML, _pt(80)), 'quiz 叁 6Nov', font=_cn(_pt(42)), fill=NAVY)
    d.text((ML, _pt(128)), 'IGCSE Physics 0625 · Thermal Physics', font=_font(_pt(15)), fill=GREY)
    d.line([(ML, _pt(148)), (_pt(300), _pt(148))], fill=GOLD, width=3)

    y = _pt(175)
    d.text((ML, y), 'Name: ________________________  Class: ____________', font=_font(_pt(12), bold=True), fill=DARK)
    y += _pt(30)
    d.text((ML, y), 'Time: 40 minutes', font=_font(_pt(12), bold=True), fill=DARK)
    d.text((_pt(280), y), 'Total: 32 marks', font=_font(_pt(12), bold=True), fill=DARK)

    y += _pt(40)
    d.text((ML, y), 'INSTRUCTIONS', font=_font(_pt(14), bold=True), fill=NAVY)
    y += _pt(26)
    for line in [
        'Answer all questions.',
        'Write in dark blue or black pen. You may use an HB pencil for diagrams.',
        'Give non-exact numerical answers correct to 3 significant figures.',
        'Section A: multiple choice — 15 marks.  Section B: structured — 17 marks.',
        'The number of marks is shown in brackets [ ] at the end of each question.',
    ]:
        for wl in _wrap(line, _font(_pt(11)), (A4_PT[0] - 62 - 28) * DPI / 72):
            d.text((_pt(62), y), wl, font=_font(_pt(11)), fill=DARK)
            y += _pt(18)
        y += _pt(3)

    d.rectangle([0, A4_PX[1] - _pt(34), A4_PX[0], A4_PX[1]], fill=NAVY)
    d.text((ML, A4_PX[1] - _pt(24)),
           'DEPU International Senior Department', font=_font(_pt(14), bold=True), fill=(255, 255, 255))
    return page


def render(pdf):
    doc = pymupdf.open(pdf)
    pix = doc[0].get_pixmap(dpi=DPI)
    png = '/tmp/_q.png'
    pix.save(png)
    doc.close()
    return png


def compose_mcq(slice_pdf, num):
    img = Image.open(render(os.path.join('igcse-slices', slice_pdf))).convert('RGB')
    d = ImageDraw.Draw(img)
    d.rectangle([_pt(40), _pt(4), _pt(70), _pt(26)], fill='white')
    d.text((_pt(40), _pt(6)), '%d.' % num, font=_font(_pt(13), bold=True), fill=NAVY)
    return img


def compose_structured(slice_pdf, num, marks, title):
    doc = pymupdf.open(os.path.join('igcse-slices', slice_pdf))
    n = doc.page_count
    pages = []
    for i in range(n):
        pix = doc[i].get_pixmap(dpi=DPI)
        png = '/tmp/_s%d.png' % i
        pix.save(png)
        img = Image.open(png).convert('RGB')
        img = img.crop((0, _pt(64), img.width, img.height))
        page = Image.new('RGB', A4_PX, 'white')
        d = ImageDraw.Draw(page)
        if i == 0:
            sy = _pt(14)
            d.text((_pt(40), sy), 'Question %d  ·  %d marks' % (num, marks),
                   font=_font(_pt(15), bold=True), fill=NAVY)
            d.text((_pt(40), sy + _pt(18)), title, font=_font(_pt(11)), fill=GREY)
            d.line([(_pt(40), sy + _pt(32)), (_pt(86), sy + _pt(32))], fill=GOLD, width=3)
            content_top = sy + _pt(40)
        else:
            content_top = _pt(14)
        cw, ch = img.size
        avail_w = A4_PX[0] - 2 * _pt(24)
        avail_h = A4_PX[1] - content_top - _pt(14)
        scale = min(avail_w / cw, avail_h / ch)
        nw, nh = int(cw * scale), int(ch * scale)
        img = img.resize((nw, nh))
        page.paste(img, ((A4_PX[0] - nw) // 2, content_top))
        pages.append(page)
    doc.close()
    return pages


def draw_band(page, text):
    d = ImageDraw.Draw(page)
    d.rectangle([0, 0, A4_PX[0], _pt(28)], fill=NAVY)
    d.rectangle([0, _pt(28), A4_PX[0], _pt(31)], fill=GOLD)
    d.text((_pt(24), _pt(6)), text, font=_font(_pt(14), bold=True), fill=(255, 255, 255))
    return _pt(38)


def main():
    out_pages = [build_cover()]

    # Section A — 15 MCQ, three per page
    mcq_cards = [compose_mcq(s, i + 1) for i, s in enumerate(MCQ)]
    per_page = 3
    for i in range(0, len(mcq_cards), per_page):
        page = Image.new('RGB', A4_PX, 'white')
        top = draw_band(page, 'Section A · Multiple Choice  (15 marks)') if i == 0 else _pt(10)
        box_h = (A4_PX[1] - top - _pt(10)) // per_page
        for j, card in enumerate(mcq_cards[i:i + per_page]):
            cw, ch = card.size
            scale = min((A4_PX[0] - 2 * _pt(20)) / cw, (box_h - _pt(6)) / ch)
            nw, nh = int(cw * scale), int(ch * scale)
            card = card.resize((nw, nh))
            page.paste(card, ((A4_PX[0] - nw) // 2, top + j * box_h))
        out_pages.append(page)

    # Section B — structured
    for i, (s, marks, title) in enumerate(STRUCTURED):
        pages = compose_structured(s, i + 1, marks, title)
        if i == 0:
            # prepend the section band: shift the first page's content down a little
            band_h = _pt(38)
            shifted = Image.new('RGB', A4_PX, 'white')
            shifted.paste(pages[0].crop((0, 0, A4_PX[0], A4_PX[1] - band_h)), (0, band_h))
            draw_band(shifted, 'Section B · Structured Questions  (17 marks)')
            pages[0] = shifted
        out_pages.extend(pages)

    out = os.path.join(HERE, 'quiz-thermal-0625.pdf')
    out_pages[0].save(out, save_all=True, append_images=out_pages[1:], resolution=DPI)
    print('quiz paper:', out, '(%d pages)' % len(out_pages))


if __name__ == '__main__':
    main()
