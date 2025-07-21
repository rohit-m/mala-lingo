<script setup>
const props = defineProps({
  word: {
    type: String,
    required: true
  },
  isSelected: {
    type: Boolean,
    default: false
  },
  isMatched: {
    type: Boolean,
    default: false
  },
  onClick: {
    type: Function,
    required: true
  },
  variant: {
    type: String,
    default: 'malayalam',
    validator: (value) => ['malayalam', 'english'].includes(value)
  }
})
</script>

<template>
  <div 
    class="word-card" 
    :class="[
      `word-card--${variant}`,
      { 
        'word-card--selected': isSelected,
        'word-card--matched': isMatched,
        'word-card--clickable': !isMatched
      }
    ]"
    @click="!isMatched && onClick()"
  >
    <span class="word-text">{{ word }}</span>
  </div>
</template>

<style scoped>
.word-card {
  padding: 1rem 1.5rem;
  border-radius: 8px;
  margin: 0.5rem 0;
  text-align: center;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  font-size: 1.1rem;
  font-weight: 500;
  min-height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.word-card--clickable {
  cursor: pointer;
}

.word-card--clickable:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* Malayalam word styling */
.word-card--malayalam {
  background-color: #e8f5e8;
  color: #2e7d32;
}

.word-card--malayalam.word-card--selected {
  background-color: #4CAF50;
  color: white;
  border-color: #45a049;
}

.word-card--malayalam.word-card--matched {
  background-color: #c8e6c9;
  color: #1b5e20;
  opacity: 0.7;
  cursor: not-allowed;
}

/* English word styling */
.word-card--english {
  background-color: #e3f2fd;
  color: #1976d2;
}

.word-card--english.word-card--selected {
  background-color: #2196F3;
  color: white;
  border-color: #1976d2;
}

.word-card--english.word-card--matched {
  background-color: #bbdefb;
  color: #0d47a1;
  opacity: 0.7;
  cursor: not-allowed;
}

.word-text {
  word-wrap: break-word;
  max-width: 100%;
}

/* Matched indicator */
.word-card--matched::after {
  content: '✓';
  position: absolute;
  top: 4px;
  right: 8px;
  font-size: 1.2rem;
  color: #4CAF50;
  font-weight: bold;
}

@media (max-width: 768px) {
  .word-card {
    padding: 0.75rem 1rem;
    font-size: 1rem;
    min-height: 45px;
  }
  
  .word-card--matched::after {
    font-size: 1rem;
    top: 2px;
    right: 6px;
  }
}
</style> 