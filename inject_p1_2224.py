# -*- coding: utf-8 -*-
"""
inject_p1_2224.py

Finalise the 2022–2024 Paper 1 by-topic data:
  1. Rename each per-question slice to the final convention
     {stem}_Q{n}_{TopicTitle}_{code1_code2...}.pdf and copy to the top level.
  2. Build a JS snippet merging the questions into `questionData`.
  3. Inject the snippet into main.html just before the render call.

Usage:
    python3 inject_p1_2224.py
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
    "1": "Physical quantities and units",
    "2": "Kinematics",
    "3": "Dynamics",
    "4": "Forces, density and pressure",
    "5": "Work, energy and power",
    "6": "Deformation of solids",
    "7": "Waves",
    "8": "Superposition",
    "9": "Electricity",
    "10": "D.C. circuits",
    "11": "Particle physics",
}

WORK = ROOT / "_p1_work"


def main():
    entries_by_code = {}
    copies = 0
    missing = []

    for stem in sorted(CAT):
        meta = json.loads((WORK / f"{stem}.json").read_text(encoding="utf-8"))
        paper = meta["paper"]
        paper_full = meta["paper_full"]
        for q in meta["questions"]:
            n = q["qnum"]
            codes = CAT[stem][n]
            title = TOPIC_TITLES[codes[0].split(".")[0]]
            code_str = "_".join(codes)
            final_name = f"{stem}_Q{n}_{title}_{code_str}.pdf"
            src = WORK / "slices" / f"{stem}_Q{n:02d}.pdf"
            if not src.exists():
                missing.append(str(src))
                continue
            shutil.copy(src, ROOT / final_name)
            copies += 1
            entry = {"paper": paper, "paper_full": paper_full, "qnum": f"Q{n}", "pdf": final_name}
            for c in codes:
                entries_by_code.setdefault(c, []).append(entry)

    if missing:
        print("MISSING SLICES:")
        for m in missing:
            print("  ", m)
        sys.exit(1)

    total = sum(len(v) for v in entries_by_code.values())
    print(f"Copied {copies} slice PDFs to top level; {total} question entries across {len(entries_by_code)} codes")

    # Build JS snippet
    data_js = json.dumps(entries_by_code, ensure_ascii=False, indent=2)
    snippet = (
        "\n// ==== 2022–2024 Paper 1 (auto-injected) ====\n"
        "(function () {\n"
        "  var d = " + data_js + ";\n"
        "  Object.keys(d).forEach(function (code) {\n"
        "    if (!questionData[code]) questionData[code] = [];\n"
        "    d[code].forEach(function (q) { questionData[code].push(q); });\n"
        "  });\n"
        "})();\n"
    )

    html_path = ROOT / "main.html"
    html = html_path.read_text(encoding="utf-8")

    anchor = "renderPaper1Panel('syllabus', questionData, pdfToCodes);"
    if anchor not in html:
        print("ERROR: render anchor not found in main.html")
        sys.exit(1)
    if "2022–2024 Paper 1 (auto-injected)" in html:
        print("Already injected; skipping (idempotent).")
        return

    # Back up
    bak = ROOT / "main.html.bak3"
    if not bak.exists():
        shutil.copy(html_path, bak)
        print(f"Backed up main.html -> {bak.name}")

    html = html.replace(anchor, snippet + "\n" + anchor, 1)
    html_path.write_text(html, encoding="utf-8")
    print("Injected into main.html")


if __name__ == "__main__":
    main()
