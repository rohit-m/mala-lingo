<script setup>
import { ref, computed, onMounted, watch } from 'vue'
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
const lessonTitle = ref('')

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

// Update page title when lesson is loaded
watch(() => lessonTitle.value, (newTitle) => {
    if (newTitle) {
        document.title = `Mala Lingo - Practice: ${newTitle}`
    }
})

// Fetch exercises for the lesson
const fetchExercises = async () => {
    loading.value = true
    error.value = null

    try {
        // First fetch the lesson title
        const { data: lessonData, error: lessonError } = await supabase
            .from('lessons')
            .select('title')
            .eq('id', lessonId.value)
            .single()

        if (lessonError) throw lessonError
        if (lessonData) {
            lessonTitle.value = lessonData.title
        }

        // Then fetch exercises
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
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.practice-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    padding: 0.5rem 0;
}

.close-button {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    padding: 0.5rem;
    color: var(--color-text);
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
    background-color: var(--color-teal);
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
    color: var(--color-text-light);
    padding: 1.5rem;
    border-radius: 8px;
    background-color: #f8f8f8;
}

.error-message {
    color: white;
    background-color: var(--color-primary-dark);
}

.exercise-content {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    overflow: hidden;
}

.exercise-prompt {
    margin-bottom: 1rem;
    text-align: center;
}

.exercise-prompt h2 {
    font-size: 1.2rem;
    margin-bottom: 0.75rem;
    color: var(--color-text);
}

.audio-prompt {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1rem;
}

.character-emoji {
    font-size: 1.8rem;
    background-color: var(--color-pink);
    color: white;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 1rem;
}

.prompt-text {
    font-size: 1.1rem;
    font-weight: bold;
    color: var(--color-text);
}

.answer-area {
    margin-bottom: 1rem;
}

.user-answer {
    min-height: 60px;
    max-height: 120px;
    border-bottom: 2px solid var(--color-border);
    padding: 0.5rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1rem;
    overflow-y: auto;
}

.answer-placeholder {
    color: var(--color-text-light);
    width: 100%;
    text-align: center;
    padding: 0.75rem 0;
}

.answer-word {
    background-color: #fff;
    border: 1px solid var(--color-border);
    border-radius: 0.25rem;
    padding: 0.5rem 0.75rem;
    cursor: pointer;
    user-select: none;
    margin-bottom: 0.25rem;
}

.word-pool {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1rem;
    justify-content: center;
    max-height: calc(100vh - 380px);
    overflow-y: auto;
    padding: 0.25rem;
}

.pool-word {
    background-color: #fff;
    border: 1px solid var(--color-border);
    border-radius: 0.25rem;
    padding: 0.5rem 0.75rem;
    cursor: pointer;
    user-select: none;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.pool-word:active {
    transform: translateY(1px);
}

.feedback-area {
    margin-bottom: 1rem;
}

.feedback {
    display: flex;
    padding: 0.75rem;
    border-radius: 0.5rem;
    margin-bottom: 0.5rem;
    align-items: center;
}

.correct-feedback {
    background-color: rgba(0, 245, 212, 0.2);
    border: 1px solid var(--color-teal);
}

.incorrect-feedback {
    background-color: rgba(241, 91, 181, 0.1);
    border: 1px solid var(--color-primary);
}

.feedback-icon {
    font-size: 1.5rem;
    margin-right: 1rem;
}

.correct-feedback .feedback-icon {
    color: var(--color-teal);
}

.incorrect-feedback .feedback-icon {
    color: var(--color-primary);
}

.feedback-text {
    font-weight: bold;
    color: var(--color-text);
}

.correct-answer {
    font-weight: normal;
    margin-top: 0.5rem;
    color: var(--color-text-light);
}

.action-buttons {
    padding: 0.5rem 0 1rem;
    margin-top: auto;
    display: flex;
    justify-content: center;
}

.submit-button,
.next-button {
    width: 100%;
    padding: 0.75rem;
    border-radius: 8px;
    font-weight: bold;
    font-size: 1rem;
    cursor: pointer;
    border: none;
    transition: all 0.3s;
}

.submit-button {
    background-color: var(--color-pink);
    color: white;
    border: 2px solid var(--color-primary-dark);
    box-shadow: 0 2px 0 var(--color-primary-dark);
}

.submit-button:disabled {
    background-color: #e0e0e0;
    cursor: not-allowed;
    border-color: #ccc;
    box-shadow: 0 2px 0 #ccc;
}

.next-button {
    background-color: var(--color-teal);
    color: var(--color-text);
    border: 2px solid #00d0b0;
    box-shadow: 0 2px 0 #00d0b0;
}

.submit-button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 0 var(--color-primary-dark);
}

.next-button:hover {
    background-color: #00ffdd;
    transform: translateY(-2px);
    box-shadow: 0 4px 0 #00d0b0;
}

.submit-button:active:not(:disabled),
.next-button:active {
    transform: translateY(1px);
    box-shadow: none;
}

@media (max-height: 700px) {
    .practice-container {
        padding: 0.5rem;
    }

    .practice-header {
        margin-bottom: 0.5rem;
    }

    .exercise-prompt {
        margin-bottom: 0.5rem;
    }

    .exercise-prompt h2 {
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }

    .character-emoji {
        font-size: 1.5rem;
        width: 36px;
        height: 36px;
    }

    .prompt-text {
        font-size: 1rem;
    }

    .user-answer {
        min-height: 50px;
        max-height: 100px;
    }

    .word-pool {
        max-height: calc(100vh - 320px);
    }

    .answer-word,
    .pool-word {
        padding: 0.4rem 0.6rem;
        font-size: 0.9rem;
    }

    .action-buttons {
        padding: 0.25rem 0 0.5rem;
    }

    .submit-button,
    .next-button {
        padding: 0.6rem;
    }
}

@media (max-width: 340px) {
    .practice-container {
        padding: 0.25rem;
    }

    .user-answer {
        min-height: 45px;
    }

    .answer-word,
    .pool-word {
        padding: 0.35rem 0.5rem;
        font-size: 0.85rem;
    }
}
</style>