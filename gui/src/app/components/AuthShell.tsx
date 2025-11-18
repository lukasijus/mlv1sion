import React from 'react';
import { Box, Container, Paper, Stack, Typography } from '@mui/material';

type AuthShellProps = {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
};

const AuthShell: React.FC<AuthShellProps> = ({ title, subtitle, children, footer }) => (
  <Box
    sx={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: (theme) =>
        `linear-gradient(135deg, ${theme.palette.primary.main}0F, ${theme.palette.background.default})`,
      py: { xs: 6, sm: 10 },
      px: 2,
    }}
  >
    <Container maxWidth="sm">
      <Paper
        elevation={8}
        sx={{
          borderRadius: 4,
          px: { xs: 3, sm: 6 },
          py: { xs: 4, sm: 6 },
          backdropFilter: 'blur(5px)',
        }}
      >
        <Stack spacing={3}>
          <div>
            <Typography variant="h4" component="h1">
              {title}
            </Typography>
            {subtitle && (
              <Typography variant="body1" color="text.secondary" sx={{ mt: 1 }}>
                {subtitle}
              </Typography>
            )}
          </div>
          {children}
          {footer && <Box sx={{ pt: 1 }}>{footer}</Box>}
        </Stack>
      </Paper>
    </Container>
  </Box>
);

export default AuthShell;
