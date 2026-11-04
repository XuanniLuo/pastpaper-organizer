# -*- coding: utf-8 -*-
"""
Inject the 2022 Paper 4 data into main.html:
  - add `const paper4Data2022 = [...]` (from data2022/*.json)
  - make the 2022 Paper 4 grid cell available
  - add the paper4-2022 panel + syllabus4-2022 container
  - wire panelIdFor, question count, and the render call
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
MAIN = os.path.join(HERE, 'main.html')

ORDER = [
    'data2022/9702_m22_qp_42.json',
    'data2022/9702_s22_qp_41.json',
    'data2022/9702_s22_qp_42.json',
    'data2022/9702_s22_qp_43.json',
    'data2022/9702_w22_qp_41.json',
    'data2022/9702_w22_qp_42.json',
    'data2022/9702_w22_qp_43.json',
]


def build_array():
    qs = []
    for path in ORDER:
        d = json.load(open(os.path.join(HERE, path), encoding='utf-8'))
        qs.extend(d['questions'])
    body = json.dumps(qs, ensure_ascii=False, indent=2)
    return 'const paper4Data2022 = ' + body + ';', len(qs)


def main():
    s = open(MAIN, encoding='utf-8').read()

    arr, nq = build_array()

    edits = [
        (
            '  <button type="button" class="gp-cell soon" data-year="2022" data-paper="4">Soon</button>',
            '  <div class="gp-cell available" data-year="2022" data-paper="4">\n'
            '    <button type="button" class="gp-open-btn">Open<span class="gp-count" id="gp-count-p4-2022"></span></button>\n'
            '  </div>',
        ),
        (
            '<div id="paper4-2023-panel" class="paper-panel">\n  <div id="syllabus4-2023"></div>\n</div>',
            '<div id="paper4-2023-panel" class="paper-panel">\n  <div id="syllabus4-2023"></div>\n</div>\n'
            '<div id="paper4-2022-panel" class="paper-panel">\n  <div id="syllabus4-2022"></div>\n</div>',
        ),
        (
            "  if (year === '2023' && paper === '4') return 'paper4-2023-panel';",
            "  if (year === '2022' && paper === '4') return 'paper4-2022-panel';\n"
            "  if (year === '2023' && paper === '4') return 'paper4-2023-panel';",
        ),
        (
            "  var p4y23 = document.getElementById('gp-count-p4-2023');",
            "  var p4y22 = document.getElementById('gp-count-p4-2022');\n"
            "  if (p4y22 && typeof paper4Data2022 !== 'undefined') p4y22.textContent = paper4Data2022.length + ' questions';\n"
            "  var p4y23 = document.getElementById('gp-count-p4-2023');",
        ),
        (
            'const paper4Data2023 = [',
            arr + '\n\nconst paper4Data2023 = [',
        ),
        (
            "if (typeof paper4Data2023 !== 'undefined') renderPaper2Panel('syllabus4-2023', paper4Data2023);",
            "if (typeof paper4Data2022 !== 'undefined') renderPaper2Panel('syllabus4-2022', paper4Data2022);\n"
            "if (typeof paper4Data2023 !== 'undefined') renderPaper2Panel('syllabus4-2023', paper4Data2023);",
        ),
    ]

    for old, new in edits:
        cnt = s.count(old)
        if cnt != 1:
            print('WARNING: expected 1 match, found', cnt, 'for:',
                  old[:70].replace('\n', '\\n'))
        s = s.replace(old, new)

    open(MAIN, 'w', encoding='utf-8').write(s)
    print('Injected paper4Data2022 with', nq, 'questions.')


if __name__ == '__main__':
    main()
