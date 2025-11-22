import React from 'react';
import { AccountCircleOutlined, FolderOutlined, HomeOutlined, SettingsOutlined } from '@mui/icons-material';
import { Box, Divider, List, ListItemButton, ListItemIcon, ListItemText, Stack, Typography } from '@mui/material';
import { Link, useLocation } from 'react-router-dom';

type NavItem = {
  label: string;
  path: string;
  icon: React.ReactElement;
};

const navItems: NavItem[] = [
  { label: 'Overview', path: '/', icon: <HomeOutlined /> },
  { label: 'Projects', path: '/projects', icon: <FolderOutlined /> },
  { label: 'Settings', path: '/settings', icon: <SettingsOutlined /> },
  { label: 'Account', path: '/account', icon: <AccountCircleOutlined /> },
];

const Sidebar: React.FC = () => {
  const location = useLocation();
  const isActive = (path: string) => {
    if (path === '/') return location.pathname === '/';
    return location.pathname === path || location.pathname.startsWith(`${path}/`);
  };

  return (
    <Box
      component="aside"
      sx={{
        width: 260,
        borderRight: (theme) => `1px solid ${theme.palette.divider}`,
        bgcolor: (theme) => (theme.palette.mode === 'light' ? 'grey.50' : 'background.paper'),
        p: 3,
        display: { xs: 'none', md: 'block' },
      }}
    >
      <Stack spacing={3}>
        <div>
          <Typography variant="h6">Workspace</Typography>
          <Typography variant="body2" color="text.secondary">
            Navigate through your labeling tools.
          </Typography>
        </div>
        <Divider />
        <List sx={{ p: 0 }}>
          {navItems.map((item) => (
            <ListItemButton
              key={item.path}
              component={Link}
              to={item.path}
              selected={isActive(item.path)}
              sx={{
                borderRadius: 2,
                mb: 1,
                '&.Mui-selected': {
                  bgcolor: 'primary.main',
                  color: 'primary.contrastText',
                  '& .MuiListItemIcon-root': {
                    color: 'inherit',
                  },
                },
              }}
            >
              <ListItemIcon sx={{ minWidth: 40, color: 'text.secondary' }}>{item.icon}</ListItemIcon>
              <ListItemText primary={item.label} />
            </ListItemButton>
          ))}
        </List>
      </Stack>
    </Box>
  );
};

export default Sidebar;
