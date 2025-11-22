import React, { useMemo, useRef, useState } from 'react';
import { ArrowBack, CloudUploadOutlined } from '@mui/icons-material';
import {
  Alert,
  Box,
  Button,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  Grid,
  Paper,
  Skeleton,
  Stack,
  TextField,
  Typography,
} from '@mui/material';
import { Link as RouterLink, useParams } from 'react-router-dom';
import {
  useListDatasetsApiV1DatasetsGet,
  useListProjectsApiV1ProjectsGet,
  usePresignAssetUploadApiV1AssetsPresignPost,
  useCreateDatasetApiV1DatasetsPost,
} from '../../api/gen/react-query';
import type { DatasetRead, ProjectRead } from '../../api/gen/types';
import { getErrorMessage } from '../utils/errors';

const DatasetCard: React.FC<{
  dataset: DatasetRead;
  onUpload: (files: FileList, datasetId: number) => Promise<void>;
  isUploading: boolean;
}> = ({ dataset, onUpload, isUploading }) => {
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const triggerUpload = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;
    event.target.value = '';
    await onUpload(files, dataset.id);
  };

  return (
    <Paper variant="outlined" sx={{ p: 3, height: '100%' }}>
      <Stack spacing={1.5} height="100%">
        <Stack direction="row" alignItems="flex-start" justifyContent="space-between" spacing={2}>
          <Box>
            <Typography variant="h6">{dataset.name}</Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
              {dataset.description || 'No description yet.'}
            </Typography>
          </Box>
          <Chip label={`ID ${dataset.id}`} size="small" variant="outlined" />
        </Stack>
        <Divider />
        <Stack direction="row" spacing={1} alignItems="center" sx={{ mt: 'auto' }}>
          <Chip label="Upload ready" size="small" color="success" variant="outlined" />
          <Button
            size="small"
            startIcon={<CloudUploadOutlined />}
            onClick={triggerUpload}
            disabled={isUploading}
          >
            {isUploading ? 'Uploading…' : 'Upload'}
          </Button>
          <input
            type="file"
            accept="*/*"
            multiple
            ref={fileInputRef}
            style={{ display: 'none' }}
            onChange={handleFileChange}
          />
        </Stack>
      </Stack>
    </Paper>
  );
};

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

const ProjectPage: React.FC = () => {
  const { projectId } = useParams<{ projectId: string }>();
  const numericProjectId = Number(projectId);
  const hasValidProjectId = Number.isFinite(numericProjectId) && numericProjectId > 0;

  const {
    data: projects,
    isLoading: isProjectsLoading,
    isError: isProjectsError,
  } = useListProjectsApiV1ProjectsGet();

  const project = useMemo<ProjectRead | undefined>(
    () => projects?.find((p) => p.id === numericProjectId),
    [projects, numericProjectId],
  );

  const {
    data: datasets,
    isLoading: isDatasetsLoading,
    isError: isDatasetsError,
    error: datasetsError,
    refetch: refetchDatasets,
    isFetching: isDatasetsFetching,
  } = useListDatasetsApiV1DatasetsGet(
    { project_id: hasValidProjectId ? numericProjectId : 0 },
    { query: { enabled: hasValidProjectId } },
  );

  const datasetList = useMemo(() => datasets ?? [], [datasets]);
  const showEmpty = hasValidProjectId && !isDatasetsLoading && !isDatasetsError && datasetList.length === 0;
  const presignMutation = usePresignAssetUploadApiV1AssetsPresignPost();
  const [uploadingDatasetIds, setUploadingDatasetIds] = useState<Record<number, boolean>>({});
  const [uploadMessage, setUploadMessage] = useState<string | null>(null);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [createOpen, setCreateOpen] = useState(false);
  const [createName, setCreateName] = useState('');
  const [createDescription, setCreateDescription] = useState('');
  const [createError, setCreateError] = useState<string | null>(null);
  const createDataset = useCreateDatasetApiV1DatasetsPost();

  const handleUpload = async (files: FileList, datasetId: number) => {
    setUploadMessage(null);
    setUploadError(null);
    setUploadingDatasetIds((prev) => ({ ...prev, [datasetId]: true }));
    try {
      const uploaded: string[] = [];
      let targetBucket: string | null = null;
      for (const file of Array.from(files)) {
        const presign = await presignMutation.mutateAsync({
          data: {
            dataset_id: datasetId,
            filename: file.name,
          },
        });
        targetBucket = presign.bucket;

        const response = await fetch(presign.upload_url, {
          method: 'PUT',
          body: file,
          headers: {
            'Content-Type': file.type || 'application/octet-stream',
          },
        });

        if (!response.ok) {
          throw new Error(`Upload failed for ${file.name} with status ${response.status}`);
        }

        uploaded.push(file.name);
      }

      if (uploaded.length > 0) {
        setUploadMessage(`Uploaded ${uploaded.join(', ')} to ${targetBucket ?? 'bucket'}`);
      }
    } catch (err: unknown) {
      setUploadError(getErrorMessage(err, 'Unable to upload file'));
    } finally {
      setUploadingDatasetIds((prev) => {
        const next = { ...prev };
        delete next[datasetId];
        return next;
      });
    }
  };

  const handleCreateDataset = async (e: React.FormEvent) => {
    e.preventDefault();
    setCreateError(null);
    if (!hasValidProjectId) {
      setCreateError('Invalid project');
      return;
    }
    try {
      await createDataset.mutateAsync({
        data: {
          project_id: numericProjectId,
          name: createName,
          description: createDescription || null,
        },
      });
      setCreateName('');
      setCreateDescription('');
      setCreateOpen(false);
      refetchDatasets();
    } catch (err: unknown) {
      setCreateError(getErrorMessage(err, 'Unable to create dataset'));
    }
  };

  if (!hasValidProjectId) {
    return (
      <Stack spacing={2}>
        <Button component={RouterLink} to="/projects" startIcon={<ArrowBack />}>
          Back to projects
        </Button>
        <Alert severity="error">The project you are looking for is not valid.</Alert>
      </Stack>
    );
  }

  return (
    <>
      <Stack spacing={3}>
        <Stack direction="row" alignItems="center" justifyContent="space-between" spacing={2}>
          <Box>
            <Button
              component={RouterLink}
              to="/projects"
              startIcon={<ArrowBack />}
              sx={{ mb: 1 }}
              variant="text"
            >
              Back to projects
            </Button>
            <Typography variant="h4" component="h1">
              {project?.name ?? `Project #${numericProjectId}`}
            </Typography>
            <Typography color="text.secondary">
              {project?.description
                ?? (isProjectsLoading ? 'Loading project details…' : 'No description yet.')}
            </Typography>
          </Box>
          <Stack direction="row" spacing={1} alignItems="center">
            <Button variant="contained" onClick={() => setCreateOpen(true)}>
              New dataset
            </Button>
            <Button onClick={() => refetchDatasets()} disabled={isDatasetsFetching}>
              Refresh
            </Button>
          </Stack>
        </Stack>

        <Alert severity="info">
          Upload files directly into a dataset using presigned uploads. Once asset listings land, they will show up under each dataset.
        </Alert>
        {uploadMessage && <Alert severity="success">{uploadMessage}</Alert>}
        {uploadError && <Alert severity="error">{uploadError}</Alert>}

        {isProjectsError && (
          <Alert severity="error">Unable to load projects. Datasets may be incomplete.</Alert>
        )}

        {!isProjectsLoading && !project && (
          <Alert severity="warning">
            We could not find this project. It might have been removed or you may not have access.
          </Alert>
        )}

        {isDatasetsError && (
          <Alert severity="error" action={<Button onClick={() => refetchDatasets()}>Retry</Button>}>
            {getErrorMessage(datasetsError, 'Unable to load datasets for this project')}
          </Alert>
        )}

        {isDatasetsLoading && <LoadingGrid />}

        {showEmpty && (
          <Paper variant="outlined" sx={{ p: 3, borderStyle: 'dashed' }}>
            <Stack spacing={1}>
              <Typography variant="subtitle1">No datasets yet</Typography>
              <Typography variant="body2" color="text.secondary">
                Create a dataset to start uploading files for this project.
              </Typography>
              <Stack direction="row" spacing={1}>
                <Button variant="contained" onClick={() => setCreateOpen(true)}>
                  New dataset
                </Button>
                <Button onClick={() => refetchDatasets()} disabled={isDatasetsFetching}>
                  Refresh
                </Button>
              </Stack>
            </Stack>
          </Paper>
        )}

        {!isDatasetsLoading && !isDatasetsError && datasetList.length > 0 && (
          <Grid container spacing={3}>
            {datasetList.map((dataset) => (
              <Grid item xs={12} md={6} lg={4} key={dataset.id}>
                <DatasetCard
                  dataset={dataset}
                  onUpload={handleUpload}
                  isUploading={Boolean(uploadingDatasetIds[dataset.id])}
                />
              </Grid>
            ))}
          </Grid>
        )}
      </Stack>

      <Dialog
        open={createOpen}
        onClose={() => {
          if (!createDataset.isPending) {
            setCreateOpen(false);
            setCreateError(null);
          }
        }}
        fullWidth
        maxWidth="sm"
      >
        <DialogTitle>New dataset</DialogTitle>
        <DialogContent>
          <Stack component="form" spacing={2} sx={{ pt: 1 }} onSubmit={handleCreateDataset}>
            {createError && <Alert severity="error">{createError}</Alert>}
            <TextField
              label="Name"
              value={createName}
              onChange={(e) => setCreateName(e.target.value)}
              required
              autoFocus
              disabled={createDataset.isPending}
            />
            <TextField
              label="Description"
              value={createDescription}
              multiline
              minRows={2}
              onChange={(e) => setCreateDescription(e.target.value)}
              disabled={createDataset.isPending}
            />
            <DialogActions sx={{ px: 0 }}>
              <Button onClick={() => setCreateOpen(false)} disabled={createDataset.isPending}>
                Cancel
              </Button>
              <Button
                type="submit"
                variant="contained"
                disabled={!createName.trim() || createDataset.isPending}
              >
                {createDataset.isPending ? 'Creating…' : 'Create'}
              </Button>
            </DialogActions>
          </Stack>
        </DialogContent>
      </Dialog>
    </>
  );
};

export default ProjectPage;
