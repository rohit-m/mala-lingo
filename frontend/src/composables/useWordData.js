import { ref, reactive } from 'vue'

export function useWordData() {
  const loading = ref(false)
  const error = ref(null)
  const wordMatchingData = ref([])

  const fetchWordData = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch('/api/word-matching/')
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const responseJson = await response.json()
      wordMatchingData.value = responseJson.data
    } catch (err) {
      console.error('Error fetching word matching data:', err)
      error.value = err.message || 'Failed to load word data. Please try again.'
    } finally {
      loading.value = false
    }
  }

  const shuffleArray = (array) => {
    const shuffled = [...array]
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
    }
    return shuffled
  }

  const getShuffledWords = () => {
    return {
      malayalam: shuffleArray(wordMatchingData.value),
      english: shuffleArray(wordMatchingData.value)
    }
  }

  const retryFetch = () => {
    fetchWordData()
  }

  return {
    // State
    loading,
    error,
    wordMatchingData,
    
    // Methods
    fetchWordData,
    shuffleArray,
    getShuffledWords,
    retryFetch
  }
} 