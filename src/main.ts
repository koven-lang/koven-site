import {createApp, createSSRApp} from 'vue'
import {createWebHistory} from 'vue-router'
import App from './App.vue'
import {makeRouter} from './router'
import {legacyUrl} from './legacy-url'
import {reveal} from './directives/reveal'
import './style.css'

const base = import.meta.env.BASE_URL
const redirect = legacyUrl(new URL(location.href), base)
if (redirect) {
    history.replaceState(history.state, '', redirect)
} else if (location.pathname.endsWith('/index.html')) {
    history.replaceState(history.state, '', location.pathname.slice(0, -'index.html'.length) + location.search + location.hash)
}

const container = document.querySelector('#app')!
const router = makeRouter(createWebHistory(base))
router.afterEach(to => {
    const seo = to.meta.seo
    document.title = seo?.title ?? '页面不存在 · Koven'
    document.querySelector('link[rel="canonical"]')?.setAttribute('href', seo?.url ?? '')
    document.querySelector('meta[property="og:url"]')?.setAttribute('content', seo?.url ?? '')
    for (const selector of ['meta[property="og:title"]', 'meta[name="twitter:title"]']) {
        document.querySelector(selector)?.setAttribute('content', document.title)
    }
    for (const selector of ['meta[name="description"]', 'meta[property="og:description"]', 'meta[name="twitter:description"]']) {
        document.querySelector(selector)?.setAttribute('content', seo?.description ?? '')
    }
    const robots = document.querySelector('meta[name="robots"]')
    robots?.setAttribute('content', seo ? 'index, follow' : 'noindex')
})

const app = (container.hasChildNodes() && !redirect ? createSSRApp : createApp)(App)
app.use(router).directive('reveal', reveal)
router.isReady().then(() => app.mount(container))
