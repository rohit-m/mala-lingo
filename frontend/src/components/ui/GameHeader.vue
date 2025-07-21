<script setup>
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  instructions: {
    type: String,
    default: ''
  },
  showStats: {
    type: Boolean,
    default: false
  },
  stats: {
    type: Object,
    default: () => ({})
  }
})
</script>

<template>
  <div class="game-header">
    <h1 class="game-title">{{ title }}</h1>
    <p v-if="instructions" class="game-instructions">{{ instructions }}</p>
    
    <div v-if="showStats && Object.keys(stats).length > 0" class="game-stats">
      <div 
        v-for="(value, key) in stats" 
        :key="key" 
        class="stat-item"
      >
        <span class="stat-label">{{ key }}:</span>
        <span class="stat-value">{{ value }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.game-header {
  text-align: center;
  margin-bottom: 2rem;
  padding: 1rem;
}

.game-title {
  font-size: 2.5rem;
  color: #333;
  margin: 0 0 1rem 0;
  font-weight: bold;
}

.game-instructions {
  font-size: 1.1rem;
  color: #666;
  line-height: 1.6;
  margin: 0 0 1.5rem 0;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.game-stats {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
  margin-top: 1rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.5rem 1rem;
  background-color: #f5f5f5;
  border-radius: 8px;
  min-width: 80px;
}

.stat-label {
  font-size: 0.875rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: bold;
  color: #4CAF50;
}

@media (max-width: 768px) {
  .game-title {
    font-size: 2rem;
  }
  
  .game-instructions {
    font-size: 1rem;
  }
  
  .game-stats {
    gap: 1rem;
  }
}
</style> 