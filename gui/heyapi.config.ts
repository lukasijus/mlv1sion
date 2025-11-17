import { defineConfig } from "@hey-api/openapi-ts";
import { axiosClient } from "@hey-api/client-axios";

export default defineConfig({
  input: "http://localhost:9000/openapi.json",
  output: "src/api/generated",
  client: axiosClient(),
});
