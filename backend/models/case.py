from pydantic import BaseModel
from typing import Optional, Literal


class CaseReference(BaseModel):
    title: str
    citation: str
    court: str
    year: int
    database_id: Optional[str] = None
    case_id: Optional[str] = None
    url: Optional[str] = None
    date_decided: Optional[str] = None
    relevance_summary: str = ""
    key_holdings: list[str] = []


class VerificationResult(BaseModel):
    citation: str
    url_checked: str
    status: Literal["verified", "unverified", "error"]
    http_status_code: Optional[int] = None
    confidence_score: float = 0.0
    notes: str = ""
