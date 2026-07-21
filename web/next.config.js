/** @type {import('next').NextConfig} */
const nextConfig = {
  // Annotator needs Route Handlers + middleware (Upstash judgments).
  // Dataset pages remain static-friendly without `output: 'export'`.
  images: { unoptimized: true },
};
module.exports = nextConfig;
