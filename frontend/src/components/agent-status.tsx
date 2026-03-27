import type { AgentStatus as AgentStatusType } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const AGENT_LABELS: Record<string, string> = {
  research: "Research",
  synthesis: "Synthesis",
  verification: "Verification",
};

const AGENT_DESCRIPTIONS: Record<string, string> = {
  research: "Searching for relevant case law",
  synthesis: "Writing research memo",
  verification: "Verifying citations",
};

function StatusIcon({ status }: { status: string }) {
  switch (status) {
    case "completed":
      return (
        <div className="h-5 w-5 rounded-full bg-green-500 flex items-center justify-center">
          <svg
            className="h-3 w-3 text-white"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={3}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M5 13l4 4L19 7"
            />
          </svg>
        </div>
      );
    case "running":
      return (
        <div className="h-5 w-5 rounded-full border-2 border-blue-500 border-t-transparent animate-spin" />
      );
    case "error":
      return (
        <div className="h-5 w-5 rounded-full bg-red-500 flex items-center justify-center">
          <svg
            className="h-3 w-3 text-white"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={3}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </div>
      );
    default:
      return (
        <div className="h-5 w-5 rounded-full border-2 border-muted-foreground/30" />
      );
  }
}

interface AgentStatusProps {
  statuses: AgentStatusType[];
}

export function AgentStatusStepper({ statuses }: AgentStatusProps) {
  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="text-sm font-medium">Agent Pipeline</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {statuses.map((s, i) => (
            <div key={s.agent} className="flex items-start gap-3">
              <div className="flex flex-col items-center">
                <StatusIcon status={s.status} />
                {i < statuses.length - 1 && (
                  <div
                    className={`w-0.5 h-6 mt-1 ${
                      s.status === "completed"
                        ? "bg-green-500"
                        : "bg-muted-foreground/20"
                    }`}
                  />
                )}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium">
                  {AGENT_LABELS[s.agent] || s.agent}
                </p>
                <p className="text-xs text-muted-foreground truncate">
                  {s.status === "pending"
                    ? AGENT_DESCRIPTIONS[s.agent]
                    : s.message}
                </p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
