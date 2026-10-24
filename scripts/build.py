#!/usr/bin/env python3
"""Build step for the Sonny Angel USA Archive (TS2 + TS4, rotation 143).

Run: python3 scripts/build.py

Why this exists (the SO4 / TS2 tension, settled at rotation 143):
the standing order is that no price ever appears on a card or on
any public surface, while the price record itself is kept as part
of the archive's internal data. Until rotation 143 this repo had
no build step, so the internal record and the public file were the
same file (data/v1/drops.json) and the price field shipped
publicly even though nothing rendered it.

Now there are two files:
- data-src/drops.internal.json: the INTERNAL source of truth.
  Every drop keeps its price_usd record here. This directory is
  listed in .vercelignore and never ships.
- data/v1/drops.json: the PUBLIC file, generated here. Every
  price field is stripped at build time, so no future template
  can show a price by accident (TS2).

TS4: the river (and the featured card, and the count line) are
pre-rendered into index.html here, in exactly the markup
assets/app.js generates, so the page is complete without
JavaScript. app.js still fetches the public data and re-renders
the identical markup when it filters or searches.

Publishing (round 2, 2026-10-24): the same run assembles the
site/ folder, only the pages, assets/ and data/v1/, and
vercel.json serves site/ as its outputDirectory with this
script as its buildCommand. data-src/, scripts/ and the repo
notes are never copied into site/, so a Git build publishes
only the site. (.vercelignore alone could not do this: it
only applies to CLI uploads, not Git builds.)

The build is deterministic apart from one date rule, shared with
app.js: a drop counts as released when its date string is not
after the build day, and "upcoming / out now" follows from that.
Re-running the build on the same day changes nothing.
"""
import json
import re
import shutil
import sys
from copy import deepcopy
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
INTERNAL = ROOT / "data-src" / "drops.internal.json"
PUBLIC = ROOT / "data" / "v1" / "drops.json"
INDEX = ROOT / "index.html"
SITE = ROOT / "site"
SITE_PAGES = ("index.html", "timeline.html", "guide.html", "watchlist.html", "404.html")

PRICE_KEY = re.compile(r"price", re.I)


def strip_prices(node):
    """Remove every price-named field, at any depth (TS2)."""
    if isinstance(node, dict):
        return {k: strip_prices(v) for k, v in node.items() if not PRICE_KEY.search(k)}
    if isinstance(node, list):
        return [strip_prices(v) for v in node]
    return node


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def ebay(d):
    # encodeURIComponent: python quote with the same unreserved set.
    return "https://www.ebay.com/sch/i.html?_nkw=" + quote(d["ebay_query"], safe="-_.!~*'()")


def plate(d):
    if d.get("image"):
        return ('<div class="plate"><img src="' + esc(d["image"])
                + '" alt="Official product photo, ' + esc(d["name"])
                + '" loading="lazy" decoding="async" onerror="this.parentNode.innerHTML=\''
                + '<span class=&quot;initial&quot; aria-hidden=&quot;true&quot;>'
                + esc(d["name"][0]) + "</span>'\"></div>")
    return ('<div class="plate"><span class="initial" aria-hidden="true">'
            + esc(d["name"][0]) + '</span></div><p class="nophoto">No photo yet.</p>')


def row(d):
    return ('<article class="drop"><div>' + plate(d) + '</div><div class="dropbody">'
            + '<p class="dropdate">' + esc(d["display_date"]) + "</p>"
            + '<h3 class="dropname">' + esc(d["name"])
            + '<span class="fam">' + esc(d["family"]) + "</span></h3>"
            + "<p>" + esc(d["theme"]) + "</p>"
            + '<p class="lineup"><b>Lineup.</b> ' + esc(d["lineup"]) + "</p>"
            + '<p class="secretline"><b>Secret.</b> ' + esc(d["secret"]) + "</p>"
            + '<a class="ebay" href="' + ebay(d) + '" rel="noopener nofollow">'
            + "Search eBay for this series</a></div></article>")


def river_html(drops):
    html, year = "", None
    for d in drops:
        y = str(d["sort"])[:4]
        if y != year:
            if year is not None:
                html += "</div></div>"
            year = y
            html += ('<div class="yearblock"><div class="year" aria-label="Year '
                     + y + '">' + y + '</div><div class="rows">')
        html += row(d)
    return html + "</div></div>"


def featured_html(drops, today):
    released = [d for d in drops if d["date"] <= today]
    if not released:
        return ""
    d = released[-1]
    parts = d["name"].split(", Sonny Angel x ")
    title = parts[0]
    collab = ("Sonny Angel x " + parts[1]) if len(parts) > 1 else ""
    secret = "Not confirmed yet." if d["secret"].startswith("To be confirmed") else d["secret"]
    state = " \u00b7 Upcoming" if d["date"] > today else " \u00b7 Out now"
    html = ('<article class="index-card featured" aria-labelledby="new-h">'
            + '<p class="card-tab">Newest</p>')
    if d.get("image"):
        html += ('<figure class="card-photo"><img src="' + esc(d["image"])
                 + '" alt="Official product photo, ' + esc(d["name"])
                 + '" width="828" height="828" fetchpriority="high" decoding="async">'
                 + '<span class="tape" aria-hidden="true"></span></figure>')
    html += ('<div class="card-lines">'
             + '<p class="card-date">' + esc(d["display_date"]) + state + "</p>"
             + '<h2 class="card-name" id="new-h">' + esc(title) + "</h2>"
             + '<p class="card-collab">'
             + (esc(collab) + " \u00b7 " if collab else "") + esc(d["family"]) + "</p>"
             + "<p>" + esc(d["theme"]) + "</p>"
             + "<p><b>Lineup.</b> " + esc(d["lineup"]) + "</p>"
             + '<p><b class="secret">Secret.</b> ' + esc(secret) + "</p>"
             + '<p><a class="card-link" href="' + ebay(d)
             + '" rel="noopener nofollow">Search eBay for this series</a></p>'
             + '</div><span class="card-hole" aria-hidden="true"></span></article>')
    return html


def replace_block(html, start_marker, end_marker, new_inner, label):
    """Replace everything between start_marker and the next
    end_marker with new_inner, keeping both markers. Idempotent:
    a re-run finds the previously generated block the same way."""
    i = html.find(start_marker)
    if i < 0:
        sys.exit(f"BUILD FAILED: {label} start marker not found in index.html")
    j = html.find(end_marker, i + len(start_marker))
    if j < 0:
        sys.exit(f"BUILD FAILED: {label} end marker not found in index.html")
    return html[: i + len(start_marker)] + new_inner + html[j:]


def assemble_site():
    """Copy only the public site into site/ (see module docstring)."""
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()
    for name in SITE_PAGES:
        shutil.copy2(ROOT / name, SITE / name)
    shutil.copytree(ROOT / "assets", SITE / "assets",
                    ignore=shutil.ignore_patterns("*.md"))
    shutil.copytree(ROOT / "data" / "v1", SITE / "data" / "v1")
    shipped = sorted(str(p.relative_to(SITE)) for p in SITE.rglob("*") if p.is_file())
    bad = [s for s in shipped
           if s.startswith(("data-src", "scripts")) or s.endswith(".md")
           or "internal" in s or "BRIEF" in s]
    if bad:
        sys.exit(f"BUILD FAILED: internal files leaked into site/: {bad}")
    return shipped


def main():
    internal = json.loads(INTERNAL.read_text(encoding="utf-8"))
    drops = internal["drops"]
    for d in drops:
        if not d.get("price_usd"):
            sys.exit(f"BUILD FAILED: internal record {d.get('id')} has no price_usd; "
                     "the internal source must stay complete (SO4)")

    public = strip_prices(deepcopy(internal))
    for d in public["drops"]:
        leaked = [k for k in d if PRICE_KEY.search(k)]
        if leaked:
            sys.exit(f"BUILD FAILED: price fields survived the strip on {d.get('id')}: {leaked}")
    PUBLIC.write_text(json.dumps(public, indent=1, sort_keys=True) + "\n", encoding="utf-8")

    ordered = sorted(public["drops"], key=lambda x: x["sort"])
    today = date.today().isoformat()
    html = INDEX.read_text(encoding="utf-8")
    html = replace_block(html, '<div id="featured-mount">', '<div class="finder">',
                         featured_html(ordered, today) + "</div>\n    ", "featured")
    html = replace_block(html, '<section id="river" aria-live="polite">', "</main>",
                         river_html(ordered) + "</section>\n", "river")
    count = f"Showing {len(ordered)} of {public['meta']['catalogued']} releases."
    html, n = re.subn(r'(<span id="count-line">)[^<]*(</span>)',
                      lambda m: m.group(1) + count + m.group(2), html)
    if n != 1:
        sys.exit("BUILD FAILED: count-line span not found exactly once in index.html")
    INDEX.write_text(html, encoding="utf-8")
    shipped = assemble_site()
    print(f"BUILD OK: public drops {len(ordered)} (price fields stripped), "
          f"river pre-rendered ({len(set(str(d['sort'])[:4] for d in ordered))} year blocks), "
          f"featured = newest released as of {today}, "
          f"site/ assembled ({len(shipped)} public files, no data-src, scripts or notes)")


if __name__ == "__main__":
    main()
