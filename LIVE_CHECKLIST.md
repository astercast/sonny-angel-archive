# LIVE CHECKLIST, Sonny Angel USA Archive

Standing state: WORKING TRACK ONLY. Not deployed, no Vercel
project, no `-live` repo. This file exists so a future live
order starts from a clean audit instead of a scramble.

## Free tier audit (at build, 2026-10-14)

- Hosting need: none yet. The site is fully static: 4 HTML
  pages, 1 CSS file, 2 JS files, 2 JSON data files.
- Server functions: none. No runtime is pinned anywhere;
  there is no vercel.json in the working repo.
- Data: all data is precomputed JSON under `data/v1/`,
  never under `api/`.
- Images: embedded hotlinks to the official stores' CDN
  (the fleet embed model), so image hosting cost is zero
  and provenance stays with the source. 21 of 39 drops are
  pictured (r37 growth); the rest carry designed absence plates.
- Search and filters: client side, over the local JSON.
- Third party calls at runtime: none, apart from the image
  embeds and outbound links a reader chooses to follow.

## If a live order ever lands

1. Verify the remote URL matches the intended `-live`
   track before any push.
2. Static data stays in `data/v1/`. Only real function
   files would ever go under `api/`, and this site has none.
3. Vercel build machine: Standard, never Turbo.
4. No `runtime` key is to be added for Node functions;
   there are no functions.
