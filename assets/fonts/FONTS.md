# Self-hosted fonts, provenance

All files in this directory are SIL Open Font License (OFL) webfonts,
served locally so the site makes zero remote font requests.

## Zen Maru Gothic (rotation 140, design consult "The Card Catalog", SO1)

| file | family | style | weight | role here |
|---|---|---|---|---|
| zen-maru-gothic-latin-400.woff2 | Zen Maru Gothic | normal | 400 | the stationery voice: body text |
| zen-maru-gothic-latin-500.woff2 | Zen Maru Gothic | normal | 500 | labels, links, the wordmark's second half |
| zen-maru-gothic-latin-700.woff2 | Zen Maru Gothic | normal | 700 | headings, card names, dates, tabs |

- Source files: the latin subset woff2 files served by the Google
  Fonts css2 request the design draft pointed at
  (family=Zen+Maru+Gothic:wght@400;500;700), fetched once at build
  time (rotation 140) and self-hosted here. The site's text is
  English, so the latin subsets carry it; Japanese glyphs, if any
  ever appear, fall back to the stack's Hiragino Maru Gothic and
  Arial Rounded faces named in assets/catalog.css.
- Files on the font CDN (zenmarugothic v20): 400
  o-0SIpIxzW5b-RxT-6A8jWAtCp-U6khn.woff2, 500
  o-0XIpIxzW5b-RxT-6A8jWAtCp-cGWtyO5Cb.woff2, 700
  o-0XIpIxzW5b-RxT-6A8jWAtCp-cUW1yO5Cb.woff2.
- SHA-256: 400 d652b5eddc2b877784592d1bb40e1713f97623ec7638801021519c1ea88b0b43;
  500 2c5953da616e5e6dcad34ae8b744f7e759f1647c041389681fa2360908508d55;
  700 9d65f92a3e11edcef9d73694b5b73cb6888243aee54e8034b162eb368c6ff3ed.
- License: SIL Open Font License 1.1.
- Unicode range (latin subset): U+0000-00FF plus the punctuation
  ranges in the css2 latin block, declared on the @font-face rules
  in assets/catalog.css.
