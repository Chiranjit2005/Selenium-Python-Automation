"""
utils/report_generator.py
Generates a styled HTML execution report.
"""

import os
from datetime import datetime
from typing import List, Dict, Any

from config.config import REPORTS_DIR


def generate_html_report(results: List[Dict[str, Any]],
                          report_title: str = "Selenium Automation – Execution Report") -> str:
    """
    Build an HTML report from a list of step-result dicts.

    Each dict should contain:
        step          str   – e.g. "TC001 - Login"
        status        str   – "PASS" | "FAIL" | "SKIP"
        message       str   – details / assertion message
        screenshot    str   – absolute path to screenshot (optional)
        duration      float – seconds (optional)

    Returns the absolute path of the saved HTML file.
    """
    os.makedirs(REPORTS_DIR, exist_ok=True)

    now       = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename  = f"execution_report_{timestamp}.html"
    filepath  = os.path.join(REPORTS_DIR, filename)

    total  = len(results)
    passed = sum(1 for r in results if r.get("status", "").upper() == "PASS")
    failed = sum(1 for r in results if r.get("status", "").upper() == "FAIL")
    skipped = total - passed - failed
    pass_pct = round((passed / total * 100) if total else 0, 1)

    rows_html = ""
    for i, r in enumerate(results, 1):
        status    = r.get("status", "SKIP").upper()
        color     = {"PASS": "#2ecc71", "FAIL": "#e74c3c", "SKIP": "#f39c12"}.get(status, "#95a5a6")
        badge     = f'<span style="background:{color};color:#fff;padding:3px 10px;border-radius:12px;font-size:.8rem">{status}</span>'
        step      = r.get("step", f"Step {i}")
        message   = r.get("message", "—")
        duration  = f"{r.get('duration', 0):.2f}s" if r.get("duration") is not None else "—"
        screenshot = r.get("screenshot", "")
        ss_link   = (f'<a href="{screenshot}" target="_blank">'
                     f'<img src="{screenshot}" style="max-width:120px;border:1px solid #ccc;border-radius:4px">'
                     f'</a>'
                     if screenshot and os.path.exists(screenshot)
                     else "—")

        rows_html += f"""
        <tr style="border-bottom:1px solid #eee">
          <td style="padding:8px;text-align:center">{i}</td>
          <td style="padding:8px">{step}</td>
          <td style="padding:8px">{message}</td>
          <td style="padding:8px;text-align:center">{duration}</td>
          <td style="padding:8px;text-align:center">{badge}</td>
          <td style="padding:8px;text-align:center">{ss_link}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{report_title}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f4f6f9; color: #333; }}
  header {{ background: linear-gradient(135deg,#1a1a2e,#16213e,#0f3460); color: #fff; padding: 30px 40px; }}
  header h1 {{ font-size: 1.6rem; margin-bottom: 6px; }}
  header p  {{ font-size: .9rem; opacity: .75; }}
  .summary  {{ display: flex; gap: 16px; padding: 24px 40px; flex-wrap: wrap; }}
  .card     {{ background: #fff; border-radius: 10px; padding: 20px 28px; flex: 1;
               min-width: 140px; box-shadow: 0 2px 8px rgba(0,0,0,.08); text-align: center; }}
  .card .num{{ font-size: 2rem; font-weight: 700; }}
  .card .lbl{{ font-size: .8rem; color: #888; margin-top: 4px; }}
  .pass  {{ color: #2ecc71; }}
  .fail  {{ color: #e74c3c; }}
  .skip  {{ color: #f39c12; }}
  .total {{ color: #3498db; }}
  .pct   {{ color: #9b59b6; }}
  .container {{ padding: 0 40px 40px; }}
  table  {{ width:100%; border-collapse:collapse; background:#fff;
            border-radius:10px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,.08); }}
  thead  {{ background:linear-gradient(135deg,#0f3460,#16213e); color:#fff; }}
  th     {{ padding:12px 10px; text-align:left; font-size:.85rem; letter-spacing:.5px; }}
  tbody tr:hover {{ background:#fafafa; }}
  footer {{ text-align:center; padding:20px; font-size:.8rem; color:#aaa; }}
  .progress-bar-wrap {{ background:#e0e0e0; border-radius:8px; height:12px; margin-top:8px; }}
  .progress-bar       {{ background:#2ecc71; height:12px; border-radius:8px;
                          width:{pass_pct}%; transition:width .6s; }}
</style>
</head>
<body>
<header>
  <h1>🧪 {report_title}</h1>
  <p>Generated on {now.strftime("%B %d, %Y  %H:%M:%S")} &nbsp;|&nbsp; Application: tutorialsninja.com/demo/</p>
</header>

<div class="summary">
  <div class="card"><div class="num total">{total}</div><div class="lbl">Total Steps</div></div>
  <div class="card"><div class="num pass">{passed}</div><div class="lbl">Passed</div></div>
  <div class="card"><div class="num fail">{failed}</div><div class="lbl">Failed</div></div>
  <div class="card"><div class="num skip">{skipped}</div><div class="lbl">Skipped</div></div>
  <div class="card">
    <div class="num pct">{pass_pct}%</div>
    <div class="lbl">Pass Rate</div>
    <div class="progress-bar-wrap"><div class="progress-bar"></div></div>
  </div>
</div>

<div class="container">
  <table>
    <thead>
      <tr>
        <th>#</th>
        <th>Step / Test Case</th>
        <th>Result / Message</th>
        <th>Duration</th>
        <th>Status</th>
        <th>Screenshot</th>
      </tr>
    </thead>
    <tbody>
      {rows_html}
    </tbody>
  </table>
</div>
<footer>Selenium WebDriver Capstone &nbsp;|&nbsp; Python Automation Framework</footer>
</body>
</html>"""

    with open(filepath, "w", encoding="utf-8") as fh:
        fh.write(html)

    print(f"\n  📊  HTML Report generated → {filepath}")
    return filepath
