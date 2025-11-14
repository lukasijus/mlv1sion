import { useQuery } from "@tanstack/react-query";
import { listProjects } from "../api/projects";
import type { Project } from "../api/types";

export function useProjects() {
  return useQuery<Project[], Error>({
    queryKey: ["projects"],
    queryFn: listProjects,
  });
}
