import type { CitationCard as CitationCardType } from "@/lib/types";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ConfidenceBadge } from "@/components/confidence-badge";

interface CitationCardProps {
  citation: CitationCardType;
}

export function CitationCard({ citation }: CitationCardProps) {
  const { case: caseRef, verification } = citation;

  let statusBadge;
  if (!verification) {
    statusBadge = (
      <Badge variant="secondary" className="text-xs">
        Checking...
      </Badge>
    );
  } else if (verification.status === "verified") {
    statusBadge = (
      <Badge className="bg-green-500/10 text-green-700 border-green-500/20 hover:bg-green-500/10 text-xs">
        Verified
      </Badge>
    );
  } else if (verification.status === "unverified") {
    statusBadge = (
      <Badge variant="destructive" className="text-xs">
        Unverified
      </Badge>
    );
  } else {
    statusBadge = (
      <Badge variant="outline" className="text-xs">
        Error
      </Badge>
    );
  }

  return (
    <Card className="overflow-hidden">
      <CardContent className="p-4">
        <div className="flex items-start justify-between gap-2">
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium leading-tight">{caseRef.title}</p>
            <p className="text-xs text-muted-foreground font-mono mt-0.5">
              {caseRef.citation}
            </p>
          </div>
          <div className="flex flex-col items-end gap-1 shrink-0">
            {statusBadge}
            {verification && (
              <ConfidenceBadge score={verification.confidence_score} />
            )}
          </div>
        </div>

        {caseRef.relevance_summary && (
          <p className="text-xs text-muted-foreground mt-2 line-clamp-2">
            {caseRef.relevance_summary}
          </p>
        )}

        <div className="flex items-center justify-between mt-2">
          <span className="text-xs text-muted-foreground">
            {caseRef.court} &middot; {caseRef.year}
          </span>
          {caseRef.url && (
            <a
              href={caseRef.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-blue-600 hover:underline"
            >
              View on CanLII
            </a>
          )}
        </div>

        {verification?.status === "unverified" && (
          <div className="mt-2 p-2 bg-red-50 dark:bg-red-950/20 rounded text-xs text-red-700 dark:text-red-400">
            {verification.notes}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
