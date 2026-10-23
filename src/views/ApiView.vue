<script setup lang="ts">
import {computed, ref} from 'vue'
import {useRoute} from 'vue-router'
import data from '@/data/generated.json'

const route = useRoute()
const query = ref('')
const api = data.api
const entries = api.artifact.entries.map((entry, index) => ({...entry, links: api.links[index],
  id: `${entry.example}/${entry.file}/${entry.function}`}))
const selected = computed(() => entries.find(entry => entry.id === route.query.symbol))
const filtered = computed(() => entries.filter(entry =>
  `${entry.function} ${entry.example} ${entry.declaration.signature}`.toLowerCase().includes(query.value.trim().toLowerCase())))
</script>

<template>
  <main class="w api-page">
    <span class="pill">API · v{{ api.artifact.guideVersion }}</span>
    <h1>从声明，回到可运行的示例。</h1>
    <p class="sub">这里收录 {{ entries.length }} 个已验证教程函数，供查阅签名与参数；不是完整标准库参考。</p>
    <p class="boundary">API 来源：v{{ api.artifact.guideVersion }} · {{ api.source.revision.slice(0, 8) }}。本站规范与导览仍使用 {{ data.source.version }} 设计快照，版本分别标注。</p>
    <template v-if="route.query.symbol">
      <RouterLink class="back" to="/api">← 全部 API 示例</RouterLink>
      <article v-if="selected" class="detail">
        <h2>{{ selected.function }}</h2>
        <pre><code>{{ selected.declaration.signature }}</code></pre>
        <p>声明来自 <strong>{{ selected.example }}</strong> 教程。声明抽取仅解析语法；此处关联的完整教程另经过真实构建与运行验证，不表示浏览器执行过代码。</p>
        <h3>参数</h3>
        <dl v-if="selected.declaration.parameters.length">
          <template v-for="parameter in selected.declaration.parameters" :key="parameter.name">
            <dt><code>{{ parameter.name }}: {{ parameter.type }}</code></dt>
            <dd>{{ parameter.mode === 'default' ? '未写模式标记（默认共享借用）' : parameter.mode }}</dd>
          </template>
        </dl>
        <p v-else>无参数。</p>
        <div class="links">
          <a :href="selected.links.source" target="_blank" rel="noopener">查看固定版本声明 ↗</a>
          <a :href="selected.links.example" target="_blank" rel="noopener">阅读同版本完整示例 ↗</a>
        </div>
        <details><summary>验证输入身份</summary><p>编译器版本 {{ selected.compilerVersion }}；以下摘要标识已验证输入，不是版本兼容承诺。</p><p>源码 SHA256：<code>{{ selected.sourceSha256 }}</code></p><p>编译器 SHA256：<code>{{ api.artifact.compilerSha256 }}</code></p></details>
      </article>
      <p v-else role="status">未找到此 API 示例，请返回列表选择。</p>
    </template>
    <template v-else>
      <label for="api-search">搜索名称、签名或教程</label>
      <input id="api-search" v-model="query" type="search" placeholder="例如 inspect、String、borrowing"/>
      <p class="count" role="status">{{ filtered.length }} 个结果</p>
      <div class="grid">
        <RouterLink v-for="entry in filtered" :key="entry.id" class="item" :to="{path:'/api',query:{symbol:entry.id}}">
          <h2>{{ entry.function }} <span aria-hidden="true">↗</span></h2>
          <code>{{ entry.declaration.signature }}</code>
          <p>{{ entry.example }} · 已验证教程</p>
        </RouterLink>
      </div>
      <p v-if="!filtered.length">没有匹配的 API 示例，请尝试其他名称。</p>
    </template>
  </main>
</template>

<style scoped>
.api-page{padding-top:48px;padding-bottom:80px}h1{font-size:clamp(28px,4vw,42px);letter-spacing:-.04em;margin:20px 0 14px}.boundary,.count{color:var(--mut);font-size:14px}.boundary{margin-bottom:28px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.item,.detail{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:24px;min-width:0}.item:hover{border-color:var(--acc)}.item h2{font-size:22px;margin:0 0 14px}.item span,.links a,.back{color:var(--acc)}.item p{color:var(--mut);margin-bottom:0}label{display:block;margin-bottom:8px}input{width:100%;max-width:560px;border:1px solid var(--line);border-radius:8px;padding:12px;background:var(--panel);color:var(--fg);font:inherit}a:focus-visible,input:focus-visible,summary:focus-visible{outline:2px solid var(--acc);outline-offset:4px}pre,code{white-space:pre-wrap;overflow-wrap:anywhere}pre{padding:16px;background:var(--bg);border-radius:8px}.back{display:inline-block;margin-bottom:20px}.detail h2{margin-top:0}.links{display:flex;flex-wrap:wrap;gap:20px;margin:24px 0}dt{margin-top:12px}dd{color:var(--mut);margin:6px 0 0}details{border-top:1px solid var(--line);padding-top:18px;font-size:13px}summary{cursor:pointer}.detail p{line-height:1.8}
@media(max-width:640px){.grid{grid-template-columns:1fr}.item,.detail{padding:18px}.api-page{padding-top:28px}}
</style>
