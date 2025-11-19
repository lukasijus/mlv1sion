import React, { useState } from 'react';
import { Alert, Box, Button, Divider, Link, Stack, TextField, Typography } from '@mui/material';
import GoogleIcon from '@mui/icons-material/Google';
import GitHubIcon from '@mui/icons-material/GitHub';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import { useAuth } from '../providers/authContext';
import { getErrorMessage } from '../utils/errors';
import AuthShell from '../components/AuthShell';
import { getOAuthAuthorizationUrl, getProviderLabel, type OAuthProvider } from '../utils/googleAuth';

const LoginPage: React.FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [externalProvider, setExternalProvider] = useState<OAuthProvider | null>(null);
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await login(email, password);
      navigate('/');
    } catch (err: unknown) {
      setError(getErrorMessage(err, 'Login failed'));
    } finally {
      setSubmitting(false);
    }
  };

  const onExternalSignIn = async (provider: OAuthProvider) => {
    setError(null);
    setExternalProvider(provider);
    try {
      const url = await getOAuthAuthorizationUrl(provider);
      window.location.href = url;
    } catch (err: unknown) {
      setExternalProvider(null);
      setError(getErrorMessage(err, `Unable to start ${getProviderLabel(provider)} sign-in`));
    }
  };

  return (
    <AuthShell
      title="Welcome back"
      subtitle="Sign in to continue labeling, reviewing, and managing projects."
      footer={(
        <Typography variant="body2" color="text.secondary">
          Don&apos;t have an account?{' '}
          <Link component={RouterLink} to="/register" underline="hover">
            Register
          </Link>
        </Typography>
      )}
    >
      <Box component="form" onSubmit={onSubmit}>
        <Stack spacing={2}>
          {error && <Alert severity="error">{error}</Alert>}
          <Stack spacing={1}>
            <Button
              type="button"
              variant="outlined"
              size="large"
              startIcon={<GoogleIcon />}
              onClick={() => onExternalSignIn('google')}
              disabled={Boolean(externalProvider)}
            >
              {externalProvider === 'google' ? 'Redirecting…' : 'Continue with Google'}
            </Button>
            <Button
              type="button"
              variant="outlined"
              size="large"
              startIcon={<GitHubIcon />}
              onClick={() => onExternalSignIn('github')}
              disabled={Boolean(externalProvider)}
            >
              {externalProvider === 'github' ? 'Redirecting…' : 'Continue with GitHub'}
            </Button>
          </Stack>
          <Divider flexItem>or continue with email</Divider>
          <TextField
            label="Email"
            type="email"
            value={email}
            autoComplete="email"
            onChange={(e) => setEmail(e.target.value)}
            required
            fullWidth
          />
          <TextField
            label="Password"
            type="password"
            value={password}
            autoComplete="current-password"
            onChange={(e) => setPassword(e.target.value)}
            required
            fullWidth
          />
          <Button type="submit" variant="contained" size="large" disabled={submitting}>
            {submitting ? 'Signing in…' : 'Sign in'}
          </Button>
        </Stack>
      </Box>
    </AuthShell>
  );
};

export default LoginPage;
