<script setup lang="ts">
import {computed} from 'vue'
import MarkdownIt from 'markdown-it'
import {highlight, esc} from '@/utils/highlight'
import {sourceUrl} from '@/data/tour'
const props = defineProps<{text: string; path: string}>()
const html = computed(() => {
  const md = new MarkdownIt({html: false, linkify: false, highlight: (code, lang) =>
    ['koven', 'kotlin'].includes(lang) ? highlight(code) : esc(code)})
  const renderLink = md.renderer.rules.link_open || ((tokens, idx, options, _env, self) => self.renderToken(tokens, idx, options))
  md.renderer.rules.link_open = (tokens, idx, options, env, self) => {
    const token = tokens[idx]
    const href = String(token.attrGet('href') || '')
    // Resolve document-relative links against the exact imported source revision.
    if (!/^[a-z][a-z0-9+.-]*:/i.test(href) && !href.startsWith('//')) {
      token.attrSet('href', new URL(href, sourceUrl(props.path)).href)
    }
    token.attrSet('target', '_blank')
    token.attrSet('rel', 'noopener noreferrer')
    return renderLink(tokens, idx, options, env, self)
  }
  return md.render(props.text)
})
</script>
<template><div class="prose" v-html="html"/></template>
<style scoped>
.prose{overflow-wrap:anywhere;line-height:1.85;color:var(--fg)}
.prose :deep(p){margin:0 0 1em}.prose :deep(a){color:var(--acc);text-decoration:underline;text-underline-offset:3px}
.prose :deep(h2),.prose :deep(h3){font-size:1.15rem;margin:1.8em 0 .7em}.prose :deep(h4){font-size:1rem}
.prose :deep(ul),.prose :deep(ol){padding-left:1.4em}.prose :deep(li){margin:.5em 0}
.prose :deep(pre){overflow:auto;padding:20px;border-radius:12px;background:var(--code);color:var(--cfg);font-size:13px;line-height:1.7}
.prose :deep(code){font-family:ui-monospace,SFMono-Regular,Menlo,monospace}.prose :deep(:not(pre)>code){background:var(--acc2);padding:2px 4px;border-radius:4px;font-size:.88em}
.prose :deep(table){display:block;overflow:auto;width:100%;border-collapse:collapse;font-size:14px;margin:20px 0}
.prose :deep(th),.prose :deep(td){padding:10px;border:1px solid var(--line);min-width:110px;text-align:left}
.prose :deep(blockquote){border-left:3px solid var(--acc);margin:1em 0;padding-left:16px;color:var(--mut)}
</style>
