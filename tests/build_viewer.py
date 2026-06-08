#!/usr/bin/env python3
"""Generate a single-file static HTML viewer for iteration-1 results.

The HTML embeds every output file inline (markdown rendered, CSV as tables,
Mermaid as text with a render hint). Includes a Benchmark tab with the same
numbers as benchmark.md, and a per-eval feedback textbox. "Submit All Reviews"
downloads feedback.json which can be re-read into the next iteration.
"""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
ITERATION = ROOT / "user-story-mapping-workspace" / "iteration-11"
OUT_HTML = ITERATION / "review.html"


def file_block(path: Path) -> str:
    """Render a single file as a collapsible block."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return f"<details><summary>{html.escape(path.name)} — read error</summary><pre>{html.escape(str(e))}</pre></details>"
    ext = path.suffix.lower()
    lang = {".md": "markdown", ".csv": "csv", ".mmd": "mermaid", ".json": "json", ".py": "python"}.get(ext, "")
    rendered = f'<pre class="lang-{lang}"><code>{html.escape(text)}</code></pre>'
    size_kb = path.stat().st_size / 1024
    return f'<details><summary>{html.escape(path.name)} <span class="muted">({size_kb:.1f} KB)</span></summary>{rendered}</details>'


def run_section(run_dir: Path, label: str) -> str:
    out_dir = run_dir / "outputs"
    if not out_dir.exists():
        return f"<div class='run'><h4>{html.escape(label)}</h4><p class='muted'>(no outputs)</p></div>"
    files = sorted([p for p in out_dir.rglob("*") if p.is_file()], key=lambda p: p.name.lower())

    grading_path = run_dir / "grading.json"
    timing_path = run_dir / "timing.json"
    grading_html = ""
    if grading_path.exists():
        grading = json.loads(grading_path.read_text(encoding="utf-8"))
        passed = sum(1 for e in grading["expectations"] if e["passed"])
        total = len(grading["expectations"])
        rows = "".join(
            f'<tr><td>{"✅" if e["passed"] else "❌"}</td><td>{html.escape(e["text"])}</td><td class="muted">{html.escape(e["evidence"][:300])}</td></tr>'
            for e in grading["expectations"]
        )
        grading_html = f'<details><summary><strong>Formal grades: {passed}/{total}</strong></summary><table class="grades"><tr><th></th><th>Assertion</th><th>Evidence</th></tr>{rows}</table></details>'

    timing_html = ""
    if timing_path.exists():
        t = json.loads(timing_path.read_text(encoding="utf-8"))
        timing_html = f'<p class="muted">Duration: {t.get("total_duration_seconds", 0):.1f}s · Tokens: {t.get("total_tokens", 0):,}</p>'

    files_html = "".join(file_block(p) for p in files)
    return f'<div class="run"><h4>{html.escape(label)}</h4>{timing_html}{grading_html}<div class="files">{files_html}</div></div>'


def main() -> int:
    benchmark = json.loads((ITERATION / "benchmark.json").read_text(encoding="utf-8"))
    per_eval = benchmark["per_eval"]
    cfg_with = benchmark["configurations"]["with_skill"]
    cfg_wo = benchmark["configurations"]["without_skill"]
    delta = benchmark["delta"]

    eval_sections = []
    eval_nav = []
    for e in per_eval:
        slug = e["eval_name"]
        eval_nav.append(f'<button class="eval-tab" data-target="eval-{slug}">{html.escape(e["eval_name"])}</button>')
        eval_dir = ITERATION / f"eval-{e['eval_id']}-{slug}"
        with_html = run_section(eval_dir / "with_skill", "WITH skill")
        without_html = run_section(eval_dir / "without_skill", "BASELINE (no skill)")
        prompt_html = html.escape(e["prompt"])
        eval_sections.append(f'''
        <section id="eval-{slug}" class="eval-pane">
          <h2>{html.escape(e["eval_name"])}</h2>
          <details class="prompt-block"><summary><strong>Prompt</strong></summary><pre>{prompt_html}</pre></details>
          <div class="two-col">{with_html}{without_html}</div>
          <div class="feedback-block">
            <label for="fb-{slug}"><strong>Your feedback for this eval</strong> (auto-saves; click Submit at top when done):</label>
            <textarea id="fb-{slug}" data-run-id="eval-{slug}-with_skill" rows="6" placeholder="What's good? What's missing? What should the next iteration change?"></textarea>
          </div>
        </section>
        ''')

    benchmark_rows = "".join(
        f'<tr><td>{html.escape(e["eval_name"])}</td>'
        f'<td>{e["with_skill"]["passed"]}/{e["with_skill"]["total"]} ({e["with_skill"]["pass_rate"]*100:.0f}%)</td>'
        f'<td>{e["without_skill"]["passed"]}/{e["without_skill"]["total"]} ({e["without_skill"]["pass_rate"]*100:.0f}%)</td>'
        f'<td>{e["with_skill"]["duration_seconds"]:.0f}s vs {e["without_skill"]["duration_seconds"]:.0f}s</td>'
        f'<td>{e["with_skill"]["tokens"]:,} vs {e["without_skill"]["tokens"]:,}</td></tr>'
        for e in per_eval
    )
    analyst_html = "".join(f'<li>{html.escape(n)}</li>' for n in benchmark["analyst_notes"])

    html_out = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>user-story-mapping — iteration 5 review</title>
<style>
  body {{ font-family: -apple-system, Segoe UI, sans-serif; max-width: 1300px; margin: 0 auto; padding: 20px; color: #222; }}
  h1 {{ border-bottom: 2px solid #4338ca; padding-bottom: 8px; }}
  h2 {{ color: #4338ca; margin-top: 0; }}
  .tabs {{ display: flex; gap: 4px; margin: 20px 0 0 0; border-bottom: 2px solid #ddd; }}
  .tab {{ padding: 10px 18px; cursor: pointer; background: #f3f4f6; border: 1px solid #ddd; border-bottom: none; border-radius: 6px 6px 0 0; }}
  .tab.active {{ background: white; border-color: #4338ca; color: #4338ca; font-weight: 600; }}
  .pane {{ display: none; padding: 20px 0; }}
  .pane.active {{ display: block; }}
  .eval-tabs {{ display: flex; gap: 4px; margin: 16px 0; flex-wrap: wrap; }}
  .eval-tab {{ padding: 8px 14px; cursor: pointer; background: #eef2ff; border: 1px solid #c7d2fe; border-radius: 6px; }}
  .eval-tab.active {{ background: #4338ca; color: white; }}
  .eval-pane {{ display: none; }}
  .eval-pane.active {{ display: block; }}
  .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }}
  .run {{ border: 1px solid #e5e7eb; padding: 16px; border-radius: 8px; background: #fafafa; }}
  .run h4 {{ margin: 0 0 8px 0; }}
  .files details {{ margin: 6px 0; }}
  .files summary {{ cursor: pointer; padding: 6px; background: #f3f4f6; border-radius: 4px; }}
  .files pre {{ background: #1f2937; color: #f3f4f6; padding: 12px; border-radius: 4px; overflow-x: auto; max-height: 500px; font-size: 12px; }}
  .prompt-block {{ background: #fffbeb; border: 1px solid #fcd34d; padding: 10px 14px; border-radius: 6px; margin: 10px 0; }}
  .prompt-block pre {{ white-space: pre-wrap; word-wrap: break-word; background: transparent; color: inherit; padding: 0; font-size: 13px; }}
  .grades {{ width: 100%; border-collapse: collapse; margin: 8px 0; font-size: 13px; }}
  .grades td, .grades th {{ padding: 6px 8px; border-bottom: 1px solid #e5e7eb; text-align: left; vertical-align: top; }}
  .grades th {{ background: #f3f4f6; }}
  .muted {{ color: #6b7280; font-size: 12px; }}
  .feedback-block {{ margin-top: 24px; padding: 14px; background: #ecfdf5; border: 1px solid #6ee7b7; border-radius: 6px; }}
  textarea {{ width: 100%; padding: 8px; font-family: inherit; font-size: 14px; border: 1px solid #d1d5db; border-radius: 4px; box-sizing: border-box; }}
  .summary-table {{ border-collapse: collapse; width: 100%; margin: 12px 0; }}
  .summary-table td, .summary-table th {{ padding: 10px; border: 1px solid #ddd; text-align: left; }}
  .summary-table th {{ background: #4338ca; color: white; }}
  .delta-good {{ color: #047857; font-weight: bold; font-size: 1.2em; }}
  button.submit {{ padding: 12px 24px; background: #4338ca; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 15px; font-weight: 600; }}
  button.submit:hover {{ background: #3730a3; }}
  .toast {{ position: fixed; bottom: 20px; right: 20px; padding: 14px 20px; background: #047857; color: white; border-radius: 6px; opacity: 0; transition: opacity 0.3s; }}
  .toast.show {{ opacity: 1; }}
</style>
</head>
<body>
<h1>user-story-mapping — iteration 5 review</h1>
<p>Skill outputs and benchmark for 3 test cases × 2 configurations (with-skill vs baseline). Auto-saves your feedback to localStorage; click <strong>Submit All Reviews</strong> to download <code>feedback.json</code>.</p>
<button class="submit" onclick="submitAll()">📥 Submit All Reviews (download feedback.json)</button>

<div class="tabs">
  <div class="tab active" data-target="pane-outputs">Outputs</div>
  <div class="tab" data-target="pane-benchmark">Benchmark</div>
</div>

<div id="pane-outputs" class="pane active">
  <div class="eval-tabs">{"".join(eval_nav)}</div>
  {"".join(eval_sections)}
</div>

<div id="pane-benchmark" class="pane">
  <h2>Summary</h2>
  <table class="summary-table">
    <tr><th>Configuration</th><th>Pass rate</th><th>Duration (mean)</th><th>Tokens (mean)</th></tr>
    <tr><td><strong>with_skill</strong></td><td>{cfg_with['pass_rate_mean']*100:.1f}% ± {cfg_with['pass_rate_stdev']*100:.1f}%</td><td>{cfg_with['duration_mean']:.0f}s</td><td>{cfg_with['tokens_mean']:,.0f}</td></tr>
    <tr><td>without_skill</td><td>{cfg_wo['pass_rate_mean']*100:.1f}% ± {cfg_wo['pass_rate_stdev']*100:.1f}%</td><td>{cfg_wo['duration_mean']:.0f}s</td><td>{cfg_wo['tokens_mean']:,.0f}</td></tr>
    <tr><td><strong>Δ (with − without)</strong></td><td class="delta-good">+{delta['pass_rate']*100:.1f}pp</td><td>{delta['duration_seconds']:+.0f}s</td><td>{delta['tokens']:+,.0f}</td></tr>
  </table>

  <h2>Per-eval</h2>
  <table class="summary-table">
    <tr><th>Eval</th><th>with_skill</th><th>without_skill</th><th>Duration</th><th>Tokens</th></tr>
    {benchmark_rows}
  </table>

  <h2>Analyst notes</h2>
  <ul>{analyst_html}</ul>
</div>

<div id="toast" class="toast"></div>

<script>
// Tab switching
document.querySelectorAll('.tab').forEach(t => t.addEventListener('click', () => {{
  document.querySelectorAll('.tab').forEach(x => x.classList.remove('active'));
  document.querySelectorAll('.pane').forEach(x => x.classList.remove('active'));
  t.classList.add('active');
  document.getElementById(t.dataset.target).classList.add('active');
}}));

// Eval sub-tabs
document.querySelectorAll('.eval-tab').forEach((t, i) => {{
  if (i === 0) {{
    t.classList.add('active');
    document.getElementById(t.dataset.target).classList.add('active');
  }}
  t.addEventListener('click', () => {{
    document.querySelectorAll('.eval-tab').forEach(x => x.classList.remove('active'));
    document.querySelectorAll('.eval-pane').forEach(x => x.classList.remove('active'));
    t.classList.add('active');
    document.getElementById(t.dataset.target).classList.add('active');
  }});
}});

// Auto-save feedback to localStorage
document.querySelectorAll('textarea').forEach(ta => {{
  const key = 'usm-feedback-' + ta.dataset.runId;
  const saved = localStorage.getItem(key);
  if (saved) ta.value = saved;
  ta.addEventListener('input', () => localStorage.setItem(key, ta.value));
}});

function showToast(msg) {{
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.add('show');
  setTimeout(() => el.classList.remove('show'), 2500);
}}

function submitAll() {{
  const reviews = [];
  document.querySelectorAll('textarea').forEach(ta => {{
    reviews.push({{
      run_id: ta.dataset.runId,
      feedback: ta.value || "",
      timestamp: new Date().toISOString(),
    }});
  }});
  const payload = JSON.stringify({{ reviews: reviews, status: "complete" }}, null, 2);
  const blob = new Blob([payload], {{ type: "application/json" }});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'feedback.json';
  a.click();
  URL.revokeObjectURL(url);
  showToast("Downloaded feedback.json — paste it into the iteration-1 workspace");
}}
</script>
</body>
</html>
'''
    OUT_HTML.write_text(html_out, encoding="utf-8")
    print(f"wrote {OUT_HTML}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
