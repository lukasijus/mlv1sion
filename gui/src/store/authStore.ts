/* src/store/authStore.ts */
import type { User } from '../api/types';

// TODO: Auth global state store. Replace with Zustand/Context later.

export interface AuthState {
  user: User | null;
  accessToken?: string;
  refreshToken?: string;
}

export const authStore: AuthState = {
  user: null,
};

export function setUser(_user: User | null) {
  // TODO: implement with Zustand/Context
}

export function setTokens(_accessToken?: string, _refreshToken?: string) {
  // TODO: implement with Zustand/Context
}
