export const SITE_URL = new URL('https://koven-lang.github.io/koven-site/')
export const BASE = SITE_URL.pathname

export const specPath = (file: string) => `/spec/${encodeURIComponent(file.replace(/\.md$/, ''))}/`
export const apiPath = (id: string) => `/api/${id.split('/').map(encodeURIComponent).join('/')}/`
export const tourPath = (id: string, mode: 'design' | 'practice') =>
    mode === 'design' && id === 'overview' ? '/tour/' : `/tour/${mode === 'practice' ? 'practice/' : ''}${encodeURIComponent(id)}/`

export function pageMetadata(path: string, title: string, description: string) {
    return {title, description, url: new URL(path.slice(1), SITE_URL).href}
}
