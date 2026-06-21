# Laurel — Project Structure (target)

This document re-imagines **Laurel** (the film-festival distribution strategist) using the same
**Claude Code "agent project"** conventions as the `ai-job-search` repo: slash commands, skills,
profile documents, and portal CLIs — adapted from *job hunting* to *festival distribution*.

> **Today** Laurel is a 4-file web app (`app.py` + `static/index.html` + `CLAUDE.md` + `requirements.txt`).
> The structure below is the **target**. Items marked **✅ exists**, **♻︎ refactor** (logic already
> lives somewhere, just needs extracting), or **➕ new**.

---

## The mapping (job-search → Laurel)

| `ai-job-search` | Laurel | What it does here |
|---|---|---|
| candidate profile | **film profile** | The film's DNA: format, genre, runtime, premiere status, budget tier |
| `/apply` (draft + review) | **`/submit`** | Draft a cover letter + press kit for one festival, drafter-reviewer pass |
| `/setup` (onboard candidate) | **`/intake`** | Onboard a film: import an EPK, paste a screener/synopsis, or guided interview |
| `/expand` (enrich from docs) | **`/expand`** | Enrich film DNA from materials + the film's online presence (reviews, prior laurels) |
| `/reset` | **`/reset`** | Wipe the film profile or the `materials/` folder |
| job-application-assistant skill | **festival-strategist skill** | Core strategy: tiering, premiere protection, fit scoring |
| behavioral profile (PI/DISC) | **creative profile** | Director's voice, themes, tone — what programmers respond to |
| job-evaluation scoring | **festival-evaluation** | The fit/score framework (currently in `app.py` system prompt) |
| interview-prep (STAR) | **q&a-prep** | Festival Q&A / pitch / on-stage prep |
| CV templates | **press-kit templates** | EPK / one-sheet LaTeX |
| job-scraper | **festival-scraper** | Festival discovery orchestration |
| `/upskill` (skill gaps) | **`/elevate`** | Festival-readiness gaps — what would make the film more competitive |
| job portals (Jobnet, Jobindex…) | **submission platforms** | FilmFreeway, FestHome, FilmFestivalLife |
| `salary_lookup.py` | **`fee_lookup.py`** | Submission-fee benchmarking by tier/region |
| `job_search_tracker.csv` | **`submission_tracker.csv`** | Submission tracking (the web UI already tracks this in localStorage) |

---

## Target tree

```
laurel/
├── CLAUDE.md                           # ✅ Project rules: voice, design system, FESTIVAL_DATA contract, workflow
├── app.py                              # ✅ FastAPI backend — Claude Opus 4.8 + web search, SSE streaming
├── requirements.txt                    # ✅ anthropic, fastapi, uvicorn, duckduckgo-search, python-multipart
├── static/
│   └── index.html                      # ✅ Single-file frontend (chat → plan → festival views)
│
├── .claude/
│   ├── commands/
│   │   ├── intake.md                   # ✅ /intake  — onboard a film (import or guided interview) → materials/PROFILE.md
│   │   ├── plan.md                     # ✅ /plan    — build / revise the tiered strategy (verified deadlines) → plans/
│   │   ├── submit.md                   # ✅ /submit  — draft cover letter + press kit for one festival (drafter-reviewer)
│   │   ├── expand.md                   # ✅ /expand  — enrich film DNA from materials + online presence
│   │   └── reset.md                    # ✅ /reset   — wipe profile / plans / materials
│   │
│   ├── skills/
│   │   ├── festival-strategist/        # ✅ Core strategy skill — Laurel's brain (app.py reads this)
│   │   │   ├── SKILL.md                # ✅ Skill manifest + load order
│   │   │   ├── 00-identity.md          # ✅ Identity + festival knowledge base + operating principles
│   │   │   ├── 01-film-profile.md      # ✅ Decode the DNA + talk-first discovery
│   │   │   ├── 02-creative-profile.md  # ✅ Reading directorial voice/tone → programmer appeal
│   │   │   ├── 03-writing-style.md     # ✅ Voice + response modes (converse/info/advise/plan)
│   │   │   ├── 04-festival-evaluation.md # ✅ Tiering, premiere, budget, fit scoring + FESTIVAL_DATA contract
│   │   │   ├── 05-document-style.md     # ✅ Cover letter / press kit / synopsis / statement writing rules
│   │   │   └── 06-qa-prep.md            # ✅ Festival Q&A / panel prep framework
│   │   ├── festival-scraper/           # ➕ Festival discovery orchestration
│   │   └── elevate/                    # ➕ /elevate — festival-readiness gap analysis
│   │
│   └── settings.local.json             # ➕ Claude Code permissions
│
├── .agents/skills/                     # ➕ Submission-platform CLI tools
│   ├── filmfreeway-search/             #     FilmFreeway
│   ├── festhome-search/                #     FestHome
│   ├── filmfestivallife-search/        #     FilmFestivalLife
│   └── circuit-calendar/               #     Deadline calendar pull
│
├── presskit/
│   └── main_example.tex                # ✅ EPK / one-sheet LaTeX template (pdflatex)
├── cover_letters/
│   ├── cover.cls                       # ✅ Custom cover-letter LaTeX class (pdflatex)
│   ├── example.tex                     # ✅ Worked example cover letter
│   └── OpenFonts/                      # ✅ Lato/Raleway font notes (binaries optional)
│
├── materials/                          # ✅ Film source materials (for /intake Path A and /expand)
│   ├── README.md                       # ✅ Folder layout instructions
│   ├── PROFILE.md                      # ➕ Decoded film profile (written by /intake)
│   ├── synopsis/                       # ➕ Loglines, short & long synopsis
│   ├── statement/                      # ➕ Director's statement
│   ├── stills/                         # ➕ Production stills, poster, key art
│   ├── reviews/                        # ➕ Press, prior selections, laurels
│   └── submissions/                    # ➕ Submission records (<festival>/{cover-letter,press-kit}.md)
│
├── fee_lookup.py                       # ➕ Submission-fee benchmarking tool (BYO data)
├── tools/
│   ├── convert_circuit_excel.py        # ➕ Convert a fee/deadline spreadsheet to JSON
│   └── README_FEE_TOOL.md
│
├── festival_scraper/                   # ➕ Scraper state (seen festivals, results)
├── elevate/                            # ➕ /elevate report output (markdown per run)
├── submission_tracker.csv              # ➕ Submission tracking spreadsheet
└── SETUP.md                            # ➕ Detailed setup guide
```

---

## What already exists vs. what's new

**Exists (the running app):** `CLAUDE.md`, `app.py`, `static/index.html`, `requirements.txt`.
The web UI already covers a lot of what the job-search repo does with files:

- **Intake** → the guided `startIntake()` / Film DNA flow in the chat.
- **Plan / evaluation** → the tiered plan, fit gauges, and the `<FESTIVAL_DATA>` contract.
- **Cover letter / press kit** → the `docMode` documents generated in chat.
- **Tracking** → per-festival status in `localStorage` (`laurel_st::*`), budget bar, `.ics` export.
- **Fee budgeting** → the budget bar + `parseFees()`.

So this isn't a rewrite — it's **extracting the domain knowledge that currently lives inside
`app.py`'s system prompt into versioned skill files**, and adding the offline/agent surface
(commands, portal CLIs, materials folder) around the same engine.

---

## How to build it (phased)

**Phase 1 — Externalize the brain (no behavior change). ✅ DONE.**
The festival expertise now lives in `.claude/skills/festival-strategist/` as `00-*.md … 04-*.md`,
and `app.py`'s `load_system_prompt()` concatenates them (in numeric order) into the `system` prompt
**on every request** — so editing a skill file changes Laurel's behavior on the next message with no
code change and no restart. A `_FALLBACK_PROMPT` keeps the app alive if the files go missing.
The `FESTIVAL_DATA` contract moved verbatim into `04-festival-evaluation.md` (still in sync with
`parseData()` in the frontend).

**Phase 2 — Slash commands as workflows. ✅ DONE.**
`.claude/commands/{intake,plan,submit,expand,reset}.md` orchestrate the skill and give a
CLI/agent way to drive the same flows the web UI exposes. They share one source of truth:
`/intake` writes `materials/PROFILE.md`; `/plan` reads it (and verifies deadlines via web search)
and writes `plans/`; `/submit` does a drafter-reviewer pass per festival; `/expand` enriches the
profile from the film's online footprint; `/reset` clears per-film data only (never the brain).
`materials/README.md` documents the layout.

**Phase 3 — Materials + templates. ✅ DONE.**
The document-writing knowledge now lives in the skill (`05-document-style.md`, `06-qa-prep.md`,
both part of the prompt), and the compilable LaTeX deliverables live at the root:
`cover_letters/cover.cls` (+ `example.tex`) and `presskit/main_example.tex` — both target `pdflatex`,
use Lato if installed, and degrade gracefully. `/submit` now writes Markdown **and** filled `.tex`
into `submissions/<festival-slug>/`. Font binaries are optional (see `cover_letters/OpenFonts/README.md`).

**Phase 4 — Discovery + data tools.**
Add the `.agents/skills/*-search/` portal CLIs (FilmFreeway etc.) and `fee_lookup.py` so
deadlines and fees come from live/benchmarked data rather than only web search.

**Phase 5 — Persistence.**
Mirror the localStorage tracking into `submission_tracker.csv` so progress survives outside
the browser and is diff-able in git.

---

## One caveat

The `ai-job-search` repo is a **pure Claude Code agent** (no server — Claude *is* the runtime).
Laurel is a **web app with its own backend**. The structure above keeps both: `app.py` + `static/`
stay as the live product, while `.claude/` and `.agents/` add the agent-project scaffolding on top
of the *same* knowledge base. The skill files become the shared brain that both the web app and the
slash commands read from.
