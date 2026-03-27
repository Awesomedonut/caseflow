"""URL verification tool for checking if CanLII citations exist."""

import httpx
from config import settings


async def check_url(url: str) -> dict:
    """Check if a URL exists by making an HTTP HEAD request.

    Returns a dict with status, http_status_code, and notes.
    In mock mode, checks against the mock case database.
    """
    if settings.mock_mode:
        return _mock_check(url)
    return await _real_check(url)


def _mock_check(url: str) -> dict:
    """Check URL against mock case database."""
    from mock.cases import MOCK_CASES

    for _key, cases in MOCK_CASES.items():
        for case in cases:
            if case.get("url") == url:
                if case.get("exists", True):
                    return {
                        "status": "verified",
                        "http_status_code": 200,
                        "notes": "Case found in database (mock verification)",
                    }
                else:
                    return {
                        "status": "unverified",
                        "http_status_code": 404,
                        "notes": "Case not found — possible hallucination (mock verification)",
                    }

    # URL not in mock database at all
    return {
        "status": "unverified",
        "http_status_code": None,
        "notes": "URL not found in mock database",
    }


async def _real_check(url: str) -> dict:
    """Make a real HTTP HEAD request to verify a URL exists."""
    try:
        async with httpx.AsyncClient(
            follow_redirects=True, timeout=10.0
        ) as client:
            response = await client.head(url)

            if response.status_code == 200:
                return {
                    "status": "verified",
                    "http_status_code": 200,
                    "notes": "URL returned 200 OK",
                }
            elif 300 <= response.status_code < 400:
                return {
                    "status": "verified",
                    "http_status_code": response.status_code,
                    "notes": f"URL redirected (HTTP {response.status_code})",
                }
            elif response.status_code == 404:
                return {
                    "status": "unverified",
                    "http_status_code": 404,
                    "notes": "URL returned 404 Not Found — case may not exist",
                }
            else:
                return {
                    "status": "error",
                    "http_status_code": response.status_code,
                    "notes": f"Unexpected HTTP status: {response.status_code}",
                }
    except httpx.TimeoutException:
        return {
            "status": "error",
            "http_status_code": None,
            "notes": "Request timed out",
        }
    except httpx.RequestError as e:
        return {
            "status": "error",
            "http_status_code": None,
            "notes": f"Request error: {e}",
        }
