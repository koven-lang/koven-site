import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import {fileURLToPath, URL} from 'node:url'
import {BASE} from './src/site'

export default defineConfig({
    base: BASE,
    build: {ssrManifest: true},
    plugins: [vue()],
    resolve: {alias: {'@': fileURLToPath(new URL('./src', import.meta.url))}},
})
