interface ConfidenceBadgeProps {
  score: number;
}

export function ConfidenceBadge({ score }: ConfidenceBadgeProps) {
  const percentage = Math.round(score * 100);

  let colorClass: string;
  if (score >= 0.8) {
    colorClass = "bg-green-500";
  } else if (score >= 0.5) {
    colorClass = "bg-yellow-500";
  } else {
    colorClass = "bg-red-500";
  }

  return (
    <div className="flex items-center gap-1.5">
      <div className={`h-2.5 w-2.5 rounded-full ${colorClass}`} />
      <span className="text-xs text-muted-foreground font-mono">
        {percentage}%
      </span>
    </div>
  );
}
