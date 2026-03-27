"""Mock Canadian case law database for development without CanLII API key."""

MOCK_CASES: dict[str, list[dict]] = {
    "landlord-tenant-bc": [
        {
            "title": "Gichuru v Pallai",
            "citation": "2013 BCHRT 55",
            "court": "BCHRT",
            "year": 2013,
            "database_id": "bchrt",
            "case_id": "2013bchrt55",
            "url": "https://www.canlii.org/en/bc/bchrt/doc/2013/2013bchrt55/2013bchrt55.html",
            "date_decided": "2013-02-15",
            "relevance_summary": (
                "Established standards for security deposit disputes and "
                "human rights considerations in tenancy contexts."
            ),
            "key_holdings": [
                "Landlords must follow proper procedures for deposit claims",
                "Tenants have rights to dispute deductions",
                "Documentation is essential for deposit withholding",
            ],
            "exists": True,
        },
        {
            "title": "Vander Schaaf v Chambers",
            "citation": "2017 BCPC 232",
            "court": "BCPC",
            "year": 2017,
            "database_id": "bcpc",
            "case_id": "2017bcpc232",
            "url": "https://www.canlii.org/en/bc/bcpc/doc/2017/2017bcpc232/2017bcpc232.html",
            "date_decided": "2017-08-10",
            "relevance_summary": (
                "Addressed the distinction between normal wear and tear "
                "versus tenant-caused damage in BC residential tenancies."
            ),
            "key_holdings": [
                "Normal wear and tear is expected deterioration from everyday living",
                "Landlord bears the burden of proving damage beyond normal wear",
                "Photographic evidence is important for damage claims",
            ],
            "exists": True,
        },
        {
            "title": "McCallum v Parkbridge Lifestyle Communities",
            "citation": "2020 BCSC 1406",
            "court": "BCSC",
            "year": 2020,
            "database_id": "bcsc",
            "case_id": "2020bcsc1406",
            "url": "https://www.canlii.org/en/bc/bcsc/doc/2020/2020bcsc1406/2020bcsc1406.html",
            "date_decided": "2020-09-18",
            "relevance_summary": (
                "Examined landlord obligations under the Residential Tenancy Act "
                "regarding security deposit returns and proper procedures."
            ),
            "key_holdings": [
                "Security deposits must be returned within statutory timelines",
                "Landlords must provide itemized deductions",
                "Failure to follow procedures may result in full deposit return",
            ],
            "exists": True,
        },
        {
            # Deliberately fake case for testing verification failure
            "title": "Zhang v Metro Housing Corp",
            "citation": "2023 BCSC 456",
            "court": "BCSC",
            "year": 2023,
            "database_id": "bcsc",
            "case_id": "2023bcsc456",
            "url": "https://www.canlii.org/en/bc/bcsc/doc/2023/2023bcsc456/2023bcsc456.html",
            "date_decided": "2023-09-01",
            "relevance_summary": "Fictional case for testing verification failure.",
            "key_holdings": ["This case does not exist"],
            "exists": False,
        },
    ],
    "employment-on": [
        {
            "title": "Bardal v The Globe & Mail Ltd",
            "citation": "1960 CanLII 294 (ON SC)",
            "court": "ONSC",
            "year": 1960,
            "database_id": "onsc",
            "case_id": "1960canlii294",
            "url": "https://www.canlii.org/en/on/onsc/doc/1960/1960canlii294/1960canlii294.html",
            "date_decided": "1960-05-10",
            "relevance_summary": (
                "Established the foundational factors for determining "
                "reasonable notice period in wrongful dismissal."
            ),
            "key_holdings": [
                "Character of employment",
                "Length of service",
                "Age of employee",
                "Availability of similar employment",
            ],
            "exists": True,
        },
        {
            "title": "Honda Canada Inc v Keays",
            "citation": "2008 SCC 39",
            "court": "SCC",
            "year": 2008,
            "database_id": "scc-csc",
            "case_id": "2008scc39",
            "url": "https://www.canlii.org/en/ca/scc/doc/2008/2008scc39/2008scc39.html",
            "date_decided": "2008-06-27",
            "relevance_summary": (
                "SCC landmark on damages in wrongful dismissal, "
                "including the framework for bad faith damages."
            ),
            "key_holdings": [
                "Damages for manner of dismissal are compensatory, not punitive",
                "Wallace bump-up replaced with Keays framework",
            ],
            "exists": True,
        },
        {
            "title": "Machtinger v HOJ Industries Ltd",
            "citation": "1992 CanLII 102 (SCC)",
            "court": "SCC",
            "year": 1992,
            "database_id": "scc-csc",
            "case_id": "1992canlii102",
            "url": "https://www.canlii.org/en/ca/scc/doc/1992/1992canlii102/1992canlii102.html",
            "date_decided": "1992-06-25",
            "relevance_summary": (
                "Addressed the enforceability of termination clauses "
                "in employment contracts under Ontario law."
            ),
            "key_holdings": [
                "Termination clauses that violate minimum standards are void",
                "Common law notice period applies when clause is unenforceable",
                "Courts interpret employment contracts in favor of employees",
            ],
            "exists": True,
        },
        {
            # Fake case
            "title": "Robertson v TechStar Industries Inc",
            "citation": "2024 ONSC 1234",
            "court": "ONSC",
            "year": 2024,
            "database_id": "onsc",
            "case_id": "2024onsc1234",
            "url": "https://www.canlii.org/en/on/onsc/doc/2024/2024onsc1234/2024onsc1234.html",
            "date_decided": "2024-03-15",
            "relevance_summary": "Fictional case for testing verification failure.",
            "key_holdings": ["This case does not exist"],
            "exists": False,
        },
    ],
    "family-on": [
        {
            "title": "Miglin v Miglin",
            "citation": "2003 SCC 24",
            "court": "SCC",
            "year": 2003,
            "database_id": "scc-csc",
            "case_id": "2003scc24",
            "url": "https://www.canlii.org/en/ca/scc/doc/2003/2003scc24/2003scc24.html",
            "date_decided": "2003-04-17",
            "relevance_summary": (
                "Two-stage test for setting aside domestic contracts "
                "under the Divorce Act."
            ),
            "key_holdings": [
                "Stage 1: Was the agreement negotiated and executed properly?",
                "Stage 2: Does the agreement comply with Divorce Act objectives?",
            ],
            "exists": True,
        },
        {
            "title": "Hickey v Hickey",
            "citation": "1999 CanLII 691 (SCC)",
            "court": "SCC",
            "year": 1999,
            "database_id": "scc-csc",
            "case_id": "1999canlii691",
            "url": "https://www.canlii.org/en/ca/scc/doc/1999/1999canlii691/1999canlii691.html",
            "date_decided": "1999-06-10",
            "relevance_summary": (
                "Established the standard of appellate review for "
                "spousal support decisions."
            ),
            "key_holdings": [
                "Trial judges have broad discretion in support decisions",
                "Appellate courts should not interfere unless clear error",
            ],
            "exists": True,
        },
    ],
}


def get_cases_for_query(jurisdiction: str = "", practice_area: str = "") -> list[dict]:
    """Return mock cases matching the jurisdiction and practice area."""
    key_parts = []
    if practice_area:
        key_parts.append(practice_area.lower().replace(" ", "-"))
    if jurisdiction:
        key_parts.append(jurisdiction.lower())

    # Try exact match first
    key = "-".join(key_parts)
    if key in MOCK_CASES:
        return MOCK_CASES[key]

    # Try reversed order
    key = "-".join(reversed(key_parts))
    if key in MOCK_CASES:
        return MOCK_CASES[key]

    # Partial match: find any key containing the practice area or jurisdiction
    for case_key, cases in MOCK_CASES.items():
        if practice_area and practice_area.lower().replace(" ", "-") in case_key:
            return cases
        if jurisdiction and jurisdiction.lower() in case_key:
            return cases

    # Default: return the first set of cases
    return list(MOCK_CASES.values())[0]
