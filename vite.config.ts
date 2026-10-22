import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import {fileURLToPath, URL} from 'node:url'

export default defineConfig({
    base: './', // 相对路径，配合 hash 路由可部署到任意静态托管（GitHub Pages 等）
    plugins: [vue()],
    resolve: {alias: {'@': fileURLToPath(new URL('./src', import.meta.url))}},
})
