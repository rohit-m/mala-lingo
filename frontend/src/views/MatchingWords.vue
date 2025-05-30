<template>
  <div class="matching-words-container">
    <h1>Word Matching Game</h1>
    <p class="game-instructions">Match each Malayalam word with its English equivalent. Click on a word from each column
      to make a match.</p>

    <div v-if="loading" class="loading">
      Loading word matching data...
    </div>

    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-else class="word-matching-content">
      <div v-if="wordMatchingData.length === 0" class="no-data">
        No word matching data available.
      </div>

      <div v-else class="matching-game">
        <div class="game-status">
          <div class="score">
            <span class="score-icon">🏆</span>
            <span class="score-text">Matches: {{ matches.length }} / {{ wordMatchingData.length }}</span>
          </div>
          <button @click="resetGame" class="reset-button">Reset Game</button>
        </div>

        <div class="columns-container">
          <!-- Malayalam Words Column -->
          <div class="word-column">
            <div class="word-list">
              <div v-for="item in malayalamWords" :key="item.id" class="word-item" :class="{
                'selected': selectedMalayalam?.id === item.id,
                'matched': isMatched(item.id)
              }" @click="selectMalayalam(item)">
                {{ item.malayalam_word }}
              </div>
            </div>
          </div>

          <!-- English Words Column -->
          <div class="word-column">
            <div class="word-list">
              <div v-for="item in englishWords" :key="item.id" class="word-item" :class="{
                'selected': selectedEnglish?.id === item.id,
                'matched': isMatched(item.id)
              }" @click="selectEnglish(item)">
                {{ item.english_word }}
              </div>
            </div>
          </div>
        </div>

        <!-- Match Animation -->
        <div v-if="showMatchAnimation" class="match-animation">
          <div class="match-content">
            <div class="match-icon">✓</div>
            <div class="match-text">Correct Match!</div>
          </div>
        </div>

        <!-- Incorrect Match Animation -->
        <div v-if="showIncorrectAnimation" class="incorrect-animation">
          <div class="incorrect-content">
            <div class="incorrect-icon">✗</div>
            <div class="incorrect-text">Try Again!</div>
          </div>
        </div>

        <!-- Completion Animation -->
        <div v-if="showCompletionAnimation" class="completion-animation">
          <div class="completion-content">
            <div class="completion-icon">🎉</div>
            <div class="completion-text">Congratulations!</div>
            <div class="completion-subtext">You've completed all matches!</div>
            <button @click="resetGame" class="go-again-button">Go Again</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'

const wordMatchingData = ref([])
const loading = ref(true)
const error = ref(null)
const selectedMalayalam = ref(null)
const selectedEnglish = ref(null)
const matches = ref([])
const showMatchAnimation = ref(false)
const showIncorrectAnimation = ref(false)
const showCompletionAnimation = ref(false)

// Computed properties to filter out matched words and shuffle them
const malayalamWords = computed(() => {
  const unmatchedWords = wordMatchingData.value
  return shuffleArray([...unmatchedWords])
})

const englishWords = computed(() => {
  const unmatchedWords = wordMatchingData.value
  return shuffleArray([...unmatchedWords])
})

// Helper function to shuffle an array using Fisher-Yates algorithm
const shuffleArray = (array) => {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
      ;[array[i], array[j]] = [array[j], array[i]]
  }
  return array
}

// Check if a word is already matched
const isMatched = (id) => {
  return matches.value.some(match => match.malayalamId === id || match.englishId === id)
}

// Check if all matches are completed
const checkCompletion = () => {
  if (matches.value.length === wordMatchingData.value.length) {
    // Show completion animation
    showCompletionAnimation.value = true
  }
}

// Select a Malayalam word
const selectMalayalam = (item) => {
  if (isMatched(item.id)) return

  selectedMalayalam.value = item
  // If an English word is already selected, check for a match
  if (selectedEnglish.value) {
    checkMatch()
  }
}

// Select an English word
const selectEnglish = (item) => {
  if (isMatched(item.id)) return

  selectedEnglish.value = item

  // If a Malayalam word is already selected, check for a match
  if (selectedMalayalam.value) {
    checkMatch()
  }
}

// Check if the selected words match
const checkMatch = () => {
  if (!selectedMalayalam.value || !selectedEnglish.value) return

  // Check if the selected words belong to the same item
  if (selectedMalayalam.value.id === selectedEnglish.value.id) {
    matches.value.push({
      malayalamId: selectedMalayalam.value.id,
      englishId: selectedEnglish.value.id
    })

    // Reset selections after animation completes
    setTimeout(() => {
      selectedMalayalam.value = null
      selectedEnglish.value = null
    }, 300) // Match the animation duration    

    // Check if all matches are completed
    checkCompletion()
  } else {
    // Incorrect match
    // Show incorrect animation
    showIncorrectAnimation.value = true
    setTimeout(() => {
      showIncorrectAnimation.value = false
    }, 1500)

    // Reset selections after a delay
    setTimeout(() => {
      selectedMalayalam.value = null
      selectedEnglish.value = null
    }, 500)
  }
}

// Reset the game
const resetGame = () => {
  matches.value = []
  selectedMalayalam.value = null
  selectedEnglish.value = null
  showCompletionAnimation.value = false

  // Fetch fresh data from the API
  fetchWordMatchingData()
}

const fetchWordMatchingData = async () => {
  loading.value = true
  error.value = null

  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/word-matching`)
    console.log(response.data)
    wordMatchingData.value = response.data.data
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to fetch word matching data'
    console.error('Error fetching word matching data:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchWordMatchingData()
})
</script>

<style scoped>
.matching-words-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  font-family: 'Nunito', 'Helvetica Neue', Arial, sans-serif;
}

h1 {
  color: var(--color-purple);
  margin-bottom: 1rem;
  text-align: center;
  font-size: 2.5rem;
  font-weight: 800;
}

.game-instructions {
  text-align: center;
  color: var(--color-text-light);
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.loading,
.no-data,
.error-message {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
}

.error-message {
  color: white;
  background-color: var(--color-primary-dark);
  border-radius: 12px;
  border: 2px solid var(--color-primary);
}

.matching-game {
  position: relative;
  background-color: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

.game-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid var(--color-border);
}

.score {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.2rem;
  font-weight: bold;
  color: var(--color-text);
}

.score-icon {
  font-size: 1.5rem;
}

.score-text {
  color: var(--color-text);
}

.reset-button {
  background-color: var(--color-yellow);
  color: #333;
  border: none;
  padding: 0.7rem 1.5rem;
  border-radius: 12px;
  cursor: pointer;
  transition: background-color 0.3s;
  font-weight: bold;
  font-size: 1rem;
  box-shadow: 0 2px 0 #d9c02c;
}

.reset-button:hover {
  background-color: #ffe85c;
}

.reset-button:active {
  transform: translateY(2px);
  box-shadow: 0 0 0 #d9c02c;
}

.columns-container {
  display: flex;
  gap: 2rem;
  justify-content: space-between;
}

.word-column {
  flex: 1;
  background-color: #f7f7f7;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.word-column h2 {
  color: var(--color-text);
  margin-bottom: 1.5rem;
  text-align: center;
  font-size: 1.5rem;
  font-weight: 700;
}

.word-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.word-item {
  background-color: white;
  padding: 1rem;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
  box-shadow: 0 2px 0 var(--color-border);
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-text);
  border: 2px solid transparent;
}

.word-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 0 var(--color-border);
}

.word-item.selected {
  background-color: #e5f6ff;
  border: 2px solid var(--color-blue);
  color: var(--color-blue);
}

.word-item.matched {
  background-color: #eefff9;
  color: var(--color-teal);
  cursor: default;
  opacity: 0.9;
  box-shadow: 0 2px 0 #b3e6cc;
  animation: subtleHighlight 1s ease-out;
}

@keyframes subtleHighlight {
  0% {
    background-color: var(--color-teal);
    color: white;
  }

  100% {
    background-color: #eefff9;
    color: var(--color-teal);
  }
}

.match-animation,
.incorrect-animation,
.completion-animation {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  padding: 2rem;
  border-radius: 16px;
  z-index: 1000;
  animation: fadeInOut 1.5s ease-in-out;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.match-animation {
  background-color: rgba(0, 245, 212, 0.9);
}

.incorrect-animation {
  background-color: rgba(241, 91, 181, 0.9);
}

.completion-animation {
  background-color: rgba(155, 93, 229, 0.9);
}

.match-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.match-icon {
  font-size: 3rem;
}

.match-text {
  font-size: 1.5rem;
  font-weight: bold;
}

.incorrect-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.incorrect-icon {
  font-size: 3rem;
}

.incorrect-text {
  font-size: 1.5rem;
  font-weight: bold;
}

.completion-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.completion-icon {
  font-size: 4rem;
}

.completion-text {
  font-size: 2rem;
  font-weight: bold;
}

.completion-subtext {
  font-size: 1.2rem;
}

.go-again-button {
  background-color: white;
  color: var(--color-purple);
  border: none;
  padding: 0.8rem 2rem;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: bold;
  font-size: 1.2rem;
  margin-top: 1rem;
  box-shadow: 0 2px 0 var(--color-border);
}

.go-again-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 0 var(--color-border);
  background-color: #f8f8f8;
}

.go-again-button:active {
  transform: translateY(1px);
  box-shadow: 0 0 0 var(--color-border);
}

@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.8);
  }

  100% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
  }
}

@keyframes fadeInOut {
  0% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.8);
  }

  20% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1.1);
  }

  80% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
  }

  100% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.8);
  }
}

@media (max-width: 768px) {
  .matching-words-container {
    padding: 1rem;
  }

  h1 {
    font-size: 1.8rem;
    margin-bottom: 0.5rem;
  }

  .game-instructions {
    font-size: 0.9rem;
    margin-bottom: 1rem;
  }

  .matching-game {
    padding: 1rem;
  }

  .game-status {
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
  }

  .score {
    font-size: 1rem;
  }

  .score-icon {
    font-size: 1.2rem;
  }

  .reset-button {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }

  .columns-container {
    gap: 1rem;
  }

  .word-column {
    padding: 0.8rem;
  }

  .word-list {
    gap: 0.5rem;
  }

  .word-item {
    padding: 0.7rem;
    font-size: 0.9rem;
  }

  .match-animation,
  .incorrect-animation,
  .completion-animation {
    padding: 1.5rem;
  }

  .match-icon,
  .incorrect-icon {
    font-size: 2.5rem;
  }

  .match-text,
  .incorrect-text {
    font-size: 1.2rem;
  }

  .completion-icon {
    font-size: 3rem;
  }

  .completion-text {
    font-size: 1.5rem;
  }

  .completion-subtext {
    font-size: 1rem;
  }

  .go-again-button {
    padding: 0.6rem 1.5rem;
    font-size: 1rem;
    margin-top: 0.5rem;
  }
}

/* Additional styles for very small screens (iPhone SE, etc.) */
@media (max-width: 375px) {
  .matching-words-container {
    padding: 0.5rem;
  }

  h1 {
    font-size: 1.5rem;
  }

  .game-instructions {
    font-size: 0.8rem;
  }

  .matching-game {
    padding: 0.8rem;
  }

  .word-item {
    padding: 0.6rem;
    font-size: 0.85rem;
  }

  .columns-container {
    gap: 0.5rem;
  }

  .word-column {
    padding: 0.6rem;
  }
}
</style>