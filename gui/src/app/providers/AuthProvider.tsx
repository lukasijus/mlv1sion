import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import { client } from '../../client/client.gen';
import { loginApiV1AuthLoginPost, registerApiV1AuthRegisterPost } from '../../client/sdk.gen';
import type { TokenResponse } from '../../client';

type AuthContextValue = {
  isAuthenticated: boolean;
  accessToken?: string | null;
  refreshToken?: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

const ACCESS_TOKEN_KEY = 'auth.access_token';
const REFRESH_TOKEN_KEY = 'auth.refresh_token';

function setClientAuth(accessToken?: string | null) {
  if (accessToken) {
    client.setConfig({
      auth: async () => accessToken,
    });
  } else {
    client.setConfig({ auth: undefined });
  }
}

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [accessToken, setAccessToken] = useState<string | null>(() => localStorage.getItem(ACCESS_TOKEN_KEY));
  const [refreshToken, setRefreshToken] = useState<string | null>(() => localStorage.getItem(REFRESH_TOKEN_KEY));

  useEffect(() => {
    setClientAuth(accessToken);
  }, [accessToken]);

  const persistTokens = useCallback((tokens: TokenResponse) => {
    localStorage.setItem(ACCESS_TOKEN_KEY, tokens.access_token);
    localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh_token);
    setAccessToken(tokens.access_token);
    setRefreshToken(tokens.refresh_token);
  }, []);

  const clearTokens = useCallback(() => {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    setAccessToken(null);
    setRefreshToken(null);
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const tokens = await loginApiV1AuthLoginPost({
      body: { email, password },
      responseStyle: 'data',
      throwOnError: true,
    });
    persistTokens(tokens);
  }, [persistTokens]);

  const register = useCallback(async (email: string, password: string) => {
    const tokens = await registerApiV1AuthRegisterPost({
      body: { email, password },
      responseStyle: 'data',
      throwOnError: true,
    });
    persistTokens(tokens);
  }, [persistTokens]);

  const logout = useCallback(() => {
    clearTokens();
  }, [clearTokens]);

  const value = useMemo(
    () => ({
      isAuthenticated: Boolean(accessToken),
      accessToken,
      refreshToken,
      login,
      register,
      logout,
    }),
    [accessToken, refreshToken, login, register, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
};
