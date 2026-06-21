# Laurel — Button / Navigation Audit

Every clickable element, what it calls, where it actually goes, and a status flag.
Legend: ✅ works as labeled · ⚠️ misleading / mislabeled / duplicate · ❌ dead or placeholder.

---

## Icon rail (left, always present)

| Button | Calls | Goes to | Status |
|---|---|---|---|
| Orb (top) | `newChat()` | Home / new chat | ✅ |
| Chat | `newChat()` | Home / new chat | ✅ (duplicates the orb) |
| Strategy plan | `openLastPlan()` | Last saved plan | ✅ |
| Explore festivals | `openExplore()` | Explore page | ✅ |
| **Deadlines** | `openLastPlan()` | Last saved plan | ⚠️ **duplicate of Strategy plan** — should open the Timeline view, not the same thing |
| Submissions tracker | `openTracker()` | Tracker | ✅ |
| Avatar "F" (bottom) | — | nothing | ⚠️ looks like a profile/account button, does nothing |
| Toggle theme | `toggleTheme()` | dark/light | ✅ |

### Post-accept group in the rail (hidden until a festival is Accepted)
| Button | Calls | Status |
|---|---|---|
| Deliverables | `openDeliverables()` | ✅ |
| Contract check | `openContract()` | ✅ |
| Press kit | `openPressKit()` | ✅ |
| Social posts | `openSocial()` | ✅ |
| Announce crew | `openAnnounce()` | ✅ |
| Presence & follow-up | `openPresence()` | ✅ |
→ ⚠️ **6 icons appear at once on accept** — heavy. Could collapse into one "When selected" entry.

---

## Home (chat empty state)

### "Laurel · Plus" top bar
| Button | Calls | Status |
|---|---|---|
| **Configuration** | `openLastPlan()` | ❌ **placeholder** — "Configuration" opens the plan; makes no sense |
| **Share** | `emailPlan(currentPlan)` | ⚠️ emails the plan; on home with no plan it's empty/misleading |
| New Chat | `newChat()` | ✅ |

### Hero cards
| Card | Calls | Status |
|---|---|---|
| Film DNA Matcher (dark) | `startIntake()` | ✅ |
| **Tasks** card + "View all" | `openLastPlan()` | ⚠️ "Tasks / View all" implies a task list that doesn't exist; opens the plan |
| Suggested prompt | `pick('What festivals…')` | ✅ (fills the composer — doesn't auto-send) |

### Action pills
| Pill | Calls | Status |
|---|---|---|
| **Connect Calendar** | `openLastPlan()` | ❌ **placeholder** — should connect/export a calendar, not open the plan |
| Find Festival Fit | `startIntake()` | ✅ |
| Browse Festivals | `openExplore()` | ✅ |
| Press Kit | `openPressKit()` | ⚠️ post-accept tool exposed on the home empty state (premature, but works) |

### Composer
| Control | Calls | Status |
|---|---|---|
| ✦ wand icon | — | decorative |
| **Select Source ▾** | *(none)* | ❌ **dead** — no handler at all |
| **Attach** | focus input | ❌ placeholder |
| **Voice** | focus input | ❌ placeholder |
| Send | `go()` | ✅ |

---

## Strategy page (planPage) — ✅ all working
Back `closePlan` · List/By-fit/Timeline toggle · Add festival `openExplore` · Share plan `emailPlan` ·
More ▾ (Export deadlines `exportICS`, Save PDF `print`, Draft press kit, Films like yours, Email plan,
Rebalance) · rows → `openFest`.

## Festival detail (festPage) — ✅ all working
Back `closeFest` · Submit on FilmFreeway `window.open` · Official site (Google) · Cover letter ·
Mark declined `markDeclined`. Accepted block → Track deliverables / Check contract / Build press kit /
Announce / Prep the room — all wired.

## Submissions tracker — mostly ✅
Board/Table toggle ✅ · **Alerts → `openLastPlan()`** ⚠️ (mislabeled — "Alerts" opens the plan) ·
Add submission `addSubmission` ✅ · rows tkOpen / tkSubmit / tkDecline ✅.

## Post-accept tools — ✅ working
- **Deliverables:** Get festival requirements (AI), Add item, check/date/note, subtitle translator.
- **Contract:** Check contract (AI flags).
- **Press kit:** Generate/Polish (AI), poster/stills upload, add/delete section, export PDF.
- **Social:** Generate caption (AI), platform/tone toggles, copy.
- **Announce:** Generate email (AI), editable crew/director, pull-from-press-kit, send.
- **Presence:** Intro / Q&A prep / The room / Follow-up tabs, all AI generators + editors.

---

## Summary of what's wrong

**❌ Dead or placeholder (look real, do nothing useful):**
1. Configuration (home bar)
2. Connect Calendar (home pill)
3. Select Source (composer) — no handler at all
4. Attach (composer)
5. Voice (composer)
6. Tasks card / "View all" (home)

**⚠️ Mislabeled / duplicate (go somewhere, but not where the label promises):**
1. Rail "Deadlines" = same as "Strategy plan"
2. Tracker "Alerts" → opens the plan
3. Home "Share" → emails the plan (empty on home)
4. Rail avatar "F" → does nothing
5. Chat icon duplicates the orb

**Clutter:**
- 6 post-accept icons appear in the rail at once.
- Press Kit (a post-accept tool) shown on the home empty state.

**✅ Genuinely working:** the whole core spine (chat → strategy → festival → tracker → accept/decline
re-plan) and all six post-accept tools' internal buttons.

---

## Suggested direction (pending your flow)
- **Remove or "coming soon"** the 6 placeholders so nothing dead is clickable.
- **Fix labels:** Deadlines → open Timeline; Alerts → real alerts or remove; Configuration/Share →
  real actions or remove.
- **Collapse** the 6 post-accept rail icons into one "When selected" hub.
- Drop **Chat** (orb already does it) and either wire or remove the **avatar**.
