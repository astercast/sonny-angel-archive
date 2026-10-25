# Sonny Angel USA Archive (Site 11)

Went live 2026-10-15. The `-live` copy
(astercast/sonny-angel-archive-live) carries the verified
snapshot of this repo at 1bc73b6, pushed at Rotation 47
close under the user's standing order. This working repo
stays the build track; the `-live` copy is updated only
on a new explicit user push order.

The complete Sonny Angel USA release chronology in one
chronological river, with lineups, secret figures, outbound
eBay searches per drop, a first class counterfeit guide, and
a restock watchlist of stores verified firsthand.

- Design study: `STUDY.md`
- Data: `data/v1/drops.json` (51 drops, provenance per
  record) is GENERATED: `python3 scripts/build.py` writes it
  from the internal source `data-src/drops.internal.json`
  (never shipped; listed in .vercelignore), stripping every
  price field for the public file, and pre-renders the river,
  the featured card and the count line into `index.html`.
  Edit the internal source, never the generated file.
  Also `data/v1/watchlist.json` (4 verified stores,
  plus a checked and not listed section) and
  `data/v1/history.json` (129 series lines, 2004 to today,
  the Full Timeline's data, with a source named per entry)
  Also `data/v1/stock.json` and `data/v1/candidates.json`
  plus `data/v1/pulse.json`, written by the heartbeat
  (`scripts/heartbeat/stock.py`, every 6 hours in CI): the
  official USA store's public product list, matched to the
  drops by name, keeping only title, link, type, date and
  in-stock, never a price; store series the archive does
  not list yet go to candidates.json for a human to check.
  A guard step fails the run if the text price appears in
  any public data file.
- Pages: `index.html` (the river, search, family filters),
  `timeline.html` (Full Timeline, the deep history; opens on
  the years before 2019, the part the river does not cover
  in full), `guide.html` (Real or Fake), `sheet.html`
  (My sticker sheet: all 51 series as stickers, collection
  saved on the visitor's device only, share link carried in
  the URL fragment), `watchlist.html`, `404.html`. Every
  page carries the pulse kit (assets/pulse.js and
  pulse.css); the build stamps `<meta name="built">` into
  the assembled site/ copies for its updated-ago bar.
- Publishing: `scripts/build.py` also assembles `site/`
  (only the pages, `assets/` and `data/v1/`; gitignored).
  `vercel.json` runs that build and serves `site/` as its
  output directory, so `data-src/`, `scripts/` and the repo
  notes never publish on a Git build.
- Checks: `python3 scripts/verify.py`
- Captures: `python3 scripts/capture.py` writes desktop and
  phone frames plus a jumble and tap census to the progress
  archive.

Serve locally with any static server, for example
`python3 -m http.server` in this directory.
