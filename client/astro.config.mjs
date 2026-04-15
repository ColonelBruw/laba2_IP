// @ts-check
import { defineConfig, envField } from 'astro/config';

// https://astro.build/config
export default defineConfig({
    devToolbar: {
        enabled: false,
  },

  env: {
    schema: {
      API_HOST: envField.string({ context: 'client', access: 'public' }),
      API_PORT: envField.string({ context: 'client', access: 'public' }),
    },
  },
});
