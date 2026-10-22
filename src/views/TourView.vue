<script setup lang="ts">
import {computed, onMounted, onUnmounted, ref, watch} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import CodeBlock from '@/components/CodeBlock.vue'
import MarkdownContent from '@/components/MarkdownContent.vue'
import {chapters, designLessons, source, sourceUrl} from '@/data/tour'
const route = useRoute(), router = useRouter()
const menuOpen = ref(false), caseIndex = ref(0)
const mode = computed(() => route.query.mode === 'practice' ? 'practice' : 'design')
const lessons = computed(() => mode.value === 'practice' ? chapters : designLessons)
const idx = computed(() => {
  const step = String(route.params.step || '')
  const byId = lessons.value.findIndex(ch => ch.id === step)
  if (byId >= 0) return byId
  const legacy = /^\d+$/.test(step) ? Number(step) - 1 : 0
  return Math.max(0, Math.min(legacy, lessons.value.length - 1))
})
const lesson = computed(() => lessons.value[idx.value])
const example = computed(() => mode.value === 'practice' ? chapters[idx.value].example : undefined)
const selectedCase = computed(() => example.value?.cases[caseIndex.value])
const link = (id: string, selectedMode = mode.value) => ({path: `/tour/${id}`, query: {mode: selectedMode}})
const go = (i: number) => { if (i >= 0 && i < lessons.value.length) router.push(link(lessons.value[i].id)) }
watch(() => route.fullPath, () => { menuOpen.value = false; caseIndex.value = 0 })
const onKey = (event: KeyboardEvent) => {
  const target = event.target as HTMLElement | null
  if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey || target?.closest('input,textarea,select,button,a,[contenteditable="true"],pre')) return
  if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
    event.preventDefault(); go(idx.value + (event.key === 'ArrowRight' ? 1 : -1))
  }
}
onMounted(() => window.addEventListener('keydown', onKey))
onUnmounted(() => window.removeEventListener('keydown', onKey))
</script>
<template>
  <div class="w tour">
    <aside>
      <div class="tour-brand">THE KOVEN TOUR <span>{{ source.version }}</span></div>
      <div class="mode-switch" aria-label="学习路径">
        <RouterLink :to="link('overview', 'design')" :class="{on: mode === 'design'}">语言设计</RouterLink>
        <RouterLink :to="link('hello', 'practice')" :class="{on: mode === 'practice'}">动手入门</RouterLink>
      </div>
      <button class="mobile-menu btn" @click="menuOpen = !menuOpen" :aria-expanded="menuOpen">章节目录 · {{ idx + 1 }} / {{ lessons.length }} ▾</button>
      <nav class="contents" :class="{expanded: menuOpen}" aria-label="Tour 章节">
        <RouterLink v-for="(item, i) in lessons" :key="item.id" :to="link(item.id)" :aria-current="i === idx ? 'step' : undefined" :class="{on: i === idx}">
          <span>{{ String(i + 1).padStart(2, '0') }}</span>{{ item.title }}
        </RouterLink>
      </nav>
      <RouterLink to="/spec" class="reference">查阅完整语言规范 ↗</RouterLink>
    </aside>
    <main class="lesson">
      <div class="eyebrow">{{ mode === 'design' ? '理解语言 / DESIGN' : '从源码开始 / PRACTICE' }} <span>{{ idx + 1 }} / {{ lessons.length }}</span></div>
      <div class="progress" role="progressbar" :aria-valuenow="idx + 1" :aria-valuemax="lessons.length" aria-valuemin="1" aria-label="章节位置"><span :style="{width: `${(idx + 1) / lessons.length * 100}%`}"/></div>
      <h1>{{ lesson.title }}</h1>
      <p v-if="mode === 'design'" class="notice">{{ source.version }} 设计说明 · 以下内容来自语言规范；规范启用不代表编译器已完整实现。可运行示例请进入「动手入门」。</p>
      <p v-else class="notice">{{ example?.status === 'planned' ? '计划示例 · 尚无执行合同，不计入验证通过。' : example?.status === 'diagnostic' ? '预期拒绝 · 查看主仓库记录的结构化诊断。' : example ? 'CLI 合同示例 · 这里展示预期输出，请在本地编译运行。' : '当前能力说明 · 请留意各入口与组合的支持边界。' }}</p>
      <MarkdownContent v-if="lesson.markdown" :text="lesson.markdown" :path="lesson.path"/>
      <template v-if="example">
        <p v-if="example.reason">{{ example.reason }}</p>
        <div v-for="file in example.files" :key="file.path" class="source-file"><CodeBlock :code="file.code" :file="file.path"/></div>
        <details v-if="example.manifest" class="run-details"><summary>工程配置 · project.toml</summary><CodeBlock :code="example.manifest" file="project.toml" plain/></details>
        <div v-if="example.commands.length" class="run-details"><h2>在本地运行</h2><p>按文件名保存上面的源码；每次构建使用新的输出路径。</p><CodeBlock :code="example.commands.join('\n')" file="terminal" plain/></div>
        <div v-if="example.cases.length" class="output">
          <div class="output-heading"><h2>预期输出</h2><label v-if="example.cases.length > 1">输入组合 <select v-model="caseIndex"><option v-for="(item, i) in example.cases" :key="i" :value="i">{{ i + 1 }} · {{ item.args.join(' ') || '无参数' }}</option></select></label></div>
          <CodeBlock v-if="selectedCase" :code="selectedCase.command" file="terminal" plain/>
          <pre>{{ selectedCase?.stdout || '（标准输出为空）' }}</pre>
          <pre v-if="selectedCase?.stderr">{{ selectedCase.stderr }}</pre>
          <small>预期退出码 {{ selectedCase?.exit }} · 来自主仓库合同，非浏览器执行结果</small>
        </div>
        <div v-if="example.diagnostics.length" class="diagnostics"><h2>预期诊断</h2><div v-for="(diagnostic, i) in example.diagnostics" :key="i"><code>{{ diagnostic.code }}</code><p>{{ diagnostic.message }}</p></div></div>
      </template>
      <a class="source-link" :href="sourceUrl(lesson.path)" target="_blank" rel="noopener">阅读主仓库原文 ↗ · {{ source.revision.slice(0, 8) }}</a>
      <div class="pager"><button class="btn" :disabled="idx === 0" @click="go(idx - 1)">← 上一章</button><RouterLink v-if="idx === lessons.length - 1" class="btn p" :to="mode === 'design' ? link('hello', 'practice') : '/spec'">{{ mode === 'design' ? '开始动手 →' : '继续查阅规范 →' }}</RouterLink><button v-else class="btn p" @click="go(idx + 1)">下一章 →</button></div>
    </main>
  </div>
</template>
<style scoped>
.tour{display:grid;grid-template-columns:250px minmax(0,1fr);gap:64px;padding-top:38px;padding-bottom:80px}
aside{position:sticky;top:88px;align-self:start;max-height:calc(100vh - 110px);overflow:auto}.tour-brand{font-size:12px;font-weight:800;letter-spacing:.08em;margin-bottom:20px}.tour-brand span{color:var(--acc);margin-left:8px}
.mode-switch{display:flex;background:var(--line);padding:4px;border-radius:10px;margin-bottom:20px}.mode-switch a{flex:1;text-align:center;padding:6px;font-size:14px;border-radius:7px}.mode-switch .on{background:var(--panel);font-weight:700}
.contents{display:flex;flex-direction:column;gap:3px}.contents a{display:flex;align-items:baseline;gap:12px;padding:8px 10px;font-size:14px;border-radius:7px;color:var(--mut)}.contents a span{font:12px ui-monospace,monospace;opacity:.65}.contents a:hover,.contents .on{color:var(--acc);background:var(--acc2)}.contents .on{font-weight:650}.reference{display:block;margin:22px 10px;color:var(--mut);font-size:13px}
.eyebrow{font-size:12px;letter-spacing:.08em;color:var(--mut);display:flex;justify-content:space-between}.progress{height:3px;background:var(--line);margin:12px 0 30px}.progress span{display:block;height:100%;background:var(--acc)}h1{font-size:clamp(28px,4vw,38px);letter-spacing:-.035em;line-height:1.3;margin:0 0 24px}h2{font-size:17px;margin:0 0 12px}.notice{font-size:14px;background:var(--acc2);border-left:3px solid var(--acc);padding:14px 18px;margin:0 0 28px;color:var(--fg)}
.source-file{margin:22px 0}.run-details{margin:26px 0}.run-details p{font-size:14px;color:var(--mut)}summary{cursor:pointer;margin:12px 0}.output{border:1px solid var(--line);border-radius:12px;padding:20px;margin:24px 0;background:var(--panel)}.output-heading{display:flex;justify-content:space-between;gap:12px;align-items:baseline;flex-wrap:wrap}.output label{font-size:12px;min-width:0;max-width:100%}select{max-width:100%;padding:6px;color:var(--fg);background:var(--bg);border:1px solid var(--line);border-radius:5px}.output pre{overflow:auto;max-height:350px}.output small{color:var(--mut)}.diagnostics{padding:20px;background:var(--badbg);border-radius:12px;margin:24px 0}.diagnostics code{color:var(--bad);font-weight:700}.diagnostics p{margin:4px 0 16px}.source-link{font-size:13px;color:var(--mut);text-decoration:underline}.pager{display:flex;justify-content:space-between;gap:12px;margin-top:36px;border-top:1px solid var(--line);padding-top:24px}.pager button:disabled{opacity:.4;cursor:default}.mobile-menu{display:none}.lesson{min-width:0}
@media(max-width:820px){.tour{grid-template-columns:1fr;gap:24px;padding-top:24px}aside{position:static;max-height:none}.contents{display:none}.contents.expanded{display:flex;max-height:320px;overflow:auto}.mobile-menu{display:block;width:100%;text-align:left}.reference{display:none}.mode-switch{margin-bottom:10px}.tour-brand{margin-bottom:12px}.output{padding:14px}}
</style>
