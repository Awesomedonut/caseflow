from typing import TypedDict, Optional, Literal


class AgentStatus(TypedDict):
    agent: Literal["research", "synthesis", "verification"]
    status: Literal["pending", "running", "completed", "error"]
    message: str


class CaseFlowState(TypedDict, total=False):
    # Input
    query: str
    jurisdiction: str
    practice_area: str

    # Research agent output
    search_queries: list[str]
    raw_search_results: list[dict]
    case_references: list[dict]

    # Synthesis agent output
    memo: Optional[dict]
    cited_cases: list[dict]

    # Verification agent output
    verification_results: list[dict]

    # Workflow metadata
    agent_statuses: list[dict]
    errors: list[str]
    iteration_count: int
