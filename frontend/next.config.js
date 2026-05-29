/** @type {import('next').NextConfig} */
// Server-side proxy: the browser calls relative /api/* and /health/* (NEXT_PUBLIC_API_URL
// is empty), and the Next standalone server forwards them to the in-cluster backend.
// BACKEND_URL can override the default service address at runtime.
const BACKEND_URL = process.env.BACKEND_URL || 'http://dclaw-train-backend:8039';

const nextConfig = {
  output: 'standalone',
  skipTrailingSlashRedirect: true,
  async rewrites() {
    return [
      { source: '/api/:path*', destination: `${BACKEND_URL}/api/:path*` },
      { source: '/health/:path*', destination: `${BACKEND_URL}/health/:path*` },
    ];
  },
}

module.exports = nextConfig
