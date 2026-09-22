# -*- coding: utf-8 -*-
"""
Build the IGCSE 0625 section and inject it into main.html.

Reads all sliced/categorized IGCSE JSONs (MCQ Paper 2 + Theory Paper 4) and:
  1. emits the IGCSE syllabus + question data as JS,
  2. emits an IGCSE year x paper grid + panels (HTML),
  3. emits IGCSE render functions (JS),
  4. inserts the whole block into main.html (backing up the original first).

Usage:
    python build_igcse_section.py
"""
import json
import glob
import os
import re

from igcse_syllabus import SYLLABUS, SUB_LABELS, TOPIC_TITLES
from igcse_syllabus_points import SUBSUBS

MAIN = "main.html"


# ---------------------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------------------
def load_mcq():
    by_year = {}
    answer_key = {}
    for path in sorted(glob.glob("igcse-data/0625_*_qp_2*.json")):
        d = json.load(open(path, encoding="utf-8"))
        year = d["paper"].split("/")[-1]
        year = "20" + year
        bucket = by_year.setdefault(year, {})
        paper_code = d["paper"]
        answer_key[paper_code] = {}
        for q in d["questions"]:
            code = q.get("code") or ""
            if not code:
                continue
            entry = {
                "paper": q["paper"] if "paper" in q else paper_code,
                "paper_full": d.get("paper_full", ""),
                "qnum": "Q%d" % q["qnum"],
                "pdf": q["pdf"],
            }
            bucket.setdefault(code, []).append(entry)
            ans = q.get("answer") or ""
            if ans:
                answer_key[paper_code]["Q%d" % q["qnum"]] = ans
    return by_year, answer_key


def load_theory():
    by_year = {}
    for path in sorted(glob.glob("igcse-data/0625_*_qp_4*.json")):
        d = json.load(open(path, encoding="utf-8"))
        year = "20" + d["paper"].split("/")[-1]
        bucket = by_year.setdefault(year, [])
        for q in d["questions"]:
            if not q.get("code"):
                continue
            # parts: drop empty answers and codes field (render uses answer + marks)
            parts = []
            for p in q.get("parts", []):
                if p.get("answer"):
                    parts.append({"label": p["label"], "marks": p["marks"],
                                  "answer": p["answer"]})
            bucket.append({
                "topic": q["topic"],
                "paper": d["paper"],
                "paper_full": d.get("paper_full", ""),
                "qnum": "Q%d" % q["qnum"],
                "title": q.get("title", ""),
                "marks": q.get("marks", 0),
                "pdf": q["pdf"],
                "parts": parts,
            })
    return by_year


# ---------------------------------------------------------------------------
# 2. Syllabus JS
# ---------------------------------------------------------------------------
def syllabus_js():
    out = []
    for topic, title, subs in SYLLABUS:
        subs_js = [{"code": c, "title": t} for c, t in subs]
        out.append({"topic": topic, "title": title, "subs": subs_js})
    return json.dumps(out, ensure_ascii=False)


# ---------------------------------------------------------------------------
# 3. Render JS
# ---------------------------------------------------------------------------
RENDER_JS = r"""
// ============================================================
// IGCSE 0625 — question organizer section
// ============================================================
function igcseEscape(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

function igcseAnswer(paper, qnum) {
  var m = igcseAnswerKey[paper];
  return m ? (m[qnum] || '') : '';
}

// --- Paper 2 (Multiple choice) ---
function renderIgcseMcqPanel(containerId, data) {
  var container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = '';
  igcseSyllabus.forEach(function(t) {
    var qCount = 0;
    t.subs.forEach(function(s) { qCount += (data[s.code] || []).length; });

    var card = document.createElement('div');
    card.className = 'topic-card t' + t.topic;

    var header = document.createElement('div');
    header.className = 'topic-header';
    header.onclick = function() {
      var closing = card.classList.contains('expanded');
      card.classList.toggle('expanded');
      if (closing) stopTimer();
    };
    var num = document.createElement('div');
    num.className = 'topic-num';
    num.textContent = t.topic;
    var info = document.createElement('div');
    info.className = 'topic-info';
    info.innerHTML = '<div class="topic-name">' + t.topic + '. ' + igcseEscape(t.title) + '</div>' +
      '<div class="topic-count">' + t.subs.length + ' sub-topics &middot; <span class="q-count">' + qCount + ' questions</span></div>';
    var chev = document.createElement('div');
    chev.className = 'chevron';
    chev.innerHTML = '&#9660;';
    header.appendChild(num); header.appendChild(info); header.appendChild(chev);
    card.appendChild(header);

    var subList = document.createElement('div');
    subList.className = 'sub-list';
    t.subs.forEach(function(s) {
      var qs = data[s.code] || [];
      var subCard = document.createElement('div');
      subCard.className = 'sub-card';
      var subHeader = document.createElement('div');
      subHeader.className = 'sub-header';
      subHeader.innerHTML = '<span class="sub-code">' + s.code + '</span><span class="sub-name">' + igcseEscape(s.title) + '</span>' +
        (qs.length > 0 ? '<span class="subsub-badge active">' + qs.length + '</span><span class="chevron">&#9660;</span>' : '');
      subCard.appendChild(subHeader);

      var subBody = document.createElement('div');
      subBody.className = 'sub-body';

      var syl = igcseSubsubs[s.code];
      if (syl) {
        var sylWrap = document.createElement('div');
        sylWrap.className = 'syl-wrap';
        var sylHtml = '';
        if (syl.subsubs) {
          syl.subsubs.forEach(function(ss) {
            sylHtml += '<div class="syl-sub"><span class="syl-sub-code">' + ss.code + '</span><span class="syl-sub-title">' + igcseEscape(ss.title) + '</span></div>';
            sylHtml += '<ul class="syl-points">' + ss.points.map(function(p) { return '<li>' + igcseEscape(p) + '</li>'; }).join('') + '</ul>';
          });
        } else {
          sylHtml += '<ul class="syl-points">' + syl.points.map(function(p) { return '<li>' + igcseEscape(p) + '</li>'; }).join('') + '</ul>';
        }
        sylWrap.innerHTML = sylHtml;
        subBody.appendChild(sylWrap);
      }

      if (qs.length > 0) {
        var sorted = qs.slice().sort(function(a, b) { return paperSortKey(a.paper) - paperSortKey(b.paper); });
        var panel = document.createElement('div');
        panel.className = 'question-panel open';
        var qCards = sorted.map(function(q) {
          var qCard = document.createElement('div');
          qCard.className = 'q-card';
          var ans = igcseAnswer(q.paper, q.qnum);
          var ansHtml = ans
            ? '<span class="answer-letter">' + ans + '</span><span>Correct answer</span>'
            : '<span class="answer-na">No answer data</span>';
          qCard.innerHTML =
            '<div class="q-meta"><span class="q-tag paper">' + igcseEscape(q.paper) + '</span><span class="q-tag qnum">' + q.qnum + '</span></div>' +
            '<div class="q-paper-full">' + igcseEscape(q.paper_full) + '</div>' +
            '<div class="answer-row"><button type="button" class="answer-btn">&#128065; View Answer</button>' +
            '<div class="answer-reveal">' + ansHtml + '</div></div>' +
            '<div class="pdf-container"><embed src="' + q.pdf + '" type="application/pdf">' +
            '<div class="pdf-fallback" style="display:none">&#128196; Preview unavailable. <a href="' + q.pdf + '" target="_blank">Download PDF</a></div></div>';
          var btn = qCard.querySelector('.answer-btn');
          var reveal = qCard.querySelector('.answer-reveal');
          btn.addEventListener('click', function(e) {
            e.stopPropagation();
            var shown = reveal.classList.toggle('shown');
            btn.innerHTML = shown ? '&#128065; Hide Answer' : '&#128065; View Answer';
          });
          var timerBadge = createTimerBadge(q.pdf);
          qCard.querySelector('.q-meta').appendChild(timerBadge);
          var markToolbar = createMarkToolbar(q.pdf, qCard);
          qCard.querySelector('.q-meta').appendChild(markToolbar);
          registerMarkable(q.pdf, qCard, markToolbar);
          return qCard;
        });
        qCards.forEach(function(c) { panel.appendChild(c); });
        var pageIdx = 0;
        if (qCards.length > 1) {
          var pager = document.createElement('div');
          pager.className = 'q-pager';
          var prevBtn = document.createElement('button');
          prevBtn.className = 'q-pager-btn';
          prevBtn.type = 'button';
          prevBtn.innerHTML = '&#8249;';
          var tabsWrap = document.createElement('div');
          tabsWrap.className = 'q-pager-tabs';
          var tabs = sorted.map(function(q, idx) {
            var tab = document.createElement('button');
            tab.className = 'q-pager-tab';
            tab.type = 'button';
            tab.innerHTML = '<span class="q-pager-tab-q">' + q.qnum + '</span><span class="q-pager-tab-season">' + seasonLabel(q.paper) + '</span>';
            tab.addEventListener('click', function(e) {
              e.stopPropagation();
              pageIdx = idx;
              renderPage();
            });
            tabsWrap.appendChild(tab);
            return tab;
          });
          var nextBtn = document.createElement('button');
          nextBtn.className = 'q-pager-btn';
          nextBtn.type = 'button';
          nextBtn.innerHTML = '&#8250;';
          var renderPage = function() {
            qCards.forEach(function(c, idx) { c.style.display = idx === pageIdx ? 'block' : 'none'; });
            tabs.forEach(function(tab, idx) { tab.classList.toggle('active', idx === pageIdx); });
            prevBtn.disabled = pageIdx === 0;
            nextBtn.disabled = pageIdx === qCards.length - 1;
          };
          prevBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            if (pageIdx > 0) { pageIdx--; renderPage(); }
          });
          nextBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            if (pageIdx < qCards.length - 1) { pageIdx++; renderPage(); }
          });
          pager.appendChild(prevBtn);
          pager.appendChild(tabsWrap);
          pager.appendChild(nextBtn);
          panel.insertBefore(pager, panel.firstChild);
          renderPage();
        }
        subBody.appendChild(panel);
      }
      subCard.appendChild(subBody);
      if (qs.length > 0 || syl) {
        subHeader.style.cursor = 'pointer';
        subHeader.addEventListener('click', function(e) {
          e.stopPropagation();
          subCard.classList.toggle('sub-open');
          if (!subCard.classList.contains('sub-open')) stopTimer();
        });
      }
      subList.appendChild(subCard);
    });
    card.appendChild(subList);
    container.appendChild(card);
  });
}

// --- Paper 4 (Theory) ---
function renderIgcseTheoryPanel(containerId, data) {
  var container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = '';
  var topicOrder = [];
  var byTopic = {};
  data.forEach(function(q) {
    if (!byTopic[q.topic]) { byTopic[q.topic] = []; topicOrder.push(q.topic); }
    byTopic[q.topic].push(q);
  });
  topicOrder.sort(function(a, b) { return parseInt(a) - parseInt(b); });

  topicOrder.forEach(function(tn) {
    var qs = byTopic[tn];
    var card = document.createElement('div');
    card.className = 'topic-card t' + tn;

    var header = document.createElement('div');
    header.className = 'topic-header';
    header.onclick = function() {
      var closing = card.classList.contains('expanded');
      card.classList.toggle('expanded');
      if (closing) stopTimer();
    };
    var num = document.createElement('div');
    num.className = 'topic-num';
    num.textContent = tn;
    var info = document.createElement('div');
    info.className = 'topic-info';
    var totalMarks = qs.reduce(function(s, q) { return s + q.marks; }, 0);
    info.innerHTML = '<div class="topic-name">' + tn + '. ' + igcseEscape(igcseTopicMeta[tn] || '') + '</div>' +
      '<div class="topic-count">' + qs.length + ' question' + (qs.length > 1 ? 's' : '') +
      ' &middot; <span class="q-count">' + totalMarks + ' marks</span></div>';
    var chev = document.createElement('div');
    chev.className = 'chevron';
    chev.innerHTML = '&#9660;';
    header.appendChild(num); header.appendChild(info); header.appendChild(chev);
    card.appendChild(header);

    var subList = document.createElement('div');
    subList.className = 'sub-list';
    qs.forEach(function(q) {
      var qCard = document.createElement('div');
      qCard.className = 'p2-q-card';
      var qHeader = document.createElement('div');
      qHeader.className = 'p2-q-header';
      qHeader.innerHTML = '<span class="p2-q-num sub-code">' + q.qnum + '</span>' +
        '<span class="p2-q-title">' + igcseEscape(q.title) + '</span>' +
        '<span class="p2-q-marks">' + q.marks + ' marks</span>' +
        '<span class="p2-chevron">&#9660;</span>';
      qHeader.addEventListener('click', function() {
        var opening = !qCard.classList.contains('expanded');
        qCard.classList.toggle('expanded');
        if (opening) { startTimer(q.pdf); } else { stopTimer(); }
      });
      var timerBadge = createTimerBadge(q.pdf);
      qHeader.insertBefore(timerBadge, qHeader.querySelector('.p2-chevron'));
      var markToolbar = createMarkToolbar(q.pdf, qCard);
      qHeader.insertBefore(markToolbar, qHeader.querySelector('.p2-chevron'));
      registerMarkable(q.pdf, qCard, markToolbar);

      var qMeta = document.createElement('div');
      qMeta.className = 'p2-q-meta';
      qMeta.textContent = q.paper + ' — ' + q.paper_full;
      qCard.appendChild(qHeader);
      qCard.appendChild(qMeta);

      var qBody = document.createElement('div');
      qBody.className = 'p2-q-body';
      var pdfWrap = document.createElement('div');
      pdfWrap.className = 'p2-pdf-wrap pdf-container';
      pdfWrap.innerHTML = '<embed src="' + q.pdf + '" type="application/pdf">' +
        '<div class="pdf-fallback" style="display:none">&#128196; Preview unavailable. <a href="' + q.pdf + '" target="_blank">Download PDF</a></div>';
      qBody.appendChild(pdfWrap);

      if (q.parts && q.parts.length) {
        var partsWrap = document.createElement('div');
        partsWrap.className = 'p2-parts';
        q.parts.forEach(function(p) {
          var part = document.createElement('div');
          part.className = 'p2-part';
          part.innerHTML =
            '<div class="p2-part-head"><span class="p2-part-label">' + igcseEscape(p.label) + '</span>' +
            '<span class="p2-part-marks">' + p.marks + ' mark' + (p.marks === 1 ? '' : 's') + '</span></div>' +
            '<div class="p2-part-answer">' + p.answer + '</div>';
          partsWrap.appendChild(part);
        });
        qBody.appendChild(partsWrap);
      }
      qCard.appendChild(qBody);
      subList.appendChild(qCard);
    });
    card.appendChild(subList);
    container.appendChild(card);
  });
}

// --- IGCSE grid selection ---
var igcseSelLabel = document.getElementById('igcse-selection-label');
function showIgcsePanel(year, paper) {
  document.querySelectorAll('.paper-panel').forEach(function(p) { p.classList.remove('active'); });
  var el = document.getElementById('igcse-' + paper + '-' + year + '-panel');
  if (el) el.classList.add('active');
  if (igcseSelLabel) igcseSelLabel.textContent = year + ' · Paper ' + paper;
}
var igcseGrid = document.getElementById('igcse-grid');
if (igcseGrid) {
  igcseGrid.querySelectorAll('.gp-cell.available').forEach(function(cell) {
    cell.addEventListener('click', function() {
      showIgcsePanel(cell.getAttribute('data-year'), cell.getAttribute('data-paper'));
    });
  });
}
"""


# ---------------------------------------------------------------------------
# 4. HTML section
# ---------------------------------------------------------------------------
def html_section(mcq_years, theory_years):
    years = sorted(set(list(mcq_years) + list(theory_years)), reverse=True)
    all_years = ["2026", "2025", "2024"]

    head = (
        '<div class="igcse-divider">'
        '<h2>IGCSE Physics 0625 — Question Organizer</h2>'
        '<p>Paper 2 (multiple choice) and Paper 4 (theory), 2024–2025</p>'
        '</div>'
    )

    grid_rows = []
    grid_rows.append('<div class="year-paper-grid" id="igcse-grid">')
    grid_rows.append('<div class="gp-corner">Year &#8595;<br>Paper &#8594;</div>')
    grid_rows.append('<div class="gp-head">Paper 2<span>Multiple choice</span></div>')
    grid_rows.append('<div class="gp-head">Paper 4<span>Theory (extended)</span></div>')

    for y in all_years:
        grid_rows.append('<div class="gp-year">%s</div>' % y)
        for paper in ["2", "4"]:
            label = "MCQ" if paper == "2" else "Theory"
            if y in (mcq_years if paper == "2" else theory_years):
                grid_rows.append(
                    '<div class="gp-cell available" data-year="%s" data-paper="%s">'
                    '<button type="button" class="gp-open-btn">Open</button></div>' % (y, paper))
            else:
                grid_rows.append(
                    '<button type="button" class="gp-cell soon" data-year="%s" data-paper="%s">Soon</button>' % (y, paper))
    grid_rows.append('</div>')
    grid_rows.append('<div class="selection-bar" id="igcse-selection-bar">'
                     '<span class="selection-label" id="igcse-selection-label">2025 · Paper 2</span></div>')

    panels = []
    for y in years:
        panels.append('<div id="igcse-2-%s-panel" class="paper-panel igcse-panel"><div id="igcse-mcq-%s"></div></div>' % (y, y))
        panels.append('<div id="igcse-4-%s-panel" class="paper-panel igcse-panel"><div id="igcse-theory-%s"></div></div>' % (y, y))

    return head + "\n" + "\n".join(grid_rows) + "\n" + "\n".join(panels)


# ---------------------------------------------------------------------------
# 5. Data JS block
# ---------------------------------------------------------------------------
def data_js(mcq_by_year, answer_key, theory_by_year):
    mcq = json.dumps(mcq_by_year, ensure_ascii=False)
    ak = json.dumps(answer_key, ensure_ascii=False)
    th = json.dumps(theory_by_year, ensure_ascii=False)
    topic_meta = json.dumps(TOPIC_TITLES, ensure_ascii=False)
    subsubs = json.dumps(SUBSUBS, ensure_ascii=False)
    return (
        "const igcseSyllabus = %s;\n"
        "const igcseTopicMeta = %s;\n"
        "const igcseSubsubs = %s;\n"
        "const igcseMcqData = %s;\n"
        "const igcseAnswerKey = %s;\n"
        "const igcseTheoryData = %s;\n"
        % (syllabus_js(), topic_meta, subsubs, mcq, ak, th)
    )


def main():
    mcq_by_year, answer_key = load_mcq()
    theory_by_year = load_theory()

    years = sorted(set(list(mcq_by_year) + list(theory_by_year)), reverse=True)

    # render calls
    render_calls = []
    for y in years:
        if y in mcq_by_year:
            render_calls.append("if (igcseMcqData['%s']) renderIgcseMcqPanel('igcse-mcq-%s', igcseMcqData['%s']);" % (y, y, y))
        if y in theory_by_year:
            render_calls.append("if (igcseTheoryData['%s']) renderIgcseTheoryPanel('igcse-theory-%s', igcseTheoryData['%s']);" % (y, y, y))
    # (no auto-show: IGCSE panels stay collapsed until a cell is clicked)

    section_html = html_section(mcq_by_year, theory_by_year)

    js_block = (
        "<!-- IGCSE SCRIPT START -->\n"
        "<script>\n"
        + data_js(mcq_by_year, answer_key, theory_by_year)
        + "\n"
        + RENDER_JS
        + "\n// initial render\n"
        + "\n".join(render_calls)
        + "\n</script>\n"
        "<!-- IGCSE SCRIPT END -->\n"
    )

    # read main.html
    with open(MAIN, encoding="utf-8") as f:
        html = f.read()

    # Scope the 9702 grid click handler to its own grid so it doesn't also
    # attach to the IGCSE grid's .gp-cell elements.
    html = html.replace(
        "document.querySelectorAll('.gp-cell').forEach(function(cell) {",
        "document.querySelectorAll('#year-paper-grid .gp-cell').forEach(function(cell) {", 1)

    # backup
    if not os.path.exists(MAIN + ".bak2"):
        import shutil
        shutil.copy(MAIN, MAIN + ".bak2")

    # remove any previously injected IGCSE block
    html = re.sub(r"<!-- IGCSE SECTION START -->.*?<!-- IGCSE SECTION END -->", "", html, flags=re.DOTALL)

    # insert HTML section before the footer, JS block before </body>
    footer_marker = '<div class="footer">'
    body_marker = '</body>'

    html_section_block = (
        "<!-- IGCSE SECTION START -->\n" + section_html + "\n<!-- IGCSE SECTION END -->\n"
    )
    if footer_marker in html:
        html = html.replace(footer_marker, html_section_block + footer_marker, 1)
    else:
        html = html.replace(body_marker, html_section_block + body_marker, 1)

    html = re.sub(r"<!-- IGCSE SCRIPT START -->.*?<!-- IGCSE SCRIPT END -->",
                  "", html, flags=re.DOTALL)
    html = html.replace(body_marker, js_block + "\n" + body_marker, 1)

    # add a small CSS block for the IGCSE divider
    css = (
        "<style>"
        "#igcse-grid{grid-template-columns:78px repeat(2,1fr);}"
        "@media (max-width:560px){#igcse-grid{grid-template-columns:54px repeat(2,1fr);}}"
        ".igcse-divider{text-align:center;margin:40px 0 16px;padding-top:24px;border-top:2px solid #d3cec5;}"
        ".igcse-divider h2{font-family:'Didot','Bodoni 72','Playfair Display',Georgia,serif;font-style:italic;"
        "font-size:30px;color:#403d38;margin-bottom:4px;}"
        ".igcse-divider p{color:#a19b90;font-size:12px;}"
        ".p2-parts{margin-top:10px;}"
        ".p2-part{border-top:1px solid #e2ded7;padding:8px 0;}"
        ".p2-part-head{display:flex;justify-content:space-between;font-weight:700;color:#403d38;font-size:13px;}"
        ".p2-part-marks{color:#a19b90;font-weight:600;font-size:12px;}"
        ".p2-part-answer{font-size:13px;color:#56524c;margin-top:3px;line-height:1.5;}"
        "body.dark .igcse-divider h2{color:#d8d4cd;}"
        "body.dark .p2-part{border-top-color:#423e36;}"
        "body.dark .p2-part-answer{color:#b6b1a7;}"
        ".sub-card .sub-header .subsub-badge{margin-left:auto;}"
        ".sub-card .chevron{transition:transform 0.2s;color:#b3aea5;}"
        ".sub-card.sub-open .chevron{transform:rotate(180deg);}"
        ".sub-card .sub-header{cursor:default;}"
        ".sub-body{display:none;}"
        ".sub-card.sub-open .sub-body{display:block;}"
        ".syl-wrap{margin:4px 0 6px;}"
        ".syl-sub{font-weight:700;color:#403d38;margin-top:10px;margin-bottom:3px;font-size:13px;}"
        ".syl-sub-code{color:#8497a8;margin-right:6px;}"
        ".syl-points{list-style:disc;padding-left:20px;margin:2px 0 8px;}"
        ".syl-points li{font-size:12.5px;color:#6b665f;line-height:1.5;margin-bottom:2px;}"
        "body.dark .syl-sub{color:#d8d4cd;}"
        "body.dark .syl-points li{color:#a9a49a;}"
        "</style>"
    )
    if ".igcse-divider{" not in html:
        html = html.replace("</head>", css + "\n</head>", 1)

    with open(MAIN, "w", encoding="utf-8") as f:
        f.write(html)

    print("Injected IGCSE section into", MAIN)
    print("  MCQ papers:", {y: len(mcq_by_year[y]) for y in mcq_by_year})
    print("  Theory papers:", {y: len(theory_by_year[y]) for y in theory_by_year})
    print("  Answer key entries:", len(answer_key))


if __name__ == "__main__":
    main()
