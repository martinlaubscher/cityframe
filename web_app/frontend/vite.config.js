import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
})

// import { defineConfig } from 'vite'
// import react from '@vitejs/plugin-react'
// import path from 'path'

// export default defineConfig({
//   plugins: [react()],
//   build: {
//     rollupOptions: {
//       input: path.resolve(__dirname, 'public/index.html')  // path is relative to the directory of vite.config.js
//     }
//   }
// })

