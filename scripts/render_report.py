#!/usr/bin/env python3
"""Render a polished, print-friendly wrong-answer diagnostic report from JSON."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def esc(value: object) -> str:
    return html.escape(str(value if value is not None else ""))


def list_items(items: list[object], ordered: bool = False) -> str:
    tag = "ol" if ordered else "ul"
    body = "".join(f"<li>{esc(item)}</li>" for item in items)
    return f"<{tag}>{body}</{tag}>"


def render(data: dict) -> str:
    meta = data.get("meta", {})
    original = data.get("original", {})
    diagnosis = data.get("diagnosis", [])
    practice = data.get("practice", [])
    review = data.get("review", [])
    answers = data.get("answers", [])

    diagnosis_html = "".join(
        f"""
        <article class="diagnosis-card">
          <div class="card-head"><h3>{esc(item.get('label', '待确认'))}</h3><span class="badge">置信度 {esc(item.get('confidence', '低'))}</span></div>
          <p><strong>观察证据：</strong>{esc(item.get('evidence', ''))}</p>
          {f'<p class="muted"><strong>另一种可能：</strong>{esc(item.get("alternative"))}</p>' if item.get('alternative') else ''}
        </article>
        """
        for item in diagnosis
    ) or '<p class="muted">暂无足够证据，建议补充一道对比题。</p>'

    practice_html = "".join(
        f"""
        <section class="practice-block">
          <div><span class="eyebrow">LEVEL {index}</span><h3>{esc(group.get('title', '变式训练'))}</h3><p>{esc(group.get('subtitle', ''))}</p></div>
          <ol class="questions">{''.join(f'<li><span>{esc(q)}</span><i></i></li>' for q in group.get('questions', []))}</ol>
        </section>
        """
        for index, group in enumerate(practice, 1)
    )

    review_html = "".join(
        f"""
        <div class="review-card"><span class="calendar">{index}</span><div><strong>{esc(item.get('when', '稍后'))}</strong>{list_items(item.get('questions', []))}</div></div>
        """
        for index, item in enumerate(review, 1)
    )

    answer_html = "".join(
        f'<div class="answer"><span>{index}</span><strong>{esc(answer)}</strong></div>'
        for index, answer in enumerate(answers, 1)
    )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(meta.get('title', '错题诊断与变式训练'))}</title>
<style>
:root{{--ink:#25243a;--muted:#6f7185;--purple:#5b5bd6;--mint:#24a58f;--sun:#f5b547;--paper:#fff;--wash:#f5f4ff;--line:#e7e5f2}}
*{{box-sizing:border-box}} body{{margin:0;background:#ecebf4;color:var(--ink);font:15px/1.65 "Microsoft YaHei","PingFang SC",sans-serif}}
.page{{width:min(920px,calc(100% - 32px));margin:28px auto;background:var(--paper);border-radius:28px;box-shadow:0 18px 60px #34325c1a;overflow:hidden}}
.hero{{padding:42px 48px 34px;background:linear-gradient(135deg,#5b5bd6 0%,#7469df 56%,#3bb4a2 100%);color:white;position:relative}}
.hero:after{{content:"";position:absolute;width:210px;height:210px;border:42px solid #ffffff18;border-radius:50%;right:-76px;top:-104px}}
.hero .kicker{{letter-spacing:.18em;font-size:12px;font-weight:800;opacity:.8}} h1{{font-size:32px;line-height:1.2;margin:8px 0 22px}} .meta{{display:flex;gap:10px;flex-wrap:wrap}} .meta span{{padding:6px 12px;border-radius:999px;background:#ffffff1f;border:1px solid #ffffff35}}
.content{{padding:34px 48px 48px}} .summary{{font-size:20px;font-weight:700;background:#fff7dc;border-left:6px solid var(--sun);padding:20px 22px;border-radius:6px 18px 18px 6px}}
.section-title{{display:flex;align-items:center;gap:12px;margin:34px 0 16px}} .section-title span{{display:grid;place-items:center;width:34px;height:34px;border-radius:11px;background:var(--wash);color:var(--purple);font-weight:900}} .section-title h2{{font-size:21px;margin:0}}
.original-grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px}} .mini{{padding:17px;border:1px solid var(--line);border-radius:16px;background:#fcfcff}} .mini b{{display:block;font-size:12px;color:var(--muted);margin-bottom:6px}}
.diagnosis-card{{padding:20px 22px;border:1px solid #dddaf7;border-radius:18px;background:linear-gradient(145deg,#fbfaff,#f5fffd)}} .card-head{{display:flex;justify-content:space-between;gap:12px;align-items:center}} .card-head h3{{margin:0}} .badge{{font-size:12px;background:#e8e6ff;color:#4747bd;border-radius:999px;padding:5px 10px;white-space:nowrap}} .muted{{color:var(--muted)}}
.explain{{display:grid;grid-template-columns:.8fr 1.2fr;gap:16px}} .speech{{padding:22px;border-radius:20px;background:#e8faf6;font-size:17px;font-weight:700}} .steps{{margin:0;padding:18px 20px 18px 42px;border:1px solid var(--line);border-radius:20px}} .steps li+li{{margin-top:8px}}
.practice-block{{display:grid;grid-template-columns:240px 1fr;gap:24px;padding:24px 0;border-top:1px dashed #d9d7e7}} .eyebrow{{font-size:11px;letter-spacing:.14em;color:var(--purple);font-weight:900}} .practice-block h3{{margin:3px 0 0}} .practice-block p{{margin:3px 0;color:var(--muted)}} .questions{{margin:0;padding-left:28px}} .questions li{{padding:8px 0 13px 5px}} .questions i{{display:block;border-bottom:1px solid #aaa9ba;margin-top:14px}}
.review-grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px}} .review-card{{display:flex;gap:14px;padding:17px;border-radius:18px;background:#fff8e7;border:1px solid #f4ddb0}} .calendar{{display:grid;place-items:center;min-width:36px;height:36px;border-radius:12px;background:var(--sun);color:white;font-weight:900}} .review-card ul{{padding-left:18px;margin:6px 0 0}}
.adult{{padding:20px;border-radius:18px;background:#f3f2fa;border:1px solid var(--line)}}
.answer-page{{page-break-before:always;padding:44px 48px 54px}} .answer-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}} .answer{{display:flex;align-items:center;gap:10px;padding:14px;border-radius:14px;background:var(--wash)}} .answer span{{display:grid;place-items:center;width:26px;height:26px;border-radius:8px;background:var(--purple);color:white;font-size:12px}} .footer{{margin-top:38px;color:var(--muted);font-size:12px;text-align:center}}
@media(max-width:680px){{.hero,.content,.answer-page{{padding-left:24px;padding-right:24px}}.original-grid,.explain,.review-grid{{grid-template-columns:1fr}}.practice-block{{grid-template-columns:1fr;gap:5px}}.answer-grid{{grid-template-columns:1fr 1fr}}}}
@media print{{@page{{size:A4;margin:10mm}}body{{background:white}}.page{{width:100%;margin:0;box-shadow:none;border-radius:0}}.hero{{padding:28px 34px 24px;-webkit-print-color-adjust:exact;print-color-adjust:exact}}.content{{padding:22px 34px 30px}}.section-title{{margin-top:24px}}.practice-block{{break-inside:avoid;padding:17px 0}}.answer-page{{padding:20px 34px}}}}
</style>
</head>
<body>
<main class="page">
  <header class="hero">
    <div class="kicker">LEARN FROM THE FIRST DIVERGENCE</div>
    <h1>{esc(meta.get('title', '错题诊断与变式训练'))}</h1>
    <div class="meta"><span>{esc(meta.get('student', '学生'))}</span><span>{esc(meta.get('grade', '年级待补充'))}</span><span>{esc(meta.get('topic', '专项训练'))}</span><span>{esc(meta.get('date', ''))}</span></div>
  </header>
  <div class="content">
    <div class="summary">{esc(data.get('summary', '先找到第一处偏差，再进行针对练习。'))}</div>
    <div class="section-title"><span>1</span><h2>原题复盘</h2></div>
    <div class="original-grid"><div class="mini"><b>原题</b>{esc(original.get('question'))}</div><div class="mini"><b>学生答案 / 正确答案</b>{esc(original.get('student_answer'))} &nbsp;→&nbsp; {esc(original.get('correct_answer'))}</div><div class="mini" style="grid-column:1/-1"><b>第一处分歧</b>{esc(original.get('first_divergence'))}</div></div>
    <div class="section-title"><span>2</span><h2>错因诊断</h2></div>{diagnosis_html}
    <div class="section-title"><span>3</span><h2>把关键一步讲明白</h2></div>
    <div class="explain"><div class="speech">{esc(data.get('child_explanation', ''))}</div><ol class="steps">{''.join(f'<li>{esc(step)}</li>' for step in data.get('worked_example', []))}</ol></div>
    <div class="section-title"><span>4</span><h2>分层变式训练</h2></div>{practice_html}
    <div class="section-title"><span>5</span><h2>延迟复习</h2></div><div class="review-grid">{review_html}</div>
    <div class="section-title"><span>6</span><h2>给家长 / 教师</h2></div><div class="adult">{esc(data.get('adult_note', '观察下一次独立完成时是否仍出现同一偏差。'))}</div>
  </div>
  <section class="answer-page"><span class="eyebrow">ANSWER KEY</span><h2>答案与核验</h2><p class="muted">答案顺序：分层训练题在前，延迟复习题在后。</p><div class="answer-grid">{answer_html}</div><div class="footer">错题不是标签，而是下一步教学的证据。</div></section>
</main>
</body>
</html>"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", type=Path)
    parser.add_argument("output_html", type=Path)
    args = parser.parse_args()
    data = json.loads(args.input_json.read_text(encoding="utf-8"))
    args.output_html.parent.mkdir(parents=True, exist_ok=True)
    args.output_html.write_text(render(data), encoding="utf-8")
    print(f"Rendered {args.output_html}")


if __name__ == "__main__":
    main()

