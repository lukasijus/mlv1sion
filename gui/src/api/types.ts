// TODO: Shared API types for the frontend

export interface User {
  id: string;
  name: string;
  email?: string;
  roles?: string[];
  tenantId?: string;
}

export interface Project {
  id: string;
  name: string;
  description?: string;
  createdAt?: string;
}

export interface Dataset {
  id: string;
  projectId: string;
  name: string;
  description?: string;
  createdAt?: string;
}

export interface Asset {
  id: string;
  datasetId: string;
  filename: string;
  url?: string;
  status?: 'PENDING' | 'READY' | 'DELETING';
}

export interface Job {
  id: string;
  type: string;
  status: 'QUEUED' | 'RUNNING' | 'FAILED' | 'COMPLETED';
  createdAt?: string;
  updatedAt?: string;
}
