import {mkdtemp, mkdir, readFile, rm, writeFile} from 'node:fs/promises'
import {join} from 'node:path'
import {pathToFileURL} from 'node:url'
import {build} from 'vite'

const output = 'dist'
// Keep the SSR bundle alongside the installed dependencies for Node resolution.
const temp = await mkdtemp(join('node_modules', '.koven-prerender-'))
const escape = value => value.replace(/[&<>"']/g, char => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
})[char])

try {
    await build({
        build: {
            ssr: 'src/prerender.ts',
            outDir: temp,
            emptyOutDir: true,
            copyPublicDir: false,
            ssrManifest: false,
        },
    })

    const {pages, renderPage, SITE_URL, REPO} = await import(pathToFileURL(join(temp, 'prerender.js')).href)
    const template = await readFile(join(output, 'index.html'), 'utf8')
    const headMarker = '<!--page-metadata-->'
    const appMarker = '<div id="app"></div>'
    for (const marker of [headMarker, appMarker]) {
        if (template.split(marker).length !== 2) throw new Error(`Expected one prerender marker: ${marker}`)
    }

    const manifestPath = join(output, '.vite', 'ssr-manifest.json')
    const manifest = JSON.parse(await readFile(manifestPath, 'utf8'))
    const image = new URL('og-image.png', SITE_URL).href
    const homepageSchema = {
        '@context': 'https://schema.org',
        '@graph': [
            {'@type': 'WebSite', name: 'Koven', alternateName: 'Koven Programming Language', url: SITE_URL.href},
            {
                '@type': 'SoftwareSourceCode',
                name: 'Koven',
                url: SITE_URL.href,
                codeRepository: REPO,
                license: ['LICENSE-MIT', 'LICENSE-APACHE'].map(file => `${REPO}/blob/main/${file}`),
            },
        ],
    }
    const paths = new Set()
    const urls = []

    for (const {path, meta: {seo}} of pages) {
        const segments = path.split('/').filter(Boolean).map(decodeURIComponent)
        if (segments.some(segment => !segment || /[/\\]/.test(segment) || segment === '.' || segment === '..')) {
            throw new Error(`Invalid static page path: ${path}`)
        }
        const directory = join(output, ...segments)
        if (paths.has(directory)) throw new Error(`Duplicate static page: ${path}`)
        paths.add(directory)
        urls.push(seo.url)

        const {html, modules} = await renderPage(path)
        const styles = new Set([...modules].flatMap(id => manifest[id] ?? []).filter(file => file.endsWith('.css')))
        const head = [
            `<title>${escape(seo.title)}</title>`,
            `<link rel="canonical" href="${escape(seo.url)}">`,
            '<meta name="robots" content="index, follow">',
            `<meta name="description" content="${escape(seo.description)}">`,
            `<meta property="og:url" content="${escape(seo.url)}">`,
            `<meta property="og:title" content="${escape(seo.title)}">`,
            `<meta property="og:description" content="${escape(seo.description)}">`,
            `<meta name="twitter:title" content="${escape(seo.title)}">`,
            `<meta name="twitter:description" content="${escape(seo.description)}">`,
            `<meta property="og:image" content="${escape(image)}">`,
            `<meta name="twitter:image" content="${escape(image)}">`,
            ...[...styles].map(file => `<link rel="stylesheet" href="${escape(file)}">`),
        ]
        if (path === '/') {
            const json = JSON.stringify(homepageSchema).replaceAll('<', '\\u003c')
            head.push(`<script type="application/ld+json">${json}</script>`)
        }
        const page = template
            .replace(headMarker, () => head.join('\n    '))
            .replace(appMarker, () => `<div id="app">${html}</div>`)
        await mkdir(directory, {recursive: true})
        await writeFile(join(directory, 'index.html'), page)
    }

    await writeFile(join(output, 'sitemap.xml'), [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        ...urls.map(url => `  <url><loc>${escape(url)}</loc></url>`),
        '</urlset>',
        '',
    ].join('\n'))
    await rm(manifestPath)
    console.log(`Prerendered ${paths.size} pages and generated sitemap.xml`)
} finally {
    await rm(temp, {recursive: true, force: true})
}
