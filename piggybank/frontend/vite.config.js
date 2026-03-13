import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), tailwindcss()],
  // Home Assistant Ingress requires relative base paths 
  // so the Vue App loads assets correctly regardless of the deeply nested path
  base: './',
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    proxy: {
      // Proxy API requests to backend during local development
      '/api': {
        target: 'http://127.0.0.1:8099',
        changeOrigin: true
      }
    }
  }
})
