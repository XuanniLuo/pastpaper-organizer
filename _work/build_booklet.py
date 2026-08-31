# -*- coding: utf-8 -*-
"""Build the combined A2 workbook: per topic -> PPT slides (2-up) -> 知识点 -> past papers."""
import json, os, re, io
import zipfile
import xml.etree.ElementTree as ET
from PIL import Image, ImageEnhance
import matplotlib
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from pypdf import PdfReader, PdfWriter
from summary_expanded import EXPANDED

# ---------- fonts ----------
MT = os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data', 'fonts', 'ttf')
pdfmetrics.registerFont(TTFont('DejaVu', os.path.join(MT, 'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', os.path.join(MT, 'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFont(TTFont('DejaVu-Oblique', os.path.join(MT, 'DejaVuSans-Oblique.ttf')))
pdfmetrics.registerFontFamily('DejaVu', normal='DejaVu', bold='DejaVu-Bold', italic='DejaVu-Oblique', boldItalic='DejaVu-Bold')
CN_FONT = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
if os.path.exists(CN_FONT):
    pdfmetrics.registerFont(TTFont('CN', CN_FONT))
else:
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

W, H = A4
OUT = '26年A2预估考_circular_motion_gravitational_field_oscillation.pdf'
NAVY = HexColor('#1f2a44')
GOLD = HexColor('#c9a24b')
GREY = HexColor('#5a6470')

# topic -> (name, cn, pptx)
TOPICS = {
    '12': ('Circular Motion', '圆周运动', os.path.expanduser('~/Desktop/new a2/c16-high-quality-non-editable.pptx')),
    '13': ('Gravitational Fields', '引力场', os.path.expanduser('~/Desktop/new a2/c17-high-quality-non-editable.pptx')),
    '17': ('Oscillations', '振动', os.path.expanduser('~/Desktop/new a2/c18-high-quality-non-editable.pptx')),
}

# ---------- helpers ----------
def sanitize(html):
    t = re.sub(r'&(?!(?:amp|lt|gt|quot|apos|#\d+);)', '&amp;', html)
    t = t.replace('<br>', '<br/>').replace('<br />', '<br/>')
    return t

def P(font='DejaVu', size=10.5, leading=15, color='#1a1a1a', align=TA_LEFT):
    return ParagraphStyle('x', fontName=font, fontSize=size, leading=leading,
                          textColor=HexColor(color), alignment=align, spaceAfter=4)

def _nob(t): return t.replace('<b>', '').replace('</b>', '')

# ---------- cover ----------
def build_cover():
    c = rl_canvas.Canvas('_work/_cover.pdf', pagesize=A4)
    c.setFillColor(NAVY); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(GOLD); c.rect(0, H*0.66, W, 3, stroke=0, fill=1); c.rect(0, H*0.655, W, 1, stroke=0, fill=1)
    c.setFillColor(HexColor('#ffffff'))
    c.setFont('CN', 44); c.drawCentredString(W/2, H*0.72, '2026｜A2预估考')
    c.setFont('DejaVu-Bold', 26); c.drawCentredString(W/2, H*0.58, 'WorkBook')
    c.setFont('DejaVu', 13); c.drawCentredString(W/2, H*0.52, 'Circular Motion  ·  Gravitational Fields  ·  Oscillations')
    c.setFont('DejaVu', 11); c.drawCentredString(W/2, H*0.47, 'slides  ·  formulae & definitions  ·  paper4 2024–2026')
    c.setFillColor(HexColor('#8fa3ad')); c.setFont('DejaVu', 10)
    c.drawCentredString(W/2, H*0.08, 'CIE 9702 A Level Physics · Paper 4')
    c.showPage(); c.save()

# ---------- TOC (two-level) ----------
def build_toc(sections):
    c = rl_canvas.Canvas('_work/_toc.pdf', pagesize=A4)
    c.setFillColor(HexColor('#ffffff')); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFont('DejaVu-Bold', 20); c.setFillColor(NAVY); c.drawString(18*mm, H-26*mm, 'Contents')
    c.setStrokeColor(GOLD); c.setLineWidth(2); c.line(18*mm, H-30*mm, W-18*mm, H-30*mm)
    y = H - 46*mm
    for name, cn, subs in sections:  # subs = list of (label, page)
        c.setFillColor(NAVY); c.setFont('DejaVu-Bold', 14)
        c.drawString(18*mm, y, name)
        y -= 8*mm
        for label, page in subs:
            c.setFillColor(HexColor('#333333')); c.setFont('CN', 11.5)
            c.drawString(26*mm, y, label)
            c.setFillColor(GREY); c.setFont('DejaVu', 11.5)
            c.drawRightString(W-18*mm, y, str(page))
            # dots
            lw = c.stringWidth(label, 'CN', 11.5)
            num_w = c.stringWidth(str(page), 'DejaVu', 11.5)
            x0, x1 = 26*mm + lw + 6, W-18*mm - num_w - 6
            c.setFillColor(GOLD); c.setFont('DejaVu', 8.5)
            x = x0
            while x + 3 < x1:
                c.drawString(x, y-1, '.'); x += 5
            y -= 6.5*mm
        y -= 5*mm
    c.showPage(); c.save()

# ---------- topic title page ----------
def build_topic_title(topic):
    name = TOPICS[topic][0]
    cn = TOPICS[topic][1]
    out = f'_work/_topic_{topic}.pdf'
    c = rl_canvas.Canvas(out, pagesize=A4)
    c.setFillColor(NAVY); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(GOLD); c.rect(0, H*0.56, W, 2.5, stroke=0, fill=1)
    c.setFillColor(HexColor('#ffffff'))
    c.setFont('DejaVu-Bold', 30); c.drawCentredString(W/2, H*0.52, f'{topic} · {name}')
    c.setFont('DejaVu', 11); c.drawCentredString(W/2, H*0.44, 'slides → formulae & definitions → paper4 2024–2026')
    c.showPage(); c.save()
    return out

# ---------- PPT slides 2-up ----------
def slide_images(pptx):
    z = zipfile.ZipFile(pptx)
    slides = sorted([n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)],
                    key=lambda n: int(re.search(r'(\d+)', n.split('/')[-1]).group(1)))
    out = []
    for s in slides:
        base = os.path.basename(s).replace('.xml', '')
        rels_path = f'ppt/slides/_rels/{base}.xml.rels'
        if rels_path in z.namelist():
            rels = ET.fromstring(z.read(rels_path))
            for rel in rels:
                if rel.get('Type', '').endswith('/image'):
                    media = os.path.normpath(os.path.join('ppt/slides', rel.get('Target')))
                    if media in z.namelist():
                        out.append(z.read(media)); break
    return out

def build_slides_2up(pptx, out):
    import pymupdf
    raw = slide_images(pptx)
    # downscale + JPEG-compress each slide to keep the PDF small
    imgs = []
    for b in raw:
        im = Image.open(io.BytesIO(b)).convert('RGB')
        if im.width > 1280:
            im = im.resize((1280, int(im.height * 1280 / im.width)))
        buf = io.BytesIO()
        im.save(buf, 'JPEG', quality=82)
        imgs.append(buf.getvalue())
    A4w, A4h = 595.3, 841.9
    margin, gap = 22, 10
    sw = A4w - 2*margin
    sh = sw * 9/16
    top = (A4h - (2*sh + gap)) / 2
    doc = pymupdf.open()
    for i in range(0, len(imgs), 2):
        page = doc.new_page(width=A4w, height=A4h)
        page.insert_image(pymupdf.Rect(margin, top, margin+sw, top+sh), stream=imgs[i])
        if i+1 < len(imgs):
            y2 = top + sh + gap
            page.insert_image(pymupdf.Rect(margin, y2, margin+sw, y2+sh), stream=imgs[i+1])
    doc.save(out, garbage=3, deflate=True); doc.close()
    return len(PdfReader(out).pages)

# ---------- per-topic summary (知识点) ----------
def build_topic_summary(topic):
    sec = next(s for s in EXPANDED if s['topic'] == topic)
    doc = SimpleDocTemplate(f'_work/_summary_{topic}.pdf', pagesize=A4,
                            leftMargin=18*mm, rightMargin=18*mm, topMargin=16*mm, bottomMargin=16*mm)
    flow = []
    h = Paragraph(f"Formulae &amp; Definitions — Topic {sec['topic']} · {sec['name']}",
                  P(font='DejaVu-Bold', size=15, color='#1f2a44'))
    h.style.alignment = TA_CENTER
    flow.append(h); flow.append(Spacer(1, 12))
    for lead, rest in sec['points']:
        flow.append(Paragraph(f"<font color='#c9a24b'>{_nob(lead)}</font>  {sanitize(_nob(rest))}",
                              P(font='CN', size=9.8, leading=13.8, color='#222222')))
    flow.append(Spacer(1, 6))
    box = Table([[Paragraph(f"<font color='#c9a24b'>点评 · Insight</font><br/>{sanitize(sec['insight'])}",
                            P(font='CN', size=9.5, leading=14.5, color='#6b5420'))]], colWidths=[W-36*mm])
    box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor('#f7efd9')),
        ('BOX', (0,0), (-1,-1), 0.8, GOLD),
        ('LEFTPADDING', (0,0), (-1,-1), 10), ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    flow.append(box)
    doc.build(flow)
    return len(PdfReader(f'_work/_summary_{topic}.pdf').pages)

# ---------- markscheme ----------
def build_markscheme(q):
    doc = SimpleDocTemplate('_work/_ms.pdf', pagesize=A4,
                            leftMargin=18*mm, rightMargin=18*mm, topMargin=14*mm, bottomMargin=14*mm)
    flow = []
    flow.append(Paragraph(f"<b>Markscheme</b>  —  {q['paper']} · {q['qnum']}", P(font='DejaVu-Bold', size=13, color='#1f2a44')))
    flow.append(Paragraph(sanitize(q['title']), P(size=10, color='#5a6470')))
    flow.append(Spacer(1, 8))
    for p in q['parts']:
        flow.append(Paragraph(f"<b>{p['label']}</b>   <font color='#c9a24b'>[{p['marks']} mark{'' if p['marks']==1 else 's'}]</font>",
                              P(font='DejaVu-Bold', size=10.5, color='#1f2a44')))
        flow.append(Paragraph(sanitize(p['answer']), P(size=10, leading=14.5)))
        flow.append(Spacer(1, 7))
    doc.build(flow)

def build_questions_pdf(topic, qs, include_ms=True):
    writer = PdfWriter()
    for q in qs:
        for pg in PdfReader(q['pdf']).pages:
            writer.add_page(pg)
        if include_ms:
            build_markscheme(q)
            for pg in PdfReader('_work/_ms.pdf').pages:
                writer.add_page(pg)
    tag = '' if include_ms else '_noms'
    out = f'_work/_questions_{topic}{tag}.pdf'
    with open(out, 'wb') as f:
        writer.write(f)
    return len(writer.pages)

# ---------- main ----------
def main(include_ms=True):
    all_q = json.load(open('_work/booklet_questions.json'))
    def year_of(q): return int(q['paper'].split('/')[-1])
    def qnum_of(q): return int(re.sub(r'\D', '', q['qnum']))
    all_q.sort(key=lambda q: (int(q['topic']), year_of(q), qnum_of(q)))

    out_file = OUT if include_ms else OUT.replace('.pdf', '_no_markscheme.pdf')

    sections = []  # (name, cn, [(label, page), ...])
    build_cover()
    writer = PdfWriter()
    # cover + toc placeholders; we'll assemble after computing pages
    page = 3  # cover=1, toc=2

    pieces = []
    for topic in ['12', '13', '17']:
        name, cn, pptx = TOPICS[topic]
        qs = [q for q in all_q if q['topic'] == topic]
        title_pdf = build_topic_title(topic)
        T = len(PdfReader(title_pdf).pages)
        S = build_slides_2up(pptx, f'_work/_slides_{topic}.pdf')
        K = build_topic_summary(topic)
        Q = build_questions_pdf(topic, qs, include_ms)

        subs = [('slides', page), ('formulae & definitions', page + T + S), ('paper4 2024-2026', page + T + S + K)]
        sections.append((f'Topic {topic} · {name}', cn, subs))
        qtag = '' if include_ms else '_noms'
        pieces.append((title_pdf, '_work/_slides_%s.pdf' % topic, '_work/_summary_%s.pdf' % topic, '_work/_questions_%s%s.pdf' % (topic, qtag)))
        page += T + S + K + Q

    build_toc(sections)

    for pg in PdfReader('_work/_cover.pdf').pages:
        writer.add_page(pg)
    for pg in PdfReader('_work/_toc.pdf').pages:
        writer.add_page(pg)
    for t, s, k, q in pieces:
        for f in [t, s, k, q]:
            for pg in PdfReader(f).pages:
                writer.add_page(pg)
    with open(out_file, 'wb') as f:
        writer.write(f)
    print(f'Wrote {out_file}: {len(writer.pages)} pages, {len(all_q)} questions')
    for name, cn, subs in sections:
        print(f'  {name}: {subs}')

if __name__ == '__main__':
    import sys
    main(include_ms=('--no-ms' not in sys.argv))
