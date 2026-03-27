import type { CitationCard as CitationCardType } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { CitationCard } from "@/components/citation-card";
import { ConfidenceBadge } from "@/components/confidence-badge";

interface CitationListProps {
  citations: CitationCardType[];
  overallConfidence: number;
}

export function CitationList({
  citations,
  overallConfidence,
}: CitationListProps) {
  const verified = citations.filter(
    (c) => c.verification?.status === "verified",
  ).length;
  const total = citations.length;

  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-sm font-medium">
            Citations ({verified}/{total} verified)
          </CardTitle>
          {total > 0 && <ConfidenceBadge score={overallConfidence} />}
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        {citations.length === 0 ? (
          <p className="text-xs text-muted-foreground">
            Citations will appear here after synthesis...
          </p>
        ) : (
          citations.map((citation) => (
            <CitationCard
              key={citation.case.citation}
              citation={citation}
            />
          ))
        )}
      </CardContent>
    </Card>
  );
}
