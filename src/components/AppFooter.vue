<script setup lang="ts">
import {REPO} from '@/data/config'
import {source} from '@/data/tour'
</script>
<template>
  <footer>
    <div class="w"><span>Koven · {{ source.version }} · {{ source.revision.slice(0, 8) }}</span><span><a :href="REPO" target="_blank" rel="noopener">GitHub</a> · <RouterLink
        to="/tour">导览</RouterLink> · <RouterLink to="/spec">规范</RouterLink> · <a href="./koven-content-license.txt" target="_blank" rel="noopener">MIT</a></span></div>
  </footer>
</template>
<style scoped>
footer {
  padding: 36px 0;
  border-top: 1px solid var(--line);
  color: var(--mut);
  font-size: 14px
}

.w {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap
}

a:hover {
  color: var(--acc)
}
</style>
