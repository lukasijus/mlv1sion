import React, { useMemo } from 'react';
import { Alert, Box, Button, Chip, Divider, Grid, Paper, Skeleton, Stack, Typography } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { useListProjectsApiV1ProjectsGet } from '../../api/gen/react-query';
import type { ProjectRead } from '../../api/gen/types';
import { getErrorMessage } from '../utils/errors';

const formatDate = (value?: string | null) => {
  if (!value) return 'Recently created';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return 'Unknown';
  return date.toLocaleString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
};

const ProjectCard: React.FC<{ project: ProjectRead }> = ({ project }) => (
  <Paper variant="outlined" sx={{ p: 3, height: '100%' }}>
    <Stack spacing={1.5} height="100%">
      <Stack direction="row" alignItems="flex-start" justifyContent="space-between" spacing={2}>
        <Box>
          <Typography variant="h6">{project.name}</Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
            {project.description || 'No description yet.'}
          </Typography>
        </Box>
        <Chip label={`ID ${project.id}`} size="small" variant="outlined" />
      </Stack>
      <Divider />
      <Stack direction="row" spacing={1} alignItems="center" sx={{ mt: 'auto' }}>
        <Typography variant="body2" color="text.secondary">
          Created
        </Typography>
        <Typography variant="body2">{formatDate(project.created_at)}</Typography>
      </Stack>
      <Chip label="Datasets coming soon" size="small" variant="outlined" sx={{ alignSelf: 'flex-start' }} />
    </Stack>
  </Paper>
);

const LoadingGrid: React.FC = () => (
  <Grid container spacing={3}>
    {Array.from({ length: 3 }).map((_, idx) => (
      <Grid item xs={12} md={6} lg={4} key={idx}>
        <Paper variant="outlined" sx={{ p: 3 }}>
          <Stack spacing={1.5}>
            <Skeleton variant="text" width="70%" height={32} />
            <Skeleton variant="text" width="90%" />
            <Divider />
            <Skeleton variant="rectangular" height={18} width="50%" />
          </Stack>
        </Paper>
      </Grid>
    ))}
  </Grid>
);

const ProjectsPage: React.FC = () => {
  const { data, isLoading, isError, error, refetch, isFetching } = useListProjectsApiV1ProjectsGet();
  const projects = useMemo(() => data ?? [], [data]);
  const showEmpty = !isLoading && projects.length === 0 && !isError;

  return (
    <Stack spacing={3}>
      <Stack direction="row" alignItems="center" justifyContent="space-between" spacing={2}>
        <Box>
          <Typography variant="h4" component="h1">
            Projects
          </Typography>
          <Typography color="text.secondary">
            Review the initiatives you and your team are driving.
          </Typography>
        </Box>
        <Button component={RouterLink} to="/protected" variant="contained" disabled>
          Create project (soon)
        </Button>
      </Stack>

      {isError && (
        <Alert severity="error" action={<Button onClick={() => refetch()}>Retry</Button>}>
          {getErrorMessage(error, 'Unable to load projects')}
        </Alert>
      )}

      {isLoading && <LoadingGrid />}

      {showEmpty && (
        <Paper variant="outlined" sx={{ p: 3, borderStyle: 'dashed' }}>
          <Stack spacing={1}>
            <Typography variant="subtitle1">No projects yet</Typography>
            <Typography variant="body2" color="text.secondary">
              Kick off a project to start labeling datasets and tracking reviews.
            </Typography>
            <Stack direction="row" spacing={1}>
              <Button component={RouterLink} to="/protected" variant="contained" disabled>
                Create project (soon)
              </Button>
              <Button onClick={() => refetch()} disabled={isFetching}>
                Refresh
              </Button>
            </Stack>
          </Stack>
        </Paper>
      )}

      {!showEmpty && !isLoading && !isError && (
        <Grid container spacing={3}>
          {projects.map((project) => (
            <Grid item xs={12} md={6} lg={4} key={project.id}>
              <ProjectCard project={project} />
            </Grid>
          ))}
        </Grid>
      )}
    </Stack>
  );
};

export default ProjectsPage;
