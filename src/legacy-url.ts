import {parseQuery} from 'vue-router'
import {chapters, designLessons, specPages} from '@/data/tour'
import {entries} from '@/data/api'
import {apiPath, specPath, tourPath} from '@/site'

export function legacyUrl(location: URL, base: string) {
    if (location.pathname !== base && location.pathname !== `${base}index.html`) return
    if (!location.hash.startsWith('#/')) return

    // Split fragment routing from the optional in-page anchor before decoding values.
    const old = new URL(`https://legacy.invalid${location.hash.slice(1).replace(/^\/+/, '/')}`)
    const [, section, rawStep = '', extra] = old.pathname.replace(/\/$/, '').split('/')
    const path = section?.toLowerCase()
    const params = parseQuery(old.search)
    if (extra !== undefined || (rawStep && path !== 'tour')) return base
    let page = '/'
    if (path === 'spec') {
        const file = specPages.find(item => item.file === params.page)
        page = file ? specPath(file.file) : '/spec/'
        old.searchParams.delete('page')
    } else if (path === 'api') {
        const entry = entries.find(item => item.id === params.symbol)
        page = entry ? apiPath(entry.id) : '/api/'
        old.searchParams.delete('symbol')
    } else if (path === 'roadmap') {
        page = '/roadmap/'
    } else if (path === 'tour') {
        const mode = params.mode === 'practice' ? 'practice' : 'design'
        const lessons = mode === 'practice' ? chapters : designLessons
        // Vue Router decoded the old step parameter and clamped numeric chapter links.
        let step = rawStep
        try {
            step = decodeURIComponent(rawStep)
        } catch { /* Keep the unknown step for the same first-chapter fallback. */ }
        const index = /^\d+$/.test(step) ? Math.max(0, Math.min(Number(step) - 1, lessons.length - 1)) : 0
        const lesson = lessons.find(item => item.id === step) ?? lessons[index]
        page = tourPath(lesson.id, mode)
        old.searchParams.delete('mode')
    }

    const query = new URLSearchParams(location.search)
    for (const [key, value] of old.searchParams) query.append(key, value)
    return `${base.slice(0, -1)}${page}${query.size ? `?${query}` : ''}${old.hash}`
}
