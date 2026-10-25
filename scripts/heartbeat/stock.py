"""Sonny Angel Archive watcher. Reads the official USA store's public product list (robots.txt allows /products.json).
Keeps ONLY: title, handle, product type, published date, in-stock yes/no. It never reads or stores a price, anywhere.
Writes data/v1/stock.json (matched to our drops by name) and data/v1/candidates.json (store series we do not list yet, for a human to check)."""
import re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from lib import get_json, read, write_if_changed, Pulse, now
STORE = "https://sonnyangelusa.com"
def guard():
    """GUARD STEP (bundle 2026-10-24): fail the whole run if the text
    price appears in ANY public data file under data/v1. The internal
    record in data-src is never scanned here and never ships; this
    guard is about public files only."""
    import glob
    data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "v1")
    bad = []
    for path in sorted(glob.glob(os.path.join(data_dir, "*.json"))):
        with open(path, encoding="utf-8") as f:
            if "price" in f.read().lower():
                bad.append(os.path.basename(path))
    if bad:
        print("GUARD FAILED: price text in public data files:", ", ".join(bad))
        sys.exit(1)
    print("guard ok: no price text in any public data file")
SERIES = {"minifigure_regular", "minifigure_limited"}
STOP = {"sonny", "angel", "series", "the", "x", "ver", "and", "of"}
tok = lambda s: set(re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()) - STOP
def match(title, drops):
    best, sc = None, 0
    for d in drops:
        a, b = tok(d["name"]), tok(title)
        s = len(a & b) / max(1, len(a | b))
        if s > sc: best, sc = d, s
    return (best, sc) if sc >= 0.6 else (None, sc)
def main():
    p = Pulse(stale_after_h=30)
    j, err = get_json(STORE + "/products.json?limit=250")
    drops = (read("drops.json", {"drops": []}))["drops"]
    if j is None or not j.get("products"):
        p.source("store", "Official USA store product list", False, error=err or "empty", url=STORE); p.write(); print("source failed", err); guard(); return
    stock, cands = {}, []
    for pr in j["products"]:
        if pr.get("product_type") not in SERIES: continue
        avail = any(v.get("available") for v in pr.get("variants", []))
        d, sc = match(pr["title"], drops)
        if d: stock[d["id"]] = {"in_stock": avail, "url": f'{STORE}/products/{pr["handle"]}'}
        else: cands.append({"title": pr["title"], "published": pr["published_at"][:10], "url": f'{STORE}/products/{pr["handle"]}'})
    prev = read("stock.json", {"items": {}})["items"]
    for k, v in stock.items():
        if k in prev and prev[k]["in_stock"] != v["in_stock"]:
            nm = next(d["name"] for d in drops if d["id"] == k)
            p.change("stock", f'{nm}: {"back in stock" if v["in_stock"] else "sold out"} at the official store', ref=k)
    old_c = {c["title"] for c in read("candidates.json", {"items": []})["items"]}
    for c in cands:
        if c["title"] not in old_c and old_c: p.change("candidate", f'Store lists a series we do not: {c["title"]} (check, then add)', ref=c["url"])
    p.source("store", "Official USA store product list", True, items=len(stock) + len(cands), url=STORE)
    write_if_changed("stock.json", {"format": "stock/1", "generated_at": now(), "checked_at": now(), "items": stock}, volatile=("generated_at", "checked_at"))
    write_if_changed("candidates.json", {"format": "candidates/1", "generated_at": now(), "items": cands})
    p.write(); print("matched", len(stock), "candidates", len(cands)); guard()
main()
