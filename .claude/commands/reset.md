---
description: Wipe the current film's profile, plans, and/or source materials so you can start fresh.
argument-hint: "[profile | plans | materials | all]"
allowed-tools: Read, Glob, Bash
---

Clear Laurel's working data for the current film. Target = `$ARGUMENTS` (default to asking if empty).

Scope:
- `profile` → delete `materials/PROFILE.md`
- `plans` → delete the contents of `plans/`
- `materials` → delete the **contents** of `materials/` (keep `materials/README.md` and the folder)
- `all` → profile + plans + materials contents

**Never touch** `.claude/`, `app.py`, `static/`, `cv/`, `cover_letters/` class files, or any
`*.md` under `.claude/skills/` — those are Laurel's brain and product, not per-film data.

Before deleting anything: list exactly what will be removed and ask for explicit confirmation.
Only proceed on a clear "yes". After clearing, confirm what's gone and suggest `/intake` to begin
a new film.
