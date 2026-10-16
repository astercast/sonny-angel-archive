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
  record), `data/v1/watchlist.json` (4 verified stores,
  plus a checked and not listed section)
- Pages: `index.html` (the river, search, family filters),
  `guide.html` (Real or Fake), `watchlist.html`, `404.html`
- Checks: `python3 scripts/verify.py`
- Captures: `python3 scripts/capture.py` writes desktop and
  phone frames plus a jumble and tap census to the progress
  archive.

Serve locally with any static server, for example
`python3 -m http.server` in this directory.
