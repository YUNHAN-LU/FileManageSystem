import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],

  server: {
    port: 3000,
    host: true, // needed for the Docker Container port mapping to work
    strictPort: true,
  },

  envPrefix: 'VITE_',

 
})
