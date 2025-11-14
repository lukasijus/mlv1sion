export const API_BASE_URL = "/api";

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }
  return (await res.json()) as T;
}

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`);
  return handleResponse<T>(res);
}

// Keep these as TODO for later
export async function apiPost<T>(path: string, body: unknown): Promise<T> {
  throw new Error("Not implemented");
}

export async function apiDelete<T>(path: string): Promise<T> {
  throw new Error("Not implemented");
}
