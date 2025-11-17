import React from 'react';
import { AppBar, Box, Button, Container, CssBaseline, Toolbar, Typography } from '@mui/material';
import { Link, Navigate, Outlet, Route, Routes, useNavigate } from 'react-router-dom';
import LoginPage from './pages/Login';
import RegisterPage from './pages/Register';
import { useAuth } from './providers/AuthProvider';

const Layout: React.FC = () => {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const onLogout = () => {
    logout();
    navigate('/login');
  };
  return (
    <>
      <CssBaseline />
      <AppBar position="static">
        <Toolbar>
          <Typography component={Link} to="/" variant="h6" sx={{ flexGrow: 1, textDecoration: 'none', color: 'inherit' }}>
            App
          </Typography>
          {isAuthenticated ? (
            <Button color="inherit" onClick={onLogout}>Logout</Button>
          ) : (
            <Button color="inherit" onClick={() => navigate('/login')}>Login</Button>
          )}
        </Toolbar>
      </AppBar>
      <Container sx={{ mt: 3 }}>
        <Outlet />
      </Container>
    </>
  );
};

const HomePage: React.FC = () => {
  const { isAuthenticated } = useAuth();
  return (
    <Box>
      <Typography variant="h5" gutterBottom>Welcome</Typography>
      <Typography variant="body1">
        {isAuthenticated ? 'You are logged in.' : 'Please sign in to continue.'}
      </Typography>
    </Box>
  );
};

const RequireAuth: React.FC<{ children: React.ReactElement }> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return children;
};

const App: React.FC = () => {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<HomePage />} />
        <Route path="login" element={<LoginPage />} />
        <Route path="register" element={<RegisterPage />} />
        <Route
          path="protected"
          element={
            <RequireAuth>
              <Typography>Protected content</Typography>
            </RequireAuth>
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
};

export default App;
