import React, { useState } from 'react';
import { Alert, Box, Button, Divider, Link, Stack, TextField, Typography } from '@mui/material';
import GoogleIcon from '@mui/icons-material/Google';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import { useAuth } from '../providers/authContext';
import { getErrorMessage } from '../utils/errors';
import AuthShell from '../components/AuthShell';
import { getGoogleAuthorizationUrl } from '../utils/googleAuth';

const RegisterPage: React.FC = () => {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [googleSubmitting, setGoogleSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await register(email, password);
      navigate('/');
    } catch (err: unknown) {
      setError(getErrorMessage(err, 'Registration failed'));
    } finally {
      setSubmitting(false);
    }
  };

  const onGoogleSignUp = async () => {
    setError(null);
    setGoogleSubmitting(true);
    try {
      const url = await getGoogleAuthorizationUrl();
      window.location.href = url;
    } catch (err: unknown) {
      setGoogleSubmitting(false);
      setError(getErrorMessage(err, 'Unable to start Google sign-up'));
    }
  };

  return (
    <AuthShell
      title="Create an account"
      subtitle="Spin up workspaces for projects, datasets, and review jobs."
      footer={(
        <Typography variant="body2" color="text.secondary">
          Already have an account?{' '}
          <Link component={RouterLink} to="/login" underline="hover">
            Sign in
          </Link>
        </Typography>
      )}
    >
      <Box component="form" onSubmit={onSubmit}>
        <Stack spacing={2}>
          {error && <Alert severity="error">{error}</Alert>}
          <Button
            type="button"
            variant="outlined"
            size="large"
            startIcon={<GoogleIcon />}
            onClick={onGoogleSignUp}
            disabled={googleSubmitting}
          >
            {googleSubmitting ? 'Redirecting…' : 'Continue with Google'}
          </Button>
          <Divider flexItem>or</Divider>
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
            autoComplete="new-password"
            onChange={(e) => setPassword(e.target.value)}
            required
            fullWidth
          />
          <Button type="submit" variant="contained" size="large" disabled={submitting}>
            {submitting ? 'Creating…' : 'Create account'}
          </Button>
        </Stack>
      </Box>
    </AuthShell>
  );
};

export default RegisterPage;
