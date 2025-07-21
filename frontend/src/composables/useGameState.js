import { ref, computed, reactive } from 'vue'

export function useMatchingGame() {
  const matches = ref([])
  const selectedMalayalam = ref(null)
  const selectedEnglish = ref(null)

  const isMatched = (itemId) => {
    return matches.value.some(match => match.id === itemId)
  }

  const selectMalayalam = (item) => {
    if (isMatched(item.id)) return
    selectedMalayalam.value = item
    checkForMatch()
  }

  const selectEnglish = (item) => {
    if (isMatched(item.id)) return
    selectedEnglish.value = item
    checkForMatch()
  }

  const checkForMatch = () => {
    if (selectedMalayalam.value && selectedEnglish.value) {
      if (selectedMalayalam.value.id === selectedEnglish.value.id) {
        // Correct match
        matches.value.push(selectedMalayalam.value)
      }
      // Reset selections regardless of match result
      selectedMalayalam.value = null
      selectedEnglish.value = null
    }
  }

  const resetGame = () => {
    matches.value = []
    selectedMalayalam.value = null
    selectedEnglish.value = null
  }

  const gameScore = computed(() => ({
    current: matches.value.length,
    total: 0 // Will be set by the component based on available data
  }))

  const isGameComplete = computed(() => {
    return gameScore.value.total > 0 && gameScore.value.current === gameScore.value.total
  })

  return {
    // State
    matches,
    selectedMalayalam,
    selectedEnglish,
    
    // Computed
    gameScore,
    isGameComplete,
    
    // Methods
    isMatched,
    selectMalayalam,
    selectEnglish,
    resetGame
  }
}

export function useFlipCardGame() {
  const flippedCards = ref({})

  const flipCard = (cardId) => {
    flippedCards.value[cardId] = !flippedCards.value[cardId]
  }

  const resetCards = () => {
    flippedCards.value = {}
  }

  const isCardFlipped = (cardId) => {
    return !!flippedCards.value[cardId]
  }

  const flippedCount = computed(() => {
    return Object.values(flippedCards.value).filter(Boolean).length
  })

  return {
    // State
    flippedCards,
    
    // Computed
    flippedCount,
    
    // Methods
    flipCard,
    resetCards,
    isCardFlipped
  }
} 