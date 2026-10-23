import {createRouter, createWebHashHistory} from 'vue-router'

export default createRouter({
    history: createWebHashHistory(),
    routes: [
        {path: '/', component: () => import('@/views/HomeView.vue')},
        {path: '/tour/:step?', component: () => import('@/views/TourView.vue')},
        {path: '/api', component: () => import('@/views/ApiView.vue')},
        {path: '/spec', component: () => import('@/views/SpecView.vue')},
        {path: '/roadmap', component: () => import('@/views/RoadmapView.vue')},
        {path: '/:pathMatch(.*)*', redirect: '/'},
    ],
    scrollBehavior: () => ({top: 0, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}),
})
