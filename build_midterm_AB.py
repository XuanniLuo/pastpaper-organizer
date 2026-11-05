# -*- coding: utf-8 -*-
"""
Build a second A2 mid-term paper (AB卷, 60 min) from 2022/2023 9702 Paper 4
questions on topics 12/13/17 — parallel to the first paper but with different
questions. Reuses the DEPU-letterhead rendering from build_midterm_2022_23.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pymupdf
from PIL import Image, ImageDraw, ImageFont
from build_midterm_2022_23 import (
    HERE, LOGO, DPI, A4_PT, A4_PX, LOGO_W_PX, LOGO_H_PX, CROP_TOP_PX,
    NAVY, GOLD, GREY, DARK, _pt, _wrap, _font, raster_page,
    compose_question_page, compose_ms_page, edit_marks,
)

CN_FONT = '/System/Library/Fonts/STHeiti Light.ttc'


def _cn(size):
    return ImageFont.truetype(CN_FONT, size)


QUESTIONS = [
    {'num': 1, 'topic': 'Motion in a circle', 'marks': 20,
     'title': 'Conical pendulum on a spring — tension, spring constant & circular motion',
     'slice': '9702_s23_qp_41_Q2_Motion_in_a_circle.pdf',
     'new_parts': [5, 2, 3, 3, 3, 4], 'old_total': 12,
     'ms': '9702_s23_ms_41.pdf', 'ms_pages': [7, 8]},
    {'num': 2, 'topic': 'Gravitational fields', 'marks': 20,
     'title': 'Gravitational field lines & circular orbits — planet mass from r³–1/ω² graph',
     'slice': '9702_m22_qp_42_Q1_Gravitational_fields.pdf',
     'new_parts': [4, 4, 4, 2, 6], 'old_total': 10,
     'ms': '9702_m22_ms_42.pdf', 'ms_pages': [6, 7]},
    {'num': 3, 'topic': 'Gravitational fields', 'marks': 20,
     'title': "Newton's law of gravitation — satellite orbit relation, geostationary height & angular speed",
     'slice': '9702_s23_qp_42_Q1_Gravitational_fields.pdf',
     'new_parts': [4, 4, 5, 3, 4], 'old_total': 11,
     'ms': '9702_s23_ms_42.pdf', 'ms_pages': [6]},
    {'num': 4, 'topic': 'Oscillations', 'marks': 20,
     'title': 'Oscillating object — amplitude, angular frequency, total energy & KE graph',
     'slice': '9702_w22_qp_42_Q4_Oscillations.pdf',
     'new_parts': [2, 4, 6, 8], 'old_total': 10,
     'ms': '9702_w22_ms_42.pdf', 'ms_pages': [9]},
    {'num': 5, 'topic': 'Oscillations', 'marks': 20,
     'title': 'Electrons oscillating in a metal rod — SHM, drift speed & alternating current',
     'slice': '9702_w23_qp_42_Q4_Oscillations.pdf',
     'new_parts': [2, 2, 4, 3, 3, 4, 2], 'old_total': 11,
     'ms': '9702_w23_ms_42.pdf', 'ms_pages': [9]},
]

TOTAL = sum(q['marks'] for q in QUESTIONS)


def build_cover():
    page = Image.new('RGB', A4_PX, 'white')
    logo = Image.open(LOGO).convert('RGB').resize((LOGO_W_PX, LOGO_H_PX))
    page.paste(logo, ((A4_PX[0] - LOGO_W_PX) // 2, _pt(16)))
    d = ImageDraw.Draw(page)
    ML = _pt(55)

    d.text((ML, _pt(82)), 'Mid-term Examination', font=_font(_pt(24), bold=True), fill=NAVY)
    d.text((ML, _pt(110)), 'PHYSICS · Paper 4 (A2)', font=_font(_pt(13)), fill=GREY)
    d.text((_pt(340), _pt(78)), 'B卷', font=_cn(_pt(30)), fill=NAVY)
    d.line([(ML, _pt(128)), (_pt(300), _pt(128))], fill=GOLD, width=3)

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

    d.rectangle([0, A4_PX[1] - _pt(34), A4_PX[0], A4_PX[1]], fill=NAVY)
    d.text((ML, A4_PX[1] - _pt(24)),
           'DEPU International Senior Department', font=_font(_pt(14), bold=True), fill=(255, 255, 255))
    return page


def build_markscheme_cover():
    page = Image.new('RGB', A4_PX, 'white')
    logo = Image.open(LOGO).convert('RGB').resize((LOGO_W_PX, LOGO_H_PX))
    page.paste(logo, ((A4_PX[0] - LOGO_W_PX) // 2, _pt(16)))
    d = ImageDraw.Draw(page)
    d.text((_pt(55), _pt(88)), 'Mark Scheme', font=_font(_pt(26), bold=True), fill=NAVY)
    d.text((_pt(55), _pt(112)), 'PHYSICS · Paper 4 (A2)', font=_font(_pt(15)), fill=GREY)
    d.text((_pt(340), _pt(84)), 'B卷', font=_cn(_pt(30)), fill=NAVY)
    d.line([(_pt(55), _pt(128)), (_pt(300), _pt(128))], fill=GOLD, width=3)
    d.text((_pt(55), _pt(150)), 'A2 Mid-term Examination — 5 questions · 100 marks',
           font=_font(_pt(14)), fill=DARK)
    return page


def main():
    paper_pages = [build_cover()]
    for q in QUESTIONS:
        edited = edit_marks(os.path.join(HERE, q['slice']), q['new_parts'],
                            q['old_total'], '/tmp/_ab_edited_%d.pdf' % q['num'])
        n = pymupdf.open(edited).page_count
        for i in range(n):
            paper_pages.append(compose_question_page(edited, i, q, first=(i == 0)))

    paper = os.path.join(HERE, 'A2-Midterm-B.pdf')
    paper_pages[0].save(paper, save_all=True, append_images=paper_pages[1:], resolution=DPI)

    ms_pages = [build_markscheme_cover()]
    for q in QUESTIONS:
        for p in q['ms_pages']:
            ms_pages.append(compose_ms_page(os.path.join(HERE, q['ms']), p - 1, q))
    ms = os.path.join(HERE, 'A2-Midterm-B_MarkScheme.pdf')
    ms_pages[0].save(ms, save_all=True, append_images=ms_pages[1:], resolution=DPI)

    print('paper:      %s (%d pages, %d marks)' % (paper, len(paper_pages), TOTAL))
    print('mark scheme: %s (%d pages)' % (ms, len(ms_pages)))


if __name__ == '__main__':
    main()
