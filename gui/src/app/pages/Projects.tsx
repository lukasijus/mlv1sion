import React from 'react';
import { Box, Button, Paper, Stack, Typography } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const ProjectsPage: React.FC = () => (
  <Stack spacing={3}>
    <Box>
      <Typography variant="h4" component="h1">
        Projects
      </Typography>
      <Typography color="text.secondary">
        Review the initiatives you and your team are driving.
      </Typography>
    </Box>
    <Paper variant="outlined" sx={{ p: 3, borderStyle: 'dashed' }}>
      <Stack spacing={1}>
        <Typography variant="subtitle1">No projects yet</Typography>
        <Typography variant="body2" color="text.secondary">
          Kick off a project to start labeling datasets and tracking reviews.
        </Typography>
        <Button component={RouterLink} to="/protected" variant="contained" sx={{ alignSelf: 'flex-start' }}>
          Create project
        </Button>
      </Stack>
    </Paper>
  </Stack>
);

export default ProjectsPage;
