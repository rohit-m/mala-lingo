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
import { ref, onMounted, watch } from 'vue'
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

// Update page title when lesson data is loaded
watch(() => lesson.value, (newLesson) => {
  if (newLesson?.title) {
    document.title = `Mala Lingo - ${newLesson.title}`
  }
}, { deep: true })

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

h1 {
  color: var(--color-purple);
  margin: 0;
  font-size: 2.2rem;
  font-weight: 800;
}

.loading,
.error-message {
  text-align: center;
  margin: 3rem 0;
  color: var(--color-text-light);
  padding: 2rem;
  border-radius: 8px;
  background-color: #f8f8f8;
}

.error-message {
  color: white;
  background-color: var(--color-primary-dark);
}

.lesson-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.lesson-order {
  background-color: var(--color-blue);
  color: white;
  font-size: 0.9rem;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-weight: bold;
}

.lesson-description {
  color: var(--color-text-light);
  margin-bottom: 2rem;
  line-height: 1.6;
  font-size: 1.1rem;
}

.lesson-sections {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.section {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
  border: 1px solid var(--color-border);
}

.section-title {
  display: flex;
  align-items: center;
  margin-top: 0;
  color: var(--color-purple);
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.section-icon {
  margin-right: 0.8rem;
  font-size: 1.3rem;
}

.empty-section {
  text-align: center;
  color: var(--color-text-light);
  padding: 1.5rem 0;
  font-style: italic;
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
  padding: 1rem;
  border-radius: 8px;
  background-color: #f8f9fa;
  transition: transform 0.2s;
  border: 1px solid var(--color-border);
}

.vocab-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

.word-arrow {
  margin: 0 0.8rem;
  color: var(--color-text-light);
  font-weight: bold;
}

.malayalam-word {
  font-weight: bold;
  color: var(--color-pink);
}

.english-word {
  color: var(--color-text);
}

/* Verbs styles */
.verbs-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.verb-item {
  padding: 1rem;
  border-radius: 8px;
  background-color: #f8f9fa;
  border: 1px solid var(--color-border);
  transition: transform 0.2s;
}

.verb-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

.verb-tense {
  font-size: 0.9rem;
  font-weight: bold;
  color: var(--color-blue);
  margin-bottom: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
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
  background-color: var(--color-teal);
  color: var(--color-text);
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 0 #00d0b0;
  flex: 1;
}

.start-button:hover {
  background-color: #00ffdd;
  transform: translateY(-2px);
  box-shadow: 0 4px 0 #00d0b0;
}

.start-button:active {
  transform: translateY(1px);
  box-shadow: 0 0 0 #00d0b0;
}

.nav-button {
  padding: 0.8rem 1.5rem;
  background-color: var(--color-blue);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 0 var(--color-secondary-dark);
}

.nav-button:hover {
  background-color: #0cc0ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 0 var(--color-secondary-dark);
}

.nav-button:active {
  transform: translateY(1px);
  box-shadow: 0 0 0 var(--color-secondary-dark);
}

@media (max-width: 768px) {
  .lesson-detail-container {
    padding: 1.5rem 1rem;
  }

  h1 {
    font-size: 1.8rem;
  }

  .lesson-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.8rem;
  }

  .lesson-order {
    align-self: flex-start;
  }

  .lesson-description {
    font-size: 1rem;
    margin-bottom: 1.5rem;
  }

  .section {
    padding: 1.2rem;
  }

  .section-title {
    font-size: 1.3rem;
    margin-bottom: 1.2rem;
  }

  .vocab-list {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
  }
}

@media (max-width: 375px) {
  .lesson-detail-container {
    padding: 1rem 0.8rem;
  }

  h1 {
    font-size: 1.6rem;
  }

  .vocab-item,
  .verb-item {
    padding: 0.8rem;
  }

  .vocab-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .verb-words {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .word-arrow {
    transform: rotate(90deg);
    margin: 0;
  }
}
</style>