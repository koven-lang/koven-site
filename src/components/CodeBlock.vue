<script setup lang="ts">
import {computed} from 'vue'
import {esc, highlight} from '@/utils/highlight'

const props = defineProps<{ code: string; file?: string; animate?: boolean; plain?: boolean }>()
const lines = computed(() => (props.plain ? esc(props.code) : highlight(props.code)).split('\n'))
</script>
<template>
  <div class="win">
    <div class="bar"><i/><i/><i/><span v-if="file">{{ file }}</span></div>
    <pre><code><span v-for="(l, i) in lines" :key="i" class="ln" :class="{ anim: animate }" :style="{ '--i': i }"
                     v-html="l || '&nbsp;'"/></code></pre>
  </div>
</template>
<style scoped>
.win {
  background: var(--code);
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid var(--line);
  box-shadow: 0 20px 50px -24px rgba(0, 0, 0, .5);
  text-align: left
}

.bar {
  display: flex;
  gap: 6px;
  align-items: center;
  padding: 10px 14px;
  background: rgba(255, 255, 255, .05);
  color: #9a948f;
  font-size: 12px
}

.bar i {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #44403c
}

.bar span {
  margin-left: 8px
}

pre {
  margin: 0;
  padding: 16px 18px;
  overflow-x: auto;
  color: var(--cfg);
  font: 13.5px/1.65 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace
}

.ln {
  display: block;
  white-space: pre
}

.ln.anim {
  animation: lineIn .5s both;
  animation-delay: calc(var(--i) * 80ms + 200ms)
}

@keyframes lineIn {
  from {
    opacity: 0;
    transform: translateX(-10px)
  }
}
</style>
