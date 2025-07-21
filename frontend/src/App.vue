<script setup>
import { RouterView } from 'vue-router'
import AppNavigation from './components/layout/AppNavigation.vue'
</script>

<template>
  <div class="app">
    <AppNavigation />
    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>



<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  background-color: #f5f5f5;
}
</style>
