<script setup>
const props = defineProps({
  frontText: {
    type: String,
    required: true
  },
  backText: {
    type: String,
    required: true
  },
  isFlipped: {
    type: Boolean,
    default: false
  },
  onFlip: {
    type: Function,
    required: true
  },
  frontHint: {
    type: String,
    default: 'Click to reveal'
  },
  backHint: {
    type: String,
    default: 'Click to hide'
  }
})
</script>

<template>
  <div class="card-container">
    <div 
      class="card" 
      @click="onFlip" 
      :class="{ 'is-flipped': isFlipped }"
    >
      <div class="card-face card-front">
        <div class="word">{{ frontText }}</div>
        <div class="hint">{{ frontHint }}</div>
      </div>
      <div class="card-face card-back">
        <div class="word">{{ backText }}</div>
        <div class="hint">{{ backHint }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card-container {
  perspective: 1000px;
  width: 200px;
  height: 120px;
}

.card {
  position: relative;
  width: 100%;
  height: 100%;
  cursor: pointer;
  transform-style: preserve-3d;
  transition: transform 0.6s;
}

.card.is-flipped {
  transform: rotateY(180deg);
}

.card-face {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  padding: 1rem;
  box-sizing: border-box;
}

.card-front {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
}

.card-back {
  background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
  color: white;
  transform: rotateY(180deg);
}

.word {
  font-size: 1.2rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: 0.5rem;
  word-wrap: break-word;
  max-width: 100%;
}

.hint {
  font-size: 0.75rem;
  opacity: 0.8;
  text-align: center;
  font-style: italic;
}

.card:hover {
  transform: translateY(-2px);
}

.card.is-flipped:hover {
  transform: rotateY(180deg) translateY(-2px);
}

@media (max-width: 768px) {
  .card-container {
    width: 160px;
    height: 100px;
  }
  
  .word {
    font-size: 1rem;
  }
  
  .hint {
    font-size: 0.7rem;
  }
}
</style> 