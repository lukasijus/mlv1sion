import React, { useEffect, useMemo, useState } from 'react';
import { Alert, Box, Button, CircularProgress, Stack, Typography } from '@mui/material';
import { useLocation, useNavigate } from 'react-router-dom';
import AuthShell from '../components/AuthShell';
import { useAuth } from '../providers/authContext';

const GoogleCallbackPage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { completeExternalLogin } = useAuth();
  const [error, setError] = useState<string | null>(null);

  const hashParams = useMemo(() => {
    const normalized = location.hash.replace(/^#/, '');
    return new URLSearchParams(normalized);
  }, [location.hash]);

  useEffect(() => {
    const errorCode = hashParams.get('error');
    const errorDescription = hashParams.get('error_description');

    if (errorCode) {
      setError(errorDescription ?? `Google sign-in failed (${errorCode})`);
      return;
    }

    const accessToken = hashParams.get('access_token');
    const refreshToken = hashParams.get('refresh_token');
    const tokenType = hashParams.get('token_type') ?? 'bearer';

    if (!accessToken || !refreshToken) {
      setError('Google callback did not include authentication tokens.');
      return;
    }

    completeExternalLogin({
      access_token: accessToken,
      refresh_token: refreshToken,
      token_type: tokenType,
    });

    const timeout = window.setTimeout(() => {
      navigate('/', { replace: true });
    }, 500);

    return () => {
      window.clearTimeout(timeout);
    };
  }, [completeExternalLogin, hashParams, navigate]);

  return (
    <AuthShell title={error ? 'Google sign-in failed' : 'Signing you in'}>
      <Box>
        <Stack spacing={3} alignItems="center">
          {error ? (
            <>
              <Alert severity="error" sx={{ width: '100%' }}>
                {error}
              </Alert>
              <Button variant="contained" onClick={() => navigate('/login')}>
                Back to login
              </Button>
            </>
          ) : (
            <>
              <CircularProgress color="primary" />
              <Typography color="text.secondary">Finishing Google sign-in…</Typography>
            </>
          )}
        </Stack>
      </Box>
    </AuthShell>
  );
};

export default GoogleCallbackPage;
