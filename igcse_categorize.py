# -*- coding: utf-8 -*-
"""
Apply manual topic categorization to a sliced IGCSE MCQ paper's JSON index.

Categorizations live in igcse-data/_categorization.py as
    CATEGORIZATION = { "<paper_stem>": { qnum: "sub_code", ... } }

Run:
    python igcse_categorize.py 0625_m24_qp_22        # one paper
    python igcse_categorize.py                       # all categorized papers
"""
import importlib.util
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from igcse_syllabus import SUB_LABELS

_CAT_PATH = os.path.join("igcse-data", "_categorization.py")
_spec = importlib.util.spec_from_file_location("_categorization", _CAT_PATH)
_cat = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cat)
CATEGORIZATION = _cat.CATEGORIZATION


def apply_one(stem):
    json_path = os.path.join("igcse-data", stem + ".json")
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    mapping = CATEGORIZATION[stem]
    for q in data["questions"]:
        code = mapping.get(q["qnum"], "")
        q["code"] = code
        q["topic_name"] = SUB_LABELS.get(code, "") if code else ""
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    # report gaps
    missing = [q["qnum"] for q in data["questions"] if not q["code"]]
    print(f"{stem}: applied {len(mapping)} codes" + (f"; MISSING {missing}" if missing else ""))


def main():
    if len(sys.argv) > 1:
        stems = sys.argv[1:]
    else:
        stems = list(CATEGORIZATION.keys())
    for stem in stems:
        if stem not in CATEGORIZATION:
            print(f"no categorization for {stem}; skipping")
            continue
        apply_one(stem)


if __name__ == "__main__":
    main()
