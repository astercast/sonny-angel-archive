/* shelf.js: "My sticker sheet". Your collection lives only in this browser (key sa.sheet.v1). Nothing is sent anywhere.
   Share: the link carries a small code in the part after #, which the server never sees. No prices anywhere. */
const KEY = "sa.sheet.v1", SEEN = "sa.seen.v1";
const load = () => { try { return JSON.parse(localStorage.getItem(KEY) || "[]"); } catch { return []; } };
const save = (a) => { try { localStorage.setItem(KEY, JSON.stringify(a)); } catch {} };
const hash = (s) => [...s].reduce((h, c) => (h * 31 + c.charCodeAt(0)) | 0, 7);
/* bit code: one bit per drop in the fixed order of drops.json (oldest first), as url-safe base64 */
export const encode = (ids, owned) => { const b = new Uint8Array(Math.ceil(ids.length / 8)); ids.forEach((id, i) => { if (owned.has(id)) b[i >> 3] |= 1 << (i & 7); }); return btoa(String.fromCharCode(...b)).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, ""); };
export const decode = (ids, s) => { try { const b = Uint8Array.from(atob(s.replace(/-/g, "+").replace(/_/g, "/")), (c) => c.charCodeAt(0)); return new Set(ids.filter((_, i) => b[i >> 3] & (1 << (i & 7)))); } catch { return new Set(); } };
export async function mountSheet(root, { drops = "data/v1/drops.json", stock = "data/v1/stock.json" } = {}) {
  const [dj, sj] = await Promise.all([fetch(drops).then((r) => r.json()), fetch(stock).then((r) => r.json()).catch(() => ({ items: {} }))]);
  const list = dj.drops.slice().sort((a, b) => a.sort - b.sort), ids = list.map((d) => d.id);
  const viewing = location.hash.startsWith("#s=");
  let owned = viewing ? decode(ids, location.hash.slice(3)) : new Set(load());
  const seen = (() => { try { return new Set(JSON.parse(localStorage.getItem(SEEN) || "null") || ids); } catch { return new Set(ids); } })();
  root.innerHTML = `<div class="sheet-head"><div class="sheet-count"></div><div class="sheet-bar"><i></i></div></div><div class="sheet-tools"></div><div class="sheet-grid"></div><p class="sheet-note"></p>`;
  const grid = root.querySelector(".sheet-grid"), tools = root.querySelector(".sheet-tools");
  const mk = (t, f) => { const b = document.createElement("button"); b.type = "button"; b.textContent = t; b.onclick = f; tools.append(b); return b; };
  const note = root.querySelector(".sheet-note"), when = sj.checked_at ? new Date(sj.checked_at) : null;
  note.textContent = (viewing ? "You are looking at someone's shared sheet. " : "Saved on this device only. ") + (when ? `"In store" means in stock at the official USA store when last checked.` : "");
  for (const d of list) {
    const b = document.createElement("button"); b.type = "button"; b.className = "stk"; b.dataset.id = d.id;
    b.style.setProperty("--r", ((hash(d.id) % 7) - 3) * .6 + "deg");
    const st = sj.items && sj.items[d.id];
    b.innerHTML = `<span class="stk-die"><img loading="lazy" alt=""></span><span class="stk-name"></span><span class="stk-year"></span>`;
    const im = b.querySelector("img"); if (d.image) im.src = d.image; else im.replaceWith(Object.assign(document.createElement("span"), { className: "stk-none", textContent: d.name.charAt(0) })); b.querySelector(".stk-name").textContent = d.name; b.querySelector(".stk-year").textContent = d.display_date;
    if (st && st.in_stock) { const s = document.createElement("span"); s.className = "stk-store"; s.textContent = "in store"; b.append(s); }
    if (!seen.has(d.id)) { const n = document.createElement("span"); n.className = "stk-new"; n.textContent = "NEW"; b.append(n); }
    b.onclick = () => { if (viewing) return; owned.has(d.id) ? owned.delete(d.id) : owned.add(d.id); save([...owned]); paint(); };
    grid.append(b);
  }
  function paint() {
    grid.querySelectorAll(".stk").forEach((b) => { b.setAttribute("aria-pressed", owned.has(b.dataset.id)); b.setAttribute("aria-label", `${b.querySelector(".stk-name").textContent}, ${owned.has(b.dataset.id) ? "you have it" : "not yet"}`); });
    root.querySelector(".sheet-count").innerHTML = `${owned.size} <small>of ${ids.length}</small>`;
    root.querySelector(".sheet-bar i").style.width = (owned.size / ids.length * 100) + "%";
  }
  if (!viewing) {
    const sh = mk("Copy a share link", async () => { const u = `${location.origin}${location.pathname}#s=${encode(ids, owned)}`; try { await navigator.clipboard.writeText(u); sh.textContent = "Copied"; } catch { prompt("Copy this link", u); } setTimeout(() => sh.textContent = "Copy a share link", 1800); });
    mk("Print my sheet", () => print());
    mk("Clear", () => { if (owned.size && confirm("Clear your whole sheet?")) { owned = new Set(); save([]); paint(); } });
    try { localStorage.setItem(SEEN, JSON.stringify(ids)); } catch {}
  } else { const a = document.createElement("a"); a.href = location.pathname; a.textContent = "Make my own sheet"; tools.append(a); }
  paint(); return { owned: () => [...owned], ids };
}
