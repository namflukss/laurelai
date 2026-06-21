---
description: Draft a tailored cover letter + press-kit blurb for one festival, with a drafter-reviewer pass.
argument-hint: "<festival name>"
allowed-tools: Read, Write, WebSearch, Glob
---

Prepare submission materials for **$ARGUMENTS** (one festival). Load the **festival-strategist**
skill — document rules from `05-document-style.md`, voice from `03`, creative read from `02`.

1. **Gather context.** Read `materials/PROFILE.md` and the latest file in `plans/` (for this
   festival's tier, role, fit, and premiere requirement). Search the web for what *this* festival
   says it wants — categories, themes this edition is foregrounding, submission rules.
2. **Eligibility gate.** If the film doesn't actually qualify (premiere already burned, wrong
   category/length, region), say so plainly and **stop** — don't draft for a submission that can't happen.
3. **DRAFTER.** Write two artifacts, tailored to this festival (not generic), following the lengths
   and structure in `05-document-style.md`:
   - a **cover letter** — why this film belongs in *this* festival's program, connecting a concrete
     trait of the film to the festival's taste.
   - a **press-kit one-sheet** — logline, short + long synopsis, director's statement, bio, key
     cast/crew, technical specs, contact.
4. **REVIEWER.** Critique your own draft against: festival fit, eligibility, tone (any hype or
   filler?), and length. List the specific weaknesses.
5. **REVISE.** Produce the final versions addressing every point.
6. **Save — Markdown + compilable LaTeX.** Create `submissions/<festival-slug>/` and write:
   - `cover-letter.md` and `press-kit.md` (the readable versions; note any eligibility risk at the top)
   - `cover-letter.tex` — a copy of `cover_letters/cover.cls`'s `example.tex` with `\setsender{}`,
     `\letterhead{}{}`, and the body filled from the profile.
   - `press-kit.tex` — `presskit/main_example.tex` with the placeholders (`\filmtitle`,
     `\filmlogline`, synopses, statement, bio, specs, contact) filled in.
   Copy `cover_letters/cover.cls` into the folder (or reference it) so `cover-letter.tex` compiles.
   Tell the user they can render with `pdflatex` (see `cover_letters/OpenFonts/README.md` for fonts).
