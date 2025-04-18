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
          <div class="score">Matches: {{ matches.length }} / {{ wordMatchingData.length }}</div>
          <button @click="resetGame" class="reset-button">Reset Game</button>
        </div>

        <div class="columns-container">
          <!-- Malayalam Words Column -->
          <div class="word-column">
            <h2>Malayalam Words</h2>
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
            <h2>English Words</h2>
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
  } else {
    // Incorrect match - reset selections after a short delay
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
}

h1 {
  color: #2c3e50;
  margin-bottom: 1rem;
  text-align: center;
}

.game-instructions {
  text-align: center;
  color: #666;
  margin-bottom: 2rem;
}

.loading,
.no-data,
.error-message {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
}

.error-message {
  color: #dc3545;
  background-color: #f8d7da;
  border-radius: 4px;
}

.matching-game {
  position: relative;
}

.game-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.score {
  font-size: 1.2rem;
  font-weight: bold;
  color: #2c3e50;
}

.reset-button {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.reset-button:hover {
  background-color: #5a6268;
}

.columns-container {
  display: flex;
  gap: 2rem;
  justify-content: space-between;
}

.word-column {
  flex: 1;
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.word-column h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
  text-align: center;
  font-size: 1.5rem;
}

.word-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.word-item {
  background-color: white;
  padding: 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.word-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.word-item.selected {
  background-color: #e3f2fd;
  border: 2px solid #2196f3;
}

.word-item.matched {
  background-color: #e8f5e9;
  color: #2e7d32;
  cursor: default;
  opacity: 0.7;
}

.match-animation {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(46, 125, 50, 0.9);
  color: white;
  padding: 2rem;
  border-radius: 8px;
  z-index: 1000;
  animation: fadeInOut 1.5s ease-in-out;
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
}
</style>