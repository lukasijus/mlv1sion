
import type { FC } from "react";
import {
  Box,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Typography,
} from "@mui/material";
import { useProjects } from "../../hooks/useProjects";

const ProjectsListPage: FC = () => {
  const { data, isLoading, error } = useProjects();

  if (isLoading) {
    return (
      <Box p={2}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={2}>
        <Typography color="error">
          Failed to load projects: {error.message}
        </Typography>
      </Box>
    );
  }

  const projects = data ?? [];

  return (
    <Box p={2}>
      <Typography variant="h5" gutterBottom>
        Projects
      </Typography>
      {projects.length === 0 ? (
        <Typography variant="body1">No projects yet.</Typography>
      ) : (
        <List>
          {projects.map((p) => (
            <ListItem key={p.id}>
              <ListItemText primary={p.name ?? `Project ${p.id}`} />
            </ListItem>
          ))}
        </List>
      )}
    </Box>
  );
};

export default ProjectsListPage;
