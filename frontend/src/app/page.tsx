export default function Home() {
  return (
    <div className="flex flex-col flex-1 items-center justify-center font-sans">
      <main className="flex flex-1 w-full max-w-3xl flex-col items-center justify-center gap-8 px-6 py-16">
        <div className="flex flex-col items-center gap-3 text-center">
          <h1 className="text-4xl font-bold tracking-tight">CaseFlow</h1>
          <p className="text-lg text-muted-foreground max-w-md">
            AI-powered legal research with verified citations for Canadian case
            law.
          </p>
        </div>
        <p className="text-sm text-muted-foreground">
          Research input form coming soon.
        </p>
      </main>
    </div>
  );
}
