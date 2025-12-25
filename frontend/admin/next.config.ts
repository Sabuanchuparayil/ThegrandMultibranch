import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  // Ensure path aliases work with Turbopack (Next.js 16+)
  // Turbopack is no longer experimental in Next.js 16, use top-level 'turbopack' instead
  turbopack: {
    resolveAlias: {
      '@': './',
    },
  },
};

export default nextConfig;
