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
- Pages: `index.html` (the river, search, family filters),
  `timeline.html` (Full Timeline, the deep history; opens on
  the years before 2019, the part the river does not cover
  in full), `guide.html` (Real or Fake), `watchlist.html`,
  `404.html`
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
