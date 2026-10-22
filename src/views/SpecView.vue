<script setup lang="ts">
import {computed} from 'vue'
import {useRoute} from 'vue-router'
import {specPages, source, sourceUrl} from '@/data/tour'
import MarkdownContent from '@/components/MarkdownContent.vue'
const route = useRoute()
const selected = computed(() => specPages.find(page => page.file === route.query.page))
</script>
<template>
  <main class="w reference-page">
    <template v-if="selected"><RouterLink class="back" to="/spec">← 全部规范</RouterLink><a class="source-link" :href="sourceUrl(selected.path)" target="_blank" rel="noopener">固定版本原文 ↗</a><MarkdownContent :text="selected.markdown" :path="selected.path"/></template>
    <template v-else><span class="pill">{{ source.version }} · LANGUAGE REFERENCE</span><h1>每条规则，都有出处。</h1><p class="sub">15 个领域页面，从词法到所有权。以下内容随语言版本同步；规范启用与编译器实现分别记录。</p><p class="source-link">来源提交 {{ source.revision.slice(0, 8) }} · <a :href="sourceUrl('docs/guide/README.md')" target="_blank" rel="noopener">在主仓库阅读 ↗</a></p><div class="grid"><RouterLink v-for="(page, i) in specPages" :key="page.file" :to="{path:'/spec',query:{page:page.file}}" class="item"><small>{{ String(i + 1).padStart(2, '0') }} ↗</small><h2>{{ page.title }}</h2><p>{{ page.description }}</p></RouterLink></div></template>
  </main>
</template>
<style scoped>
.reference-page{padding-top:48px;padding-bottom:80px}h1{font-size:clamp(30px,4vw,42px);letter-spacing:-.04em;margin:20px 0 14px}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:32px}.item{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:22px;transition:border-color .2s}.item:hover{border-color:var(--acc)}small{color:var(--acc);font:12px ui-monospace,monospace}.item h2{font-size:18px;margin:12px 0 8px}.item p{font-size:14px;color:var(--mut);margin:0}.source-link,.back{font-size:13px;color:var(--mut)}.back{display:inline-block;margin:0 24px 24px 0;color:var(--acc)}
@media(max-width:860px){.grid{grid-template-columns:1fr 1fr}}@media(max-width:520px){.grid{grid-template-columns:1fr}}
</style>
