/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/processed/:path*',
        destination: 'http://localhost:8000/processed/:path*',
      },
      {
        source: '/search',
        destination: 'http://localhost:8000/search',
      }
    ];
  },
};

module.exports = nextConfig;
