const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function getHealth() {
  const res = await fetch(`${API_BASE}/api/health`);
  return res.json();
}

export async function getExamples() {
  const res = await fetch(`${API_BASE}/api/examples`);
  const data = await res.json();
  return data.examples;
}

export function startResearchStream(
  query: string,
  jurisdiction: string = "",
  practiceArea: string = "",
): ReadableStream<Uint8Array> | null {
  // We use fetch with POST since EventSource only supports GET
  const controller = new AbortController();

  const response = fetch(`${API_BASE}/api/research`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query,
      jurisdiction,
      practice_area: practiceArea,
    }),
    signal: controller.signal,
  });

  // Return a promise that resolves to the response body stream
  return null; // Handled in the hook
}

export async function fetchResearchStream(
  query: string,
  jurisdiction: string = "",
  practiceArea: string = "",
): Promise<Response> {
  return fetch(`${API_BASE}/api/research`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query,
      jurisdiction,
      practice_area: practiceArea,
    }),
  });
}
