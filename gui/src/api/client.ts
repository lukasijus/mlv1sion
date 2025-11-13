// TODO: Implement API client (Axios or fetch wrappers) targeting FastAPI backend
export const API_BASE_URL = '/api';

export async function apiGet<T>(path: string): Promise<T> {
  // TODO: implement with fetch/axios
  throw new Error('Not implemented');
}

export async function apiPost<T>(path: string, body: unknown): Promise<T> {
  // TODO: implement with fetch/axios
  throw new Error('Not implemented');
}

export async function apiDelete<T>(path: string): Promise<T> {
  // TODO: implement with fetch/axios
  throw new Error('Not implemented');
}
