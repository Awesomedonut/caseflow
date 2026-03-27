import type { ResearchMemo as ResearchMemoType } from "@/lib/types";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";

interface ResearchMemoProps {
  memo: ResearchMemoType | null;
  isLoading: boolean;
}

function renderMarkdown(text: string): string {
  // Simple markdown rendering for the MVP
  return text
    .replace(/## (.*)/g, '<h2 class="text-lg font-semibold mt-6 mb-2">$1</h2>')
    .replace(
      /\*\*(.*?)\*\*/g,
      '<strong class="font-semibold">$1</strong>',
    )
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(
      /^\d+\. (.*)/gm,
      '<li class="ml-4 list-decimal text-sm leading-relaxed">$1</li>',
    )
    .replace(
      /^- (.*)/gm,
      '<li class="ml-4 list-disc text-sm leading-relaxed">$1</li>',
    )
    .replace(/\n\n/g, '</p><p class="text-sm leading-relaxed mt-3">')
    .replace(/\n/g, "<br />");
}

export function ResearchMemoDisplay({ memo, isLoading }: ResearchMemoProps) {
  if (isLoading && !memo) {
    return (
      <Card>
        <CardHeader>
          <Skeleton className="h-6 w-3/4" />
          <Skeleton className="h-4 w-1/2 mt-2" />
        </CardHeader>
        <CardContent className="space-y-3">
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-3/4" />
          <Skeleton className="h-4 w-full mt-4" />
          <Skeleton className="h-4 w-5/6" />
          <Skeleton className="h-4 w-full" />
        </CardContent>
      </Card>
    );
  }

  if (!memo) return null;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-xl">{memo.title}</CardTitle>
        <CardDescription className="text-sm italic">
          &ldquo;{memo.question}&rdquo;
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Summary */}
        <div className="p-4 bg-accent/50 rounded-lg">
          <p className="text-sm font-medium mb-1">Summary</p>
          <p className="text-sm text-muted-foreground leading-relaxed">
            {memo.summary}
          </p>
        </div>

        <Separator />

        {/* Analysis */}
        <div
          className="prose prose-sm dark:prose-invert max-w-none"
          dangerouslySetInnerHTML={{
            __html: `<p class="text-sm leading-relaxed">${renderMarkdown(memo.analysis)}</p>`,
          }}
        />

        <Separator />

        {/* Conclusion */}
        <div className="p-4 bg-accent/50 rounded-lg">
          <p className="text-sm font-medium mb-1">Conclusion</p>
          <p className="text-sm leading-relaxed">{memo.conclusion}</p>
        </div>

        {/* Jurisdiction note */}
        {memo.jurisdiction_note && (
          <p className="text-xs text-muted-foreground italic">
            {memo.jurisdiction_note}
          </p>
        )}

        {/* Disclaimer */}
        <Alert>
          <AlertDescription className="text-xs">
            {memo.disclaimer}
          </AlertDescription>
        </Alert>
      </CardContent>
    </Card>
  );
}
