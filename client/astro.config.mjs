// @ts-check
import { defineConfig, envField } from 'astro/config';
import node from '@astrojs/node';

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

  output: 'server',

  adapter: node({
    mode: 'standalone',
  }),
});