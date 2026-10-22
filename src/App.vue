<script setup lang="ts">
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'
</script>
<template>
  <AppHeader/>
  <div>
    <RouterView v-slot="{ Component, route }">
      <Transition name="page" mode="out-in">
        <component :is="Component" :key="route.path.split('/')[1]"/>
      </Transition>
    </RouterView>
  </div>
  <AppFooter/>
</template>
