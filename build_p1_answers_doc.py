# -*- coding: utf-8 -*-
"""
build_p1_answers_doc.py

Generate a single self-contained HTML "解析版答案" for 9702 Paper 1
(2024 + 2025): every question number, its correct answer letter, and a short
Chinese explanation.

Usage:
    python3 build_p1_answers_doc.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "_p1_work"))
from explanations import EXPL  # noqa: E402

ORDER = [
    "9702_m24_qp_12", "9702_s24_qp_11", "9702_s24_qp_12", "9702_s24_qp_13",
    "9702_w24_qp_11", "9702_w24_qp_12", "9702_w24_qp_13",
    "9702_m25_qp_12", "9702_s25_qp_11", "9702_s25_qp_12", "9702_s25_qp_13",
    "9702_w25_qp_11", "9702_w25_qp_12", "9702_w25_qp_13", "9702_w25_qp_14",
]

# w25 Paper 13 is the companion paper to Paper 11 (identical questions/answers)
EXPL["9702_w25_qp_13"] = EXPL["9702_w25_qp_11"]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    sections = []
    total_q = 0
    for stem in ORDER:
        meta = json.loads((ROOT / "_p1_work" / f"{stem}.json").read_text(encoding="utf-8"))
        paper, paper_full = meta["paper"], meta["paper_full"]
        answers = {q["qnum"]: q["answer"] for q in meta["questions"]}
        ex = EXPL.get(stem, {})
        rows = []
        for n in range(1, 41):
            ans = answers.get(n, "?")
            expl = ex.get(n, "")
            rows.append(
                f'<div class="q"><span class="qn">Q{n}</span>'
                f'<span class="ans">{ans}</span>'
                f'<span class="expl">{esc(expl)}</span></div>'
            )
            total_q += 1
        sections.append(
            f'<section class="paper"><h2>{esc(paper_full)}<span class="code">{esc(paper)}</span></h2>'
            + "".join(rows) + "</section>"
        )

    html = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>9702 Paper 1 24/25 解析版答案</title>
<style>
:root { color-scheme: light; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", sans-serif;
  color: #2b2a27; background: #f6f4f0; line-height: 1.6; padding: 0 0 80px; }
header { background: #0a1828; color: #f8fafc; padding: 34px 24px; text-align: center; }
header h1 { font-size: 28px; letter-spacing: .5px; }
header .sub { color: #7c93a8; font-size: 13px; margin-top: 6px; }
.wrap { max-width: 860px; margin: 0 auto; padding: 0 20px; }
.paper { margin-top: 34px; }
.paper h2 { font-size: 20px; border-bottom: 2px solid #2b2a27; padding-bottom: 6px; display:flex; align-items:baseline; gap:10px; }
.paper h2 .code { font-size: 12px; color: #8a8578; font-weight: 600; margin-left: auto; }
.q { display:flex; align-items:baseline; gap:12px; padding: 9px 12px; border-bottom: 1px solid #e5e0d8; }
.q:nth-child(even) { background: #fff; }
.qn { font-weight: 700; color: #8a8578; min-width: 34px; }
.ans { font-weight: 800; font-size: 17px; min-width: 26px; height: 26px; line-height: 26px; text-align: center;
  background: #2f6b2f; color: #fff; border-radius: 5px; }
.expl { color: #3d3a34; }
@media print { body { background:#fff; } .q { page-break-inside: avoid; } }
</style>
</head>
<body>
<header>
  <h1>9702 Paper 1 · 24/25 解析版答案</h1>
  <div class="sub">Multiple Choice · 2024–2025 · 每题答案 + 简要解析</div>
</header>
<div class="wrap">
"""
    html += "".join(sections)
    html += f"\n<p style='text-align:center;color:#8a8578;font-size:12px;margin-top:40px;'>{total_q} 道题 · {len(ORDER)} 套卷子</p>\n</div>\n</body>\n</html>\n"

    out = ROOT / "9702 Paper1 24-25 解析版答案.html"
    out.write_text(html, encoding="utf-8")
    print(f"Wrote {out.name} ({total_q} questions, {len(ORDER)} papers)")


if __name__ == "__main__":
    main()
