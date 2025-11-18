type MaybeAxiosError = {
  message?: string;
  response?: {
    data?: {
      detail?: string;
      message?: string;
    };
  };
};

export const getErrorMessage = (error: unknown, fallback: string) => {
  if (typeof error === 'string') return error;
  if (error instanceof Error && error.message) return error.message;

  if (error && typeof error === 'object') {
    const maybeError = error as MaybeAxiosError;
    const detail = maybeError.response?.data?.detail ?? maybeError.response?.data?.message;
    if (detail) return detail;
    if (maybeError.message) return maybeError.message;
  }

  return fallback;
};
