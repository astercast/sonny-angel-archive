#!/usr/bin/env python3
"""Captures for the Full Timeline surface (2026-10-15)."""
import json, subprocess, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parent.parent
OUT = Path.home() / "workspace/progress-archive/sonny-angel-archive/2026-10-15-full-timeline"
OUT.mkdir(parents=True, exist_ok=True)
MEASURE = """() => {
  const vw = document.documentElement.clientWidth;
  const overflow = document.documentElement.scrollWidth > vw + 1;
  const els = [...document.querySelectorAll('a,button,input')].filter(e => {
    const r = e.getBoundingClientRect(); const s = getComputedStyle(e);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden'; });
  const small = els.filter(e => { const r = e.getBoundingClientRect();
    return r.height < 43.5 || r.width < 20; })
    .map(e => ({tag: e.tagName, text: (e.textContent||'').trim().slice(0,40), h: Math.round(e.getBoundingClientRect().height)}));
  return {overflow, small, targets: els.length, drops: document.querySelectorAll('.drop').length,
          count: (document.getElementById('count-line')||{}).textContent || ''};
}"""
srv = subprocess.Popen([sys.executable, "-m", "http.server", "8932", "--directory", str(ROOT)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
try:
    census = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        for w, h, tag in [(1440, 900, "desktop"), (390, 844, "390")]:
            pg = b.new_page(viewport={"width": w, "height": h})
            pg.goto("http://127.0.0.1:8932/timeline.html", wait_until="networkidle")
            pg.wait_for_timeout(700)
            pg.screenshot(path=str(OUT / f"timeline-{tag}.png"))
            pg.screenshot(path=str(OUT / f"timeline-{tag}-full.png"), full_page=True)
            census[tag] = pg.evaluate(MEASURE)
            pg.close()
        b.close()
    (OUT / "census.json").write_text(json.dumps(census, indent=1))
    print(json.dumps(census, indent=1))
finally:
    srv.terminate()
