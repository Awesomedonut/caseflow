"""Web search tool with mock and real modes."""

from config import settings


class SearchResult:
    def __init__(self, title: str, url: str, snippet: str):
        self.title = title
        self.url = url
        self.snippet = snippet

    def to_dict(self) -> dict:
        return {"title": self.title, "url": self.url, "snippet": self.snippet}


async def web_search(query: str) -> list[dict]:
    """Search the web for a query. Returns mock results in mock mode."""
    if settings.mock_mode:
        return _mock_search(query)
    return await _real_search(query)


def _mock_search(query: str) -> list[dict]:
    """Return mock search results based on keyword matching."""
    from mock.search_results import MOCK_SEARCH_RESULTS

    query_lower = query.lower()

    # Try exact key match
    for key, results in MOCK_SEARCH_RESULTS.items():
        if key.lower() in query_lower or query_lower in key.lower():
            return results

    # Try partial keyword matching
    best_match: list[dict] = []
    best_score = 0
    for key, results in MOCK_SEARCH_RESULTS.items():
        key_words = set(key.lower().split())
        query_words = set(query_lower.split())
        score = len(key_words & query_words)
        if score > best_score:
            best_score = score
            best_match = results

    if best_match:
        return best_match

    # Default: return first available results
    return list(MOCK_SEARCH_RESULTS.values())[0]


async def _real_search(query: str) -> list[dict]:
    """Placeholder for real web search API integration."""
    # TODO: Implement with Tavily, Serper, or DuckDuckGo API
    raise NotImplementedError(
        f"Real search not configured. Set MOCK_MODE=true or configure "
        f"SEARCH_PROVIDER. Current provider: {settings.search_provider}"
    )
