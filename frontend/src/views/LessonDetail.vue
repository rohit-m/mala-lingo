<template>
  <div class="lesson-detail-container">
    <div v-if="loading" class="loading">
      Loading lesson...
    </div>

    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-else class="lesson-content">
      <div class="lesson-header">
        <h1>{{ lesson.title }}</h1>
        <span class="lesson-order">Lesson {{ lesson.order }}</span>
      </div>

      <p class="lesson-description">{{ lesson.description }}</p>

      <div class="lesson-sections">
        <!-- Vocabulary Section -->
        <div class="section vocabulary-section">
          <h2 class="section-title">
            <span class="section-icon">📚</span> Vocabulary
          </h2>

          <div v-if="vocabulary.length === 0" class="empty-section">
            No vocabulary words available for this lesson.
          </div>

          <div v-else class="vocab-list">
            <div v-for="vocab in vocabulary" :key="vocab.id" class="vocab-item">
              <div class="malayalam-word">{{ vocab.malayalam_word }}</div>
              <div class="word-arrow">→</div>
              <div class="english-word">{{ vocab.english_word }}</div>
            </div>
          </div>
        </div>

        <!-- Verbs Section -->
        <div class="section verbs-section">
          <h2 class="section-title">
            <span class="section-icon">🔤</span> Verbs
          </h2>

          <div v-if="verbs.length === 0" class="empty-section">
            No verbs available for this lesson.
          </div>

          <div v-else class="verbs-list">
            <div v-for="verb in verbs" :key="verb.id" class="verb-item">
              <div class="verb-tense">{{ verb.tense }}</div>
              <div class="verb-words">
                <div class="malayalam-word">{{ verb.malayalam_word }}</div>
                <div class="word-arrow">→</div>
                <div class="english-word">{{ verb.english_word }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="action-buttons">
        <button class="start-button" @click="startLesson">Start Lesson</button>
        <button class="nav-button" @click="goToLessons">Back to Lessons</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { supabase } from '../lib/supabase'

const route = useRoute()
const router = useRouter()

const lesson = ref({})
const vocabulary = ref([])
const verbs = ref([])
const exercises = ref([])
const loading = ref(true)
const error = ref(null)

const fetchLessonData = async () => {
  loading.value = true
  error.value = null

  try {
    const lessonId = route.params.id

    // Fetch lesson details
    const { data: lessonData, error: lessonError } = await supabase
      .from('lessons')
      .select('*')
      .eq('id', lessonId)
      .single()

    if (lessonError) throw lessonError
    lesson.value = lessonData

    // Fetch vocabulary
    const { data: vocabData, error: vocabError } = await supabase
      .from('lesson_vocab')
      .select('*')
      .eq('lesson_id', lessonId)

    if (vocabError) throw vocabError
    vocabulary.value = vocabData

    // Fetch verbs
    const { data: verbsData, error: verbsError } = await supabase
      .from('lesson_verbs')
      .select('*')
      .eq('lesson_id', lessonId)

    if (verbsError) throw verbsError
    verbs.value = verbsData

    // Fetch exercises
    const { data: exercisesData, error: exercisesError } = await supabase
      .from('exercises')
      .select('*')
      .eq('lesson_id', lessonId)

    if (exercisesError) throw exercisesError
    exercises.value = exercisesData

  } catch (e) {
    console.error('Error fetching lesson data:', e)
    error.value = 'Failed to load lesson data. Please try again later.'
  } finally {
    loading.value = false
  }
}

const goToLessons = () => {
  router.push('/lessons')
}

const startLesson = () => {
  // Navigate to practice/exercises page with the lesson ID
  router.push(`/practice/${route.params.id}`)
}

onMounted(async () => {
  await fetchLessonData()
})
</script>

<style scoped>
.lesson-detail-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
}

.loading,
.error-message {
  text-align: center;
  margin: 3rem 0;
  color: #666;
}

.error-message {
  color: #e74c3c;
}

.lesson-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.lesson-order {
  background-color: #3498db;
  color: white;
  font-size: 0.9rem;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
}

.lesson-description {
  color: #555;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.lesson-sections {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.section {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

.section-title {
  display: flex;
  align-items: center;
  margin-top: 0;
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.section-icon {
  margin-right: 0.5rem;
}

.empty-section {
  text-align: center;
  color: #777;
  padding: 1.5rem 0;
}

/* Vocabulary styles */
.vocab-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.vocab-item {
  display: flex;
  align-items: center;
  padding: 0.8rem;
  border-radius: 6px;
  background-color: #f8f9fa;
}

.word-arrow {
  margin: 0 0.5rem;
  color: #7f8c8d;
}

.malayalam-word {
  font-weight: bold;
  color: #2c3e50;
}

.english-word {
  color: #34495e;
}

/* Verbs styles */
.verbs-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.verb-item {
  padding: 0.8rem;
  border-radius: 6px;
  background-color: #f8f9fa;
}

.verb-tense {
  font-size: 0.9rem;
  font-weight: bold;
  color: #3498db;
  margin-bottom: 0.5rem;
}

.verb-words {
  display: flex;
  align-items: center;
}

.action-buttons {
  margin-top: 2rem;
  display: flex;
  gap: 1rem;
}

.start-button {
  padding: 0.8rem 1.5rem;
  background-color: #2ecc71;
  color: white;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.start-button:hover {
  background-color: #27ae60;
}

.nav-button {
  padding: 0.8rem 1.5rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.nav-button:hover {
  background-color: #2980b9;
}
</style>