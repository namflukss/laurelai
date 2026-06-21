---
description: Build or revise the tiered festival strategy for the current film, with verified deadlines.
argument-hint: "[optional constraints, e.g. 'budget under $1000' or 'keep world premiere intact']"
allowed-tools: Read, Write, WebSearch, WebFetch, Glob
---

Load the **festival-strategist** skill — follow `04-festival-evaluation.md` (tiering, premiere
protection, budget, fit scoring) and `03-writing-style.md` (voice + response modes).

1. **Read the film profile** at `materials/PROFILE.md`. If it's missing, tell the user to run
   `/intake` first (or run a quick talk-first discovery to capture the essentials before planning).
2. **Apply any constraints** in `$ARGUMENTS` (budget cap, premiere to protect, region, deadline to hit).
3. **Verify before you recommend.** For every festival you're seriously considering, search the web
   for its current edition's submission deadline and fee ("[festival] [year] submission deadline").
   Never state a date you didn't confirm — mark unconfirmed ones as "check website".
4. **Produce the plan** per `04`: tiered festivals with honest `fit` scores, premiere-conflict
   awareness, a named strategy, a realistic budget range, and — most important — the **submission
   path** (Phase 1 = submit now; later phases conditional). Lead with 1–2 sentences of framing.
5. **Persist it.** Write the readable plan to `plans/<YYYY-MM-DD>-<short-slug>.md` (create `plans/`
   if needed) so the run is diff-able. Append the `FESTIVAL_DATA` JSON block at the end of that file
   exactly as specified in `04` — it's the contract the web UI's `parseData()` consumes.

Be discriminating with `fit` (reserve 90+ for bullseyes). If the profile is thin, name your
assumptions in one line and proceed rather than stalling.
