import type { User } from './types';

// TODO: Auth API functions (login, logout, refresh, me)
export async function login(username: string, password: string): Promise<User> {
  throw new Error('Not implemented');
}

export async function logout(): Promise<void> {
  throw new Error('Not implemented');
}

export async function getCurrentUser(): Promise<User | null> {
  throw new Error('Not implemented');
}
