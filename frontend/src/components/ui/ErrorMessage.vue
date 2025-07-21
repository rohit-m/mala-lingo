<script setup>
const props = defineProps({
  message: {
    type: String,
    required: true
  },
  severity: {
    type: String,
    default: 'error',
    validator: (value) => ['error', 'warning', 'info'].includes(value)
  },
  showRetry: {
    type: Boolean,
    default: false
  },
  onRetry: {
    type: Function,
    default: null
  }
})

const getIcon = () => {
  switch (props.severity) {
    case 'error': return '❌'
    case 'warning': return '⚠️'
    case 'info': return 'ℹ️'
    default: return '❌'
  }
}
</script>

<template>
  <div class="error-container" :class="[`error-${severity}`]">
    <div class="error-content">
      <span class="error-icon">{{ getIcon() }}</span>
      <p class="error-message">{{ message }}</p>
    </div>
    <button 
      v-if="showRetry && onRetry" 
      @click="onRetry"
      class="retry-button"
    >
      🔄 Try Again
    </button>
  </div>
</template>

<style scoped>
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  border-radius: 8px;
  margin: 1rem 0;
  min-height: 120px;
  justify-content: center;
}

.error-error {
  background-color: #ffebee;
  border: 1px solid #ffcdd2;
  color: #c62828;
}

.error-warning {
  background-color: #fff8e1;
  border: 1px solid #ffecb3;
  color: #f57c00;
}

.error-info {
  background-color: #e3f2fd;
  border: 1px solid #bbdefb;
  color: #1976d2;
}

.error-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.error-icon {
  font-size: 1.5rem;
}

.error-message {
  margin: 0;
  font-size: 1rem;
  text-align: center;
  line-height: 1.5;
}

.retry-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: background-color 0.3s;
}

.retry-button:hover {
  background-color: #45a049;
}
</style> 