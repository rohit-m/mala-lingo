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
  const unmatchedWords = wordMatchingData.value.filter(item => !isMatched(item.id))
  return shuffleArray([...unmatchedWords])
})

const englishWords = computed(() => {
  const unmatchedWords = wordMatchingData.value.filter(item => !isMatched(item.id))
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

// Trigger confetti animation with dynamic import
const triggerConfetti = async () => {
  try {
    // Dynamically import the confetti library
    const confettiModule = await import('canvas-confetti')
    const confetti = confettiModule.default || confettiModule

    // Fire confetti from the left side
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { x: 0, y: 0.6 }
    })

    // Fire confetti from the right side
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { x: 1, y: 0.6 }
    })

    // Fire confetti from the bottom
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { x: 0.5, y: 1 }
    })

    // Fire confetti from the top
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { x: 0.5, y: 0 }
    })

    // Fire a big burst of confetti from the center
    confetti({
      particleCount: 200,
      spread: 160,
      origin: { x: 0.5, y: 0.5 }
    })
  } catch (error) {
    console.error('Error loading confetti:', error)
    // Fallback: just show the completion animation without confetti
  }
}

// Check if all matches are completed
const checkCompletion = () => {
  if (matches.value.length === wordMatchingData.value.length) {
    // Show completion animation
    showCompletionAnimation.value = true

    // Trigger confetti
    triggerConfetti()

    // We no longer need to hide the completion animation after a timeout
    // since we now have a "Go Again" button
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
    // Correct match
    matches.value.push({
      malayalamId: selectedMalayalam.value.id,
      englishId: selectedEnglish.value.id
    })

    // Show match animation
    showMatchAnimation.value = true
    setTimeout(() => {
      showMatchAnimation.value = false
    }, 1500)

    // Reset selections
    selectedMalayalam.value = null
    selectedEnglish.value = null

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
  color: #58cc02;
  margin-bottom: 1rem;
  text-align: center;
  font-size: 2.5rem;
  font-weight: 800;
}

.game-instructions {
  text-align: center;
  color: #4b4b4b;
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
  color: #ff4b4b;
  background-color: #fff5f5;
  border-radius: 12px;
  border: 2px solid #ff4b4b;
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
  border-bottom: 2px solid #e5e5e5;
}

.score {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.2rem;
  font-weight: bold;
  color: #4b4b4b;
}

.score-icon {
  font-size: 1.5rem;
}

.score-text {
  color: #4b4b4b;
}

.reset-button {
  background-color: #ff9600;
  color: white;
  border: none;
  padding: 0.7rem 1.5rem;
  border-radius: 12px;
  cursor: pointer;
  transition: background-color 0.3s;
  font-weight: bold;
  font-size: 1rem;
  box-shadow: 0 2px 0 #cc7a00;
}

.reset-button:hover {
  background-color: #ffa31a;
}

.reset-button:active {
  transform: translateY(2px);
  box-shadow: 0 0 0 #cc7a00;
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
  color: #4b4b4b;
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
  box-shadow: 0 2px 0 #e5e5e5;
  font-size: 1.1rem;
  font-weight: 600;
  color: #4b4b4b;
  border: 2px solid transparent;
}

.word-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 0 #e5e5e5;
}

.word-item.selected {
  background-color: #e5f6ff;
  border: 2px solid #1cb0f6;
  color: #1cb0f6;
}

.word-item.matched {
  background-color: #d4f7e3;
  color: #58cc02;
  cursor: default;
  opacity: 0.9;
  box-shadow: 0 2px 0 #b3e6cc;
}

.match-animation {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(88, 204, 2, 0.9);
  color: white;
  padding: 2rem;
  border-radius: 16px;
  z-index: 1000;
  animation: fadeInOut 1.5s ease-in-out;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
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

.incorrect-animation {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(255, 75, 75, 0.9);
  color: white;
  padding: 2rem;
  border-radius: 16px;
  z-index: 1000;
  animation: fadeInOut 1.5s ease-in-out;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
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

.completion-animation {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(88, 204, 2, 0.9);
  color: white;
  padding: 2rem;
  border-radius: 16px;
  z-index: 1000;
  animation: fadeIn 0.5s ease-in-out;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
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
  color: #58cc02;
  border: none;
  padding: 0.8rem 2rem;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: bold;
  font-size: 1.2rem;
  margin-top: 1rem;
  box-shadow: 0 2px 0 #e5e5e5;
}

.go-again-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 0 #e5e5e5;
  background-color: #f8f8f8;
}

.go-again-button:active {
  transform: translateY(1px);
  box-shadow: 0 0 0 #e5e5e5;
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
  .columns-container {
    flex-direction: column;
  }

  .matching-game {
    padding: 1.5rem;
  }

  h1 {
    font-size: 2rem;
  }
}
</style>