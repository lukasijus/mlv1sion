export const OAUTH_CALLBACK_PATHS = {
  google: '/auth/google/callback',
  github: '/auth/github/callback',
} as const;

export type OAuthProvider = keyof typeof OAUTH_CALLBACK_PATHS;

type OAuthUrlResponse = {
  authorization_url: string;
};

export const getOAuthAuthorizationUrl = async (
  provider: OAuthProvider,
  redirectPath: string = OAUTH_CALLBACK_PATHS[provider],
) => {
  const params = new URLSearchParams();
  if (redirectPath) {
    params.set('redirect_to', redirectPath);
  }

  const response = await fetch(`/api/v1/auth/${provider}/url?${params.toString()}`, {
    method: 'GET',
    credentials: 'include',
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Failed to start ${provider} authentication`);
  }

  const payload = (await response.json()) as OAuthUrlResponse;
  if (!payload.authorization_url) {
    throw new Error('Missing authorization url from the server');
  }

  return payload.authorization_url;
};

export const getProviderLabel = (provider: OAuthProvider) => {
  switch (provider) {
    case 'github':
      return 'GitHub';
    case 'google':
    default:
      return 'Google';
  }
};
