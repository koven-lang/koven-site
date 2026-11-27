import {h} from 'vue'
import {createRouter, type RouterHistory, type RouteMeta, type RouteRecordSingleView} from 'vue-router'
import {chapters, designLessons, specPages} from '@/data/tour'
import {entries} from '@/data/api'
import {apiPath, pageMetadata, specPath, tourPath} from '@/site'

declare module 'vue-router' {
    interface RouteMeta {
        seo?: ReturnType<typeof pageMetadata>
        tour?: {id: string, mode: 'design' | 'practice'}
        specFile?: string
        apiId?: string
    }
}

const tour = () => import('@/views/TourView.vue')
const spec = () => import('@/views/SpecView.vue')
const api = () => import('@/views/ApiView.vue')

function page(path: string, component: RouteRecordSingleView['component'], title: string, description: string, meta: RouteMeta = {}) {
    return {path, component, meta: {...meta, seo: pageMetadata(path, title, description)}}
}

function tourPage(lesson: {id: string, title: string}, mode: 'design' | 'practice') {
    return page(tourPath(lesson.id, mode), tour, `${lesson.title} · Koven ${mode === 'design' ? '语言设计' : '动手导览'}`,
        mode === 'design'
            ? `阅读 Koven 导览的「${lesson.title}」，查阅对应的语言规范与设计说明。`
            : `通过「${lesson.title}」了解 Koven 教程的源码、运行方式或当前实现边界。`,
        {tour: {id: lesson.id, mode}})
}

export const pages = [
    page('/', () => import('@/views/HomeView.vue'), 'Koven 编程语言 · 语言规范与导览',
        'Koven 是一门采用 Kotlin 风格语法的原生编译语言，采用显式所有权和调用点借用检查，通过 LLVM 生成原生代码。阅读语言规范、动手示例与编译器路线图。'),
    ...designLessons.map(lesson => tourPage(lesson, 'design')),
    ...chapters.map(chapter => tourPage(chapter, 'practice')),
    page('/spec/', spec, '语言规范 · Koven 编程语言', '查阅 Koven 的词法、类型、所有权、借用、资源析构和其他语言规则。'),
    ...specPages.map(item => page(specPath(item.file), spec, `${item.title} · Koven 语言规范`, item.description, {specFile: item.file})),
    page('/api/', api, '教程 API 参考 · Koven 编程语言', '查阅 Koven 已验证教程中的函数签名和参数，跳转到固定版本的声明与完整示例。'),
    ...entries.map(entry => page(apiPath(entry.id), api, `${entry.function} · ${entry.example}/${entry.file} · Koven 教程 API`,
        entry.declaration.signature, {apiId: entry.id})),
    page('/roadmap/', () => import('@/views/RoadmapView.vue'), 'v1 路线图 · Koven 编程语言', '跟踪 Koven 编译器和生态的 v1 里程碑、实现边界与验证状态。'),
]

export function makeRouter(history: RouterHistory) {
    return createRouter({
        history,
        routes: [...pages, {
            path: '/:pathMatch(.*)*',
            component: {render: () => h('main', {class: 'w'}, [h('h1', '页面不存在')])},
        }],
        scrollBehavior(to, _from, savedPosition) {
            return savedPosition ?? (to.hash ? {el: to.hash} : {top: 0, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'})
        },
    })
}
