import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import apiClient from '@kubb/plugin-client/clients/axios';
import { loginApiV1AuthLoginPost, registerApiV1AuthRegisterPost } from '../../api/gen/client';
import type { TokenResponse } from '../../api/gen/types';

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

const applyClientAuth = (token: string | null) => {
  const currentConfig = apiClient.getConfig();
  const headers = {
    ...((currentConfig.headers as Record<string, string | undefined>) ?? {}),
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  } else {
    delete headers.Authorization;
  }

  apiClient.setConfig({
    ...currentConfig,
    headers,
  });
};


export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [accessToken, setAccessToken] = useState<string | null>(() => localStorage.getItem(ACCESS_TOKEN_KEY));
  const [refreshToken, setRefreshToken] = useState<string | null>(() => localStorage.getItem(REFRESH_TOKEN_KEY));

  useEffect(() => {
    applyClientAuth(accessToken);
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
    const tokens = await loginApiV1AuthLoginPost({ email, password });
    persistTokens(tokens);
  }, [persistTokens]);

  const register = useCallback(async (email: string, password: string) => {
    const tokens = await registerApiV1AuthRegisterPost({ email, password });
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
