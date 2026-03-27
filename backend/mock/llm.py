"""Mock LLM that returns realistic deterministic responses for each agent role."""

import json
from mock.cases import get_cases_for_query


class MockLLM:
    """Drop-in replacement for a real LLM. Returns deterministic responses
    based on the system prompt and query context."""

    async def generate(self, prompt: str, system: str = "") -> str:
        system_lower = system.lower()
        if "search queries" in system_lower:
            return self._mock_search_queries(prompt)
        elif "research memo" in system_lower or "memo writer" in system_lower:
            return self._mock_synthesis(prompt)
        elif "extract" in system_lower and "citation" in system_lower:
            return self._mock_citation_extraction(prompt)
        return json.dumps({"response": "Mock LLM response"})

    def _mock_search_queries(self, prompt: str) -> str:
        """Generate mock search queries from user question."""
        prompt_lower = prompt.lower()

        if "security deposit" in prompt_lower or "wear and tear" in prompt_lower:
            queries = [
                "security deposit BC normal wear tear",
                "Residential Tenancy Act BC security deposit return",
                "CanLII landlord withhold deposit normal wear BC",
            ]
        elif "wrongful dismissal" in prompt_lower or "termination" in prompt_lower:
            queries = [
                "wrongful dismissal Ontario reasonable notice",
                "termination without cause Ontario employment law",
                "CanLII wrongful dismissal reasonable notice factors",
            ]
        elif "spousal support" in prompt_lower or "divorce" in prompt_lower:
            queries = [
                "spousal support domestic contract Divorce Act",
                "setting aside separation agreement Canada",
                "CanLII spousal support variation domestic contract",
            ]
        else:
            queries = [
                f"CanLII {prompt[:50]}",
                f"Canadian case law {prompt[:50]}",
                f"legal precedent Canada {prompt[:50]}",
            ]

        return json.dumps({"queries": queries})

    def _mock_synthesis(self, prompt: str) -> str:
        """Generate a mock research memo."""
        prompt_lower = prompt.lower()

        # Determine topic from context
        if "security deposit" in prompt_lower or "wear and tear" in prompt_lower:
            return self._security_deposit_memo()
        elif "wrongful dismissal" in prompt_lower or "termination" in prompt_lower:
            return self._employment_memo()
        elif "spousal support" in prompt_lower or "divorce" in prompt_lower:
            return self._family_memo()
        else:
            return self._generic_memo()

    def _security_deposit_memo(self) -> str:
        return json.dumps({
            "title": "Security Deposits and Normal Wear and Tear in BC",
            "summary": (
                "Under British Columbia's Residential Tenancy Act, landlords cannot "
                "withhold security deposits for normal wear and tear. The Act and "
                "case law establish clear standards for what constitutes normal wear "
                "versus tenant-caused damage, with the burden of proof on the landlord."
            ),
            "analysis": (
                "## Legal Framework\n\n"
                "Section 38 of the BC *Residential Tenancy Act* (RTA) governs "
                "security deposit returns. A landlord must return the deposit within "
                "15 days of the tenancy ending unless the tenant agrees to deductions "
                "or the landlord applies for dispute resolution.\n\n"
                "## Key Case Law\n\n"
                "In *Gichuru v Pallai*, 2013 BCHRT 55, the tribunal established "
                "important standards for security deposit disputes, emphasizing that "
                "landlords must follow proper procedures when withholding deposits "
                "and that documentation is essential.\n\n"
                "The BC Provincial Court in *Vander Schaaf v Chambers*, 2017 BCPC 232, "
                "directly addressed the distinction between normal wear and tear "
                "versus tenant-caused damage. The court held that normal wear and "
                "tear is the expected deterioration from everyday living, and that "
                "the landlord bears the burden of proving damage beyond this standard. "
                "Photographic evidence was deemed important for establishing damage claims.\n\n"
                "In *McCallum v Parkbridge Lifestyle Communities*, 2020 BCSC 1406, "
                "the BC Supreme Court examined landlord obligations regarding deposit "
                "returns, reinforcing that failure to follow statutory procedures "
                "may result in an order to return the full deposit.\n\n"
                "The case *Zhang v Metro Housing Corp*, 2023 BCSC 456 further "
                "explored the boundaries of permissible deductions from security "
                "deposits in the context of multi-unit residential buildings.\n\n"
                "## Analysis\n\n"
                "The case law is consistent: landlords in BC cannot deduct from "
                "security deposits for normal wear and tear. The key factors courts "
                "consider include:\n\n"
                "1. **Documentation**: Condition reports at move-in and move-out\n"
                "2. **Burden of proof**: The landlord must prove damage beyond normal wear\n"
                "3. **Statutory procedures**: Strict compliance with RTA timelines\n"
                "4. **Reasonableness**: Deductions must be proportionate to actual damage"
            ),
            "conclusion": (
                "No, a landlord in BC cannot lawfully withhold a security deposit "
                "for normal wear and tear. The Residential Tenancy Act and consistent "
                "case law establish that normal wear is an expected part of tenancy, "
                "and landlords must prove damage beyond this threshold to justify "
                "any deductions."
            ),
            "jurisdiction_note": "This analysis applies to British Columbia under the Residential Tenancy Act, RSBC 2002, c 78.",
            "cited_cases": [
                "2013 BCHRT 55",
                "2017 BCPC 232",
                "2020 BCSC 1406",
                "2023 BCSC 456",
            ],
        })

    def _employment_memo(self) -> str:
        return json.dumps({
            "title": "Wrongful Dismissal and Reasonable Notice in Ontario",
            "summary": (
                "Ontario courts apply the Bardal factors to determine reasonable "
                "notice periods in wrongful dismissal cases. The Supreme Court of "
                "Canada has established frameworks for both the notice period and "
                "damages for manner of dismissal."
            ),
            "analysis": (
                "## The Bardal Factors\n\n"
                "The foundational case for wrongful dismissal in Ontario is "
                "*Bardal v The Globe & Mail Ltd*, 1960 CanLII 294 (ON SC), which "
                "established four key factors for determining reasonable notice:\n\n"
                "1. Character of employment\n"
                "2. Length of service\n"
                "3. Age of the employee\n"
                "4. Availability of similar employment\n\n"
                "## Supreme Court Framework\n\n"
                "In *Honda Canada Inc v Keays*, 2008 SCC 39, the Supreme Court "
                "overhauled the framework for damages in wrongful dismissal. The "
                "Court held that damages for the manner of dismissal are compensatory "
                "rather than punitive, replacing the previous Wallace bump-up approach.\n\n"
                "The enforceability of termination clauses was addressed in "
                "*Machtinger v HOJ Industries Ltd*, 1992 CanLII 102 (SCC). The "
                "Court held that termination clauses falling below Employment "
                "Standards Act minimums are void, and common law notice applies.\n\n"
                "Recently, *Robertson v TechStar Industries Inc*, 2024 ONSC 1234, "
                "applied these principles in the context of tech industry layoffs."
            ),
            "conclusion": (
                "The test for wrongful dismissal in Ontario is well-established "
                "through the Bardal factors, as modified by subsequent SCC decisions. "
                "Employers must provide reasonable notice or pay in lieu, and "
                "termination clauses must meet statutory minimums to be enforceable."
            ),
            "jurisdiction_note": "This analysis applies to Ontario under the Employment Standards Act, 2000, SO 2000, c 41.",
            "cited_cases": [
                "1960 CanLII 294 (ON SC)",
                "2008 SCC 39",
                "1992 CanLII 102 (SCC)",
                "2024 ONSC 1234",
            ],
        })

    def _family_memo(self) -> str:
        return json.dumps({
            "title": "Setting Aside Domestic Contracts Under the Divorce Act",
            "summary": (
                "The Supreme Court of Canada's Miglin framework provides a "
                "two-stage test for setting aside domestic contracts, balancing "
                "the principles of finality with fairness."
            ),
            "analysis": (
                "## The Miglin Test\n\n"
                "In *Miglin v Miglin*, 2003 SCC 24, the Supreme Court established "
                "a two-stage test for reviewing domestic contracts:\n\n"
                "**Stage 1**: Was the agreement negotiated and executed in "
                "compliance with contract law principles?\n\n"
                "**Stage 2**: Does the agreement substantially comply with "
                "the objectives of the Divorce Act?\n\n"
                "## Standard of Review\n\n"
                "*Hickey v Hickey*, 1999 CanLII 691 (SCC) established that "
                "trial judges have broad discretion in support decisions and "
                "appellate courts should not interfere unless there is clear error."
            ),
            "conclusion": (
                "Domestic contracts can be set aside under the Miglin framework "
                "if they fail either the negotiation/execution stage or the "
                "Divorce Act compliance stage."
            ),
            "jurisdiction_note": "This analysis applies federally under the Divorce Act, RSC 1985, c 3 (2nd Supp), with Ontario-specific considerations.",
            "cited_cases": ["2003 SCC 24", "1999 CanLII 691 (SCC)"],
        })

    def _generic_memo(self) -> str:
        cases = get_cases_for_query()
        return json.dumps({
            "title": "Legal Research Memo",
            "summary": "This is a mock research memo generated in development mode.",
            "analysis": (
                "## Analysis\n\n"
                "The following cases were identified as potentially relevant:\n\n"
                + "\n".join(
                    f"- *{c['title']}*, {c['citation']}: {c['relevance_summary']}"
                    for c in cases[:3]
                )
            ),
            "conclusion": "Further research is recommended with real case law databases.",
            "jurisdiction_note": "Jurisdiction not specified.",
            "cited_cases": [c["citation"] for c in cases[:3]],
        })

    def _mock_citation_extraction(self, prompt: str) -> str:
        """Extract citations from memo text. In mock mode, just return
        whatever citations are mentioned."""
        # This is used by the verification agent to independently
        # re-extract citations from the memo text
        return json.dumps({"message": "Use citation_parser tool for extraction"})
