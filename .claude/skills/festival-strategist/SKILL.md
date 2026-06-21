---
name: festival-strategist
description: Laurel's core film-festival distribution brain — festival knowledge, film-DNA discovery, fit scoring, premiere protection, tiered strategy, and the FESTIVAL_DATA output contract. Load whenever planning, scoring, or advising on a festival run.
---

# Festival Strategist — Laurel's brain

This skill is **Laurel's knowledge base**, split into numbered, versioned files. It is the
single source of truth for how Laurel thinks and talks — edited as Markdown, not buried in code.

## Who reads this

1. **The web app** (`app.py`) assembles its `system` prompt at request time by concatenating the
   numbered files below **in order**. Editing a numbered file changes Laurel's behavior on the next
   message — no code change, no restart. (See `load_system_prompt()` in `app.py`.)
2. **Claude Code / slash commands** (`/plan`, `/submit`, …) load this skill the normal way.

## Load order (the assembled prompt)

| File | Section |
|---|---|
| `00-identity.md` | Who Laurel is + festival knowledge base + operating principles |
| `01-film-profile.md` | Decoding the film's DNA + talk-first discovery (intake) |
| `02-creative-profile.md` | Reading directorial voice/tone → programmer appeal |
| `03-writing-style.md` | Laurel's voice + response modes (converse / info / advise / plan) |
| `04-festival-evaluation.md` | Tiering, premiere protection, budget, fit scoring + the `FESTIVAL_DATA` contract |
| `05-document-style.md` | Writing rules for cover letters, press kits/EPK, synopses, director's statement |
| `06-qa-prep.md` | Festival Q&A / panel preparation framework |
| `07-contract-review.md` | Post-accept contract review — flag risky clauses (+ `CONTRACT_FLAGS` block) |

Only `NN-*.md` files are concatenated into the prompt. `SKILL.md` is the manifest and is **not**
part of the prompt. Do **not** add YAML frontmatter to the numbered files — it would leak into the
prompt.

## Rendering templates (artifacts, not prompt)

The compilable LaTeX deliverables referenced by `05` and the `/submit` command live at the repo root,
**not** in this skill (they're artifacts, not knowledge):
- `cover_letters/cover.cls` + `cover_letters/example.tex` — festival cover letter (pdflatex)
- `presskit/main_example.tex` — EPK / one-sheet (pdflatex)
- `cover_letters/OpenFonts/README.md` — optional Lato/Raleway fonts

## Editing rules

- Keep each file focused on its one concern; cross-reference rather than duplicate.
- The `FESTIVAL_DATA` JSON shape in `04` is a **contract with the frontend parser** (`parseData()`
  in `static/index.html`). Changing field names there means changing the parser too.
- Preserve the **talk-first** behavior in `01`/`03`: Laurel converses and gathers before planning.
