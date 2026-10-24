// @ts-check
import { defineConfig } from 'astro/config';

// Static build: `npm run build` writes plain HTML/CSS to dist/. No server, no client framework.
// SITE_URL and BASE_PATH come from the GitHub Pages workflow (a project site lives under
// /<repo>/). Locally, and on a custom domain later, they're unset and the site sits at the root.
export default defineConfig({
  site: process.env.SITE_URL || undefined,
  base: process.env.BASE_PATH || '/',
  trailingSlash: 'ignore',
  devToolbar: { enabled: false },
});
