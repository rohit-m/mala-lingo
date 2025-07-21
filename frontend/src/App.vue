<script setup>
import { RouterView } from 'vue-router'
import { useRouter } from 'vue-router'
import Button from './components/button.vue'

const router = useRouter()
</script>

<template>
  <div class="app">
    <div class="nav">
      <div class="button-container">
        <Button variant="outlined" label="Home" :onClick="() => {
          router.push('/')
        }" />
      </div>
    </div>
    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>



<style scoped>
body {
  background-color: #BEC4C6;
}
.nav {
  display: flex;
  justify-content: flex-start;
  padding: 10px;
}

.button-container {
  margin-right: 10px;
}
</style>
