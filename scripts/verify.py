#!/usr/bin/env python3
"""Standing checks for the Sonny Angel USA Archive tree.

Run: python3 scripts/verify.py
Fails loudly on: em dashes in presented copy, drops without
provenance, pictured drops without an image source, count
drift between the data file and its meta block, duplicate
ids, unsorted sort keys, and prices or resale figures in the
fields rendered on a series card.
"""
import json, re, sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
fail = []

pages = ["index.html", "guide.html", "watchlist.html", "404.html", "timeline.html",
         "assets/style.css", "assets/app.js", "assets/watchlist.js", "assets/timeline.js"]
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

if fail:
    print("VERIFY FAILED (history):")
    [print(" -", f) for f in fail]
    sys.exit(1)
print("VERIFY OK")
