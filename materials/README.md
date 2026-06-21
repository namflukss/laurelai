# materials/ — your film's source material

Drop anything about the film here. `/intake` reads this folder to decode the film's DNA, and
`/expand` enriches the profile from it. Nothing here is required — `/intake` can also just
interview you — but the more you add, the sharper Laurel's plan.

## Layout

```
materials/
├── README.md          # this file
├── PROFILE.md         # ← written by /intake (the decoded film profile; the other commands read it)
├── synopsis/          # loglines, short & long synopsis
├── statement/         # director's statement
├── stills/            # production stills, poster, key art
├── reviews/           # press, prior selections, laurels (with sources)
└── submissions/       # per-festival records, written by /submit: <festival-slug>/{cover-letter,press-kit}.md
```

## Notes

- `PROFILE.md` is the single source of truth about *this film*. The festival expertise (how Laurel
  thinks) lives separately in `.claude/skills/festival-strategist/`.
- Plans land in `../plans/` (created by `/plan`), not here.
- `/reset` clears the contents of this folder but keeps this README.
