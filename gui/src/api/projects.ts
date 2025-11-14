import type { Project } from "./types";
import { apiGet } from "./client";

// GET /api/v1/projects/
export async function listProjects(): Promise<Project[]> {
  return apiGet<Project[]>("/v1/projects/");
}
