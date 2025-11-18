import React from 'react';
import { Divider, Paper, Stack, Switch, Typography } from '@mui/material';

const SettingsPage: React.FC = () => (
  <Stack spacing={3}>
    <div>
      <Typography variant="h4" component="h1">
        Settings
      </Typography>
      <Typography color="text.secondary">
        Configure workspace preferences and notifications.
      </Typography>
    </div>
    <Paper variant="outlined" sx={{ p: 3 }}>
      <Typography variant="subtitle1" gutterBottom>
        Notifications
      </Typography>
      <Stack direction="row" alignItems="center" justifyContent="space-between">
        <Typography>Email me when a project needs review</Typography>
        <Switch defaultChecked />
      </Stack>
      <Divider sx={{ my: 2 }} />
      <Stack direction="row" alignItems="center" justifyContent="space-between">
        <Typography>Weekly summary</Typography>
        <Switch />
      </Stack>
    </Paper>
  </Stack>
);

export default SettingsPage;
