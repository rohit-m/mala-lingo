<script setup>
import Button from '../ui/Button.vue'

const props = defineProps({
  score: {
    type: Object,
    default: () => ({ current: 0, total: 0 })
  },
  scoreIcon: {
    type: String,
    default: '🏆'
  },
  scoreLabel: {
    type: String,
    default: 'Score'
  },
  actions: {
    type: Array,
    default: () => []
    // Expected format: [{ label: 'Reset', onClick: fn, variant: 'outlined', icon: '🔄' }]
  }
})
</script>

<template>
  <div class="game-status">
    <div class="score-section">
      <span class="score-icon">{{ scoreIcon }}</span>
      <span class="score-text">
        {{ scoreLabel }}: {{ score.current }} / {{ score.total }}
      </span>
    </div>
    
    <div v-if="actions.length > 0" class="actions-section">
      <Button
        v-for="(action, index) in actions"
        :key="index"
        :label="action.icon ? `${action.icon} ${action.label}` : action.label"
        :variant="action.variant || 'outlined'"
        :onClick="action.onClick"
        class="action-button"
      />
    </div>
  </div>
</template>

<style scoped>
.game-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.score-section {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.score-icon {
  font-size: 1.5rem;
}

.score-text {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
}

.actions-section {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.action-button {
  min-width: auto;
  padding: 0.5rem 1rem;
}

@media (max-width: 768px) {
  .game-status {
    flex-direction: column;
    text-align: center;
  }
  
  .score-section {
    order: 1;
  }
  
  .actions-section {
    order: 2;
    justify-content: center;
  }
}
</style> 