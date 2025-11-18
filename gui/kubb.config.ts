
// kubb.config.ts
import { defineConfig } from '@kubb/core';
import { pluginOas } from '@kubb/plugin-oas';
import { pluginTs } from '@kubb/plugin-ts';
import { pluginClient } from '@kubb/plugin-client';
import { pluginReactQuery } from '@kubb/plugin-react-query';
import { pluginZod } from '@kubb/plugin-zod';

export default defineConfig({
  // your repo root for Kubb
  root: '.',

  // point this to your spec
  input: {
    path: 'openapi.json',
  },

  // base output folder (everything goes under here)
  output: {
    path: './src/api/gen',
    clean: true, // wipe this folder before each generate
  },

  plugins: [
    // 1) Read + parse OpenAPI
    pluginOas({
      // keep validators OFF for now, given the trauma from Orval
      validate: false,
      // we don't need OAS -> JSON files
      generators: [],
    }),

    // 2) TypeScript types for schemas + operations
    pluginTs({
      output: {
        // => src/api/gen/types/*
        path: './types',
      },
    }),

    // 3) Low-level HTTP client
    pluginClient({
      output: {
        // => src/api/gen/client/*
        path: './client',
      },
      // simplest possible client definition
      clients: [
        {
          // you can switch this to 'axios' if you prefer
          client: 'fetch',
          // optional: configure baseUrl if you want
          // options: { baseUrl: 'http://localhost:8000' },
        },
      ],
    }),

    // 4) React Query hooks (TanStack Query v5)
    pluginReactQuery({
      output: {
        // => src/api/gen/react-query/*
        path: './react-query',
        // group files by first tag (like Orval tags-split)
        group: {
          type: 'tag',
        },
      },
      // defaults are usually fine; this is how you *could* tune:
      // query: {
      //   importPath: '@tanstack/react-query',
      // },
      // mutation: {
      //   importPath: '@tanstack/react-query',
      // },
    }),

    // 5) Zod runtime validators from the same schemas
    pluginZod({
      output: {
        // => src/api/gen/zod/*
        path: './zod',
      },
    }),
  ],
});
