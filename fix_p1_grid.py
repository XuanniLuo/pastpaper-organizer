# -*- coding: utf-8 -*-
"""
fix_p1_grid.py

Split the 2022–2024 Paper 1 data into per-year objects (matching the 2026
pattern) instead of the single merged object, and wire up the dashboard grid:
  - replace the merged IIFE with questionData2022 / 2023 / 2024
  - add render blocks + panels for each year
  - map grid cells (2022/2023/2024 Paper 1) to their panels
  - make the "Soon" cells available and add a 2022 row
  - populate question counts

Usage:
    python3 fix_p1_grid.py
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "_p1_work"))
from categorization import CAT  # noqa: E402

TOPIC_TITLES = {
    "1": "Physical quantities and units", "2": "Kinematics", "3": "Dynamics",
    "4": "Forces, density and pressure", "5": "Work, energy and power",
    "6": "Deformation of solids", "7": "Waves", "8": "Superposition",
    "9": "Electricity", "10": "D.C. circuits", "11": "Particle physics",
}


def year_of(stem):
    return "20" + re.match(r"9702_[msw](\d{2})_qp_\d{2}$", stem).group(1)


def build_year_objects():
    years = {"2022": {}, "2023": {}, "2024": {}}
    for stem in sorted(CAT):
        y = year_of(stem)
        meta = json.loads((ROOT / "_p1_work" / f"{stem}.json").read_text(encoding="utf-8"))
        paper, paper_full = meta["paper"], meta["paper_full"]
        for q in meta["questions"]:
            n = q["qnum"]
            codes = CAT[stem][n]
            title = TOPIC_TITLES[codes[0].split(".")[0]]
            code_str = "_".join(codes)
            entry = {
                "paper": paper, "paper_full": paper_full,
                "qnum": f"Q{n}",
                "pdf": f"{stem}_Q{n}_{title}_{code_str}.pdf",
            }
            for c in codes:
                years[y].setdefault(c, []).append(entry)
    return years


def main():
    years = build_year_objects()
    html_path = ROOT / "main.html"
    html = html_path.read_text(encoding="utf-8")

    # Backup the pre-fix file (with the merged IIFE) before mutating.
    bak = ROOT / "main.html.bak4"
    if not bak.exists():
        bak.write_text(html, encoding="utf-8")

    # 1. Replace the merged IIFE with three object definitions.
    start = html.find("// ==== 2022–2024 Paper 1 (auto-injected) ====")
    if start == -1:
        print("ERROR: old merged snippet not found")
        sys.exit(1)
    end = html.find("})();", start)
    if end == -1:
        print("ERROR: cannot find end of old snippet")
        sys.exit(1)
    end += len("})();")
    objs = "// ==== 2022–2024 Paper 1 (auto-injected) ====\n"
    for y in ("2022", "2023", "2024"):
        objs += f"const questionData{y} = {json.dumps(years[y], ensure_ascii=False, indent=2)};\n"
    html = html[:start] + objs + html[end:]

    # 2. Add render blocks before the 2026 render block's closing brace.
    anchor = "  renderPaper1Panel('syllabus-2026', questionData2026, pdfToCodes2026);\n}"
    if anchor not in html:
        print("ERROR: 2026 render anchor not found")
        sys.exit(1)
    blocks = ""
    for y in ("2022", "2023", "2024"):
        blocks += (
            f"if (typeof questionData{y} !== 'undefined') {{\n"
            f"  const pdfToCodes{y} = {{}};\n"
            f"  Object.keys(questionData{y}).forEach(function(code) {{\n"
            f"    questionData{y}[code].forEach(function(q) {{\n"
            f"      if (!pdfToCodes{y}[q.pdf]) pdfToCodes{y}[q.pdf] = [];\n"
            f"      if (pdfToCodes{y}[q.pdf].indexOf(code) === -1) pdfToCodes{y}[q.pdf].push(code);\n"
            f"    }});\n"
            f"  }});\n"
            f"  renderPaper1Panel('syllabus-{y}', questionData{y}, pdfToCodes{y});\n"
            f"}}\n"
        )
    html = html.replace(anchor, anchor + blocks, 1)

    # 3. Add panel divs after the paper1-panel block.
    panel_anchor = '<div id="paper1-panel" class="paper-panel">\n  <div id="syllabus"></div>\n</div>'
    if panel_anchor not in html:
        print("ERROR: paper1-panel anchor not found")
        sys.exit(1)
    new_panels = panel_anchor
    for y in ("2022", "2023", "2024"):
        new_panels += f'\n<div id="paper1-{y}-panel" class="paper-panel">\n  <div id="syllabus-{y}"></div>\n</div>'
    html = html.replace(panel_anchor, new_panels, 1)

    # 4. Map grid cells in panelIdFor.
    pid_old = "  if (year === '2024' && paper === '2') return 'paper2-2024-panel';\n"
    pid_new = (
        "  if (year === '2022' && paper === '1') return 'paper1-2022-panel';\n"
        "  if (year === '2023' && paper === '1') return 'paper1-2023-panel';\n"
        "  if (year === '2024' && paper === '1') return 'paper1-2024-panel';\n"
        + pid_old
    )
    if pid_old not in html:
        print("ERROR: panelIdFor anchor not found")
        sys.exit(1)
    html = html.replace(pid_old, pid_new, 1)

    # 5. Grid: 2024 Paper 1 and 2023 Paper 1 -> available.
    def p1_cell(year):
        return (
            f'  <div class="gp-cell available" data-year="{year}" data-paper="1">\n'
            f'    <button type="button" class="gp-open-btn">Open<span class="gp-count" id="gp-count-p1-{year}"></span></button>\n'
            f'  </div>'
        )

    for y in ("2023", "2024"):
        old = f'<button type="button" class="gp-cell soon" data-year="{y}" data-paper="1">Soon</button>'
        if old not in html:
            print(f"ERROR: {y} p1 soon cell not found")
            sys.exit(1)
        html = html.replace(old, p1_cell(y), 1)

    # Add a 2022 row before the grid's closing </div>.
    row23_end = '  <button type="button" class="gp-cell soon" data-year="2023" data-paper="5">Soon</button>\n</div>'
    if row23_end not in html:
        print("ERROR: 2023 row end not found")
        sys.exit(1)
    row2022 = (
        '  <button type="button" class="gp-cell soon" data-year="2023" data-paper="5">Soon</button>\n'
        '  <div class="gp-year">2022</div>\n'
        + p1_cell("2022")
        + '\n'
        '  <button type="button" class="gp-cell soon" data-year="2022" data-paper="2">Soon</button>\n'
        '  <button type="button" class="gp-cell soon" data-year="2022" data-paper="4">Soon</button>\n'
        '  <button type="button" class="gp-cell soon" data-year="2022" data-paper="5">Soon</button>\n'
        '</div>'
    )
    html = html.replace(row23_end, row2022, 1)

    # 6. Populate counts (const objects are not on window, so build a lookup).
    count_anchor = "  var p1y26 = document.getElementById('gp-count-p1-2026');"
    count_new = (
        "  var p1ByYear = {};\n"
        "  if (typeof questionData2022 !== 'undefined') p1ByYear['2022'] = questionData2022;\n"
        "  if (typeof questionData2023 !== 'undefined') p1ByYear['2023'] = questionData2023;\n"
        "  if (typeof questionData2024 !== 'undefined') p1ByYear['2024'] = questionData2024;\n"
        "  ['2022','2023','2024'].forEach(function(y) {\n"
        "    var el = document.getElementById('gp-count-p1-' + y);\n"
        "    var d = p1ByYear[y];\n"
        "    if (el && d) {\n"
        "      var s = new Set();\n"
        "      Object.keys(d).forEach(function(code) { (d[code] || []).forEach(function(q) { s.add(q.pdf); }); });\n"
        "      el.textContent = s.size + ' questions';\n"
        "    }\n"
        "  });\n"
        + count_anchor
    )
    if count_anchor not in html:
        print("ERROR: count anchor not found")
        sys.exit(1)
    html = html.replace(count_anchor, count_new, 1)

    html_path.write_text(html, encoding="utf-8")
    print("OK: split 22/23/24 into per-year objects, wired grid + panels + counts")
    for y in ("2022", "2023", "2024"):
        print(f"  {y}: {sum(len(v) for v in years[y].values())} entries across {len(years[y])} codes")


if __name__ == "__main__":
    main()
