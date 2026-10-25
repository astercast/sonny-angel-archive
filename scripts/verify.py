#!/usr/bin/env python3
"""Standing checks for the Sonny Angel USA Archive tree.

Run: python3 scripts/verify.py
Fails loudly on: em dashes in presented copy, drops without
provenance, pictured drops without an image source, count
drift between the data file and its meta block, duplicate
ids, unsorted sort keys, and prices or resale figures in the
fields rendered on a series card. Also (rotation 143): any price
field surviving in the PUBLIC data file (TS2: prices live only
in the internal source, data-src/drops.internal.json, which
must itself stay complete), and a river that is not fully
pre-rendered into index.html (TS4).
"""
import json, re, sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
fail = []

pages = ["index.html", "guide.html", "watchlist.html", "404.html", "timeline.html", "sheet.html",
         "assets/style.css", "assets/app.js", "assets/watchlist.js", "assets/timeline.js",
         "assets/shelf.css", "assets/shelf.js", "assets/pulse.css", "assets/pulse.js"]
for p in pages:
    t = (root / p).read_text(encoding="utf-8")
    if "\u2014" in t or "\u2013" in t:
        fail.append(f"em/en dash found in presented file {p}")

d = json.loads((root / "data/v1/drops.json").read_text())
drops = d["drops"]
if len(drops) != d["meta"]["catalogued"]:
    fail.append("meta.catalogued does not match drop count")
ids = [x["id"] for x in drops]
if len(set(ids)) != len(ids):
    fail.append("duplicate drop ids")
sorts = [x["sort"] for x in drops]
if sorts != sorted(sorts):
    fail.append("drops are not in sort order in the file")

# TS2 (rotation 143): the public file ships no price field at all;
# the internal source keeps the complete record, price included.
for x in drops:
    leaked = [k for k in x if "price" in k.lower()]
    if leaked:
        fail.append(f"{x['id']}: price field in PUBLIC data: {leaked}")
internal_path = root / "data-src" / "drops.internal.json"
if not internal_path.exists():
    fail.append("internal source missing: data-src/drops.internal.json")
else:
    internal = json.loads(internal_path.read_text())["drops"]
    if [x["id"] for x in internal] != ids:
        fail.append("internal source drop ids do not match the public file, in order")
    for x in internal:
        if not x.get("price_usd"):
            fail.append(f"{x['id']}: internal record missing price_usd")
        if "\u2014" in str(x.get("price_usd", "")):
            fail.append(f"{x['id']}: em dash in internal price_usd")

# TS4 (rotation 143): index.html carries the whole river and the
# featured card as built markup, so the page is complete with no
# JavaScript. app.js re-renders the identical markup to filter.
index_html = (root / "index.html").read_text(encoding="utf-8")
if index_html.count('<article class="drop">') != len(drops):
    fail.append("river is not fully pre-rendered in index.html (drop article count)")
year_count = len({str(x["sort"])[:4] for x in drops})
if index_html.count('<div class="yearblock">') != year_count:
    fail.append("river is not fully pre-rendered in index.html (year block count)")
if '<article class="index-card featured"' not in index_html:
    fail.append("featured card is not pre-rendered in index.html")
if not re.search(r'<span id="count-line">[^<]+</span>', index_html):
    fail.append("count line is not pre-rendered in index.html")
CARD_FIELDS = ("display_date", "name", "family", "theme", "lineup", "secret")
CARD_MONEY_PATTERNS = [
    re.compile(r"[$€£¥]"),
    re.compile(r"\b(?:USD|CAD|GBP|EUR|dollars?|pounds?|euros?|cents?|bucks)\b", re.I),
    re.compile(r"\b(?:price|priced|pricing|resale|resell|resold|market\s+value)\b", re.I),
    re.compile(r"\b\d+(?:[.,]\d+)?\s*(?:USD|CAD|GBP|EUR|dollars?|pounds?|euros?|cents?|bucks)\b", re.I),
]
for x in drops:
    for field in CARD_FIELDS:
        value = str(x.get(field, ""))
        if any(pattern.search(value) for pattern in CARD_MONEY_PATTERNS):
            fail.append(f"{x['id']}: price or resale figure in card field {field}")
    if not x.get("source"):
        fail.append(f"{x['id']}: missing source provenance")
    if x.get("image"):
        if not x.get("image_source"):
            fail.append(f"{x['id']}: image without image_source")
        img = x["image"]
        if img.startswith("http"):
            fail.append(f"{x['id']}: image is a hotlink, must be self hosted")
        else:
            p = root / img
            if not p.exists():
                fail.append(f"{x['id']}: image file missing: {img}")
            else:
                head = p.read_bytes()[:8]
                if not (head[:3] == b"\xff\xd8\xff" or head[:8] == b"\x89PNG\r\n\x1a\n"):
                    fail.append(f"{x['id']}: image file is not a JPEG or PNG: {img}")
    if not x.get("ebay_query"):
        fail.append(f"{x['id']}: missing ebay_query")
    for key in ("name", "theme", "lineup", "secret", "price_usd"):
        if "\u2014" in str(x.get(key, "")):
            fail.append(f"{x['id']}: em dash in {key}")
pictured = sum(1 for x in drops if x.get("image"))
print(f"drops={len(drops)} pictured={pictured} absent={len(drops)-pictured}")

# Round 2 (2026-10-24): no price FIGURES in any presented copy.
# (The word price may appear, for example the guide's price check;
# an amount, a dollar figure or a percent off never may.)
PRICE_FIGURE_PATTERNS = [
    re.compile(r"\$\s*\d"),
    re.compile(r"\b\d+(?:[.,]\d+)?\s*(?:dollars|USD|bucks)\b", re.I),
    re.compile(r"\b(?:\d+|ten|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)\s+percent\b", re.I),
]
for p in pages + ["guide.html", "data/v1/watchlist.json"]:
    t = (root / p).read_text(encoding="utf-8")
    for pattern in PRICE_FIGURE_PATTERNS:
        if pattern.search(t):
            fail.append(f"price figure in presented copy {p}: {pattern.pattern}")

# Bundle 2026-10-24 (My sticker sheet + heartbeat): the word
# price itself never appears in any PUBLIC data file. This is the
# verify-side mirror of the guard step in
# scripts/heartbeat/stock.py (which fails the heartbeat run on
# the same condition) and of the workflow guard step.
for name in ("drops.json", "history.json", "watchlist.json",
             "stock.json", "candidates.json", "pulse.json"):
    p = root / "data/v1" / name
    if not p.exists():
        fail.append(f"data/v1/{name} missing (heartbeat seed: scripts/heartbeat/stock.py)")
    elif "price" in p.read_text(encoding="utf-8").lower():
        fail.append(f"price text in public data file data/v1/{name}")

# The sheet page exists, mounts the sheet, and every page's main
# nav carries My Sheet between Real or Fake and Watchlist.
sheet = (root / "sheet.html").read_text(encoding="utf-8")
if '<main id="m" class="sheet">' not in sheet:
    fail.append("sheet.html: mount point <main id=\"m\" class=\"sheet\"> missing")
if "mountSheet" not in sheet or "assets/shelf.js" not in sheet:
    fail.append("sheet.html: shelf.js mount script missing")
if "assets/shelf.css" not in sheet:
    fail.append("sheet.html: shelf.css link missing")
for p in ("index.html", "timeline.html", "guide.html", "watchlist.html", "sheet.html"):
    t = (root / p).read_text(encoding="utf-8")
    nav = t[t.find('<nav aria-label="Main">'):t.find("</nav>")]
    order = [nav.find(x) for x in ("Real or Fake", "My Sheet", "Watchlist")]
    if -1 in order or order != sorted(order):
        fail.append(f"{p}: main nav does not carry My Sheet between Real or Fake and Watchlist")
    if "assets/pulse.js" not in t or "assets/pulse.css" not in t:
        fail.append(f"{p}: pulse kit not wired")
t404 = (root / "404.html").read_text(encoding="utf-8")
nav404 = t404[t404.find('<nav aria-label="Main">'):t404.find("</nav>")]
order404 = [nav404.find(x) for x in ("Real or Fake", "My Sheet", "Watchlist")]
if -1 in order404 or order404 != sorted(order404):
    fail.append("404.html: main nav does not carry My Sheet between Real or Fake and Watchlist")

w = json.loads((root / "data/v1/watchlist.json").read_text())
for s in w["retailers"]:
    if not s.get("verification") or not s.get("verified"):
        fail.append(f"watchlist {s.get('name')}: missing verification")
print(f"watchlist_verified={len(w['retailers'])} not_listed={len(w['checked_not_listed'])}")

if fail:
    print("VERIFY FAILED:")
    [print(" -", f) for f in fail]
    sys.exit(1)
_early_ok = True

h = json.loads((root / "data/v1/history.json").read_text())
entries = h["entries"]
if len(entries) != h["meta"]["entries"]:
    fail.append("history meta.entries does not match entry count")
names = [x["name"] for x in entries]
if len(set(names)) != len(names):
    fail.append("duplicate history entry names")
years = [x["year"] for x in entries if x["year"] is not None]
if years != sorted(years):
    fail.append("history entries are not in year order")
for x in entries:
    if not x.get("source"):
        fail.append(f"history {x['name']}: missing source provenance")
    if x.get("evidence") not in ("A", "B", "C"):
        fail.append(f"history {x['name']}: evidence level missing")
    for field in ("name", "scope", "display"):
        value = str(x.get(field, ""))
        if any(pattern.search(value) for pattern in CARD_MONEY_PATTERNS):
            fail.append(f"history {x['name']}: price or resale figure in {field}")
    if x.get("image"):
        if not x.get("image_source"):
            fail.append(f"history {x['name']}: image without image_source")
        img = x["image"]
        if img.startswith("http"):
            fail.append(f"history {x['name']}: image is a hotlink, must be self hosted")
        else:
            ip = root / img
            if not ip.exists():
                fail.append(f"history {x['name']}: image file missing: {img}")
            else:
                head = ip.read_bytes()[:8]
                if not (head[:3] == b"\xff\xd8\xff" or head[:8] == b"\x89PNG\r\n\x1a\n"):
                    fail.append(f"history {x['name']}: image file is not a JPEG or PNG: {img}")
    if "\u2014" in str(x.get("image_source", "")):
        fail.append(f"history {x['name']}: em dash in image_source")
print(f"history_entries={len(entries)}")

# Round 2 (2026-10-24): when a build has assembled site/, it must
# hold the whole public site and nothing internal.
site = root / "site"
if site.exists():
    for name in ("index.html", "timeline.html", "guide.html", "watchlist.html", "404.html", "sheet.html",
                 "assets/style.css", "assets/catalog.css", "assets/app.js",
                 "assets/timeline.js", "assets/watchlist.js",
                 "assets/shelf.css", "assets/shelf.js", "assets/pulse.css", "assets/pulse.js",
                 "data/v1/drops.json", "data/v1/history.json", "data/v1/watchlist.json",
                 "data/v1/stock.json", "data/v1/candidates.json", "data/v1/pulse.json"):
        if not (site / name).exists():
            fail.append(f"site/ is missing {name}")
    for name in ("index.html", "timeline.html", "guide.html", "watchlist.html", "404.html", "sheet.html"):
        if '<meta name="built"' not in (site / name).read_text(encoding="utf-8"):
            fail.append(f"site/{name}: build stamp <meta name=\"built\"> missing (pulse bar needs it)")
    for name in ("stock.json", "candidates.json", "pulse.json"):
        if "price" in (site / "data/v1" / name).read_text(encoding="utf-8").lower():
            fail.append(f"price text in shipped public data file site/data/v1/{name}")
    for p in site.rglob("*"):
        if p.is_file():
            rel = str(p.relative_to(site))
            if rel.startswith(("data-src", "scripts")) or rel.endswith(".md") or "internal" in rel or "BRIEF" in rel:
                fail.append(f"internal file shipped in site/: {rel}")
    site_drops = json.loads((site / "data/v1/drops.json").read_text())
    for x in site_drops["drops"]:
        leaked = [k for k in x if "price" in k.lower()]
        if leaked:
            fail.append(f"site drops {x['id']}: price field in shipped public data: {leaked}")
    print(f"site_files={sum(1 for p in site.rglob('*') if p.is_file())}")
else:
    print("site/ not built yet (run scripts/build.py)")

if fail:
    print("VERIFY FAILED (history):")
    [print(" -", f) for f in fail]
    sys.exit(1)
print("VERIFY OK")
