"""FastAPI route definitions for CaseFlow."""

from fastapi import APIRouter
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from config import settings
from api.sse import run_workflow_with_sse

router = APIRouter(prefix="/api")


class ResearchRequest(BaseModel):
    query: str
    jurisdiction: str = ""
    practice_area: str = ""


@router.get("/health")
async def health():
    return {
        "status": "ok",
        "mock_mode": settings.mock_mode,
        "version": "0.1.0",
    }


@router.get("/examples")
async def examples():
    return {
        "examples": [
            {
                "query": "Can a landlord in BC withhold a security deposit for normal wear and tear?",
                "jurisdiction": "BC",
                "practice_area": "landlord-tenant",
            },
            {
                "query": "What is the test for wrongful dismissal in Ontario?",
                "jurisdiction": "ON",
                "practice_area": "employment",
            },
            {
                "query": "Can a domestic contract be set aside under the Divorce Act?",
                "jurisdiction": "ON",
                "practice_area": "family",
            },
            {
                "query": "What are the Bardal factors for reasonable notice?",
                "jurisdiction": "ON",
                "practice_area": "employment",
            },
        ],
    }


@router.post("/research")
async def research(request: ResearchRequest):
    """Start a legal research query. Returns SSE stream with agent updates."""
    return EventSourceResponse(
        run_workflow_with_sse(
            query=request.query,
            jurisdiction=request.jurisdiction,
            practice_area=request.practice_area,
        )
    )
