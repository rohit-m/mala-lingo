<template>
  <div class="matching-words-container">
    <h1>Word Matching</h1>

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

      <div v-else class="word-matching-list">
        <div v-for="(item, index) in wordMatchingData" :key="index" class="word-matching-item">
          <div class="word-card">
            <h3>{{ item.word }}</h3>
            <p>{{ item.definition }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const wordMatchingData = ref([])
const loading = ref(true)
const error = ref(null)

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
  margin-bottom: 2rem;
  text-align: center;
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

.word-matching-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.word-matching-item {
  transition: transform 0.3s;
}

.word-matching-item:hover {
  transform: translateY(-5px);
}

.word-card {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.word-card h3 {
  color: #42b883;
  margin-bottom: 0.5rem;
}

.word-card p {
  color: #666;
  line-height: 1.5;
}
</style>