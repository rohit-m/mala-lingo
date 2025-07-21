<script setup>
import { useRouter } from 'vue-router'
import Button from '../ui/Button.vue'

const router = useRouter()
</script>

<template>
  <nav class="app-navigation">
    <div class="nav-content">
      <Button 
        variant="outlined" 
        label="Home" 
        :onClick="() => router.push('/')" 
      />
    </div>
  </nav>
</template>

<style scoped>
.app-navigation {
  display: flex;
  justify-content: flex-start;
  padding: 1rem;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e0e0e0;
}

.nav-content {
  display: flex;
  gap: 1rem;
  align-items: center;
}
</style> 