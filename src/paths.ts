/**
 * Prefixes an internal path with the deploy base, so links work both at the root of a domain and
 * under a subpath like GitHub Pages' /fununciation-landing/. Pass paths with a leading slash.
 */
export const withBase = (path: string) => `${import.meta.env.BASE_URL.replace(/\/$/, '')}${path}`;
