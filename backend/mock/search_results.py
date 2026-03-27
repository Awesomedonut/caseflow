"""Mock web search results for development."""

MOCK_SEARCH_RESULTS: dict[str, list[dict]] = {
    "security deposit BC normal wear tear": [
        {
            "title": "Security Deposits and Normal Wear - BC Residential Tenancy Branch",
            "url": "https://www2.gov.bc.ca/gov/content/housing-tenancy/residential-tenancies/ending-a-tenancy/returning-deposits",
            "snippet": (
                "Under s. 38 of the Residential Tenancy Act, a landlord must "
                "return a security deposit within 15 days of the tenancy ending "
                "unless the tenant agrees to deductions or the landlord applies "
                "for dispute resolution. Normal wear and tear is expected "
                "deterioration from everyday living."
            ),
        },
        {
            "title": "Gichuru v Pallai, 2013 BCHRT 55 - CanLII",
            "url": "https://www.canlii.org/en/bc/bchrt/doc/2013/2013bchrt55/2013bchrt55.html",
            "snippet": (
                "The tribunal considered the landlord's obligations regarding "
                "security deposits and proper procedures for withholding."
            ),
        },
        {
            "title": "Vander Schaaf v Chambers, 2017 BCPC 232 - CanLII",
            "url": "https://www.canlii.org/en/bc/bcpc/doc/2017/2017bcpc232/2017bcpc232.html",
            "snippet": (
                "Court examined the distinction between normal wear and tear "
                "versus tenant-caused damage in a security deposit dispute."
            ),
        },
        {
            "title": "McCallum v Parkbridge, 2020 BCSC 1406 - CanLII",
            "url": "https://www.canlii.org/en/bc/bcsc/doc/2020/2020bcsc1406/2020bcsc1406.html",
            "snippet": (
                "Examined landlord obligations under the Residential Tenancy Act "
                "regarding security deposit returns."
            ),
        },
    ],
    "wrongful dismissal Ontario reasonable notice": [
        {
            "title": "Bardal v The Globe & Mail Ltd, 1960 CanLII 294 (ON SC)",
            "url": "https://www.canlii.org/en/on/onsc/doc/1960/1960canlii294/1960canlii294.html",
            "snippet": (
                "The foundational case establishing the factors for determining "
                "reasonable notice in wrongful dismissal: character of employment, "
                "length of service, age, and availability of similar employment."
            ),
        },
        {
            "title": "Honda Canada Inc v Keays, 2008 SCC 39 - CanLII",
            "url": "https://www.canlii.org/en/ca/scc/doc/2008/2008scc39/2008scc39.html",
            "snippet": (
                "Supreme Court of Canada landmark on damages in wrongful "
                "dismissal cases, establishing that damages for manner of "
                "dismissal are compensatory, not punitive."
            ),
        },
        {
            "title": "Machtinger v HOJ Industries Ltd, 1992 CanLII 102 (SCC)",
            "url": "https://www.canlii.org/en/ca/scc/doc/1992/1992canlii102/1992canlii102.html",
            "snippet": (
                "SCC addressed the enforceability of termination clauses "
                "in employment contracts that fall below statutory minimums."
            ),
        },
    ],
    "spousal support domestic contract Divorce Act": [
        {
            "title": "Miglin v Miglin, 2003 SCC 24 - CanLII",
            "url": "https://www.canlii.org/en/ca/scc/doc/2003/2003scc24/2003scc24.html",
            "snippet": (
                "SCC established the two-stage test for setting aside "
                "domestic contracts under the Divorce Act."
            ),
        },
        {
            "title": "Hickey v Hickey, 1999 CanLII 691 (SCC)",
            "url": "https://www.canlii.org/en/ca/scc/doc/1999/1999canlii691/1999canlii691.html",
            "snippet": (
                "Established the standard of appellate review for "
                "spousal support decisions."
            ),
        },
    ],
}
