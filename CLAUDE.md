# Laurel — Figma ↔ Code Integration Rules

Rules for translating Figma designs into this codebase (and back) via the Figma MCP. Read this before importing any design or editing the UI.

> **One-line truth:** Laurel is a **single-file, vanilla HTML/CSS/JS app**. There is no framework, no build step, no component files, no npm UI deps. Everything lives in `static/index.html`. Do not introduce React/Tailwind/bundlers when implementing a Figma design — match the existing patterns below.

---

## Project Structure

```
laurel/
├── app.py              # FastAPI backend — Claude Opus 4.8 + web search, SSE streaming
├── requirements.txt    # anthropic, fastapi, uvicorn, duckduckgo-search, python-multipart
├── static/
│   └── index.html      # ENTIRE frontend: inline <style> + inline <script> (≈1600 lines)
├── .claude/skills/
│   └── festival-strategist/  # Laurel's BRAIN — system prompt, split into NN-*.md skill files
├── STRUCTURE.md        # target "agent project" layout + build phases
└── CLAUDE.md           # this file
```

- **No `src/`, no components dir, no package.json.** The frontend is one document.
- **Laurel's system prompt is NOT a string in `app.py`.** It lives in `.claude/skills/festival-strategist/` as numbered Markdown (`00-identity.md … 04-festival-evaluation.md`); `load_system_prompt()` concatenates them in order **on every request** (edit a skill file → effective next message, no restart). `SKILL.md` is the manifest and is excluded. The `<FESTIVAL_DATA>` contract lives in `04-festival-evaluation.md` and must stay in sync with `parseData()` in the frontend.
- Backend serves `static/index.html` at `/` and streams chat at `POST /api/chat` (SSE).
- Run: `ANTHROPIC_API_KEY=… python3 -m uvicorn app:app --port 8001` → http://localhost:8001
- **Web search** (`do_web_search` in `app.py`): official **Brave Search API** when `BRAVE_API_KEY` is set, else the unofficial `duckduckgo-search` library as a dev fallback. Both read **public search results only** — Laurel never scrapes gated/ToS-restricted sites. FilmFreeway is an *outbound submission link* (`window.open`), never fetched. Set `BRAVE_API_KEY=…` alongside `ANTHROPIC_API_KEY` for the sanctioned path.
- After any edit to `static/index.html`, syntax-check the script:
  ```bash
  python3 -c "import re;h=open('static/index.html').read();m=re.search(r'<script>(.*?)</script>',h,re.S);open('/tmp/l.js','w').write(m.group(1))"
  node --check /tmp/l.js
  ```

---

## 1. Token Definitions

**Where:** a single `:root` block at the top of the `<style>` in `static/index.html`. These CSS custom properties are the source of truth. **Never hardcode a hex/size that a token already covers.**

```css
:root {
  /* Ink scale (text + hairlines) — light theme (default) */
  --ink:    #1C2029;            /* primary text */
  --ink80:  rgba(28,32,41,.82);
  --ink60:  #3A4150;            /* slate — secondary text */
  --ink40:  #5C616B;            /* dim — WCAG-safe small text */
  --ink20:  #8A909B;            /* faint — DECORATIVE ONLY, never body text */
  --ink10:  rgba(28,32,41,.10);
  --ink05:  rgba(28,32,41,.045);
  --bdr:    #E7E4DE;            /* border / line */
  --bdr-lt: rgba(31,30,29,.10); /* hairline / line-soft */
  /* Surfaces */
  --bg:     #F5F7FA;            /* canvas (page) — cool light */
  --bg2:    #FFFFFF;            /* sidebar / raised panels */
  --card:   #FFFFFF;            /* cards, white panel */
  --card-hover: #FBFAF8;        /* card hover surface (themed — flips in dark) */
  /* Accent */
  --orange: #F4530E;            /* Laranja — the only accent; use sparingly */
  --orange-dk: #D8420A;
  --indigo: #2563EB;            /* cool accent — premiere-conflict state only */
  --grad:   linear-gradient(120deg,#CE1F0B 0%,#F4530E 52%,#C2740C 100%);
  --shadow: 0 1px 2px rgba(28,32,41,.04), 0 10px 30px -14px rgba(28,32,41,.12);
  /* Radius */
  --r-md:   12px;              /* cards, inputs, primary buttons */
  --r-sm:   8px;               /* small buttons, chips, checkboxes */
  /* (pills use border-radius: 999px directly) */
  /* Type */
  --display:'Lato','Plus Jakarta Sans',system-ui,sans-serif;  /* headings */
  --sans:   'Plus Jakarta Sans','Lato',system-ui,sans-serif;  /* body / UI */
  --mono:   'Space Mono',monospace;                           /* micro-labels, data */
  /* Motion */
  --ease:   cubic-bezier(0.16,1,0.3,1);
}
```

### Dark theme

A second token set lives under `[data-theme="dark"]` on `<html>` (right after `:root`). It **only redefines color/surface tokens** — every component reads `var(--token)`, so the theme flips automatically. Same accent (`--orange`, `--grad`, `--indigo`) in both themes.

```css
[data-theme="dark"] {
  --ink: #E7EAF0; --ink80: rgba(231,234,240,.82); --ink60: #B4BBC6;
  --ink40: #949BA7; --ink20: #6A7280;
  --ink10: rgba(231,234,240,.10); --ink05: rgba(231,234,240,.05);
  --bdr: #2B313B; --bdr-lt: rgba(231,234,240,.12);
  --bg: #0E1116; --bg2: #161B22; --card: #161B22; --card-hover: #1D232D;
  --shadow: 0 1px 2px rgba(0,0,0,.45), 0 12px 32px -14px rgba(0,0,0,.7);
}
```

**Mechanics:**
- **Toggle:** sun/moon icon button (`.icon-btn#themeBtn`) in the chat `.panel-head`. `toggleTheme()` sets/removes `data-theme="dark"` on `document.documentElement` and saves to `localStorage` key **`laurel_theme`**.
- **No flash:** a tiny inline `<script>` in `<head>` (before the stylesheet) reads `laurel_theme` — or falls back to `prefers-color-scheme` — and sets the attribute before first paint.
- **Smooth switch:** key surfaces carry a `transition` on `background-color/border-color/color`.

**Rules when adding UI (so dark mode keeps working):**
- **Never hardcode `#fff` / `#9ca3af` / `rgba(31,30,29,…)` as a surface or text color** — route through `--card`, `--bg2`, `--ink*`, `--bdr-lt`. Hardcoded `#fff` is only allowed as text/icon color *on top of* the orange/gradient accents (it stays white in both themes).
- **Inversion trap:** anything using `--ink` as a *background* with light text (user message bubble, active send button, the "L" brand marks, timeline tooltip) needs a `[data-theme="dark"]` override so it doesn't become light-on-light. These overrides already exist — mirror the pattern for any new inverted element.

**Format:** plain CSS custom properties. **No transformation system** (no Style Dictionary, no Tailwind config, no JSON tokens). Usage: `color: var(--ink40)`, `border: 0.5px solid var(--bdr)`, `transition: … var(--ease)`.

**Figma mapping:** these tokens are mirrored 1:1 as a Figma variable collection **`Laurel/Color`** in file `BgTYePNMmPv9FFaxVlpdpL`. When importing a design, map Figma variables → these CSS vars by name (canvas→`--bg`, panel→`--card`, ink→`--ink`, slate→`--ink60`, dim→`--ink40`, faint→`--ink20`, line→`--bdr`, line-soft→`--bdr-lt`, accent→`--orange`).

### Token rules
- **Accessibility first:** body/label text uses `--ink`, `--ink60`, or `--ink40` (all ≥4.5:1 on `--bg`/`--card`). `--ink20` is **decorative only** (idx numbers, placeholders, faint hints) — never real text.
- **One accent.** `--orange` is the sole brand accent; keep it sparse (CTAs, active states, the laurel berry). `--grad` is confined to: timeline submission bars, the laurel seal accent. Do **not** add gradient text on headings.
- **Borders are `0.5px`** hairlines using `--bdr` / `--bdr-lt`. Elevation uses `var(--shadow)`, not glows.

---

## 2. Typography

Three families, loaded once via Google Fonts `<link>` in `<head>`:

```html
<link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Mono&display=swap" rel="stylesheet">
```

| Role | Token | Family | Typical use |
|---|---|---|---|
| Display | `--display` | **Lato** 900 | Hero & plan/festival titles, festival names, fit-gauge number, seal |
| Body / UI | `--sans` | **Plus Jakarta Sans** 400–800 | All prose, buttons, inputs |
| Mono | `--mono` | **Space Mono** | Eyebrows, micro-labels, data (deadline/fee), counts |

Patterns: big headings `font-family: var(--display); font-weight: 900; letter-spacing: -.02em` (Lato carries weight 900 — use it for the hero/plan titles). Body uses Plus Jakarta 400–600. Mono labels are tiny + tracked: `font-size: 9px; letter-spacing: .14em; text-transform: uppercase; color: var(--ink40)`.

> **Note:** Lato ships weights 300/400/700/900 only (no 500/600) — display elements that ask for 600 fall back to the nearest. Don't rely on a 500/600 Lato weight.

> **Figma note:** the MCP write tool can't load custom fonts; Lato / Plus Jakarta Sans / Space Mono are all Google fonts available in Figma, so they map directly.

---

## 3. Component Library

**There are no component files.** "Components" are DOM built imperatively in the `<script>` via template-literal `innerHTML`, or written as static markup in the body. Architecture = **plain functions that return/append DOM**, styled by shared CSS classes.

Canonical builder pattern (copy this when adding UI):

```js
function buildPlan(data){
  const wrap = document.createElement('div')
  wrap.className = 'plan'                       // styling via class, never inline
  wrap.innerHTML = `… template literal …`        // use esc() on ALL interpolated text
  wrap.querySelector('.plan-tab').onclick = …    // wire handlers after innerHTML
  return wrap
}
```

Key UI classes already defined (reuse, don't reinvent): `.hero-cta`, `.chip`, `.wi` (what-if chip), `.pa-btn` (ghost), `.pa-mi` (menu item), `.send`, `.fcard` (festival card), `.fcard-name/-why/-data/-actions`, `.fit-bar/.fit-fill`, `.status-pill`, `.fcard-check`, `.plan` / `.plan-tab`, `.seal` (laurel), `.budget-bar`, `.ck` (checklist), `.doc` (generated documents), `.skel` (skeleton loader).

**Component documentation = the Figma library** (`BgTYePNMmPv9FFaxVlpdpL`, page `02 · Components`): `Button/Primary`, `Button/Ghost`, `Button/Send`, `Chip/Example`, `Chip/WhatIf`, `Pill/Status`, `Festival Card`, `Seal/Official-Selection`. No Storybook.

### Rules when importing a Figma component
- Realize it as a **CSS class + a builder function**, not a new file/framework.
- Pull values from existing tokens; if Figma uses a raw value not in `:root`, add a token first, then reference it.
- Match the three view layers (see §7). New rich output belongs on the **plan page** or **festival page**, not the chat bubble.

---

## 4. Frameworks & Libraries

- **UI framework:** none (vanilla DOM). Do not add one.
- **Backend:** FastAPI (`app.py`), Anthropic SDK (`claude-opus-4-8`, adaptive thinking, SSE streaming), DuckDuckGo search tool.
- **Frontend deps (CDN `<script>` only):**
  - `gsap` 3.12.5 (cdnjs) — all animation. Guarded with `if (typeof gsap !== 'undefined')`.
  - `marked` (jsDelivr) — markdown → HTML for streamed responses. Guarded by a shim so a CDN miss can't break the app.
- **Build system / bundler:** **none.** Edit `static/index.html` directly; FastAPI reads it fresh each request (no restart needed for static edits).

---

## 5. Styling Approach

- **Methodology:** a single global `<style>` block with **flat, hand-named classes** (loosely BEM-ish: `.fcard`, `.fcard-name`, `.fcard-why`). No CSS Modules, no styled-components, no utility classes.
- **Global styles:** reset (`*{box-sizing;margin;padding:0}`), `html,body` base, and the `:root` tokens.
- **Layout:** flexbox + CSS grid. Festival grid is `repeat(auto-fill, minmax(200px,1fr))`.
- **Responsive:** mobile-first-ish with `@media (max-width: 820px)` / `(max-width: 640px)` — sidebar hides, paddings shrink, grids collapse to 1 col. Also a `@media print` block restyles the plan page to a clean white PDF.
- **Motion:** GSAP for entrances/reveals; CSS `transition: … var(--ease)` for hovers. Animate only `transform`/`opacity`. Tactile press = `scale(.97)` on `:active`.
- **No grain/noise, no glows, no glass.** (Removed deliberately — keep it clean.)

```css
/* Representative component style — match this density/idiom */
.fcard {
  background: var(--card); border: 0.5px solid var(--bdr); border-radius: var(--r-sm);
  padding: 18px; box-shadow: var(--shadow);
  transition: border-color .3s var(--ease), transform .3s var(--ease);
}
.fcard:hover { border-color: var(--orange); transform: translateY(-2px); }
```

---

## 6. Asset Management & Icons

- **Images:** none. The design uses **no raster/CDN assets** — surfaces are solid tokens. (Figma MCP write tool also can't import images; don't introduce image-dependent designs without flagging it.)
- **Icons:** **inline SVG** written directly in markup/template literals. No icon library, no sprite, no `<img>`.
  - Convention: `viewBox="0 0 20 20"`, `fill="none" stroke="currentColor" stroke-width="1.5"`, `stroke-linecap="round"`. `currentColor` so icons inherit text color. Sizes set in CSS (`svg { width: 13px; height: 13px }`).
  - **No emoji as icons.**
  ```html
  <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5">
    <path d="M5 10h10M11 6l4 4-4 4" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
  ```

---

## 7. App Architecture (view layers)

The frontend is three stacked, full-height "pages" inside one document; navigation is class-toggling + GSAP slides, not routing:

1. **Chat** (`.app` → `.side` sidebar + `.main` thread + composer) — the persistent conversation. Guided intake lives here.
2. **Plan page** (`#planPage`, slides over main) — the festival strategy: laurel seal header, Cards/Timeline tabs, festival grid, what-if chips, budget bar, actions (Export / PDF / More ▾).
3. **Festival page** (`#festPage`, slides over plan) — one festival: stats, submission checklist, live AI briefing (skeleton-loaded), FilmFreeway link.

State: module-scoped vars (`history`, `convs`, `currentPlan`, `budgetSet`, `intake`). Persistence via `localStorage` (`laurel_convs`, `laurel_st::*`, `laurel_ck::*`). Backend contract: assistant responses may append a `<FESTIVAL_DATA>{…json…}</FESTIVAL_DATA>` block (parsed client-side, stripped from visible text) — preserve this when touching the parser or the contract in `.claude/skills/festival-strategist/04-festival-evaluation.md` (the prompt source, not `app.py`).

---

## Do / Don't (quick reference)

**Do:** edit `static/index.html`; use `var(--token)`; reuse existing classes; build UI with builder functions + `esc()`; inline SVG with `currentColor`; guard `gsap`/`marked`; keep one accent; `node --check` after JS edits.

**Don't:** add React/Vue/Tailwind/a bundler/npm UI deps; hardcode colors or radii; introduce icon libraries or images; use `--ink20` for readable text; add gradient text, grain, glows, or glassmorphism; put rich plan output inside chat bubbles.
