"""Synthesis agent: writes a research memo from case references."""

import json
from models.state import CaseFlowState
from models.memo import ResearchMemo, CitationCard
from models.case import CaseReference
from mock.llm import MockLLM
from agents.prompts import SYNTHESIS_SYSTEM_PROMPT


async def synthesis_node(state: CaseFlowState) -> dict:
    """Write a legal research memo using the found case references.

    Takes the original question and case references, produces a
    structured research memo with inline citations.
    """
    query = state["query"]
    case_references = state.get("case_references", [])
    iteration_count = state.get("iteration_count", 0)

    llm = MockLLM()

    # Build context with case information
    cases_context = "\n\n".join(
        f"Case: {c['title']}, {c['citation']}\n"
        f"Court: {c['court']} ({c['year']})\n"
        f"Relevance: {c.get('relevance_summary', 'N/A')}\n"
        f"Key holdings: {', '.join(c.get('key_holdings', []))}"
        for c in case_references
    )

    prompt = (
        f"Legal question: {query}\n\n"
        f"Available case law:\n{cases_context}\n\n"
        f"Write a research memo answering this question using the above cases."
    )

    memo_response = await llm.generate(
        prompt=prompt,
        system=SYNTHESIS_SYSTEM_PROMPT,
    )
    memo_data = json.loads(memo_response)

    # Build citation cards from cited cases
    cited_citation_strings = memo_data.get("cited_cases", [])
    citation_cards = []
    for citation_str in cited_citation_strings:
        # Find matching case reference
        matching_case = None
        for c in case_references:
            if c["citation"] == citation_str or citation_str in c["citation"]:
                matching_case = c
                break

        if matching_case:
            card = CitationCard(
                case=CaseReference(**matching_case),
                in_memo_location="analysis",
            )
        else:
            # Citation referenced but not in our case list
            card = CitationCard(
                case=CaseReference(
                    title="Unknown",
                    citation=citation_str,
                    court="",
                    year=0,
                    relevance_summary="Referenced in memo but not found in research results",
                ),
                in_memo_location="analysis",
            )
        citation_cards.append(card)

    memo = ResearchMemo(
        title=memo_data.get("title", "Legal Research Memo"),
        question=query,
        summary=memo_data.get("summary", ""),
        analysis=memo_data.get("analysis", ""),
        conclusion=memo_data.get("conclusion", ""),
        citations=[c.model_dump() for c in citation_cards],
        jurisdiction_note=memo_data.get("jurisdiction_note", ""),
    )

    return {
        "memo": memo.model_dump(),
        "cited_cases": [c.model_dump() for c in citation_cards],
        "iteration_count": iteration_count + 1,
        "agent_statuses": state.get("agent_statuses", [])
        + [
            {
                "agent": "synthesis",
                "status": "completed",
                "message": f"Memo complete with {len(citation_cards)} citations",
            }
        ],
    }
