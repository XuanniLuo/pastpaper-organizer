# -*- coding: utf-8 -*-
"""
inject_p1_answers.py

Add the 2022–2024 Paper 1 answer key (parsed from the official mark schemes)
into main.html as `answerKey2224`, and wire it into getAnswer().

Usage:
    python3 inject_p1_answers.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "_p1_work"


def main():
    answer_key = {}
    n_answers = 0
    for f in sorted(WORK.glob("9702_*_qp_1[0-9].json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        qmap = {}
        for q in d["questions"]:
            qmap[f"Q{q['qnum']}"] = q["answer"]
            n_answers += 1
        answer_key[d["paper"]] = qmap

    assert n_answers == 840, f"expected 840 answers, got {n_answers}"

    html_path = ROOT / "main.html"
    html = html_path.read_text(encoding="utf-8")

    # 1. Insert answerKey2224 right after the existing answerKey block.
    anchor = "};\n\nfunction getAnswer(paper, qnum) {"
    if anchor not in html:
        print("ERROR: answerKey/getAnswer anchor not found")
        sys.exit(1)
    obj = "const answerKey2224 = " + json.dumps(answer_key, ensure_ascii=False, indent=2) + ";\n"
    html = html.replace(anchor, "};\n\n" + obj + "\nfunction getAnswer(paper, qnum) {", 1)

    # 2. Wire answerKey2224 into getAnswer.
    old = "var m = answerKey[paper] || (typeof answerKey2026 !== 'undefined' ? answerKey2026[paper] : null);"
    new = "var m = answerKey[paper] || answerKey2224[paper] || (typeof answerKey2026 !== 'undefined' ? answerKey2026[paper] : null);"
    if old not in html:
        print("ERROR: getAnswer lookup line not found")
        sys.exit(1)
    html = html.replace(old, new, 1)

    html_path.write_text(html, encoding="utf-8")
    print(f"OK: injected answerKey2224 ({len(answer_key)} papers, {n_answers} answers) and wired getAnswer")


if __name__ == "__main__":
    main()
