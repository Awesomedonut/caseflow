"""Extract Canadian legal citations from text using regex patterns."""

import re

# Pattern: "2024 BCSC 123" or "2017 BCPC 232"
NEUTRAL_CITATION = re.compile(
    r"(\d{4})\s+([A-Z]{2,6})\s+(\d+)",
)

# Pattern: "1960 CanLII 294 (ON SC)" or "1992 CanLII 102 (SCC)"
CANLII_CITATION = re.compile(
    r"(\d{4})\s+CanLII\s+(\d+)\s+\(([^)]+)\)",
)

# Pattern: "[2003] 1 SCR 303" (traditional reporter citation)
REPORTER_CITATION = re.compile(
    r"\[(\d{4})\]\s+(\d+)\s+([A-Z]{2,5})\s+(\d+)",
)


def extract_citations(text: str) -> list[str]:
    """Extract all unique Canadian legal citations from text.

    Returns a deduplicated list of citation strings in the order found.
    """
    citations: list[str] = []
    seen: set[str] = set()

    # Extract CanLII-style citations first (more specific pattern)
    for match in CANLII_CITATION.finditer(text):
        citation = match.group(0)
        if citation not in seen:
            citations.append(citation)
            seen.add(citation)

    # Extract neutral citations
    for match in NEUTRAL_CITATION.finditer(text):
        citation = match.group(0)
        # Skip if it's part of a CanLII citation we already captured
        if citation not in seen and f"CanLII {match.group(3)}" not in text[
            max(0, match.start() - 10) : match.end() + 5
        ]:
            citations.append(citation)
            seen.add(citation)

    # Extract reporter citations
    for match in REPORTER_CITATION.finditer(text):
        citation = match.group(0)
        if citation not in seen:
            citations.append(citation)
            seen.add(citation)

    return citations


def citation_to_canlii_url(citation: str) -> str | None:
    """Attempt to construct a CanLII URL from a citation string.

    Returns None if the citation format is not recognized.
    """
    # Map court abbreviations to CanLII database paths
    court_to_path: dict[str, tuple[str, str]] = {
        # BC courts
        "BCSC": ("bc", "bcsc"),
        "BCCA": ("bc", "bcca"),
        "BCPC": ("bc", "bcpc"),
        "BCHRT": ("bc", "bchrt"),
        "BCRTB": ("bc", "bcrtb"),
        # Ontario courts
        "ONSC": ("on", "onsc"),
        "ONCA": ("on", "onca"),
        "ONCJ": ("on", "oncj"),
        # Alberta courts
        "ABCA": ("ab", "abca"),
        "ABKB": ("ab", "abkb"),
        "ABQB": ("ab", "abqb"),
        # Federal / Supreme Court
        "SCC": ("ca", "scc-csc"),
        "FCA": ("ca", "fca-caf"),
        "FC": ("ca", "fct-cf"),
    }

    # Try neutral citation: "2024 BCSC 123"
    m = NEUTRAL_CITATION.match(citation.strip())
    if m:
        year, court, number = m.group(1), m.group(2), m.group(3)
        if court in court_to_path:
            province, db = court_to_path[court]
            case_id = f"{year}{court.lower()}{number}"
            return (
                f"https://www.canlii.org/en/{province}/{db}/"
                f"doc/{year}/{case_id}/{case_id}.html"
            )

    # Try CanLII citation: "1960 CanLII 294 (ON SC)"
    m = CANLII_CITATION.match(citation.strip())
    if m:
        year, number, court_raw = m.group(1), m.group(2), m.group(3).strip()
        # Normalize court abbreviation
        court_normalized = court_raw.replace(" ", "").upper()
        if court_normalized in court_to_path:
            province, db = court_to_path[court_normalized]
            case_id = f"{year}canlii{number}"
            return (
                f"https://www.canlii.org/en/{province}/{db}/"
                f"doc/{year}/{case_id}/{case_id}.html"
            )

    return None
