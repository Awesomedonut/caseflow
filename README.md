# CaseFlow

AI-powered legal research agent for Canadian case law with source verification.

## What it does

1. Enter a natural language legal question
2. **Research Agent** searches for relevant Canadian case law
3. **Synthesis Agent** writes a structured research memo with citations
4. **Verification Agent** independently confirms every cited case actually exists

The key differentiator: every citation is verified against CanLII (Canadian Legal Information Institute) to prevent AI hallucination of legal sources.

## Architecture

- **Backend**: Python, FastAPI, LangGraph (multi-agent orchestration)
- **Frontend**: Next.js, TypeScript, Tailwind CSS, shadcn/ui
- **Communication**: Server-Sent Events (SSE) for real-time agent status updates

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

The app runs in **mock mode** by default — no API keys needed. Set `MOCK_MODE=false` in `backend/.env` and provide LLM/search API keys to use real services.

## Project Structure

```
caseflow/
├── backend/          # Python FastAPI + LangGraph
│   ├── models/       # Pydantic data models
│   ├── agents/       # Research, Synthesis, Verification agents
│   ├── tools/        # Citation parser, web search, URL checker
│   ├── graph/        # LangGraph workflow definition
│   ├── mock/         # Mock data for development
│   └── api/          # FastAPI routes + SSE streaming
└── frontend/         # Next.js + shadcn/ui
    ├── app/          # Pages (landing, research results)
    ├── components/   # UI components
    ├── hooks/        # React hooks (SSE streaming)
    └── lib/          # Types, API client
```

## License

MIT
