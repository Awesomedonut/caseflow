"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface ResearchInputProps {
  onSubmit: (query: string, jurisdiction: string, practiceArea: string) => void;
  isLoading: boolean;
  initialQuery?: string;
  initialJurisdiction?: string;
  initialPracticeArea?: string;
}

export function ResearchInput({
  onSubmit,
  isLoading,
  initialQuery = "",
  initialJurisdiction = "",
  initialPracticeArea = "",
}: ResearchInputProps) {
  const [query, setQuery] = useState(initialQuery);
  const [jurisdiction, setJurisdiction] = useState(initialJurisdiction);
  const [practiceArea, setPracticeArea] = useState(initialPracticeArea);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!query.trim()) return;
    onSubmit(query.trim(), jurisdiction, practiceArea);
  }

  return (
    <form onSubmit={handleSubmit} className="w-full space-y-4">
      <Textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter a legal research question..."
        className="min-h-[100px] resize-none text-base"
        disabled={isLoading}
      />
      <div className="flex flex-col sm:flex-row gap-3">
        <Select value={jurisdiction} onValueChange={(v) => setJurisdiction(v ?? "")}>
          <SelectTrigger className="w-full sm:w-[160px]">
            <SelectValue placeholder="Jurisdiction" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Canada</SelectItem>
            <SelectItem value="BC">British Columbia</SelectItem>
            <SelectItem value="ON">Ontario</SelectItem>
            <SelectItem value="AB">Alberta</SelectItem>
            <SelectItem value="QC">Quebec</SelectItem>
            <SelectItem value="Federal">Federal</SelectItem>
          </SelectContent>
        </Select>
        <Select value={practiceArea} onValueChange={(v) => setPracticeArea(v ?? "")}>
          <SelectTrigger className="w-full sm:w-[180px]">
            <SelectValue placeholder="Practice area" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All areas</SelectItem>
            <SelectItem value="landlord-tenant">Landlord-Tenant</SelectItem>
            <SelectItem value="employment">Employment</SelectItem>
            <SelectItem value="family">Family</SelectItem>
            <SelectItem value="contract">Contract</SelectItem>
            <SelectItem value="criminal">Criminal</SelectItem>
          </SelectContent>
        </Select>
        <Button
          type="submit"
          disabled={isLoading || !query.trim()}
          className="sm:ml-auto"
        >
          {isLoading ? "Researching..." : "Research"}
        </Button>
      </div>
    </form>
  );
}
