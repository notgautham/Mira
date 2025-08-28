// src/api/http.ts
const BASE_URL =
  (import.meta.env.VITE_MIRA_API as string) || "http://127.0.0.1:8765";

export async function getJSON<T>(path: string): Promise<T> {
  const r = await fetch(`${BASE_URL}${path}`);
  if (!r.ok) throw new Error(`GET ${path} -> ${r.status}`);
  return r.json();
}

export async function putJSON<T>(path: string, body: unknown): Promise<T> {
  const r = await fetch(`${BASE_URL}${path}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error(`PUT ${path} -> ${r.status}`);
  return r.json();
}
