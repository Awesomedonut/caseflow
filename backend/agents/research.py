"""Research agent: searches for relevant Canadian case law."""

import json
from models.state import CaseFlowState
from models.case import CaseReference
from mock.llm import MockLLM
from tools.web_search import web_search
from agents.prompts import RESEARCH_SYSTEM_PROMPT


async def research_node(state: CaseFlowState) -> dict:
    """Search for relevant case law based on the user's legal question.

    1. Generate search queries from the user question
    2. Execute web searches for each query
    3. Parse results into structured CaseReference objects
    """
    query = state["query"]
    jurisdiction = state.get("jurisdiction", "")
    practice_area = state.get("practice_area", "")

    llm = MockLLM()

    # Step 1: Generate search queries
    context = f"Question: {query}"
    if jurisdiction:
        context += f"\nJurisdiction: {jurisdiction}"
    if practice_area:
        context += f"\nPractice area: {practice_area}"

    queries_response = await llm.generate(
        prompt=context,
        system=RESEARCH_SYSTEM_PROMPT,
    )
    queries_data = json.loads(queries_response)
    search_queries = queries_data.get("queries", [query])

    # Step 2: Execute searches
    all_results: list[dict] = []
    seen_urls: set[str] = set()
    for search_query in search_queries:
        results = await web_search(search_query)
        for r in results:
            url = r.get("url", "")
            if url not in seen_urls:
                seen_urls.add(url)
                all_results.append(r)

    # Step 3: Parse into CaseReference objects
    # In mock mode, we match search results to our mock case database
    from mock.cases import get_cases_for_query

    mock_cases = get_cases_for_query(jurisdiction, practice_area)
    case_references = []
    for case_data in mock_cases:
        ref = CaseReference(
            title=case_data["title"],
            citation=case_data["citation"],
            court=case_data["court"],
            year=case_data["year"],
            database_id=case_data.get("database_id"),
            case_id=case_data.get("case_id"),
            url=case_data.get("url"),
            date_decided=case_data.get("date_decided"),
            relevance_summary=case_data.get("relevance_summary", ""),
            key_holdings=case_data.get("key_holdings", []),
        )
        case_references.append(ref.model_dump())

    return {
        "search_queries": search_queries,
        "raw_search_results": all_results,
        "case_references": case_references,
        "agent_statuses": state.get("agent_statuses", [])
        + [
            {
                "agent": "research",
                "status": "completed",
                "message": f"Found {len(case_references)} relevant cases",
            }
        ],
    }
