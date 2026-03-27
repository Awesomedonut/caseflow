"""Verification agent: independently verifies every citation in the memo."""

from models.state import CaseFlowState
from models.case import VerificationResult
from tools.citation_parser import extract_citations, citation_to_canlii_url
from tools.url_checker import check_url


async def verification_node(state: CaseFlowState) -> dict:
    """Independently verify every citation in the research memo.

    This agent does NOT trust the synthesis agent. It:
    1. Re-extracts all citations from the memo text independently
    2. Constructs CanLII URLs for each citation
    3. Checks if each URL actually exists
    4. Returns verification results with confidence scores
    """
    memo = state.get("memo")
    if not memo:
        return {
            "verification_results": [],
            "errors": state.get("errors", [])
            + ["No memo to verify"],
            "agent_statuses": state.get("agent_statuses", [])
            + [
                {
                    "agent": "verification",
                    "status": "error",
                    "message": "No memo to verify",
                }
            ],
        }

    # Step 1: Independently extract citations from memo text
    memo_text = f"{memo.get('analysis', '')} {memo.get('conclusion', '')}"
    extracted_citations = extract_citations(memo_text)

    # Also check citations listed in the memo's citation cards
    for card in memo.get("citations", []):
        case_data = card.get("case", {})
        citation = case_data.get("citation", "")
        if citation and citation not in extracted_citations:
            extracted_citations.append(citation)

    # Step 2 & 3: Verify each citation
    verification_results = []
    for citation in extracted_citations:
        # Construct the CanLII URL
        url = citation_to_canlii_url(citation)

        if url is None:
            # Could not construct URL from citation format
            result = VerificationResult(
                citation=citation,
                url_checked="N/A",
                status="error",
                confidence_score=0.0,
                notes=f"Could not construct CanLII URL from citation: {citation}",
            )
        else:
            # Check if the URL exists
            check_result = await check_url(url)
            status = check_result["status"]
            http_code = check_result.get("http_status_code")

            # Calculate confidence score
            if status == "verified":
                confidence = 1.0 if http_code == 200 else 0.7
            elif status == "unverified":
                confidence = 0.0
            else:
                confidence = 0.3

            result = VerificationResult(
                citation=citation,
                url_checked=url,
                status=status,
                http_status_code=http_code,
                confidence_score=confidence,
                notes=check_result.get("notes", ""),
            )

        verification_results.append(result.model_dump())

    # Summary stats
    verified_count = sum(
        1 for r in verification_results if r["status"] == "verified"
    )
    total = len(verification_results)

    return {
        "verification_results": verification_results,
        "agent_statuses": state.get("agent_statuses", [])
        + [
            {
                "agent": "verification",
                "status": "completed",
                "message": f"Verified {verified_count}/{total} citations",
            }
        ],
    }
