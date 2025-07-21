<script setup>
import { onMounted, computed } from 'vue'
import { useWordData } from '../composables/useWordData'
import { useMatchingGame } from '../composables/useGameState'

// UI Components
import LoadingSpinner from '../components/ui/LoadingSpinner.vue'
import ErrorMessage from '../components/ui/ErrorMessage.vue'
import GameHeader from '../components/ui/GameHeader.vue'
import GameStatus from '../components/game/GameStatus.vue'
import WordCard from '../components/game/WordCard.vue'

// Composables
const { loading, error, wordMatchingData, fetchWordData, retryFetch, getShuffledWords } = useWordData()
const { 
  matches, 
  selectedMalayalam, 
  selectedEnglish, 
  gameScore,
  isGameComplete,
  isMatched, 
  selectMalayalam, 
  selectEnglish, 
  resetGame 
} = useMatchingGame()

// Computed properties
const shuffledWords = computed(() => getShuffledWords())
const malayalamWords = computed(() => shuffledWords.value.malayalam)
const englishWords = computed(() => shuffledWords.value.english)

// Update game score total when data loads
const updatedGameScore = computed(() => ({
  current: gameScore.value.current,
  total: wordMatchingData.value.length
}))

// Game actions for GameStatus component
const gameActions = computed(() => [
  {
    label: 'Reset Game',
    onClick: resetGame,
    variant: 'outlined',
    icon: '🔄'
  }
])

// Load data on mount
onMounted(() => {
  fetchWordData()
})
</script>

<template>
  <div class="matching-words-container">
    <GameHeader
      title="Word Matching Game"
      instructions="Match each Malayalam word with its English equivalent. Click on a word from each column to make a match."
    />

    <LoadingSpinner 
      v-if="loading" 
      text="Loading word matching data..." 
    />

    <ErrorMessage 
      v-else-if="error"
      :message="error"
      :showRetry="true"
      :onRetry="retryFetch"
    />

    <div v-else-if="wordMatchingData.length === 0" class="no-data">
      <ErrorMessage 
        message="No word matching data available."
        severity="info"
      />
    </div>

    <div v-else class="word-matching-content">
      <GameStatus
        :score="updatedGameScore"
        scoreIcon="🏆"
        scoreLabel="Matches"
        :actions="gameActions"
      />

      <div v-if="isGameComplete" class="completion-message">
        <h2>🎉 Congratulations!</h2>
        <p>You've matched all the words!</p>
      </div>

      <div class="columns-container">
        <!-- Malayalam Words Column -->
        <div class="word-column">
          <h3 class="column-title">Malayalam</h3>
          <div class="word-list">
            <WordCard
              v-for="item in malayalamWords"
              :key="`mal-${item.id}`"
              :word="item.malayalam_word"
              :isSelected="selectedMalayalam?.id === item.id"
              :isMatched="isMatched(item.id)"
              :onClick="() => selectMalayalam(item)"
              variant="malayalam"
            />
          </div>
        </div>

        <!-- English Words Column -->
        <div class="word-column">
          <h3 class="column-title">English</h3>
          <div class="word-list">
            <WordCard
              v-for="item in englishWords"
              :key="`eng-${item.id}`"
              :word="item.english_word"
              :isSelected="selectedEnglish?.id === item.id"
              :isMatched="isMatched(item.id)"
              :onClick="() => selectEnglish(item)"
              variant="english"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.matching-words-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.word-matching-content {
  margin-top: 2rem;
}

.no-data {
  text-align: center;
  margin: 2rem 0;
}

.completion-message {
  text-align: center;
  margin: 2rem 0;
  padding: 2rem;
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.completion-message h2 {
  margin: 0 0 1rem 0;
  font-size: 2rem;
}

.completion-message p {
  margin: 0;
  font-size: 1.2rem;
}

.columns-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-top: 2rem;
}

.word-column {
  background-color: #f8f9fa;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.column-title {
  text-align: center;
  margin: 0 0 1.5rem 0;
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e0e0e0;
}

.word-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

@media (max-width: 768px) {
  .matching-words-container {
    padding: 1rem;
  }
  
  .columns-container {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .word-column {
    padding: 1rem;
  }
  
  .column-title {
    font-size: 1.25rem;
  }
  
  .completion-message h2 {
    font-size: 1.5rem;
  }
  
  .completion-message p {
    font-size: 1rem;
  }
}
</style>