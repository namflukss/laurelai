# Laurel — Design System ("Orbit")

The single source of truth for Laurel's UI. Everything lives in **`static/index.html`** (vanilla HTML/CSS/JS, one global `<style>`, CSS custom properties). No framework, no build step, no component files. This document describes the tokens, type, and component patterns that are actually in the code today.

> The accent is **blue**. The token is `--accent` (`#3D6BFF`). Always reference `var(--accent)` / `var(--accent-*)` — never hardcode a hex.

---

## 1. Principles

- **One accent, used sparingly.** Blue `#3D6BFF` is the only brand color. Everything else is a neutral ink/surface. Green/red appear *only* as status semantics (accepted / high-risk), never as decoration.
- **Group with hairlines and negative space, not boxes.** `0.5–1px` dividers (`--bdr`, `--bdr-lt`) and ledger layouts over nested cards. Use a card only when elevation communicates hierarchy.
- **Type is the art.** No raster assets. Festival "posters" are monogram crests built from type on a dark gradient.
- **Mono micro-labels.** Eyebrows, counts, and data labels are tracked, uppercase, tiny.
- **Motion is physical and restrained.** One easing curve, `transform`/`opacity` only, tactile press on interactive elements.
- **Dark-theme safe by construction.** Every surface/text color is a token; the theme flips by overriding tokens under `[data-theme="dark"]`.

---

## 2. Color tokens

Defined in the single `:root` block at the top of the `<style>`. **Never hardcode a value a token already covers.**

### Ink (text + lines) — light
| Token | Value | Use |
|---|---|---|
| `--ink` | `#0E1320` | Primary text, headings |
| `--ink80` | `rgba(14,19,32,.82)` | Strong body on light |
| `--ink60` | `#3F4654` | Secondary text |
| `--ink40` | `#8A92A3` | Muted labels (WCAG-safe small text) |
| `--ink20` | `#B6BCC8` | **Decorative only** — never real text |
| `--ink10` | `rgba(14,19,32,.08)` | Ring tracks, faint fills |
| `--ink05` | `rgba(14,19,32,.04)` | Subtle tints, icon wells |

### Surfaces & lines — light
| Token | Value | Use |
|---|---|---|
| `--bg` | `#E9EAEE` | Page canvas (cool gray) |
| `--bg2` | `#F4F5F7` | Subtle raised fill, inputs |
| `--card` | `#FFFFFF` | Cards, panels |
| `--card-hover` | `#F4F5F7` | Card hover surface |
| `--bdr` | `#E7E9ED` | Standard border / hairline |
| `--bdr-lt` | `rgba(15,23,42,.08)` | Soft hairline / divider |

### Accent (blue) — same in both themes
| Token | Value | Use |
|---|---|---|
| `--accent` | `#3D6BFF` | The one accent — CTAs, active states, indices, fit |
| `--accent-deep` | `#2547C9` | Deep accent ("best"/strong fit, pressed) |
| `--accent-hi` | `#7FA6FF` | Light accent (gradient top, crest letters) |
| `--accent-tint` | `#E8EEFF` | Accent wash (badges, pills, icon wells) |
| `--indigo` | `#5E8AFF` | Cool secondary |
| `--ring` | `#3D6BFF` | = accent |
| `--grad` | `linear-gradient(180deg, var(--accent-hi), var(--accent))` | Primary buttons, accents |

### Semantic (status only — not decoration)
| Meaning | Color |
|---|---|
| Accepted / success | `#5fd08a` (pill) · `#1A9E63` (solid) |
| High risk (contract) | `#D6453F` |
| Waitlist / caution | warm tint, used sparingly |

### Dark theme
A second token set under `[data-theme="dark"]` redefines **only color/surface tokens**; every component reads `var(--token)`, so it flips automatically. Same accent. Highlights: `--bg #08090C`, `--bg2 #101218`, `--card #14161C`, `--ink #F3F5F9`, `--accent-deep #9DB9FF`.

**Toggle:** `toggleTheme()` sets/removes `data-theme="dark"` on `<html>`, persisted to `localStorage["laurel_theme"]`; a tiny inline head script applies it before first paint (no flash).

---

## 3. Typography

**One typeface: Urbanist** (variable, weights 100–900), loaded once via Google Fonts. Every role token maps to it:

```
--display / --sans / --serif / --mono  →  'Urbanist'
```

| Role | Pattern |
|---|---|
| Display / headings | `font-weight: 800–900; letter-spacing: -.01em to -.02em; line-height: 1.0–1.1` |
| Body / UI | `400–600`, `line-height: 1.5–1.6`, body max-width `~54–65ch` |
| Mono micro-label | `font-size: 8–11px; letter-spacing: .08–.2em; text-transform: uppercase; color: var(--ink40)` |
| Data numerals | add `font-variant-numeric: tabular-nums` to avoid jitter (rings, counts) |

> Because there's no separate mono font, "mono" labels are just tracked uppercase Urbanist. Keep them tiny and tracked — that tracking *is* the device.

---

## 4. Spacing, radius, elevation, motion

- **Radius:** tokens `--r-sm: 8px`, `--r-md: 12px`. De-facto scale in use: tiles `6–9px`, buttons `9–10px`, cards `14–18px`, pills `999px`.
- **Elevation:** `--shadow` (`0 1px 3px …, 0 14px 44px -20px …`) — soft, wide, tinted to the page. No glows. Hover lift = `translateY(-1px|-2px)` + a deeper tinted shadow.
- **Motion:** one curve `--ease: cubic-bezier(0.16,1,0.3,1)`. Transitions on `border-color`, `background`, `box-shadow`, `transform`, `opacity` only. **Tactile press:** `:active { transform: scale(.99) / translateY }` with a fast `.12s` transition. GSAP (guarded `if (typeof gsap !== 'undefined')`) handles entrance reveals and ring/number animations.

---

## 5. Fit-strength ramp (blue intensity)

Fit scores are visualized on **one blue ramp** (never green/red), so strong→weak reads as a single hue family:

| Strength | Threshold | Ring/arc color |
|---|---|---|
| Strong | `≥ 80` | `var(--accent-deep)` `#2547C9` |
| Moderate | `30–79` | `var(--accent)` `#3D6BFF` |
| Long shot | `< 30` | `var(--ink40)` (grey) |

By-fit gauges use matching gradients: `fitStrong #2547C9→#5B86FF`, `fitMod #3D6BFF→#88AAFF`, `fitWeak grey`. Mini-rings (`miniRing`) use the solid colors above.

---

## 6. Components & patterns

All "components" are CSS classes + plain builder functions that return/append DOM via template literals. **Always `esc()` interpolated text. Wire handlers after `innerHTML`.**

### "The Programme" section header — `.sec-head`
The signature device that threads every view (List tiers, By-fit, Timeline, Explorer, Contract). A numbered/marked editorial overline:
```
[mono index 01 / glyph]  ·  [display label]  ·  ───hairline rule───  ·  [mono meta]
   var(--accent)             var(--ink)          var(--bdr)              var(--ink40)
```
Classes: `.sec-head`, `.sec-idx` (accent mono index), `.sec-mark` (accent glyph), `.sec-label` (display 14/700), `.sec-rule` (flex:1 hairline), `.sec-meta` (mono uppercase, `b` = bold ink).

### Festival card — `.fcard` (the rich strategy card; what the List tab renders)
Layout: **crest poster · content · fit ring**, then **stat ledger** → **stepper** → **footer**.
- `.fc-poster` — dark gradient tile, `.fc-poster-mono` monogram (accent letters, from `tkTag(name)`), `.fc-poster-meta` micro-label. No duplicated name/location.
- `.fc-gauge` / `.fc-ring` — the fit ring (see §5), big number + small `%`, `.fc-gauge-cap` strength label below.
- `.fc-stats` — **hairline ledger**: 3 columns split by `.fc-stat + .fc-stat { border-left }`, lighter inline icons (no filled boxes).
- `.fc-foot` — `[status pill] ··· [View details][Submit]`. Primary button = `var(--grad)`.

### Monograms & tiles
`tkTag(name)` → up to 4 uppercase letters from the first word. Rendered on a dark gradient (`#1B2433→#0B1220`) with accent letters. Used in cards, the timeline, the explorer, and the calendar — one crest language everywhere.

### Rings & gauges
- `miniRing(pct)` — 46px, solid ramp color, number + tiny `%`.
- `fc-ring` (card) — 84px, gradient arc, count-up.
- `.fgc` (By-fit) — 100-wide semicircle gauge with a traveling tip knob, count-up, rank chip (`★ #1`), and `.fgc-badge` (Best/Strong/Moderate).

### Explorer
- `.exp-card` — crest · name/loc · mini-ring · why · `.exp-ledger` (Deadline/Fee/Category hairline ledger) · `.exp-prem` badge + add button.
- `.exp-cal` / `.cal-month` / `.cal-row` — month-grouped deadline calendar; past months dimmed, current flagged `.cal-soon`, undated grouped as "Rolling / invite".
- `.exp-toggle` reuses `.oh-toggle` (Grid / Calendar).

### Contract
- `.ct-guide` — "What Laurel checks" checklist (icon well + title + desc, hairline-separated), `.ct-legend` risk chips (`.ct-lg.high/.med/.low`).
- `.ct-flag` / `.ct-sev` — result cards, severity chip.

### Pills, badges, buttons
- **View toggle** `.oh-toggle` / `.oh-tg` — segmented, active = ink fill + soft shadow, press-scale.
- **Status pill** `.status-pill[data-s="…"]` — Planned (ink) · Submitted (accent) · Accepted (green) · Waitlist (warm) · Rejected (grey).
- **Filter pill** `.fb-pill` — hairline, active = accent border + tint.
- **Primary button** — `background: var(--grad); color:#fff`. **Ghost** — transparent + hairline, accent border on hover. All buttons `:active { transform: scale(.97) }`.

---

## 7. Navigation

Two-part left nav (current layout):

- **`.rail`** — the slim icon rail. `toggleRail()` adds `.expanded` to reveal `.rail-label`s. Holds, top→bottom: **Chat · Strategy plan · Explore festivals · Deadlines · Submissions tracker**, then a separator and the always-visible toolkit **Contract check · Press kit · Social posts · Announce crew** (`#wsSel`), then Toggle theme + the filmmaker avatar.
- **`.side2`** — the wide conversation panel: brand, **New Chat**, the **SAVED** list (fills from `localStorage` as plans/chats are created), and the account footer.

---

## 8. Conventions (do / don't)

**Do:** edit `static/index.html`; use `var(--token)`; reuse existing classes; build UI with builder functions + `esc()`; inline SVG with `currentColor` (`viewBox 0 0 20 20`, `stroke-width 1.5`, `stroke-linecap round`); guard `gsap`/`marked`; keep one accent; use hairline ledgers over boxes; `node --check` the inline script after JS edits:
```bash
python3 -c "import re;h=open('static/index.html').read();b=re.findall(r'<script>(.*?)</script>',h,re.S)[1];open('/tmp/l.js','w').write(b)"
node --check /tmp/l.js
```

**Don't:** add React/Tailwind/a bundler/npm UI deps; hardcode hex/rgba a token covers; use `--ink20` for readable text; add a second accent; add gradient text, grain, glows, or glassmorphism; duplicate data within a component (e.g. name in both poster and title).

---

## 9. Architecture pointers

- **Frontend:** one document, stacked full-height "pages" toggled by class + GSAP slides (Chat → Plan → Festival; plus feat-pages: Explore, Tracker, Press kit, Social, Announce, Contract). State in module-scoped vars; persisted via `localStorage` (`laurel_convs`, `laurel_st::*`, `laurel_theme`, `laurel_pk`, …).
- **Backend:** `app.py` (FastAPI), Claude Opus 4.8, SSE streaming at `POST /api/chat`. The system prompt is **not** a string in `app.py` — it's the Markdown under `.claude/skills/festival-strategist/`, concatenated per request.
- **Data contract:** assistant responses may append `<FESTIVAL_DATA>{…}</FESTIVAL_DATA>`, parsed client-side and stripped from visible text. Keep `parseData()` in sync with `04-festival-evaluation.md`.

---

*This file documents the live "Orbit" build. If you change a token or pattern in `static/index.html`, update this file in the same change.*
