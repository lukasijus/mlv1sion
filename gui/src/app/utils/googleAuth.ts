export const GOOGLE_CALLBACK_PATH = '/auth/google/callback';

type GoogleAuthUrlResponse = {
  authorization_url: string;
};

export const getGoogleAuthorizationUrl = async (redirectPath: string = GOOGLE_CALLBACK_PATH) => {
  const params = new URLSearchParams();
  if (redirectPath) {
    params.set('redirect_to', redirectPath);
  }

  const response = await fetch(`/api/v1/auth/google/url?${params.toString()}`, {
    method: 'GET',
    credentials: 'include',
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || 'Failed to start Google authentication');
  }

  const payload = (await response.json()) as GoogleAuthUrlResponse;
  if (!payload.authorization_url) {
    throw new Error('Missing authorization url from the server');
  }

  return payload.authorization_url;
};
