<script setup lang="ts">
import {computed, ref} from 'vue'
import CodeBlock from '@/components/CodeBlock.vue'
import {features, snippets, gettingStarted} from '@/data/home'
import {source, sourceUrl} from '@/data/tour'
const active = ref(0)
const current = computed(() => snippets[active.value])
</script>
<template>
  <main>
    <section class="hero">
      <div class="w hero-grid">
        <div>
          <span class="eyebrow">KOVEN / A LANGUAGE IN THE MAKING</span>
          <h1>熟悉的表达。<br><span>明确的所有权。</span></h1>
          <p class="lead">一门采用 Kotlin 风格语法的原生编译语言。<br class="desktop">从一段小程序开始，理解值如何传递、借用与释放。</p>
          <div class="cta"><RouterLink class="btn p" to="/tour">开始语言导览 <span>→</span></RouterLink><RouterLink class="text-link" to="/spec">阅读语言规范 ↗</RouterLink></div>
          <p class="version-note"><span class="dot"/> {{ source.version }} 设计基线 · 编译器持续实现中</p>
        </div>
        <div class="hero-example">
          <div class="example-heading"><span>一点代码，认识 Koven</span><span class="code-mark">{ k }</span></div>
          <div class="tabs" aria-label="示例选择"><button v-for="(snippet, i) in snippets" :key="snippet.id" :class="{on: active === i}" :aria-pressed="active === i" @click="active = i">{{ snippet.title }}</button></div>
          <CodeBlock :code="current.code" file="source.ko"/>
          <div class="example-footer"><span>源码取自主仓库 Tour</span><RouterLink :to="`/tour/${current.id}?mode=practice`">逐步阅读 →</RouterLink></div>
        </div>
      </div>
    </section>
    <section class="paths">
      <div class="w">
        <div class="section-heading"><span class="eyebrow">CHOOSE YOUR PATH</span><h2>带着问题，开始探索。</h2><p>先看语言的样子，再动手运行；遇到细节，回到规范。</p></div>
        <div class="cards"><RouterLink v-for="feature in features" :key="feature.number" class="path-card" :to="feature.to"><span class="number">{{ feature.number }} /</span><h3>{{ feature.title }}</h3><p>{{ feature.desc }}</p><span class="arrow">开始阅读 →</span></RouterLink></div>
      </div>
    </section>
    <section class="learning">
      <div class="w learning-grid"><div><span class="eyebrow">SMALL STEPS, REAL SOURCE</span><h2>设计可以向前。<br>示例需要有据可查。</h2><p>Tour 提供两条互相连接的路径：理解最新语言设计，以及运行主仓库维护的实例。每一页都能回到对应版本的源码。</p><RouterLink class="text-link" to="/tour/argv-word-frequency?mode=practice">试试 Map 词频统计 →</RouterLink></div><div class="learning-list"><RouterLink to="/tour/overview"><b>语言设计</b><span>{{ source.version }} Guide 摘选与新规则</span><i>01</i></RouterLink><RouterLink to="/tour/hello?mode=practice"><b>动手入门</b><span>源码、运行命令与预期输出</span><i>02</i></RouterLink><RouterLink to="/tour/reject-ownership?mode=practice"><b>读懂诊断</b><span>查看编译器应当拒绝的程序</span><i>03</i></RouterLink></div></div>
    </section>
    <section class="resources"><div class="w"><div class="section-heading"><span class="eyebrow">KEEP EXPLORING</span><h2>从这里，走得更远。</h2></div><div class="resource-grid"><a :href="gettingStarted" target="_blank" rel="noopener"><h3>安装与构建 ↗</h3><p>环境准备、编译器构建与命令行入口。</p></a><RouterLink to="/spec"><h3>语言参考 →</h3><p>15 个领域，查阅完整规则与相邻概念。</p></RouterLink><RouterLink to="/roadmap"><h3>实现路线图 →</h3><p>了解已交付基线、实施阶段与后续边界。</p></RouterLink><a :href="sourceUrl('docs/architecture/guide-conformance.md')" target="_blank" rel="noopener"><h3>实现覆盖 ↗</h3><p>从设计承诺追溯当前实现证据。</p></a></div></div></section>
    <section class="closing"><div class="w"><span class="eyebrow">LET’S WRITE SOME KOVEN</span><h2>从 Hello 开始。</h2><RouterLink class="btn p" to="/tour/hello?mode=practice">进入动手入门 →</RouterLink></div></section>
  </main>
</template>
<style scoped>
.hero{padding:86px 0 76px;background:radial-gradient(ellipse at 90% 15%,var(--acc2),transparent 65%)}.hero-grid{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center}.eyebrow{font:600 11px/1.5 ui-monospace,monospace;letter-spacing:.14em;color:var(--mut)}h1{font-size:clamp(38px,4.6vw,60px);line-height:1.22;letter-spacing:-.055em;margin:23px 0}h1 span{color:var(--acc)}.lead{font-size:17px;line-height:1.9;color:var(--mut);margin:0}.cta{display:flex;align-items:center;gap:22px;flex-wrap:wrap;margin:30px 0 22px}.cta .btn{padding:13px 22px}.cta .btn span{margin-left:25px}.text-link{font-size:14px;font-weight:650;color:var(--acc)}.version-note{display:flex;align-items:center;gap:8px;font-size:12px;color:var(--mut)}.dot{width:6px;height:6px;border-radius:50%;background:var(--acc)}.hero-example{min-width:0;background:var(--panel);border:1px solid var(--line);border-radius:20px;padding:24px;box-shadow:0 20px 60px -35px #55342055}.example-heading{display:flex;justify-content:space-between;align-items:center;font-size:13px}.code-mark{font:700 27px ui-monospace,monospace;color:var(--acc)}.tabs{display:flex;gap:6px;margin:20px 0 14px;flex-wrap:wrap}.tabs button{font:inherit;font-size:12px;padding:6px 11px;border:1px solid var(--line);border-radius:6px;background:transparent;color:var(--mut);cursor:pointer}.tabs .on{background:var(--acc2);color:var(--acc);border-color:var(--acc)}.example-footer{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-size:11px;color:var(--mut);margin-top:18px}.example-footer a{color:var(--acc)}.paths{border-top:1px solid var(--line)}.section-heading{margin-bottom:32px}.section-heading h2{margin:10px 0}.section-heading p{color:var(--mut);margin:0;font-size:15px}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}.path-card{display:block;border:1px solid var(--line);border-radius:14px;padding:28px;background:var(--panel);transition:border-color .2s,transform .2s}.path-card:hover{border-color:var(--acc);transform:translateY(-3px)}.number{font:13px ui-monospace,monospace;color:var(--acc)}h3{font-size:20px;letter-spacing:-.02em;margin:20px 0 12px}.path-card p{font-size:15px;color:var(--mut);margin:0 0 25px}.arrow{font-size:13px;color:var(--acc);font-weight:650}.learning{background:var(--panel);border-block:1px solid var(--line)}.learning-grid{display:grid;grid-template-columns:1fr 1fr;gap:100px;align-items:center}.learning h2{margin:14px 0 20px}.learning p{color:var(--mut);font-size:15px;max-width:430px}.learning-list a{display:grid;grid-template-columns:1fr auto;padding:22px 0;border-bottom:1px solid var(--line)}.learning-list b{font-size:18px}.learning-list span{font-size:13px;color:var(--mut);grid-column:1}.learning-list i{grid-row:1/3;grid-column:2;font:32px ui-monospace,monospace;color:var(--acc);align-self:center;opacity:.6}.resource-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:25px}.resource-grid h3{font-size:17px;margin:0 0 8px}.resource-grid p{font-size:14px;color:var(--mut);margin:0}.resource-grid a{padding-top:18px;border-top:1px solid var(--line)}.resource-grid a:hover{border-color:var(--acc)}.closing{text-align:center;background:var(--acc2)}.closing h2{margin:14px 0 25px}
@media(max-width:900px){.hero-grid{gap:32px}.learning-grid{gap:40px}.resource-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:760px){.hero{padding:42px 0}.hero-grid,.learning-grid{grid-template-columns:1fr;gap:36px}.cards{grid-template-columns:1fr}.hero-example{padding:18px}h1{font-size:44px}.desktop{display:none}.path-card{padding:24px}.path-card h3{margin:12px 0}.path-card p{margin-bottom:14px}.resource-grid{gap:24px}section{padding:46px 0}}
@media(max-width:380px){.cta{gap:16px}.resource-grid{grid-template-columns:1fr}h1{font-size:38px}}
</style>
