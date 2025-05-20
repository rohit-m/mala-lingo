<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { supabase } from '../lib/supabase'

const route = useRoute()
const router = useRouter()

const lessonId = computed(() => route.params.id)
const exercises = ref([])
const currentExerciseIndex = ref(0)
const loading = ref(true)
const error = ref(null)
const userAnswer = ref([])
const feedback = ref({ visible: false, correct: false, correctAnswer: '' })
const activeWordPool = ref([])

// Human emojis for the exercise prompts
const humanEmojis = [
    '👨', '👩', '👧', '👦', '👶', '👵', '👴',
    '👱‍♀️', '👱', '👸', '🤴', '👰', '🤵', '👼',
    '🧑', '🧒', '🧓', '🧕', '👲', '👳‍♀️', '👳'
]

// Get a random human emoji
const getRandomHumanEmoji = () => {
    const randomIndex = Math.floor(Math.random() * humanEmojis.length)
    return humanEmojis[randomIndex]
}

// Store the emoji for the current exercise
const currentExerciseEmoji = ref(getRandomHumanEmoji())

// Compute current exercise
const currentExercise = computed(() => {
    if (exercises.value.length === 0) return null
    return exercises.value[currentExerciseIndex.value]
})

// Fetch exercises for the lesson
const fetchExercises = async () => {
    loading.value = true
    error.value = null

    try {
        const { data, error: fetchError } = await supabase
            .from('exercises')
            .select('*')
            .eq('lesson_id', lessonId.value)
            .eq('type', 'word_order')

        if (fetchError) throw fetchError

        if (data && data.length > 0) {
            exercises.value = data
            // Initialize the word pool for the first exercise
            resetExercise()
        } else {
            error.value = 'No exercises found for this lesson'
        }
    } catch (e) {
        console.error('Error fetching exercises:', e)
        error.value = 'Failed to load exercises. Please try again later.'
    } finally {
        loading.value = false
    }
}

// Reset the current exercise
const resetExercise = () => {
    userAnswer.value = []
    feedback.value = { visible: false, correct: false, correctAnswer: '' }
    currentExerciseEmoji.value = getRandomHumanEmoji()

    if (currentExercise.value?.word_pool) {
        activeWordPool.value = [...currentExercise.value.word_pool]
    } else {
        activeWordPool.value = []
    }
}

// Add a word to the user answer
const selectWord = (word, index) => {
    if (!feedback.value.visible) {
        userAnswer.value.push(word)
        activeWordPool.value.splice(index, 1)
    }
}

// Remove a word from the user answer
const removeWord = (word, index) => {
    if (!feedback.value.visible) {
        activeWordPool.value.push(word)
        userAnswer.value.splice(index, 1)
    }
}

// Check the user's answer
const checkAnswer = () => {
    const userAnswerString = userAnswer.value.join(' ')
    const correctAnswerString = currentExercise.value?.malayalam || ''

    feedback.value = {
        visible: true,
        correct: userAnswerString.trim() === correctAnswerString.trim(),
        correctAnswer: correctAnswerString
    }
}

// Move to the next exercise
const nextExercise = () => {
    if (currentExerciseIndex.value < exercises.value.length - 1) {
        currentExerciseIndex.value++
        resetExercise()
    } else {
        // If we've reached the end of exercises, go back to lesson
        finishPractice()
    }
}

// Finish the practice session
const finishPractice = () => {
    router.push(`/lesson/${lessonId.value}`)
}

onMounted(async () => {
    await fetchExercises()
})
</script>

<template>
    <div class="practice-container">
        <div class="practice-header">
            <button class="close-button" @click="finishPractice">×</button>
            <div class="progress-bar">
                <div class="progress-track">
                    <div class="progress-fill"
                        :style="{ width: `${(currentExerciseIndex + 1) / exercises.length * 100}%` }"></div>
                </div>
            </div>
            <div class="hearts">❤️❤️❤️</div>
        </div>

        <div v-if="loading" class="loading">
            Loading exercises...
        </div>

        <div v-else-if="error" class="error-message">
            {{ error }}
        </div>

        <div v-else-if="!currentExercise" class="error-message">
            No exercises available.
        </div>

        <div v-else class="exercise-content">
            <div class="exercise-prompt">
                <h2>Translate this sentence</h2>
                <div class="audio-prompt">
                    <div class="character-emoji">
                        {{ currentExerciseEmoji }}
                    </div>
                    <div class="prompt-text">{{ currentExercise.prompt }}</div>
                </div>
            </div>

            <div class="answer-area">
                <div class="user-answer">
                    <div v-for="(word, index) in userAnswer" :key="'answer-' + index" class="answer-word"
                        @click="removeWord(word, index)">
                        {{ word }}
                    </div>
                    <div v-if="userAnswer.length === 0" class="answer-placeholder">
                        Tap the words in the correct order
                    </div>
                </div>

                <div class="word-pool">
                    <div v-for="(word, index) in activeWordPool" :key="'pool-' + index" class="pool-word"
                        @click="selectWord(word, index)">
                        {{ word }}
                    </div>
                </div>
            </div>

            <div class="feedback-area" v-if="feedback.visible">
                <div class="feedback"
                    :class="{ 'correct-feedback': feedback.correct, 'incorrect-feedback': !feedback.correct }">
                    <div class="feedback-icon">{{ feedback.correct ? '✓' : '✗' }}</div>
                    <div class="feedback-text">
                        <div>{{ feedback.correct ? 'Correct!' : 'Incorrect' }}</div>
                        <div v-if="!feedback.correct" class="correct-answer">
                            Correct answer: {{ feedback.correctAnswer }}
                        </div>
                    </div>
                </div>
            </div>

            <div class="action-buttons">
                <button v-if="!feedback.visible" class="submit-button" :disabled="userAnswer.length === 0"
                    @click="checkAnswer">
                    Check
                </button>
                <button v-else class="next-button" @click="nextExercise">
                    {{ currentExerciseIndex < exercises.length - 1 ? 'Continue' : 'Finish' }} </button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.practice-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 1rem;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.practice-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}

.close-button {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    padding: 0.5rem;
}

.progress-bar {
    flex-grow: 1;
    margin: 0 1rem;
}

.progress-track {
    background-color: #e0e0e0;
    height: 0.5rem;
    border-radius: 1rem;
    overflow: hidden;
}

.progress-fill {
    background-color: #58cc02;
    height: 100%;
    transition: width 0.3s ease;
}

.hearts {
    font-size: 1.2rem;
}

.loading,
.error-message {
    text-align: center;
    margin: 3rem 0;
    color: #666;
}

.exercise-content {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
}

.exercise-prompt {
    margin-bottom: 2rem;
    text-align: center;
}

.exercise-prompt h2 {
    font-size: 1.2rem;
    margin-bottom: 1rem;
    color: #4b4b4b;
}

.audio-prompt {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1rem;
}

.character-emoji {
    font-size: 2rem;
    background-color: #f0f0f0;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 1rem;
}

.prompt-text {
    font-size: 1.1rem;
    font-weight: bold;
}

.answer-area {
    margin-bottom: 2rem;
}

.user-answer {
    min-height: 60px;
    border-bottom: 2px solid #e0e0e0;
    padding: 0.5rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
}

.answer-placeholder {
    color: #afafaf;
    width: 100%;
    text-align: center;
    padding: 1rem 0;
}

.answer-word {
    background-color: #fff;
    border: 1px solid #e0e0e0;
    border-radius: 0.25rem;
    padding: 0.5rem 1rem;
    cursor: pointer;
    user-select: none;
}

.word-pool {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
    justify-content: center;
}

.pool-word {
    background-color: #fff;
    border: 1px solid #e0e0e0;
    border-radius: 0.25rem;
    padding: 0.5rem 1rem;
    cursor: pointer;
    user-select: none;
}

.feedback-area {
    margin-bottom: 2rem;
}

.feedback {
    display: flex;
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    align-items: center;
}

.correct-feedback {
    background-color: #e6f8e0;
    border: 1px solid #58cc02;
}

.incorrect-feedback {
    background-color: #fce9e9;
    border: 1px solid #ea2b2b;
}

.feedback-icon {
    font-size: 1.5rem;
    margin-right: 1rem;
}

.correct-feedback .feedback-icon {
    color: #58cc02;
}

.incorrect-feedback .feedback-icon {
    color: #ea2b2b;
}

.feedback-text {
    font-weight: bold;
}

.correct-answer {
    font-weight: normal;
    margin-top: 0.5rem;
}

.action-buttons {
    margin-top: auto;
    display: flex;
    justify-content: center;
}

.submit-button,
.next-button {
    width: 100%;
    padding: 1rem;
    border-radius: 0.5rem;
    font-weight: bold;
    font-size: 1rem;
    cursor: pointer;
    border: none;
    transition: background-color 0.2s;
}

.submit-button {
    background-color: #58cc02;
    color: white;
}

.submit-button:disabled {
    background-color: #e0e0e0;
    cursor: not-allowed;
}

.next-button {
    background-color: #58cc02;
    color: white;
}

.submit-button:hover:not(:disabled),
.next-button:hover {
    background-color: #47a600;
}
</style>