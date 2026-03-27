import type { ExampleQuery } from "@/lib/types";
import { Badge } from "@/components/ui/badge";

const EXAMPLES: ExampleQuery[] = [
  {
    query:
      "Can a landlord in BC withhold a security deposit for normal wear and tear?",
    jurisdiction: "BC",
    practice_area: "landlord-tenant",
  },
  {
    query: "What is the test for wrongful dismissal in Ontario?",
    jurisdiction: "ON",
    practice_area: "employment",
  },
  {
    query: "Can a domestic contract be set aside under the Divorce Act?",
    jurisdiction: "ON",
    practice_area: "family",
  },
  {
    query: "What are the Bardal factors for reasonable notice?",
    jurisdiction: "ON",
    practice_area: "employment",
  },
];

interface ExampleQueriesProps {
  onSelect: (example: ExampleQuery) => void;
}

export function ExampleQueries({ onSelect }: ExampleQueriesProps) {
  return (
    <div className="w-full">
      <p className="text-xs text-muted-foreground mb-3">Try an example:</p>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
        {EXAMPLES.map((example) => (
          <button
            key={example.query}
            onClick={() => onSelect(example)}
            className="text-left p-3 rounded-lg border border-border hover:border-foreground/20 hover:bg-accent/50 transition-colors"
          >
            <p className="text-sm leading-snug">{example.query}</p>
            <div className="flex gap-1.5 mt-2">
              <Badge variant="secondary" className="text-xs">
                {example.jurisdiction}
              </Badge>
              <Badge variant="outline" className="text-xs">
                {example.practice_area}
              </Badge>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
