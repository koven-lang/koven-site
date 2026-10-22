<script setup lang="ts">
import {ref} from 'vue'
import {useRoute} from 'vue-router'
import {REPO} from '@/data/config'

const nav = [{to: '/', label: '首页'}, {to: '/tour', label: '语言导览'}, {to: '/spec', label: '规范'}, {
  to: '/roadmap',
  label: '路线图'
}]
const route = useRoute()
const isOn = (to: string) => (to === '/' ? route.path === '/' : route.path.startsWith(to))
const dark = ref(document.documentElement.dataset.theme === 'dark')

function toggle() {
  dark.value = !dark.value
  const v = dark.value ? 'dark' : 'light'
  document.documentElement.dataset.theme = v
  try {
    localStorage.setItem('koven-theme', v)
  } catch { /* ignore */
  }
}
</script>
<template>
  <header>
    <div class="w">
      <RouterLink to="/" class="logo"><b>K</b>oven</RouterLink>
      <nav>
        <RouterLink v-for="n in nav" :key="n.to" :to="n.to" :class="{ on: isOn(n.to) }">{{ n.label }}</RouterLink>
      </nav>
      <button class="btn tg" aria-label="切换主题" @click="toggle">{{ dark ? '☀' : '☾' }}</button>
      <a class="btn p" :href="REPO" target="_blank" rel="noopener">GitHub ↗</a>
    </div>
  </header>
</template>
<style scoped>
header {
  position: sticky;
  top: 0;
  z-index: 9;
  background: color-mix(in srgb, var(--bg) 85%, transparent);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--line)
}

.w {
  display: flex;
  align-items: center;
  gap: 14px;
  height: 58px
}

.logo {
  font-weight: 800;
  font-size: 20px
}

.logo b {
  color: var(--acc);
  display: inline-block;
  transition: transform .4s
}

.logo:hover b {
  transform: rotate(-12deg) scale(1.2)
}

nav {
  display: flex;
  gap: 22px;
  flex: 1;
  margin-left: 14px
}

nav a {
  position: relative;
  color: var(--mut);
  font-size: 15px;
  padding: 4px 0
}

nav a::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: -2px;
  height: 2px;
  background: var(--acc);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform .3s
}

nav a:hover, nav a.on {
  color: var(--fg)
}

nav a:hover::after, nav a.on::after {
  transform: scaleX(1)
}

.tg {
  padding: 6px 12px
}

@media (max-width: 640px) {
  nav {
    gap: 10px;
    margin-left: 0
  }

  .w {
    gap: 8px;
    padding: 0 12px
  }

  .btn.p {
    display: none
  }
}
</style>

<style scoped>
@media(max-width:390px){nav a{font-size:12px}nav{gap:8px}.logo{font-size:18px}.tg{padding:5px 8px}.w{gap:7px}}
</style>
