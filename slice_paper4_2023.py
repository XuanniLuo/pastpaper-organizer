# -*- coding: utf-8 -*-
"""
Slice the 2023 9702 Paper 4 question papers into per-question PDFs.

Each data2023/*.json carries a `pages` list (1-indexed, blank pages already
excluded by the transcriber) and the per-question `pdf` filename. This extracts
exactly those pages from the raw question paper in the repo root and writes the
per-question PDF next to main.html.

Usage:  python slice_paper4_2023.py
"""
import json
import glob
import os
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))


def slice_one(json_path):
    d = json.load(open(json_path, encoding='utf-8'))
    paper = d['paper']                       # e.g. 9702/42/F/M/23
    sess = paper.split('/')[2].lower()       # f / m / o
    n = paper.split('/')[1]
    year = paper.split('/')[4]
    session_prefix = {'f': 'm', 'm': 's', 'o': 'w'}[sess]
    src = os.path.join(HERE, f'9702_{session_prefix}{year}_qp_{n}.pdf')
    if not os.path.exists(src):
        print('  MISSING SOURCE', src)
        return 0
    doc = pymupdf.open(src)
    done = 0
    for q in d['questions']:
        pages = q.get('pages') or []
        if not pages:
            print('  NO PAGES for', q['qnum'])
            continue
        out = pymupdf.open()
        for p in pages:
            out.insert_pdf(doc, from_page=p - 1, to_page=p - 1)
        out.save(os.path.join(HERE, q['pdf']))
        out.close()
        done += 1
    doc.close()
    return done


def main():
    jsons = sorted(
        glob.glob(os.path.join(HERE, 'data2022', '9702_*_qp_4*.json'))
        + glob.glob(os.path.join(HERE, 'data2023', '9702_*_qp_4*.json'))
    )
    total = 0
    for j in jsons:
        base = os.path.basename(j)
        n = slice_one(j)
        print(f'{base}: sliced {n} questions')
        total += n
    print(f'\nSliced {total} per-question PDFs total.')


if __name__ == '__main__':
    main()
