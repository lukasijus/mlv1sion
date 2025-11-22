import React from 'react';
import { AppBar, Box, Button, CssBaseline, Stack, Toolbar, Typography } from '@mui/material';
import { Link, Navigate, Outlet, Route, Routes, useNavigate } from 'react-router-dom';
import LoginPage from './pages/Login';
import RegisterPage from './pages/Register';
import ProjectsPage from './pages/Projects';
import SettingsPage from './pages/Settings';
import AccountPage from './pages/Account';
import OAuthCallbackPage from './pages/GoogleCallback';
import ProjectPage from './pages/Project';
import { useAuth } from './providers/authContext';
import Sidebar from './components/Sidebar';

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
      <AppBar position="sticky" elevation={0} color="inherit" sx={{ borderBottom: (theme) => `1px solid ${theme.palette.divider}` }}>
        <Toolbar>
          <Typography component={Link} to="/" variant="h6" sx={{ flexGrow: 1, textDecoration: 'none', color: 'inherit' }}>
            mlv1sion
          </Typography>
          {isAuthenticated ? (
            <Button color="primary" onClick={onLogout} variant="outlined">
              Logout
            </Button>
          ) : (
            <Button color="primary" onClick={() => navigate('/login')} variant="contained">
              Login
            </Button>
          )}
        </Toolbar>
      </AppBar>
      <Box sx={{ display: 'flex', minHeight: 'calc(100vh - 64px)' }}>
        {isAuthenticated && <Sidebar />}
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            p: { xs: 3, md: 5 },
            bgcolor: (theme) => (theme.palette.mode === 'light' ? 'grey.100' : 'background.default'),
          }}
        >
          <Outlet />
        </Box>
      </Box>
    </>
  );
};

const HomePage: React.FC = () => {
  const { isAuthenticated } = useAuth();
  return (
    <Stack spacing={2}>
      <Typography variant="h4" component="h1">
        Welcome to mlv1sion
      </Typography>
      <Typography variant="body1" color="text.secondary">
        {isAuthenticated ? 'Use the sidebar to jump into your projects, configure settings, or inspect account details.' : 'Sign in to access labeling projects, datasets, and review tasks.'}
      </Typography>
      <Box>
        {isAuthenticated ? (
          <Button component={Link} to="/projects" variant="contained">
            View projects
          </Button>
        ) : (
          <Button component={Link} to="/login" variant="contained">
            Sign in
          </Button>
        )}
      </Box>
    </Stack>
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
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/auth/:provider/callback" element={<OAuthCallbackPage />} />
      <Route path="/" element={<Layout />}>
        <Route index element={<HomePage />} />
        <Route
          path="projects"
          element={(
            <RequireAuth>
              <ProjectsPage />
            </RequireAuth>
          )}
        />
        <Route
          path="projects/:projectId"
          element={(
            <RequireAuth>
              <ProjectPage />
            </RequireAuth>
          )}
        />
        <Route
          path="settings"
          element={(
            <RequireAuth>
              <SettingsPage />
            </RequireAuth>
          )}
        />
        <Route
          path="account"
          element={(
            <RequireAuth>
              <AccountPage />
            </RequireAuth>
          )}
        />
        <Route
          path="protected"
          element={(
            <RequireAuth>
              <Typography>Protected content</Typography>
            </RequireAuth>
          )}
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

export default App;
