# CaseFlow

AI-powered legal research agent for Canadian case law with source verification.

## What it does

1. Enter a natural language legal question
2. **Research Agent** searches for relevant Canadian case law
3. **Synthesis Agent** writes a structured research memo with citations
4. **Verification Agent** independently confirms every cited case actually exists

The key differentiator: every citation is verified against CanLII (Canadian Legal Information Institute) to prevent AI hallucination of legal sources.

## Architecture

```
Frontend (Next.js + shadcn/ui)     Backend (Python FastAPI + LangGraph)
├── Query input form         →     POST /api/research (SSE stream)
├── Agent status stepper     ←       ├── Research Agent
├── Research memo display    ←       ├── Synthesis Agent
├── Citation cards w/ status ←       └── Verification Agent
└── Example queries          ←     GET /api/examples
```

**LangGraph Workflow:**
```
START → Research → [has cases?] → Synthesis → [has memo?] → Verification → Compile → END
```

- **Backend**: Python, FastAPI, LangGraph (multi-agent orchestration), Pydantic
- **Frontend**: Next.js 15, TypeScript, Tailwind CSS v4, shadcn/ui
- **Communication**: Server-Sent Events (SSE) for real-time agent status updates
- **Mock Mode**: Full pipeline works without any API keys

## Quick Start

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 and enter a legal question. The app runs in **mock mode** by default — no API keys needed.

### Run Tests

```bash
cd backend
source .venv/bin/activate
pytest tests/ -v
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Health check (returns mock mode status) |
| GET | `/api/examples` | Example research queries |
| POST | `/api/research` | Start research — returns SSE event stream |

### SSE Events

The `/api/research` endpoint streams these events:

```
agent_status        → Agent pipeline updates (running/completed/error)
research_complete   → Cases found by research agent
synthesis_complete  → Research memo written by synthesis agent
verification_update → Individual citation verification results
complete            → Final memo with all verifications merged
error               → Error message if pipeline fails
```

## Switching to Real APIs

Set environment variables in `backend/.env`:

```bash
MOCK_MODE=false
LLM_PROVIDER=anthropic        # or "openai"
ANTHROPIC_API_KEY=sk-...
SEARCH_PROVIDER=tavily         # or "serper"
TAVILY_API_KEY=tvly-...
```

No code changes needed — restart the backend and it uses real services.

## Project Structure

```
caseflow/
├── backend/
│   ├── main.py                # FastAPI app entrypoint
│   ├── config.py              # Settings + mock mode toggle
│   ├── models/
│   │   ├── state.py           # LangGraph state (CaseFlowState)
│   │   ├── case.py            # CaseReference, VerificationResult
│   │   └── memo.py            # ResearchMemo, CitationCard
│   ├── agents/
│   │   ├── research.py        # Searches for case law
│   │   ├── synthesis.py       # Writes research memo
│   │   ├── verification.py    # Verifies citations exist
│   │   └── prompts.py         # Prompt templates
│   ├── tools/
│   │   ├── citation_parser.py # Canadian citation regex extraction
│   │   ├── web_search.py      # Web search (mock + real)
│   │   └── url_checker.py     # HTTP URL verification
│   ├── graph/
│   │   └── workflow.py        # LangGraph StateGraph definition
│   ├── mock/
│   │   ├── llm.py             # Mock LLM responses
│   │   ├── cases.py           # Mock Canadian case database
│   │   └── search_results.py  # Mock search results
│   └── api/
│       ├── routes.py          # FastAPI routes
│       └── sse.py             # SSE streaming infrastructure
├── frontend/
│   └── src/
│       ├── app/page.tsx       # Main page (landing + results)
│       ├── components/
│       │   ├── research-input.tsx
│       │   ├── research-memo.tsx
│       │   ├── agent-status.tsx
│       │   ├── citation-card.tsx
│       │   ├── citation-list.tsx
│       │   ├── confidence-badge.tsx
│       │   └── example-queries.tsx
│       ├── hooks/
│       │   └── use-research.ts    # SSE streaming hook
│       └── lib/
│           ├── types.ts           # TypeScript types
│           └── api.ts             # API client
└── README.md
```

## License

MIT
