---
description: Onboard a film — import from materials/ or run a guided interview, then write the decoded film profile.
argument-hint: "[optional: path to a screener link, synopsis, or EPK]"
allowed-tools: Read, Write, Glob, Bash
---

Load the **festival-strategist** skill (`.claude/skills/festival-strategist/`), especially
`01-film-profile.md` (the essentials + talk-first rules) and `02-creative-profile.md`.

Goal: produce a clean, decoded **film profile** at `materials/PROFILE.md` that `/plan`, `/submit`,
and `/expand` can rely on. Pick the path that fits what's available:

**Path A — Materials exist.** If `materials/` already has content (synopsis, statement, stills,
reviews) or the user passed `$ARGUMENTS`, read everything you can and extract the DNA yourself.
Only ask the user about gaps you genuinely can't infer.

**Path B — Guided interview.** Otherwise, interview the filmmaker the **talk-first** way: react to
what they say, ask for the 1–2 most important gaps at a time, never a long questionnaire. Cover the
essentials from `01-film-profile.md`: format & runtime, genre & tone + logline, completion status,
**premiere status** (screened anywhere yet?), goal, and fee budget / hard deadlines.

When you have a working picture, write `materials/PROFILE.md` with these sections:
`# Film profile`, then `## Logline`, `## Format & runtime`, `## Genre & tone`,
`## Completion & premiere status`, `## Creative read` (voice/themes/comparables per `02`),
`## Goals & constraints`, and `## Open questions` (anything still unknown — don't invent it).

Finish with a 2–3 sentence summary of who this film is and your first instinct on its festival
lane. Do **not** build a full plan here — that's `/plan`.
