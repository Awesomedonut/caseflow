"""End-to-end tests for the CaseFlow LangGraph workflow."""

import pytest
from graph.workflow import build_workflow


@pytest.fixture
def workflow():
    return build_workflow()


def make_initial_state(
    query: str,
    jurisdiction: str = "",
    practice_area: str = "",
) -> dict:
    return {
        "query": query,
        "jurisdiction": jurisdiction,
        "practice_area": practice_area,
        "search_queries": [],
        "raw_search_results": [],
        "case_references": [],
        "memo": None,
        "cited_cases": [],
        "verification_results": [],
        "agent_statuses": [],
        "errors": [],
        "iteration_count": 0,
    }


@pytest.mark.asyncio
async def test_full_pipeline_landlord_tenant(workflow):
    """End-to-end: landlord-tenant query runs all three agents."""
    state = make_initial_state(
        query="Can a landlord in BC withhold a security deposit for normal wear and tear?",
        jurisdiction="BC",
        practice_area="landlord-tenant",
    )
    result = await workflow.ainvoke(state)

    # Research agent found cases
    assert len(result["case_references"]) >= 3

    # Synthesis agent wrote a memo
    assert result["memo"] is not None
    assert result["memo"]["title"] != ""
    assert result["memo"]["analysis"] != ""
    assert result["memo"]["conclusion"] != ""

    # Verification agent checked citations
    assert len(result["verification_results"]) >= 2

    # At least one verified, at least one unverified (from mock data)
    statuses = [vr["status"] for vr in result["verification_results"]]
    assert "verified" in statuses

    # Confidence score was computed
    assert 0 <= result["memo"]["confidence_score"] <= 1


@pytest.mark.asyncio
async def test_full_pipeline_employment(workflow):
    """Employment law query runs the full pipeline."""
    state = make_initial_state(
        query="What is the test for wrongful dismissal in Ontario?",
        jurisdiction="ON",
        practice_area="employment",
    )
    result = await workflow.ainvoke(state)

    assert len(result["case_references"]) >= 2
    assert result["memo"] is not None
    assert len(result["verification_results"]) >= 2


@pytest.mark.asyncio
async def test_agent_statuses_tracked(workflow):
    """Agent status updates are accumulated in state."""
    state = make_initial_state(
        query="Can a landlord in BC withhold a security deposit?",
        jurisdiction="BC",
        practice_area="landlord-tenant",
    )
    result = await workflow.ainvoke(state)

    agent_statuses = result.get("agent_statuses", [])
    agents_completed = [s["agent"] for s in agent_statuses if s["status"] == "completed"]

    assert "research" in agents_completed
    assert "synthesis" in agents_completed
    assert "verification" in agents_completed


@pytest.mark.asyncio
async def test_verification_catches_fake_case(workflow):
    """The fake case in mock data should be flagged as unverified."""
    state = make_initial_state(
        query="Can a landlord in BC withhold a security deposit for normal wear and tear?",
        jurisdiction="BC",
        practice_area="landlord-tenant",
    )
    result = await workflow.ainvoke(state)

    # The mock data includes "Zhang v Metro Housing Corp" (2023 BCSC 456)
    # which has exists=False
    unverified = [
        vr for vr in result["verification_results"]
        if vr["status"] == "unverified"
    ]
    assert len(unverified) >= 1, "Should catch at least one fake citation"
