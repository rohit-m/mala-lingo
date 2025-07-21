<script setup>
const props = defineProps({
  text: {
    type: String,
    default: 'Loading...'
  },
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  }
})
</script>

<template>
  <div class="loading-container" :class="[`loading-${size}`]">
    <div class="spinner"></div>
    <p class="loading-text">{{ text }}</p>
  </div>
</template>

<style scoped>
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.loading-small { min-height: 100px; }
.loading-medium { min-height: 200px; }
.loading-large { min-height: 300px; }

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

.loading-small .spinner {
  width: 24px;
  height: 24px;
  border-width: 3px;
}

.loading-large .spinner {
  width: 56px;
  height: 56px;
  border-width: 5px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  margin: 0;
  color: #666;
  font-size: 1rem;
}

.loading-small .loading-text {
  font-size: 0.875rem;
}

.loading-large .loading-text {
  font-size: 1.125rem;
}
</style> 