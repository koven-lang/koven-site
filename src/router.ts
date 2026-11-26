import {createRouter, createWebHashHistory} from 'vue-router'

const DEFAULT_TITLE = 'Koven — Compiled Systems Programming Language · 门户与语言导览'
const DEFAULT_DESCRIPTION =
    'Koven is a compiled systems programming language with Kotlin-inspired syntax, explicit ownership without a garbage collector, call-site borrow checking, and LLVM native code generation. 认识 Koven：从语言规范、可执行示例到实现路线图。'

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            path: '/',
            component: () => import('@/views/HomeView.vue'),
            meta: {
                title: DEFAULT_TITLE,
                description: DEFAULT_DESCRIPTION,
            },
        },
        {
            path: '/tour/:step?',
            component: () => import('@/views/TourView.vue'),
            meta: {
                title: 'Language Tour · Koven Programming Language',
                description: 'Walk through Koven executable examples covering syntax, ownership, call-site borrowing, collections, and deterministic cleanup.',
            },
        },
        {
            path: '/api',
            component: () => import('@/views/ApiView.vue'),
            meta: {
                title: 'Standard Library API · Koven Programming Language',
                description: 'Browse the Koven standard library API reference generated from pinned source contracts.',
            },
        },
        {
            path: '/spec',
            component: () => import('@/views/SpecView.vue'),
            meta: {
                title: 'Language Specification · Koven Programming Language',
                description: 'Read the Koven language specification covering lexical structure, types, ownership, borrowing, and deterministic drop.',
            },
        },
        {
            path: '/roadmap',
            component: () => import('@/views/RoadmapView.vue'),
            meta: {
                title: 'v1 Roadmap · Koven Programming Language',
                description: 'Track Koven compiler and ecosystem v1 milestones, implementation boundaries, and verification status.',
            },
        },
        {path: '/:pathMatch(.*)*', redirect: '/'},
    ],
    scrollBehavior: () => ({top: 0, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}),
})

router.afterEach((to) => {
    const title = typeof to.meta.title === 'string' ? to.meta.title : DEFAULT_TITLE
    const description = typeof to.meta.description === 'string' ? to.meta.description : DEFAULT_DESCRIPTION
    document.title = title
    const metaDesc = document.querySelector('meta[name="description"]')
    if (metaDesc) {
        metaDesc.setAttribute('content', description)
    }
})

export default router
