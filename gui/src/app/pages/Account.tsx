import React from 'react';
import { Avatar, Paper, Stack, Typography } from '@mui/material';
import { deepPurple } from '@mui/material/colors';
import { useAuth } from '../providers/authContext';

const AccountPage: React.FC = () => {
  const { accessToken } = useAuth();
  const initials = 'ML';

  return (
    <Stack spacing={3}>
      <div>
        <Typography variant="h4" component="h1">
          Account
        </Typography>
        <Typography color="text.secondary">
          Manage authentication details and tokens for API access.
        </Typography>
      </div>
      <Paper variant="outlined" sx={{ p: 3, display: 'flex', alignItems: 'center', gap: 2 }}>
        <Avatar sx={{ bgcolor: deepPurple[500], width: 56, height: 56 }}>{initials}</Avatar>
        <div>
          <Typography variant="subtitle1">demo@mlv1sion.dev</Typography>
          <Typography variant="body2" color="text.secondary">
            Token preview: {accessToken ? `${accessToken.slice(0, 8)}…` : 'Not authenticated'}
          </Typography>
        </div>
      </Paper>
    </Stack>
  );
};

export default AccountPage;
