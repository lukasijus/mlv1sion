import { createContext, useContext } from 'react';
import type { TokenResponse } from '../../api/gen/types';

export type AuthContextValue = {
  isAuthenticated: boolean;
  accessToken?: string | null;
  refreshToken?: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  completeExternalLogin: (tokens: TokenResponse) => void;
  logout: () => void;
};

export const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return ctx;
};
