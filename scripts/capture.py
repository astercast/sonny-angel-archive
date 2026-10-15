#!/usr/bin/env python3
"""Render captures + fleet instruments for the archive.

Serves the repo locally, captures desktop (1440x900) and
phone (390x844, 320x700) frames of all three pages into the
progress archive, and measures at 320 and 390:
  - horizontal overflow (jumble class 1)
  - painted overlaps between visible blocks (jumble class 2)
  - sub-44px interactive targets (tap census)
Writes census.json next to the frames.
"""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = Path.home() / "workspace/progress-archive/sonny-angel-archive/rotation-036"
OUT.mkdir(parents=True, exist_ok=True)
PAGES = ["index.html", "guide.html", "watchlist.html"]

MEASURE = """() => {
  const vw = document.documentElement.clientWidth;
  const overflow = document.documentElement.scrollWidth > vw + 1;
  const els = [...document.querySelectorAll('a,button,input')].filter(e => {
    const r = e.getBoundingClientRect(); const s = getComputedStyle(e);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden';
  });
  const small = els.filter(e => { const r = e.getBoundingClientRect();
    return r.height < 43.5 || r.width < 20; })
    .map(e => ({tag: e.tagName, text: (e.textContent||'').trim().slice(0,40),
                h: Math.round(e.getBoundingClientRect().height)}));
  const blocks = [...document.querySelectorAll('.drop,.shop,.checks li,.warning')]
    .filter(e => e.getBoundingClientRect().height > 0);
  let overlaps = 0;
  for (let i = 0; i < blocks.length; i++) for (let j = i+1; j < blocks.length; j++) {
    const a = blocks[i].getBoundingClientRect(), b = blocks[j].getBoundingClientRect();
    if (a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom
        && !blocks[i].contains(blocks[j]) && !blocks[j].contains(blocks[i])) overlaps++;
  }
  return {overflow, small, overlaps, targets: els.length};
}"""

def main():
    census = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        for w, h, tag in [(1440, 900, "desktop"), (390, 844, "390"), (320, 700, "320")]:
            pg = b.new_page(viewport={"width": w, "height": h})
            for name in PAGES:
                pg.goto(f"http://127.0.0.1:8931/{name}", wait_until="networkidle")
                pg.wait_for_timeout(600)
                stem = name.replace(".html", "")
                if tag == "desktop":
                    pg.screenshot(path=str(OUT / f"{stem}-desktop.png"))
                if tag in ("320", "390"):
                    pg.screenshot(path=str(OUT / f"{stem}-{tag}.png"))
                    census[f"{name}@{tag}"] = pg.evaluate(MEASURE)
            pg.close()
        b.close()
    (OUT / "census.json").write_text(json.dumps(census, indent=1))
    bad = {k: v for k, v in census.items() if v["overflow"] or v["overlaps"]}
    print("overflow/overlap failures:", bad if bad else "none")
    for k, v in census.items():
        print(k, "targets:", v["targets"], "sub44:", len(v["small"]), v["small"][:4])

if __name__ == "__main__":
    main()
