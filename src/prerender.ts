import {createSSRApp} from 'vue'
import {renderToString, type SSRContext} from 'vue/server-renderer'
import {createMemoryHistory} from 'vue-router'
import App from './App.vue'
import {makeRouter, pages} from './router'
import {BASE} from './site'
import {reveal} from './directives/reveal'

export {pages}
export {SITE_URL} from './site'
export {REPO} from './data/config'

export async function renderPage(path: string) {
    const app = createSSRApp(App)
    const router = makeRouter(createMemoryHistory(BASE))
    app.use(router).directive('reveal', reveal)
    await router.push(path)
    await router.isReady()

    const context: SSRContext = {}
    const html = await renderToString(app, context)
    return {html, modules: context.modules as Set<string>}
}
