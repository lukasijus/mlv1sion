import type { User } from '../api/types';

// TODO: Implement auth hook (React Query + auth store integration)
export function useAuth() {
  const user: User | null = null;
  return {
    user,
    isAuthenticated: !!user,
    login: (_u: string, _p: string) => {
      // TODO
    },
    logout: () => {
      // TODO
    },
  };
}
