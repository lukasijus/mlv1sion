import React, { useState } from 'react';
import { Alert, Box, Button, Container, Link, Stack, TextField, Typography } from '@mui/material';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import { useAuth } from '../providers/AuthProvider';

const RegisterPage: React.FC = () => {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await register(email, password);
      navigate('/');
    } catch (err: any) {
      const msg = typeof err === 'string' ? err : (err?.error?.detail ?? 'Registration failed');
      setError(msg);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 8 }}>
      <Typography variant="h4" component="h1" gutterBottom>Create account</Typography>
      <Box component="form" onSubmit={onSubmit}>
        <Stack spacing={2}>
          {error && <Alert severity="error">{error}</Alert>}
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
          <Button type="submit" variant="contained" disabled={submitting}>
            {submitting ? 'Creating…' : 'Create account'}
          </Button>
          <Typography variant="body2">
            Already have an account?{' '}
            <Link component={RouterLink} to="/login">Sign in</Link>
          </Typography>
        </Stack>
      </Box>
    </Container>
  );
};

export default RegisterPage;
