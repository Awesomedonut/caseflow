"use client";

import { useState } from "react";
import { useResearch } from "@/hooks/use-research";
import { ResearchInput } from "@/components/research-input";
import { ExampleQueries } from "@/components/example-queries";
import { ResearchMemoDisplay } from "@/components/research-memo";
import { AgentStatusStepper } from "@/components/agent-status";
import { CitationList } from "@/components/citation-list";
import { Alert, AlertDescription } from "@/components/ui/alert";
import type { ExampleQuery } from "@/lib/types";

export default function Home() {
  const {
    agentStatuses,
    memo,
    isLoading,
    error,
    startResearch,
    reset,
  } = useResearch();

  const [hasStarted, setHasStarted] = useState(false);
  const [inputQuery, setInputQuery] = useState("");
  const [inputJurisdiction, setInputJurisdiction] = useState("");
  const [inputPracticeArea, setInputPracticeArea] = useState("");

  function handleSubmit(
    query: string,
    jurisdiction: string,
    practiceArea: string,
  ) {
    setHasStarted(true);
    startResearch(query, jurisdiction, practiceArea);
  }

  function handleExampleSelect(example: ExampleQuery) {
    setInputQuery(example.query);
    setInputJurisdiction(example.jurisdiction);
    setInputPracticeArea(example.practice_area);
  }

  function handleNewSearch() {
    setHasStarted(false);
    reset();
    setInputQuery("");
    setInputJurisdiction("");
    setInputPracticeArea("");
  }

  // Landing state (no search started yet)
  if (!hasStarted) {
    return (
      <div className="flex flex-col flex-1 items-center justify-center font-sans">
        <main className="flex flex-1 w-full max-w-2xl flex-col items-center justify-center gap-8 px-6 py-16">
          <div className="flex flex-col items-center gap-3 text-center">
            <h1 className="text-4xl font-bold tracking-tight">CaseFlow</h1>
            <p className="text-lg text-muted-foreground max-w-md">
              AI-powered legal research with verified citations for Canadian
              case law.
            </p>
          </div>

          <ResearchInput
            onSubmit={handleSubmit}
            isLoading={false}
            initialQuery={inputQuery}
            initialJurisdiction={inputJurisdiction}
            initialPracticeArea={inputPracticeArea}
          />

          <ExampleQueries onSelect={handleExampleSelect} />
        </main>
      </div>
    );
  }

  // Research in progress / completed
  return (
    <div className="flex flex-col flex-1 font-sans">
      {/* Header */}
      <header className="border-b px-6 py-3 flex items-center justify-between">
        <h1 className="text-lg font-bold tracking-tight">CaseFlow</h1>
        <button
          onClick={handleNewSearch}
          className="text-sm text-muted-foreground hover:text-foreground transition-colors"
        >
          New Search
        </button>
      </header>

      {/* Main content */}
      <main className="flex-1 flex flex-col lg:flex-row gap-6 p-6 max-w-7xl mx-auto w-full">
        {/* Left column: Memo */}
        <div className="flex-1 min-w-0 space-y-4">
          <ResearchMemoDisplay memo={memo} isLoading={isLoading} />
        </div>

        {/* Right column: Status + Citations */}
        <div className="w-full lg:w-80 shrink-0 space-y-4">
          <AgentStatusStepper statuses={agentStatuses} />

          {memo && (
            <CitationList
              citations={memo.citations}
              overallConfidence={memo.confidence_score}
            />
          )}
        </div>
      </main>

      {/* Error display */}
      {error && (
        <div className="px-6 pb-6 max-w-7xl mx-auto w-full">
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        </div>
      )}
    </div>
  );
}
