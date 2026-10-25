# -*- coding: utf-8 -*-
"""
Build IGCSE 0625 practice workbooks.

Outputs:
  1. Compact workbook (all 6 topics, 10 MCQ + 3 theory each):
       IGCSE_0625_2025_Compact.pdf / _Answers.pdf
  2. Full workbook, topics 1-4 only, no schedule:
       IGCSE_0625_2025_Workbook.pdf / _Answers.pdf  (cover: "IGCSE Physics Workbook Topic 1-4")

Usage: python build_igcse_workbook.py
"""
import json
import glob
import os
import re

import pymupdf
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter

from igcse_syllabus import SYLLABUS, SUB_LABELS
from igcse_syllabus_points import SUBSUBS

W, H = A4
NAVY = HexColor('#1f2a44')
GOLD = HexColor('#c9a24b')
GREY = HexColor('#5a6470')
INK = HexColor('#262626')

try:
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
    CN = 'STSong-Light'
except Exception:
    CN = 'Helvetica'

# Unicode font that covers Greek letters + math symbols (for the answer key).
try:
    import matplotlib
    _MT = os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data', 'fonts', 'ttf')
    pdfmetrics.registerFont(TTFont('DejaVu', os.path.join(_MT, 'DejaVuSans.ttf')))
    pdfmetrics.registerFont(TTFont('DejaVu-Bold', os.path.join(_MT, 'DejaVuSans-Bold.ttf')))
    MATH_FONT = 'DejaVu'
    MATH_FONT_B = 'DejaVu-Bold'
except Exception:
    MATH_FONT = CN
    MATH_FONT_B = CN


# Map the PDF Symbol-font private-use characters (U+F0xx) back to real Unicode.
SYMBOL_MAP = {
    '': '×', '': '÷', '': '•',
    '': 'Δ', '': 'θ', '': 'λ', '': 'ρ', '': 'μ',
    '': 'Ω', '': 'π', '': 'α', '': 'β', '': 'γ',
    '': '>', '': '<', '': '=',
    '': '∝', '': '°', '': '±', '': '≥', '': '≤',
    '': ')', '': '[', '': ']', '': '{', '': '}',
    # fraction-bar glyphs (0xEC–0xFE) collapse to a slash
    '': '/', '': '/', '': '/', '': '/', '': '/', '': '/',
    '': ' ',
}


def fix_symbols(text):
    for k, v in SYMBOL_MAP.items():
        text = text.replace(k, v)
    text = re.sub(r'/+', '/', text)                     # collapse fraction-bar slashes
    text = re.sub(r'[-]', '', text)          # drop any remaining PUA chars
    text = re.sub(r'[ \t]+', ' ', text).strip()
    return text


def load_year(year='25'):
    mcq, theory = {}, {}
    for f in sorted(glob.glob('igcse-data/0625_*_qp_2*.json')):
        d = json.load(open(f, encoding='utf-8'))
        if d['paper'].split('/')[-1] != year:
            continue
        for q in d['questions']:
            code = q.get('code')
            if not code:
                continue
            mcq.setdefault(code, []).append({
                'qnum': q['qnum'], 'paper': d['paper'], 'paper_full': d['paper_full'],
                'answer': q.get('answer', ''), 'pdf': q['pdf'],
            })
    for f in sorted(glob.glob('igcse-data/0625_*_qp_4*.json')):
        d = json.load(open(f, encoding='utf-8'))
        if d['paper'].split('/')[-1] != year:
            continue
        for q in d['questions']:
            code = q.get('code')
            if not code:
                continue
            theory.setdefault(code, []).append({
                'qnum': q['qnum'], 'paper': d['paper'], 'paper_full': d['paper_full'],
                'title': q.get('title', ''), 'marks': q.get('marks', 0),
                'pdf': q['pdf'], 'parts': q.get('parts', []),
            })
    return mcq, theory


def q_sort_key(q):
    return (q['paper'], q['qnum'])


# Knowledge-recall prompts per topic (Chinese), shown after the vocabulary page.
RECALL = {
    "1": [
        "速度、平均速度、加速度的定义与公式",
        "速度-时间图：面积表示____，斜率表示____",
        "重量 W = ____；质量与重量的区别",
        "密度 ρ = ____",
        "力矩 = ____；物体平衡的两个条件",
        "动量 p = ____；冲量 = ____；动量守恒",
        "动能 = ____；重力势能 = ____；功 = ____；功率 = ____",
        "压强 p = ____；液体压强 Δp = ____",
    ],
    "2": [
        "固 / 液 / 气三态粒子的排列与运动",
        "气体压强产生的原因；等温时 pV = ____",
        "比热容：Q = ____；熔化 / 沸腾时温度____",
        "传导、对流、辐射三种传热方式的区别",
        "黑色 / 白色、粗糙 / 光滑表面对辐射的影响",
    ],
    "3": [
        "波速 v = ____；横波与纵波的区别",
        "反射定律；折射定律 n = ____",
        "全反射的两个条件",
        "电磁波谱按频率由低到高排列",
        "声速公式；人耳频率范围；超声频率",
        "凸透镜成像：实像与虚像的区别",
    ],
    "4": [
        "电流 I = ____；电阻 R = ____；功率 P = ____",
        "串联电路：电流____，电压____；并联电路：电流____，电压____",
        "e.m.f. 与 p.d. 的定义",
        "磁感线方向；磁极间相互作用",
        "电磁感应现象（导线切割磁感线）",
        "变压器：Vp/Vs = ____",
    ],
    "5": [
        "原子结构：质子、中子、电子",
        "质子数、核子数、同位素",
        "α、β、γ 三种辐射的性质（穿透 / 电离）",
        "半衰期的定义",
        "核裂变与核聚变",
    ],
    "6": [
        "太阳系的组成（行星、卫星、彗星等）",
        "轨道速度 v = ____",
        "红移现象与宇宙膨胀",
        "哈勃常数与宇宙年龄",
        "恒星的生命周期",
    ],
}


# English-Chinese vocabulary for each topic (shown before each topic's questions).
VOCAB = {
    "1": [
        ("speed", "速度"), ("velocity", "速度（矢量）"), ("acceleration", "加速度"),
        ("distance", "距离"), ("displacement", "位移"), ("scalar", "标量"), ("vector", "矢量"),
        ("mass", "质量"), ("weight", "重量"), ("gravitational field strength", "重力场强度"),
        ("density", "密度"), ("force", "力"), ("resultant force", "合力"),
        ("friction", "摩擦力"), ("air resistance", "空气阻力"), ("drag", "阻力"),
        ("spring constant", "弹簧常数"), ("extension", "伸长量"), ("moment", "力矩"),
        ("pivot", "支点"), ("centre of gravity", "重心"), ("equilibrium", "平衡"),
        ("momentum", "动量"), ("impulse", "冲量"), ("conservation of momentum", "动量守恒"),
        ("energy", "能量"), ("kinetic energy", "动能"), ("gravitational potential energy", "重力势能"),
        ("elastic potential energy", "弹性势能"), ("work done", "做功"), ("power", "功率"),
        ("efficiency", "效率"), ("pressure", "压强"), ("renewable", "可再生"), ("non-renewable", "不可再生"),
    ],
    "2": [
        ("temperature", "温度"), ("thermal energy", "热能"), ("internal energy", "内能"),
        ("specific heat capacity", "比热容"), ("melting", "熔化"), ("boiling", "沸腾"),
        ("evaporation", "蒸发"), ("condensation", "冷凝"), ("solidification / freezing", "凝固"),
        ("conduction", "传导"), ("convection", "对流"), ("radiation", "辐射"),
        ("infrared", "红外线"), ("conductor", "导体"), ("insulator", "绝缘体"),
        ("Brownian motion", "布朗运动"), ("particle model", "粒子模型"), ("absolute zero", "绝对零度"),
        ("kelvin", "开尔文"), ("thermal expansion", "热膨胀"),
    ],
    "3": [
        ("wave", "波"), ("wavelength", "波长"), ("frequency", "频率"), ("amplitude", "振幅"),
        ("wavefront", "波前"), ("wave speed", "波速"), ("transverse wave", "横波"),
        ("longitudinal wave", "纵波"), ("reflection", "反射"), ("refraction", "折射"),
        ("diffraction", "衍射"), ("dispersion", "色散"), ("electromagnetic spectrum", "电磁波谱"),
        ("radio waves", "无线电波"), ("microwaves", "微波"), ("infrared", "红外线"),
        ("visible light", "可见光"), ("ultraviolet", "紫外线"), ("X-rays", "X 射线"),
        ("gamma rays", "伽马射线"), ("sound", "声音"), ("ultrasound", "超声波"), ("echo", "回声"),
        ("critical angle", "临界角"), ("total internal reflection", "全反射"),
        ("refractive index", "折射率"), ("lens", "透镜"), ("converging lens", "凸透镜"),
        ("diverging lens", "凹透镜"), ("focal length", "焦距"), ("real image", "实像"),
        ("virtual image", "虚像"), ("magnifying glass", "放大镜"),
    ],
    "4": [
        ("electric charge", "电荷"), ("current", "电流"), ("potential difference (p.d.)", "电势差"),
        ("electromotive force (e.m.f.)", "电动势"), ("resistance", "电阻"), ("voltage", "电压"),
        ("circuit", "电路"), ("series", "串联"), ("parallel", "并联"), ("resistor", "电阻器"),
        ("diode", "二极管"), ("thermistor", "热敏电阻"), ("LDR", "光敏电阻"),
        ("ammeter", "电流表"), ("voltmeter", "电压表"), ("fuse", "保险丝"),
        ("magnet", "磁铁"), ("magnetic field", "磁场"), ("magnetic field lines", "磁感线"),
        ("pole", "磁极"), ("electromagnet", "电磁铁"), ("solenoid", "螺线管"),
        ("electromagnetic induction", "电磁感应"), ("generator", "发电机"), ("transformer", "变压器"),
        ("step-up", "升压"), ("step-down", "降压"), ("motor", "电动机"), ("commutator", "换向器"),
        ("brushes", "电刷"), ("earthing", "接地"),
    ],
    "5": [
        ("atom", "原子"), ("nucleus", "原子核"), ("proton", "质子"), ("neutron", "中子"),
        ("electron", "电子"), ("proton number", "质子数"), ("nucleon number", "核子数"),
        ("isotope", "同位素"), ("radioactivity", "放射性"), ("radioactive decay", "放射性衰变"),
        ("alpha particle", "α 粒子"), ("beta particle", "β 粒子"), ("gamma radiation", "γ 辐射"),
        ("half-life", "半衰期"), ("background radiation", "背景辐射"), ("ionising radiation", "电离辐射"),
        ("nuclear fission", "核裂变"), ("nuclear fusion", "核聚变"),
    ],
    "6": [
        ("solar system", "太阳系"), ("planet", "行星"), ("moon", "月球"), ("comet", "彗星"),
        ("asteroid", "小行星"), ("galaxy", "星系"), ("Milky Way", "银河系"), ("star", "恒星"),
        ("Sun", "太阳"), ("orbit", "轨道"), ("orbital speed", "轨道速度"),
        ("gravitational field", "引力场"), ("redshift", "红移"), ("Hubble constant", "哈勃常数"),
        ("Big Bang", "大爆炸"), ("CMBR", "宇宙微波背景辐射"), ("light-year", "光年"),
        ("protostar", "原恒星"), ("red giant", "红巨星"), ("white dwarf", "白矮星"),
        ("supernova", "超新星"), ("neutron star", "中子星"), ("black hole", "黑洞"),
    ],
}


# Simple Chinese hints shown above each multiple-choice question.
HINTS = {
    "1.1": "提示：读数要估读；向量有大小和方向",
    "1.2": "提示：速度 = 路程÷时间；速度-时间图面积 = 路程，斜率 = 加速度",
    "1.3": "提示：重量 W = mg；质量不变，重量随 g 变",
    "1.4": "提示：密度 ρ = m/V；密度大的物体沉",
    "1.5": "提示：力矩 = 力 × 垂直距离；合力；胡克定律 F = kx",
    "1.6": "提示：动量 p = mv；冲量 = FΔt = Δ(mv)；动量守恒",
    "1.7": "提示：功 W = Fd；动能 = ½mv²；重力势能 = mgh；能量守恒",
    "1.8": "提示：压强 p = F/A；液体压强 Δp = ρgΔh",
    "2.1": "提示：气体压强来自粒子碰撞；温度升高粒子运动变快",
    "2.2": "提示：比热容 Q = mcΔT；熔化/沸腾时温度不变",
    "2.3": "提示：传导/对流/辐射；黑色粗糙表面辐射吸收强",
    "3.1": "提示：波速 v = fλ；横波振动⊥传播，纵波振动∥传播",
    "3.2": "提示：折射 n = sin i / sin r；全反射需从密到疏且 i > 临界角",
    "3.3": "提示：所有电磁波真空速度相同；按频率排：无线电<微波<红外<可见<紫外<X<γ",
    "3.4": "提示：声速 v = fλ；人耳范围 20 Hz–20 kHz；超声 > 20 kHz",
    "4.1": "提示：磁感线 N→S；同名相斥；软铁 = 临时磁体",
    "4.2": "提示：I = Q/t；V = IR；P = IV",
    "4.3": "提示：串联电流相同，并联电压相同；分压器",
    "4.4": "提示：保险丝/接地线/双绝缘，避免触电",
    "4.5": "提示：电磁感应；变压器 Vp/Vs = Np/Ns",
    "5.1": "提示：原子结构（质子/中子/电子）；质子数 = 核电荷",
    "5.2": "提示：α/β/γ 三种辐射的穿透与电离；半衰期",
    "6.1": "提示：太阳系组成；轨道速度 v = 2πr/T",
    "6.2": "提示：红移；哈勃常数；恒星生命周期",
}


def select_balanced(by_code, n):
    """Pick n questions, cycling through subtopics (sorted) for a balanced spread."""
    remaining = {c: sorted(by_code[c], key=q_sort_key) for c in by_code if by_code[c]}
    codes = sorted(remaining.keys())
    out = []
    while len(out) < n and any(remaining.values()):
        for c in codes:
            if remaining[c]:
                out.append(remaining[c].pop(0))
                if len(out) == n:
                    break
    return out


def filter_syllabus(topics):
    return [(t, title, subs) for t, title, subs in SYLLABUS if int(t) in topics]


HEADER_H = 22    # header strip (pt) added above every question for Date / Score
BOTTOM_MARGIN = 14  # blank space below every question for the page number

def question_with_header(src_path):
    """Return a temp PDF path: the question with a Date/Score header on top and
    blank margin below (for the page number)."""
    out = '/tmp/_q_header.pdf'
    src = pymupdf.open(src_path)
    new = pymupdf.open()
    for page in src:
        w, h = page.rect.width, page.rect.height
        np = new.new_page(width=w, height=h + HEADER_H + BOTTOM_MARGIN)
        np.insert_text((36, HEADER_H - 10),
                       "Date: ______________   Score: ____________",
                       fontsize=8.5, fontname="helv", color=(0.30, 0.30, 0.30))
        np.draw_rect(pymupdf.Rect(36, HEADER_H - 3, w - 36, HEADER_H - 2.2),
                     color=None, fill=(0.72, 0.72, 0.72))
        np.show_pdf_page(pymupdf.Rect(0, HEADER_H, w, HEADER_H + h), src, page.number)
    new.save(out)
    new.close()
    src.close()
    return out


def add_page_numbers(path):
    """Stamp a page number at the bottom centre of every page."""
    doc = pymupdf.open(path)
    for i, page in enumerate(doc):
        w = page.rect.width
        h = page.rect.height
        txt = str(i + 1)
        tw = pymupdf.get_text_length(txt, fontname='helv', fontsize=9)
        page.insert_text((w / 2 - tw / 2, h - 22), txt, fontsize=9, fontname='helv',
                         color=(0.42, 0.42, 0.42))
    doc.saveIncr()
    doc.close()


MCQ_DPI = 200

# Source PDFs (copied verbatim) and their per-topic page indices (0-based).
VOCAB_SRC = "IG-英文词汇表.pdf"
RECALL_SRC = "IG总复习知识点默写.pdf"
VOCAB_PAGES = {"1": [0, 1, 2, 3, 4, 5], "2": [6, 7], "3": [8, 9, 10], "4": [10, 11],
               "5": [12, 13], "6": [13]}
RECALL_PAGES = {"1": [0], "2": [1], "3": [2, 3, 4, 5, 6, 7],
                "4": [8, 9, 10, 11, 12], "5": [13, 14], "6": [15, 16, 17, 18]}


def _src_page_png(src, idx):
    doc = pymupdf.open(src)
    page = doc[idx]
    w, h = page.rect.width, page.rect.height
    out = '/tmp/_src_%d.png' % idx
    # crop the bottom ~36pt to drop the source document's own page number
    page.get_pixmap(dpi=200, clip=pymupdf.Rect(0, 0, w, h - 36)).save(out)
    doc.close()
    return out, w, h - 36


def source_page_fns(src, indices):
    """Return canvas draw functions that place each source page (verbatim) on A4."""
    fns = []
    for idx in indices:
        png, w, h = _src_page_png(src, idx)
        scale = min(555.0 / w, 790.0 / h)
        dw, dh = w * scale, h * scale
        def draw(c, png=png, dw=dw, dh=dh):
            c.setFillColor(HexColor('#ffffff')); c.rect(0, 0, W, H, fill=1, stroke=0)
            c.drawImage(png, (W - dw) / 2, H - 45 - dh, width=dw, height=dh)
            c.showPage()
        fns.append(draw)
    return fns

def _render_mcq(q, idx):
    doc = pymupdf.open(q['pdf'])
    page = doc[0]
    w, h = page.rect.width, page.rect.height
    out = '/tmp/_mcq_%d.png' % idx
    page.get_pixmap(dpi=MCQ_DPI).save(out)
    doc.close()
    return out, w, h


def mcq_page_fns(mcq_qs, code, banner=None):
    """Pack several MCQs per page (each with note lines below).
    Returns a list of reportlab canvas draw functions, one per page.
    If `banner` is given (a 2-tuple of strings), it is drawn as a compact
    subtopic header on the first page instead of a separate divider page."""
    items = []
    for i, q in enumerate(mcq_qs):
        png, w, h = _render_mcq(q, i)
        scaled_h = h * (500.0 / w)   # fit to 500pt content width
        items.append({'q': q, 'png': png, 'h': scaled_h})

    usable_first = (H - 140) if banner else (H - 102)
    usable_rest = H - 102
    pages, cur, cur_h = [], [], 0
    usable = usable_first
    for it in items:
        block_h = it['h'] + 58   # image + label(12) + note lines(3*12) + gaps
        if cur and cur_h + block_h > usable:
            pages.append(cur)
            cur, cur_h = [], 0
            usable = usable_rest
        cur.append(it)
        cur_h += block_h
    if cur:
        pages.append(cur)

    def _date_line(c, y):
        c.setFont('Helvetica', 9); c.setFillColor(HexColor('#5a6470'))
        c.drawString(47, y, 'Date: _________________   Score: ____________')

    fns = []
    for pi, pg in enumerate(pages):
        def draw(c, pg=pg, pi=pi):
            c.setFillColor(HexColor('#ffffff')); c.rect(0, 0, W, H, fill=1, stroke=0)
            if pi == 0 and banner:
                c.setFillColor(NAVY); c.setFont('Helvetica-Bold', 14)
                c.drawString(47, H - 34, banner[0])
                c.setFont('Helvetica', 9); c.setFillColor(GREY)
                c.drawString(47, H - 50, banner[1])
                c.setStrokeColor(GOLD); c.setLineWidth(2)
                c.line(47, H - 58, 98, H - 58)
                _date_line(c, H - 72)
                y = H - 88
            else:
                _date_line(c, H - 34)
                y = H - 48
            for it in pg:
                c.drawImage(it['png'], 47, y - it['h'], width=500, height=it['h'])
                y -= it['h'] + 4
                c.setFont('Helvetica', 8); c.setFillColor(GREY)
                c.drawString(47, y, '%s  Q%s' % (it['q']['paper'], it['q']['qnum']))
                y -= 12
                c.setStrokeColor(HexColor('#d3d7dd')); c.setLineWidth(0.6)
                for k in range(3):
                    c.line(47, y - k * 12, 547, y - k * 12)
                y -= 3 * 12 + 6
            c.showPage()
        fns.append(draw)
    return fns


# ---------------------------------------------------------------- drawing
def cover(c, title, subtitle, year='25'):
    # medium-tone cover with a navy title band + name/class blanks
    c.setFillColor(HexColor('#c6d1de')); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(NAVY); c.rect(0, H - 150, W, 150, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(0, H - 150, W, 5, fill=1, stroke=0)
    c.setFillColor(HexColor('#ffffff'))
    size = 30
    while size > 14 and stringWidth(title, 'Helvetica-Bold', size) > W - 110:
        size -= 2
    c.setFont('Helvetica-Bold', size)
    c.drawString(55, H - 92, title)
    c.setFont('Helvetica', 11); c.setFillColor(HexColor('#d7dee6'))
    c.drawString(55, H - 122, subtitle)
    # name / class blanks
    c.setFont('Helvetica-Bold', 13); c.setFillColor(NAVY)
    c.drawString(55, H - 200, 'Name:')
    c.drawString(55, H - 245, 'Class:')
    c.setStrokeColor(HexColor('#8f9aa8')); c.setLineWidth(1)
    c.line(130, H - 205, 520, H - 205)
    c.line(130, H - 250, 520, H - 250)
    # footer
    c.setFont('Helvetica', 10); c.setFillColor(HexColor('#4a5560'))
    c.drawString(55, 70, 'Cambridge IGCSE Physics 0625 — 20%s (Feb/Mar, May/Jun, Oct/Nov)' % year)
    c.setFont(CN, 13); c.setFillColor(HexColor('#4a5560'))
    c.drawString(55, 46, '练习册')


def toc_page(c, syl, mcq, theory, pages_by_code, offset, vocab_pages=None, recall_page=None):
    c.setFillColor(HexColor('#ffffff')); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(NAVY); c.setFont('Helvetica-Bold', 24)
    c.drawString(55, H - 60, 'Contents')
    c.setFont('Helvetica', 11); c.setFillColor(GREY)
    c.drawString(55, H - 82, 'Topic · Subtopic · page')
    y = H - 118
    for topic, title, subs in syl:
        if y < 70:
            c.showPage(); y = H - 60
        c.setFont('Helvetica-Bold', 13); c.setFillColor(NAVY)
        c.drawString(55, y, '%s  %s' % (topic, title))
        y -= 20
        c.setFont('Helvetica', 10); c.setFillColor(INK)
        vp = (vocab_pages or {}).get(topic)
        if vp is not None:
            c.setFont('Helvetica-Bold', 10); c.setFillColor(INK)
            c.drawString(55, y, '   Vocabulary ')
            c.setFont(CN, 10); c.setFillColor(GREY)
            c.drawString(55 + stringWidth('   Vocabulary ', 'Helvetica-Bold', 10), y, '词汇表')
            c.setFont('Helvetica', 10); c.setFillColor(INK)
            c.drawString(520, y, str(offset + vp))
            y -= 15
        for code, sub in subs:
            n = len(mcq.get(code, [])) + len(theory.get(code, []))
            if n == 0:
                continue
            c.drawString(55, y, '   %s  %s' % (code, sub))
            pg = pages_by_code.get(code)
            if pg is not None:
                c.drawString(520, y, str(offset + pg))
            y -= 15
            if y < 70:
                c.showPage(); y = H - 60
        y -= 8
    if recall_page is not None:
        if y < 90:
            c.showPage(); y = H - 60
        c.setFont('Helvetica-Bold', 13); c.setFillColor(NAVY)
        c.drawString(55, y, 'Knowledge Recall ')
        c.setFont(CN, 13); c.setFillColor(GREY)
        c.drawString(55 + stringWidth('Knowledge Recall ', 'Helvetica-Bold', 13), y, '知识点默写')
        c.setFont('Helvetica', 13); c.setFillColor(NAVY)
        c.drawString(520, y, str(offset + recall_page))
    c.showPage()


def topic_div(c, topic, title, n):
    c.setFillColor(HexColor('#eef1f5')); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(NAVY); c.rect(0, H - 14, W, 14, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(0, H - 18, W, 4, fill=1, stroke=0)
    c.setFillColor(NAVY)
    text = '%s  %s' % (topic, title)
    size = 30
    while size > 14 and stringWidth(text, 'Helvetica-Bold', size) > W - 110:
        size -= 2
    c.setFont('Helvetica-Bold', size)
    c.drawString(55, H - 160, text)
    c.setFont('Helvetica', 13); c.setFillColor(GREY)
    c.drawString(55, H - 195, '%d questions · Paper 2 & Paper 4' % n)


def vocab_page(c, topic, title, vocab):
    """Two-column English-Chinese vocabulary list for a topic."""
    c.setFillColor(HexColor('#f7f8fa')); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(NAVY); c.rect(0, H - 56, W, 56, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(0, H - 56, W, 4, fill=1, stroke=0)
    c.setFillColor(HexColor('#ffffff')); c.setFont('Helvetica-Bold', 19)
    c.drawString(55, H - 36, 'Vocabulary · Topic %s  %s' % (topic, title))
    c.setFont(CN, 12); c.setFillColor(HexColor('#e8d9b0'))
    c.drawString(55, H - 88, '词汇表（中英对照）')
    half = (len(vocab) + 1) // 2
    cols = [vocab[:half], vocab[half:]]
    col_x = [52, 312]
    for ci, col in enumerate(cols):
        y = H - 120
        for en, zh in col:
            c.setFont('Helvetica-Bold', 11.5); c.setFillColor(INK)
            c.drawString(col_x[ci], y, en)
            c.setFont(CN, 11.5); c.setFillColor(GREY)
            c.drawString(col_x[ci] + 184, y, zh)
            y -= 19
    c.showPage()


def recall_page(c, topic, prompts):
    """Knowledge-recall worksheet: prompts with blank ruled lines."""
    c.setFillColor(HexColor('#fbfbfc')); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(NAVY); c.rect(0, H - 56, W, 56, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(0, H - 56, W, 4, fill=1, stroke=0)
    c.setFillColor(HexColor('#ffffff')); c.setFont('Helvetica-Bold', 19)
    c.drawString(55, H - 36, 'Knowledge Recall · Topic %s' % topic)
    c.setFont(CN, 13); c.setFillColor(HexColor('#e8d9b0'))
    c.drawString(55, H - 88, '知识点默写（凭记忆写出定义 / 公式）')
    y = H - 122
    for p in prompts:
        if y < 110:
            c.showPage()
            y = H - 60
        c.setFont(CN, 11); c.setFillColor(INK)
        c.drawString(55, y, p)
        y -= 18
        c.setStrokeColor(HexColor('#d3d7dd')); c.setLineWidth(0.6)
        for k in range(3):
            c.line(55, y - k * 15, 545, y - k * 15)
        y -= 52
    c.showPage()


def sub_head(c, code, sub, mcq_qs, th_qs):
    c.setFillColor(HexColor('#ffffff')); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(55, H - 90, 4, 34, fill=1, stroke=0)
    c.setFillColor(NAVY)
    text = '%s  %s' % (code, sub)
    size = 20
    while size > 11 and stringWidth(text, 'Helvetica-Bold', size) > W - 130:
        size -= 1
    c.setFont('Helvetica-Bold', size)
    c.drawString(70, H - 72, text)
    c.setFont('Helvetica', 10.5); c.setFillColor(GREY)
    c.drawString(70, H - 96, '%d MCQ + %d theory questions · Paper 2 & Paper 4' % (len(mcq_qs), len(th_qs)))
    syl = SUBSUBS.get(code)
    pts = []
    if syl:
        pts = syl.get('points', [])
        if syl.get('subsubs'):
            pts = [p for ss in syl['subsubs'] for p in ss['points']]
    c.setFont('Helvetica', 9); c.setFillColor(HexColor('#777777'))
    y = H - 120
    for p in pts[:7]:
        c.drawString(70, y, '· ' + p[:115])
        y -= 13


def ans_div(c):
    c.setFillColor(NAVY); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(0, H - 10, W, 10, fill=1, stroke=0)
    c.setFillColor(HexColor('#ffffff')); c.setFont('Helvetica-Bold', 34)
    c.drawString(55, H - 180, 'Answer Key')


def wrap(text, width=100):
    words = text.split()
    lines, cur = [], ''
    for w in words:
        if len(cur) + len(w) + 1 <= width:
            cur = (cur + ' ' + w).strip()
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def answers(c, topic, title, code, mcq_qs, th_qs):
    y = H - 60
    c.setFillColor(NAVY); c.setFont('Helvetica-Bold', 15)
    c.drawString(55, y, 'Answers — %s %s' % (topic, title))
    y -= 24
    c.setFont('Helvetica-Bold', 12); c.setFillColor(GOLD)
    c.drawString(55, y, '%s  %s' % (code, SUB_LABELS.get(code, '')))
    y -= 20
    c.setFont('Helvetica', 9.5); c.setFillColor(INK)
    for q in sorted(mcq_qs, key=q_sort_key):
        if y < 60:
            c.showPage(); y = H - 60
        c.drawString(55, y, '%s  (Q%s):  %s' % (q['paper'], q['qnum'], q['answer'] or '—'))
        y -= 14
    for q in sorted(th_qs, key=q_sort_key):
        head = fix_symbols('%s  Q%s — %s  [%d marks]' % (q['paper'], q['qnum'], q['title'], q['marks']))
        for ln in wrap(head, 100):
            if y < 60:
                c.showPage(); y = H - 60
            c.setFont(MATH_FONT_B, 9.5); c.drawString(55, y, ln); y -= 14
        c.setFont(MATH_FONT, 9.5)
        for p in q['parts']:
            for ln in wrap('%s [%d] %s' % (p['label'], p['marks'], fix_symbols(p['answer'])), 104):
                if y < 60:
                    c.showPage(); y = H - 60
                c.drawString(70, y, ln); y -= 13
        y -= 4
    c.showPage()


# ---------------------------------------------------------------- assembly
class Builder:
    def __init__(self):
        self.writer = PdfWriter()
        self.pages = 0

    def add_pdf(self, path):
        if not os.path.exists(path):
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


def build(out_path, with_answers, topics, cover_title, cover_subtitle, with_schedule=False, compact=False, year='25'):
    mcq, theory = load_year(year)
    syl = filter_syllabus(topics)
    weeks = None
    if with_schedule:
        weeks = build_schedule(mcq, theory)

    body = Builder()
    pages_by_code = {}
    vocab_pages = {}
    recall_page = None

    for topic, title, subs in syl:
        if compact:
            topic_mcq = {c: mcq.get(c, []) for c, _ in subs}
            topic_th = {c: theory.get(c, []) for c, _ in subs}
            sel_mcq = select_balanced(topic_mcq, 10)
            sel_th = select_balanced(topic_th, 3)
            body.add_canvas(lambda c, topic=topic, title=title, n=len(sel_mcq) + len(sel_th):
                            topic_div(c, topic, title, n))
            for q in sel_mcq:
                body.add_pdf(question_with_header(q['pdf']))
            for q in sel_th:
                body.add_pdf(question_with_header(q['pdf']))
        else:
            n = sum(len(mcq.get(c, [])) + len(theory.get(c, [])) for c, _ in subs)
            body.add_canvas(lambda c, topic=topic, title=title, n=n: topic_div(c, topic, title, n))
            vocab = VOCAB.get(topic, [])
            if vocab:
                vocab_pages[topic] = body.pages + 1
                body.add_canvas(lambda c, topic=topic, title=title, vocab=vocab:
                                vocab_page(c, topic, title, vocab))
            for code, sub in subs:
                mcq_qs = sorted(mcq.get(code, []), key=q_sort_key)
                th_qs = sorted(theory.get(code, []), key=q_sort_key)
                if not mcq_qs and not th_qs:
                    continue
                pages_by_code[code] = body.pages + 1
                banner = ('%s  %s' % (code, sub),
                          '%d MCQ + %d theory · Paper 2 & Paper 4' % (len(mcq_qs), len(th_qs)))
                if mcq_qs:
                    for draw in mcq_page_fns(mcq_qs, code, banner=banner):
                        body.add_canvas(draw)
                for q in th_qs:
                    body.add_pdf(question_with_header(q['pdf']))

    if with_answers:
        body.add_canvas(ans_div)
        for topic, title, subs in syl:
            for code, sub in subs:
                mcq_qs = sorted(mcq.get(code, []), key=q_sort_key)
                th_qs = sorted(theory.get(code, []), key=q_sort_key)
                if not mcq_qs and not th_qs:
                    continue
                body.add_canvas(lambda c, topic=topic, title=title, code=code, mcq_qs=mcq_qs, th_qs=th_qs:
                                answers(c, topic, title, code, mcq_qs, th_qs))

    # Knowledge-recall worksheet at the very end (whole source file, verbatim).
    def recall_div(c):
        c.setFillColor(NAVY); c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(GOLD); c.rect(0, H - 10, W, 10, fill=1, stroke=0)
        c.setFillColor(HexColor('#ffffff')); c.setFont('Helvetica-Bold', 34)
        c.drawString(55, H - 180, 'Knowledge Recall')
        c.setFont(CN, 18); c.setFillColor(HexColor('#e8d9b0'))
        c.drawString(55, H - 225, '知识点默写')
    recall_page = body.pages + 1
    body.add_canvas(recall_div)
    for draw in source_page_fns(RECALL_SRC, list(range(19))):
        body.add_canvas(draw)

    # front matter
    front = Builder()
    front.add_canvas(lambda c: cover(c, cover_title, cover_subtitle, year))
    if with_schedule:
        front.add_canvas(lambda c: schedule_page(c, weeks, mcq, theory))

    tmp = Builder()
    tmp.add_canvas(lambda c: toc_page(c, syl, mcq, theory, pages_by_code, offset=0,
                                      vocab_pages=vocab_pages, recall_page=recall_page))
    toc_pages = tmp.pages
    offset = 1 + (1 if with_schedule else 0) + toc_pages

    front.add_canvas(lambda c: toc_page(c, syl, mcq, theory, pages_by_code, offset=offset,
                                        vocab_pages=vocab_pages, recall_page=recall_page))

    final = PdfWriter()
    for p in front.writer.pages:
        final.add_page(p)
    for p in body.writer.pages:
        final.add_page(p)

    with open(out_path, 'wb') as f:
        final.write(f)
    add_page_numbers(out_path)
    print('wrote %s (%d pages)' % (out_path, len(final.pages)))


def build_schedule(mcq, theory, n_weeks=16):
    weeks = [[] for _ in range(n_weeks)]
    wi = 0
    for topic, title, subs in SYLLABUS:
        for code, sub in subs:
            total = len(mcq.get(code, [])) + len(theory.get(code, []))
            if total == 0:
                continue
            weeks[wi].append(code)
            if sum(len(mcq.get(c, [])) + len(theory.get(c, [])) for c in weeks[wi]) >= 22 and wi < n_weeks - 1:
                wi += 1
    while weeks and not weeks[-1]:
        weeks.pop()
    return weeks


def schedule_page(c, weeks, mcq, theory):
    c.setFillColor(HexColor('#ffffff')); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(NAVY); c.setFont('Helvetica-Bold', 24)
    c.drawString(55, H - 60, 'Study Schedule')
    c.setFont('Helvetica', 11); c.setFillColor(GREY)
    c.drawString(55, H - 82, '4 months · 7 lessons per week · Paper 2 & Paper 4 mixed by topic')
    c.setStrokeColor(NAVY); c.line(55, H - 92, 555, H - 92)
    cols = [(55, 'Week'), (115, 'Month'), (175, 'Topics'), (230, 'Subtopics')]
    c.setFont('Helvetica-Bold', 11); c.setFillColor(NAVY)
    for x, h in cols:
        c.drawString(x, H - 110, h)
    y = H - 128
    c.setFont('Helvetica', 9.5); c.setFillColor(INK)
    for i, wk in enumerate(weeks, start=1):
        month = (i - 1) // 4 + 1
        topics = ','.join(sorted(set(code.split('.')[0] for code in wk)))
        subs = ', '.join(wk)
        c.drawString(55, y, str(i))
        c.drawString(115, y, 'M%d' % month)
        c.drawString(175, y, topics)
        c.drawString(230, y, subs[:70])
        y -= 16
    c.showPage()


if __name__ == '__main__':
    # 1. Compact workbook — all 6 topics, 10 MCQ + 3 theory each
    build('IGCSE_0625_2025_Compact.pdf', with_answers=False,
          topics=(1, 2, 3, 4, 5, 6),
          cover_title='IGCSE Physics 0625',
          cover_subtitle='2025 Compact Workbook · 10 multiple choice + 3 theory questions per topic',
          compact=True)
    build('IGCSE_0625_2025_Compact_Answers.pdf', with_answers=True,
          topics=(1, 2, 3, 4, 5, 6),
          cover_title='IGCSE Physics 0625',
          cover_subtitle='2025 Compact Workbook · 10 multiple choice + 3 theory questions per topic',
          compact=True)

    # 2. Full workbook — topics 1-4 only, no schedule, retitled
    build('IGCSE_0625_2025_Workbook.pdf', with_answers=False,
          topics=(1, 2, 3, 4),
          cover_title='IGCSE Physics Workbook Topic 1-4',
          cover_subtitle='2024 · Paper 2 (Multiple Choice) + Paper 4 (Theory) mixed by topic',
          with_schedule=False, year='24')
    build('IGCSE_0625_2025_Workbook_Answers.pdf', with_answers=True,
          topics=(1, 2, 3, 4),
          cover_title='IGCSE Physics Workbook Topic 1-4',
          cover_subtitle='2024 · Paper 2 (Multiple Choice) + Paper 4 (Theory) mixed by topic',
          with_schedule=False, year='24')
