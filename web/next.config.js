/** @type {import('next').NextConfig} */
const nextConfig = {
  // Annotator needs Route Handlers (Upstash judgments); dashboard is public.
  // Dataset pages remain static-friendly without `output: 'export'`.
  // /results client-redirects to /#leaderboard (see app/results/page.tsx).
  images: { unoptimized: true },
};
module.exports = nextConfig;
