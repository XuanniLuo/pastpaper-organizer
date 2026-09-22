# -*- coding: utf-8 -*-
"""
Merge a sliced theory paper JSON with its mark-scheme answers and manual
topic categorization into the final per-question index used by the app.

Categorizations live in igcse-data/_theory_categorization.py:
    THEORY_CAT = { "<stem>": { qnum: {"code": "1.2", "title": "..."} } }

Run:
    python igcse_theory_finalize.py 0625_m24_qp_42
    python igcse_theory_finalize.py           # all categorized papers
"""
import importlib.util
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from igcse_syllabus import SUB_LABELS, topic_of
from igcse_theory_ms import build_index

_CAT_PATH = os.path.join("igcse-data", "_theory_categorization.py")
_spec = importlib.util.spec_from_file_location("_theory_cat", _CAT_PATH)
_cat = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cat)
THEORY_CAT = _cat.THEORY_CAT


def finalize(stem, ms_path):
    json_path = os.path.join("igcse-data", stem + ".json")
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    ms_by_q = build_index(ms_path) if ms_path and os.path.exists(ms_path) else {}

    cat = THEORY_CAT.get(stem, {})
    for q in data["questions"]:
        n = q["qnum"]
        info = cat.get(n, {})
        code = info.get("code", "")
        q["code"] = code
        q["title"] = info.get("title", "")
        q["topic"] = topic_of(code) if code else ""
        ms = ms_by_q.get(n, {})
        q["marks"] = ms.get("marks", 0)
        parts = []
        for p in ms.get("parts", []):
            parts.append({"label": p["label"], "marks": p["marks"],
                          "codes": [code] if code else [],
                          "answer": p["answer"]})
        q["parts"] = parts

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    missing = [q["qnum"] for q in data["questions"] if not q["code"]]
    print(f"{stem}: finalized" + (f"; MISSING {missing}" if missing else ""))


def main():
    stems = sys.argv[1:] or list(THEORY_CAT.keys())
    for stem in stems:
        if stem not in THEORY_CAT:
            print(f"no categorization for {stem}; skipping")
            continue
        ms_name = stem.replace("_qp_", "_ms_") + ".pdf"
        hits = []
        for base in ("igcse-2024", "igcse-2025", os.path.join("igcse-2025", "NOV")):
            p = os.path.join(base, ms_name)
            if os.path.exists(p):
                hits.append(p)
        ms_path = hits[0] if hits else ""
        finalize(stem, ms_path)


if __name__ == "__main__":
    main()
