"""
Laurel — World-Class Film Festival Distribution Agent
FastAPI backend with streaming Claude claude-opus-4-8 + web search
"""

import os
import json
import threading
import asyncio
import urllib.parse
import urllib.request
from pathlib import Path

import anthropic
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Preferred: an official, sanctioned search API (Brave). DuckDuckGo's unofficial
# client is kept only as a zero-config local fallback.
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY", "").strip()

try:
    from duckduckgo_search import DDGS
    HAS_DDG = True
except ImportError:
    HAS_DDG = False

_SEARCH_PROVIDER = (
    "Brave Search API" if BRAVE_API_KEY
    else "DuckDuckGo (unofficial, dev fallback)" if HAS_DDG
    else "NONE — set BRAVE_API_KEY or install duckduckgo-search"
)
print(f"[laurel] web search provider: {_SEARCH_PROVIDER}")

app = FastAPI(title="Laurel")
client = anthropic.Anthropic()

# ─────────────────────────────────────────────────────────────
# Laurel's Identity & Knowledge
#
# Laurel's "brain" lives in versioned Markdown files under
# .claude/skills/festival-strategist/ (NN-*.md). The system prompt is
# assembled from them on every request, so editing a skill file changes
# Laurel's behavior on the next message — no code change, no restart.
# See STRUCTURE.md and the skill's SKILL.md for the layout.
# ─────────────────────────────────────────────────────────────

SKILL_DIR = Path(__file__).parent / ".claude" / "skills" / "festival-strategist"

# Minimal safety net if the skill files are missing — keeps the app alive
# (degraded: no rich plan contract) and makes the misconfiguration obvious.
_FALLBACK_PROMPT = (
    "You are Laurel, a world-class film festival distribution strategist. "
    "Converse with the filmmaker, decode their film's DNA, verify festival "
    "details by searching the web, and never invent deadlines. "
    "[Knowledge base missing: .claude/skills/festival-strategist/ NN-*.md not found.]"
)


def load_system_prompt() -> str:
    """Concatenate the numbered skill files (NN-*.md) into Laurel's system prompt.

    Read fresh each call so edits to the skill files take effect on the next
    message without restarting the server. SKILL.md (the manifest) is excluded.
    """
    parts: list[str] = []
    if SKILL_DIR.is_dir():
        for path in sorted(SKILL_DIR.glob("[0-9][0-9]-*.md")):
            try:
                text = path.read_text(encoding="utf-8").strip()
                if text:
                    parts.append(text)
            except OSError:
                continue
    if not parts:
        print(f"[laurel] WARNING: no skill files in {SKILL_DIR}; using fallback prompt.")
        return _FALLBACK_PROMPT
    return "\n\n".join(parts)

TOOLS = [
    {
        "name": "web_search",
        "description": (
            "Search the web for current film festival information: submission deadlines, fees, "
            "eligibility requirements, and distribution news. Call this for any festival where "
            "you need verified current information rather than relying on potentially outdated "
            "training data. Search for specific festivals, genres, or distribution topics."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "Specific search query. Examples: "
                        "'Sundance 2026 feature film submission deadline', "
                        "'Cannes 2025 short film submissions open', "
                        "'IDFA 2025 documentary submission fee'"
                    )
                }
            },
            "required": ["query"]
        }
    }
]

# ─────────────────────────────────────────────────────────────
# Web Search Implementation
# ─────────────────────────────────────────────────────────────

def _search_brave(query: str, n: int = 6) -> list[tuple[str, str, str]]:
    """Official Brave Search API. Reads public search results over a sanctioned endpoint."""
    url = "https://api.search.brave.com/res/v1/web/search?" + urllib.parse.urlencode(
        {"q": query, "count": n}
    )
    req = urllib.request.Request(
        url, headers={"Accept": "application/json", "X-Subscription-Token": BRAVE_API_KEY}
    )
    with urllib.request.urlopen(req, timeout=12) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    results = (data.get("web") or {}).get("results") or []
    return [
        (r.get("title", "No title"), r.get("description", ""), r.get("url", ""))
        for r in results[:n]
    ]


def _search_ddg(query: str, n: int = 6) -> list[tuple[str, str, str]]:
    """Unofficial DuckDuckGo client — local/dev fallback only."""
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=n))
    return [
        (r.get("title", "No title"), r.get("body", ""), r.get("href", ""))
        for r in results
    ]


def do_web_search(query: str) -> str:
    """Search the open web via the best available provider.

    Provider priority: official Brave Search API (if BRAVE_API_KEY is set) → DuckDuckGo
    fallback (if the library is installed). Both read PUBLIC search results only — Laurel
    never scrapes gated or ToS-restricted sites (e.g. FilmFreeway is linked to, not fetched).
    """
    try:
        if BRAVE_API_KEY:
            rows = _search_brave(query)
        elif HAS_DDG:
            rows = _search_ddg(query)
        else:
            return (
                "Web search is unavailable. Set BRAVE_API_KEY for the official Brave Search "
                "API, or `pip install duckduckgo-search` for the dev fallback. "
                "Proceeding with training knowledge."
            )

        if not rows:
            return f"No web results found for: '{query}'. Proceeding with training knowledge."

        return "\n\n---\n\n".join(
            f"**{title}**\n{body}\nSource: {url}" for title, body, url in rows
        )

    except Exception as e:
        return f"Search error for '{query}': {str(e)}. Proceeding with training knowledge."


# ─────────────────────────────────────────────────────────────
# Agent Streaming Loop (runs in a background thread)
# ─────────────────────────────────────────────────────────────

def _run_agent(messages: list[dict], system_prompt: str, queue: asyncio.Queue, loop: asyncio.AbstractEventLoop):
    """
    Synchronous agent loop. Runs in a thread, puts JSON events into the
    asyncio queue so the async generator can yield them to the client.
    """
    def emit(event: dict):
        loop.call_soon_threadsafe(queue.put_nowait, event)

    conversation = [
        {"role": m["role"], "content": m["content"]}
        for m in messages
    ]

    try:
        while True:
            with client.messages.stream(
                model="claude-opus-4-8",
                max_tokens=16000,
                system=system_prompt,
                tools=TOOLS,
                thinking={"type": "adaptive"},
                messages=conversation,
            ) as stream:
                for event in stream:
                    if event.type == "content_block_delta":
                        delta = event.delta
                        if hasattr(delta, "type") and delta.type == "text_delta":
                            emit({"type": "text", "content": delta.text})

                final = stream.get_final_message()

            # Append assistant turn (with tool_use blocks) to conversation
            conversation.append({
                "role": "assistant",
                "content": final.content
            })

            if final.stop_reason == "end_turn":
                break

            elif final.stop_reason == "tool_use":
                tool_results = []
                for block in final.content:
                    if block.type == "tool_use" and block.name == "web_search":
                        query = block.input.get("query", "")
                        emit({"type": "searching", "query": query})
                        result = do_web_search(query)
                        emit({"type": "searched", "query": query})
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        })

                if tool_results:
                    conversation.append({"role": "user", "content": tool_results})
                else:
                    break
            else:
                break

    except Exception as e:
        emit({"type": "error", "content": str(e)})
    finally:
        loop.call_soon_threadsafe(queue.put_nowait, None)


# ─────────────────────────────────────────────────────────────
# API Routes
# ─────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    messages: list[dict]


@app.post("/api/chat")
async def chat(request: ChatRequest):
    async def event_generator():
        queue: asyncio.Queue = asyncio.Queue()
        loop = asyncio.get_running_loop()

        system_prompt = load_system_prompt()  # re-read skill files each request

        thread = threading.Thread(
            target=_run_agent,
            args=(request.messages, system_prompt, queue, loop),
            daemon=True,
        )
        thread.start()

        while True:
            event = await queue.get()
            if event is None:
                break
            yield f"data: {json.dumps(event)}\n\n"

        thread.join(timeout=2)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


_NOCACHE = {"Cache-Control": "no-store, no-cache, must-revalidate", "Pragma": "no-cache"}


@app.get("/")
async def root():
    html_path = Path(__file__).parent / "static" / "index.html"
    return HTMLResponse(html_path.read_text(), headers=_NOCACHE)


@app.get("/landing")
async def landing():
    """Marketing site (awwwards-style, GSAP + WebGL) — separate from the app."""
    html_path = Path(__file__).parent / "static" / "landing.html"
    return HTMLResponse(html_path.read_text(), headers=_NOCACHE)


# Mount static files
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
