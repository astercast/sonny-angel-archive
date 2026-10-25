# LIVE CHECKLIST, Sonny Angel USA Archive

Standing state: LIVE SNAPSHOT EXECUTED 2026-10-15 at
Rotation 47 close, under the user's standing order. The
`-live` repo astercast/sonny-angel-archive-live carries the
verified snapshot of this working repo at 1bc73b6 (remote
main f6e223c97a2f003849e05d4e6f4417ea513be0a0, remote tree
verified equal to the snapshot tree, 53 of 53 files
SHA-equal; record: fleet-ops ROTATION-47-REPORT.md). This
working repo remains the build track. The `-live` repo is
updated ONLY on a new explicit user push order; the R47
authorization does not renew. No Vercel project exists yet:
connecting the `-live` repo in Vercel (Standard build
machine, never Turbo) is the user's hand-step.

## Free tier audit (at build, 2026-10-14)

- Hosting need: none yet. The site is fully static: 6 HTML
  pages (sheet.html, My sticker sheet, added 2026-10-24),
  CSS and JS under assets/, 6 JSON data files (the heartbeat
  outputs stock.json, candidates.json and pulse.json ship
  with the rest of data/v1; the heartbeat workflow file
  lands in the working repo, and carrying workflow files to
  the live repo rides the owner's web-UI move, the standing
  gh-push workflow-scope wall).
- Server functions: none. No runtime is pinned anywhere.
  The working repo's vercel.json (round 2, 2026-10-24) runs
  scripts/build.py and serves the assembled site/ folder
  only, so repo internals never publish on a Git build.
- Data: all data is precomputed JSON under `data/v1/`,
  never under `api/`.
- Images: self hosted in this repo under assets/img/
  (user's order, 2026-10-15: all pictures must load).
  Every file is a copy of an official store or official
  Dreams news photo, provenance recorded per record in
  data/v1/drops.json. 38 of 39 drops are pictured; the one
  absence (HIPPERS Garden) is named in its record with the
  evidence. Self hosting is static files only, no cost.
- Search and filters: client side, over the local JSON.
- Third party calls at runtime: none, apart from the image
  embeds and outbound links a reader chooses to follow.

## For any future live update (a new user order is required)

1. Verify the remote URL matches the intended `-live`
   track before any push.
2. Static data stays in `data/v1/`. Only real function
   files would ever go under `api/`, and this site has none.
3. Vercel build machine: Standard, never Turbo.
4. No `runtime` key is to be added for Node functions;
   there are no functions.
