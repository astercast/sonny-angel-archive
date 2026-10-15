# Sonny Angel USA Archive (Site 11)

Working repo only. Never deployed. A `-live` copy is made
only on the user's explicit push order, and none exists.

The complete Sonny Angel USA release chronology in one
chronological river, with lineups, secret figures, outbound
eBay searches per drop, a first class counterfeit guide, and
a restock watchlist of stores verified firsthand.

- Design study: `STUDY.md`
- Data: `data/v1/drops.json` (39 drops, provenance per
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
