export interface CaseReference {
  title: string;
  citation: string;
  court: string;
  year: number;
  database_id?: string;
  case_id?: string;
  url?: string;
  date_decided?: string;
  relevance_summary: string;
  key_holdings: string[];
}

export interface VerificationResult {
  citation: string;
  url_checked: string;
  status: "verified" | "unverified" | "error";
  http_status_code?: number;
  confidence_score: number;
  notes: string;
}

export interface CitationCard {
  case: CaseReference;
  verification?: VerificationResult | null;
  in_memo_location: string;
}

export interface ResearchMemo {
  title: string;
  question: string;
  summary: string;
  analysis: string;
  conclusion: string;
  citations: CitationCard[];
  confidence_score: number;
  jurisdiction_note: string;
  disclaimer: string;
}

export type AgentName = "research" | "synthesis" | "verification";
export type AgentStatusValue = "pending" | "running" | "completed" | "error";

export interface AgentStatus {
  agent: AgentName;
  status: AgentStatusValue;
  message: string;
}

export interface ExampleQuery {
  query: string;
  jurisdiction: string;
  practice_area: string;
}

export type SSEEvent =
  | { type: "agent_status"; data: AgentStatus }
  | { type: "research_complete"; data: { case_references: CaseReference[] } }
  | { type: "synthesis_complete"; data: { memo: ResearchMemo } }
  | { type: "verification_update"; data: { result: VerificationResult } }
  | { type: "complete"; data: { memo: ResearchMemo } }
  | { type: "error"; data: { message: string } };
