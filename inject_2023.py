# -*- coding: utf-8 -*-
"""
Inject the 2023 Paper 4 data into main.html:
  - add `const paper4Data2023 = [...]` (from data2023/*.json)
  - make the 2023 Paper 4 grid cell available
  - add the paper4-2023 panel + syllabus4-2023 container
  - wire panelIdFor, question count, and the render call
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
MAIN = os.path.join(HERE, 'main.html')

# chronological order of the 7 papers
ORDER = [
    'data2023/9702_m23_qp_42.json',
    'data2023/9702_s23_qp_41.json',
    'data2023/9702_s23_qp_42.json',
    'data2023/9702_s23_qp_43.json',
    'data2023/9702_w23_qp_41.json',
    'data2023/9702_w23_qp_42.json',
    'data2023/9702_w23_qp_43.json',
]


def build_array():
    qs = []
    for path in ORDER:
        d = json.load(open(os.path.join(HERE, path), encoding='utf-8'))
        qs.extend(d['questions'])
    body = json.dumps(qs, ensure_ascii=False, indent=2)
    return 'const paper4Data2023 = ' + body + ';', len(qs)


def main():
    s = open(MAIN, encoding='utf-8').read()

    arr, nq = build_array()

    edits = [
        # 1. grid cell: 2023 Paper 4 soon -> available
        (
            '  <button type="button" class="gp-cell soon" data-year="2023" data-paper="4">Soon</button>',
            '  <div class="gp-cell available" data-year="2023" data-paper="4">\n'
            '    <button type="button" class="gp-open-btn">Open<span class="gp-count" id="gp-count-p4-2023"></span></button>\n'
            '  </div>',
        ),
        # 2. panel container (insert after the paper4-2025 panel)
        (
            '<div id="paper4-2025-panel" class="paper-panel">\n  <div id="syllabus4-2025"></div>\n</div>',
            '<div id="paper4-2025-panel" class="paper-panel">\n  <div id="syllabus4-2025"></div>\n</div>\n'
            '<div id="paper4-2023-panel" class="paper-panel">\n  <div id="syllabus4-2023"></div>\n</div>',
        ),
        # 3. panelIdFor mapping
        (
            "  if (year === '2024' && paper === '4') return 'paper4-2024-panel';",
            "  if (year === '2023' && paper === '4') return 'paper4-2023-panel';\n"
            "  if (year === '2024' && paper === '4') return 'paper4-2024-panel';",
        ),
        # 4. question count wiring (DOMContentLoaded)
        (
            "  var p4y24 = document.getElementById('gp-count-p4-2024');",
            "  var p4y23 = document.getElementById('gp-count-p4-2023');\n"
            "  if (p4y23 && typeof paper4Data2023 !== 'undefined') p4y23.textContent = paper4Data2023.length + ' questions';\n"
            "  var p4y24 = document.getElementById('gp-count-p4-2024');",
        ),
        # 5. data array (insert before paper4Data2024)
        (
            'const paper4Data2024 = [',
            arr + '\n\nconst paper4Data2024 = [',
        ),
        # 6. render call (insert before paper4Data2024 render call)
        (
            "if (typeof paper4Data2024 !== 'undefined') renderPaper2Panel('syllabus4-2024', paper4Data2024);",
            "if (typeof paper4Data2023 !== 'undefined') renderPaper2Panel('syllabus4-2023', paper4Data2023);\n"
            "if (typeof paper4Data2024 !== 'undefined') renderPaper2Panel('syllabus4-2024', paper4Data2024);",
        ),
    ]

    for old, new in edits:
        cnt = s.count(old)
        if cnt != 1:
            print('WARNING: expected 1 match, found', cnt, 'for:',
                  old[:70].replace('\n', '\\n'))
        s = s.replace(old, new)

    open(MAIN, 'w', encoding='utf-8').write(s)
    print('Injected paper4Data2023 with', nq, 'questions.')


if __name__ == '__main__':
    main()
