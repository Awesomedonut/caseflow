"""LangGraph workflow connecting research, synthesis, and verification agents."""

from langgraph.graph import StateGraph, END
from models.state import CaseFlowState
from agents.research import research_node
from agents.synthesis import synthesis_node
from agents.verification import verification_node


def check_research(state: CaseFlowState) -> str:
    """Route after research: proceed if cases found, else end with error."""
    case_refs = state.get("case_references", [])
    if len(case_refs) > 0:
        return "synthesis_node"
    return "end"


def check_synthesis(state: CaseFlowState) -> str:
    """Route after synthesis: proceed if memo exists, retry once if not."""
    memo = state.get("memo")
    if memo is not None:
        return "verification_node"
    iteration_count = state.get("iteration_count", 0)
    if iteration_count < 2:
        return "synthesis_node"
    return "end"


async def compile_results_node(state: CaseFlowState) -> dict:
    """Merge verification results into the memo and compute overall confidence."""
    memo = state.get("memo")
    verification_results = state.get("verification_results", [])

    if memo and verification_results:
        # Build a lookup from citation to verification result
        verification_lookup: dict[str, dict] = {}
        for vr in verification_results:
            verification_lookup[vr["citation"]] = vr

        # Merge verification into citation cards
        updated_citations = []
        for card in memo.get("citations", []):
            case_data = card.get("case", {})
            citation = case_data.get("citation", "")
            vr = verification_lookup.get(citation)
            if vr:
                card["verification"] = vr
            updated_citations.append(card)
        memo["citations"] = updated_citations

        # Compute overall confidence
        if verification_results:
            avg_confidence = sum(
                vr.get("confidence_score", 0) for vr in verification_results
            ) / len(verification_results)
            memo["confidence_score"] = round(avg_confidence, 2)

    return {"memo": memo}


def build_workflow() -> StateGraph:
    """Build and return the compiled CaseFlow LangGraph workflow."""
    workflow = StateGraph(CaseFlowState)

    # Add nodes
    workflow.add_node("research_node", research_node)
    workflow.add_node("synthesis_node", synthesis_node)
    workflow.add_node("verification_node", verification_node)
    workflow.add_node("compile_results_node", compile_results_node)

    # Set entry point
    workflow.set_entry_point("research_node")

    # Add edges with conditional routing
    workflow.add_conditional_edges(
        "research_node",
        check_research,
        {"synthesis_node": "synthesis_node", "end": END},
    )

    workflow.add_conditional_edges(
        "synthesis_node",
        check_synthesis,
        {
            "verification_node": "verification_node",
            "synthesis_node": "synthesis_node",
            "end": END,
        },
    )

    workflow.add_edge("verification_node", "compile_results_node")
    workflow.add_edge("compile_results_node", END)

    return workflow.compile()


# Pre-built compiled workflow instance
app = build_workflow()
