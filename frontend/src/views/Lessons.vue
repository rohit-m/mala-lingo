<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '../lib/supabase'

const lessons = ref([])
const loading = ref(true)
const error = ref(null)
const router = useRouter()

// Environment variables for Supabase auth
const SUPABASE_EMAIL = import.meta.env.VITE_SUPABASE_EMAIL || ''
const SUPABASE_PASSWORD = import.meta.env.VITE_SUPABASE_PASSWORD || ''

// Sort lessons by order
const sortedLessons = computed(() => {
  return [...lessons.value].sort((a, b) => a.order - b.order)
})

// Authenticate with Supabase using email and password
const authenticateWithSupabase = async () => {
  try {
    if (!SUPABASE_EMAIL || !SUPABASE_PASSWORD) {
      throw new Error('Supabase email or password is not configured')
    }

    const { data, error: authError } = await supabase.auth.signInWithPassword({
      email: SUPABASE_EMAIL,
      password: SUPABASE_PASSWORD
    })

    if (authError) throw authError

    console.log('Successfully authenticated with Supabase')
    return data.session
  } catch (e) {
    console.error('Authentication error:', e)
    throw e
  }
}

// Fetch all lessons with counts
const fetchLessons = async () => {
  loading.value = true
  error.value = null

  try {
    // Authenticate with Supabase first
    await authenticateWithSupabase()

    // Fetch lessons
    const { data: lessonsData, error: lessonsError } = await supabase
      .from('lessons')
      .select('*')
      .order('order')

    if (lessonsError) throw lessonsError

    // For each lesson, get counts of vocab, verbs, and exercises
    const lessonsWithCounts = await Promise.all(lessonsData.map(async (lesson) => {
      // Count vocabulary items
      const { count: vocabCount, error: vocabError } = await supabase
        .from('lesson_vocab')
        .select('*', { count: 'exact', head: true })
        .eq('lesson_id', lesson.id)

      // Count verbs
      const { count: verbCount, error: verbError } = await supabase
        .from('lesson_verbs')
        .select('*', { count: 'exact', head: true })
        .eq('lesson_id', lesson.id)

      // Count exercises
      const { count: exerciseCount, error: exerciseError } = await supabase
        .from('exercises')
        .select('*', { count: 'exact', head: true })
        .eq('lesson_id', lesson.id)

      return {
        ...lesson,
        vocab_count: vocabCount,
        verb_count: verbCount,
        exercise_count: exerciseCount
      }
    }))
    console.log("lessonsData", lessonsData)
    console.log("lessonsError", lessonsError)
    console.log("lessonsWithCounts", lessonsWithCounts)
    lessons.value = lessonsWithCounts
  } catch (e) {
    console.error('Error fetching lessons:', e)
    error.value = 'Failed to load lessons. Please try again later.'
  } finally {
    loading.value = false
  }
}

// Start a lesson
const startLesson = (lessonId) => {
  router.push(`/lesson/${lessonId}`)
}

onMounted(async () => {
  await fetchLessons()
})
</script>

<template>
  <div class="lessons-container">
    <h1>Malayalam Lessons</h1>
    <p class="lessons-instructions">
      Explore our Malayalam language lessons below. Each lesson contains vocabulary,
      verbs, and exercises to help you learn.
    </p>

    <div v-if="loading" class="loading">
      Loading lessons...
    </div>

    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-else class="lessons-content">
      <div v-if="lessons.length === 0" class="no-data">
        No lessons available at the moment.
      </div>

      <div v-else class="lessons-list">
        <div v-for="lesson in sortedLessons" :key="lesson.id" class="lesson-card">
          <div class="lesson-header">
            <h2 class="lesson-title">{{ lesson.title }}</h2>
            <span class="lesson-order">Lesson {{ lesson.order }}</span>
          </div>
          <p class="lesson-description">{{ lesson.description }}</p>
          <div class="lesson-stats">
            <div class="stat-item">
              <span class="stat-icon">📚</span>
              <span class="stat-text">{{ lesson.vocab_count || 0 }} Vocabulary Words</span>
            </div>
            <div class="stat-item">
              <span class="stat-icon">🔤</span>
              <span class="stat-text">{{ lesson.verb_count || 0 }} Verbs</span>
            </div>
            <div class="stat-item">
              <span class="stat-icon">✏️</span>
              <span class="stat-text">{{ lesson.exercise_count || 0 }} Exercises</span>
            </div>
          </div>
          <button class="start-lesson-btn" @click="startLesson(lesson.id)">
            Start Lesson
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.lessons-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  color: var(--color-purple);
  margin-bottom: 1rem;
  text-align: center;
  font-size: 2.5rem;
  font-weight: 800;
}

.lessons-instructions {
  margin-bottom: 2rem;
  color: var(--color-text-light);
  line-height: 1.6;
  text-align: center;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

.loading,
.error-message,
.no-data {
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

.lessons-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.lesson-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
  transition: transform 0.3s, box-shadow 0.3s;
  display: flex;
  flex-direction: column;
  border: 1px solid var(--color-border);
  height: 100%;
}

.lesson-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.lesson-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.lesson-title {
  margin: 0;
  color: var(--color-text);
  font-size: 1.4rem;
  font-weight: 700;
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
  margin-bottom: 1.5rem;
  flex-grow: 1;
  line-height: 1.5;
}

.lesson-stats {
  margin-bottom: 1.5rem;
  background-color: #f8f8f8;
  padding: 1rem;
  border-radius: 8px;
}

.stat-item {
  display: flex;
  align-items: center;
  margin-bottom: 0.8rem;
}

.stat-item:last-child {
  margin-bottom: 0;
}

.stat-icon {
  margin-right: 0.8rem;
  font-size: 1.2rem;
}

.stat-text {
  color: var(--color-text);
  font-weight: 500;
}

.start-lesson-btn {
  padding: 0.8rem 1.5rem;
  background-color: var(--color-teal);
  color: var(--color-text);
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: auto;
  box-shadow: 0 2px 0 #00d0b0;
}

.start-lesson-btn:hover {
  background-color: #00ffdd;
  transform: translateY(-2px);
  box-shadow: 0 4px 0 #00d0b0;
}

.start-lesson-btn:active {
  transform: translateY(1px);
  box-shadow: 0 0 0 #00d0b0;
}

@media (max-width: 768px) {
  .lessons-container {
    padding: 1.5rem 1rem;
  }

  h1 {
    font-size: 2rem;
  }

  .lessons-instructions {
    font-size: 0.95rem;
  }

  .lessons-list {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .lesson-card {
    padding: 1.2rem;
  }

  .lesson-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .lesson-order {
    align-self: flex-start;
  }

  .lesson-title {
    font-size: 1.3rem;
  }

  .start-lesson-btn {
    width: 100%;
    text-align: center;
    padding: 1rem;
  }
}

@media (max-width: 375px) {
  .lessons-container {
    padding: 1rem 0.8rem;
  }

  h1 {
    font-size: 1.8rem;
  }

  .lessons-instructions {
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
  }

  .loading,
  .error-message,
  .no-data {
    padding: 1.5rem 1rem;
    margin: 2rem 0;
  }
}
</style>