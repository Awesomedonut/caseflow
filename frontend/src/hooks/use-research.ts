"use client";

import { useState, useCallback, useRef } from "react";
import type {
  AgentStatus,
  CaseReference,
  ResearchMemo,
  VerificationResult,
} from "@/lib/types";
import { fetchResearchStream } from "@/lib/api";

interface UseResearchReturn {
  agentStatuses: AgentStatus[];
  caseReferences: CaseReference[];
  memo: ResearchMemo | null;
  verificationResults: VerificationResult[];
  isLoading: boolean;
  error: string | null;
  startResearch: (
    query: string,
    jurisdiction?: string,
    practiceArea?: string,
  ) => Promise<void>;
  reset: () => void;
}

export function useResearch(): UseResearchReturn {
  const [agentStatuses, setAgentStatuses] = useState<AgentStatus[]>([
    { agent: "research", status: "pending", message: "Waiting to start..." },
    { agent: "synthesis", status: "pending", message: "Waiting to start..." },
    {
      agent: "verification",
      status: "pending",
      message: "Waiting to start...",
    },
  ]);
  const [caseReferences, setCaseReferences] = useState<CaseReference[]>([]);
  const [memo, setMemo] = useState<ResearchMemo | null>(null);
  const [verificationResults, setVerificationResults] = useState<
    VerificationResult[]
  >([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  const reset = useCallback(() => {
    setAgentStatuses([
      { agent: "research", status: "pending", message: "Waiting to start..." },
      {
        agent: "synthesis",
        status: "pending",
        message: "Waiting to start...",
      },
      {
        agent: "verification",
        status: "pending",
        message: "Waiting to start...",
      },
    ]);
    setCaseReferences([]);
    setMemo(null);
    setVerificationResults([]);
    setIsLoading(false);
    setError(null);
  }, []);

  const startResearch = useCallback(
    async (
      query: string,
      jurisdiction: string = "",
      practiceArea: string = "",
    ) => {
      // Cancel any previous request
      abortRef.current?.abort();
      abortRef.current = new AbortController();

      reset();
      setIsLoading(true);

      // Set research to running
      setAgentStatuses((prev) =>
        prev.map((s) =>
          s.agent === "research"
            ? { ...s, status: "running", message: "Searching for case law..." }
            : s,
        ),
      );

      try {
        const response = await fetchResearchStream(
          query,
          jurisdiction,
          practiceArea,
        );

        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }

        const reader = response.body?.getReader();
        if (!reader) throw new Error("No response body");

        const decoder = new TextDecoder();
        let buffer = "";

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split("\n");
          buffer = lines.pop() || "";

          let currentEvent = "";

          for (const line of lines) {
            if (line.startsWith("event: ")) {
              currentEvent = line.slice(7).trim();
            } else if (line.startsWith("data: ") && currentEvent) {
              const data = JSON.parse(line.slice(6));
              handleSSEEvent(currentEvent, data);
              currentEvent = "";
            }
          }
        }
      } catch (err) {
        if (err instanceof DOMException && err.name === "AbortError") return;
        const message =
          err instanceof Error ? err.message : "Unknown error occurred";
        setError(message);
      } finally {
        setIsLoading(false);
      }
    },
    [reset],
  );

  function handleSSEEvent(eventType: string, data: unknown) {
    switch (eventType) {
      case "agent_status": {
        const status = data as AgentStatus;
        setAgentStatuses((prev) =>
          prev.map((s) => (s.agent === status.agent ? status : s)),
        );
        break;
      }
      case "research_complete": {
        const { case_references } = data as {
          case_references: CaseReference[];
        };
        setCaseReferences(case_references);
        // Set synthesis to running
        setAgentStatuses((prev) =>
          prev.map((s) =>
            s.agent === "synthesis"
              ? {
                  ...s,
                  status: "running",
                  message: "Writing research memo...",
                }
              : s,
          ),
        );
        break;
      }
      case "synthesis_complete": {
        const { memo: memoData } = data as { memo: ResearchMemo };
        setMemo(memoData);
        break;
      }
      case "verification_update": {
        const { result } = data as { result: VerificationResult };
        setVerificationResults((prev) => [...prev, result]);
        break;
      }
      case "complete": {
        const { memo: finalMemo } = data as { memo: ResearchMemo };
        setMemo(finalMemo);
        setIsLoading(false);
        break;
      }
      case "error": {
        const { message } = data as { message: string };
        setError(message);
        setIsLoading(false);
        break;
      }
    }
  }

  return {
    agentStatuses,
    caseReferences,
    memo,
    verificationResults,
    isLoading,
    error,
    startResearch,
    reset,
  };
}
