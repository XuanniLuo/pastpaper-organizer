# -*- coding: utf-8 -*-
"""Answer key for the 0625 Thermal Physics quiz (quiz 叁 6Nov)."""
import os
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


MCQ_ANSWERS = 'D D D B C A C D B D B B A B D'.split()

STRUCTURED = [
    ('Question 1 · Air in a car tyre · 8 marks', [
        ('(a)', 3, 'pV = constant  →  V = (1.02 × 1.0 × 10⁵) ÷ (2.6 × 10⁵) = 0.39 m³'),
        ('(b)(i)', 3, 'separation: large / far apart;  arrangement: irregular / random;  motion: rapid / random (directions)'),
        ('(b)(ii)', 2, 'average kinetic energy of the particles decreases'),
    ]),
    ('Question 2 · Heating water in a saucepan · 9 marks', [
        ('(a)', 1, 'average kinetic energy of the particles increases / particles move faster'),
        ('(b)(i)', 2, 'ρ = m/V;  250 cm³ = 2.5 × 10⁻⁴ m³;  m = ρV = 1000 × 2.5 × 10⁻⁴ = 0.25 kg'),
        ('(b)(ii)', 3, 'Δθ = 65 − 20 = 45 °C;  E = mcΔθ = 0.25 × 4200 × 45 = 47 000 J'),
        ('(b)(iii)', 1, 'thermal energy is also transferred to the pan / surroundings'),
        ('(c)', 2, 'any two: takes longer to heat the water · more thermal energy needed for the same temperature rise · aluminium has a higher specific heat capacity'),
    ]),
]


def header(page, subtitle='Answer Key'):
    logo = Image.open(LOGO).convert('RGB').resize((LOGO_W_PX, LOGO_H_PX))
    page.paste(logo, ((A4_PX[0] - LOGO_W_PX) // 2, _pt(16)))
    d = ImageDraw.Draw(page)
    d.text((_pt(55), _pt(80)), 'quiz 叁 6Nov', font=_cn(_pt(34)), fill=NAVY)
    d.text((_pt(55), _pt(118)), subtitle, font=_font(_pt(18), bold=True), fill=GOLD)
    d.text((_pt(55), _pt(142)), 'IGCSE Physics 0625 · Thermal Physics', font=_font(_pt(13)), fill=GREY)
    d.line([(_pt(55), _pt(158)), (_pt(300), _pt(158))], fill=GOLD, width=3)
    return _pt(180)


def build():
    page = Image.new('RGB', A4_PX, 'white')
    d = ImageDraw.Draw(page)
    y = header(page)

    # Section A
    d.text((_pt(55), y), 'Section A — Multiple Choice', font=_font(_pt(14), bold=True), fill=NAVY)
    y += _pt(26)
    # answer grid: 5 per row
    for r in range(0, 15, 5):
        line = '   '.join('%2d  %s' % (i + 1, MCQ_ANSWERS[i]) for i in range(r, r + 5))
        d.text((_pt(70), y), line, font=_font(_pt(14)), fill=DARK)
        y += _pt(26)
    y += _pt(12)

    # Section B
    d.text((_pt(55), y), 'Section B — Structured Questions', font=_font(_pt(14), bold=True), fill=NAVY)
    y += _pt(26)
    for title, parts in STRUCTURED:
        if y > _pt(700):
            d.text((_pt(55), A4_PX[1] - _pt(30)), 'continued …', font=_font(_pt(11)), fill=GREY)
            break
        d.text((_pt(55), y), title, font=_font(_pt(12.5), bold=True), fill=GOLD)
        y += _pt(22)
        for label, marks, ans in parts:
            head = '%s [%d]  ' % (label, marks)
            lw = _font(_pt(11), bold=True).getlength(head)
            lines = _wrap(ans, _font(_pt(11)), (A4_PT[0] - 62 - 28 - 30) * DPI / 72)
            for j, ln in enumerate(lines):
                if y > _pt(700):
                    d.text((_pt(55), A4_PX[1] - _pt(30)), 'continued …', font=_font(_pt(11)), fill=GREY)
                    break
                if j == 0:
                    d.text((_pt(62), y), head, font=_font(_pt(11), bold=True), fill=NAVY)
                    d.text((_pt(62) + lw, y), ln, font=_font(_pt(11)), fill=DARK)
                else:
                    d.text((_pt(62) + lw, y), ln, font=_font(_pt(11)), fill=DARK)
                y += _pt(17)
            y += _pt(4)
        y += _pt(10)

    d.rectangle([0, A4_PX[1] - _pt(34), A4_PX[0], A4_PX[1]], fill=NAVY)
    d.text((_pt(55), A4_PX[1] - _pt(24)),
           'DEPU International Senior Department', font=_font(_pt(14), bold=True), fill=(255, 255, 255))

    out = os.path.join(HERE, 'quiz-thermal-0625-answers.pdf')
    page.save(out, resolution=DPI)
    print('answer key:', out)


if __name__ == '__main__':
    build()
