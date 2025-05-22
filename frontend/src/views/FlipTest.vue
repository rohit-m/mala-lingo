<template>
    <div class="flip-test-container">
        <h1>Flip Test</h1>
        <p class="game-instructions">Click on a card to reveal its English translation.</p>

        <div v-if="loading" class="loading">
            Loading word data...
        </div>

        <div v-else-if="error" class="error-message">
            {{ error }}
        </div>

        <div v-else class="flip-test-content">
            <div v-if="wordMatchingData.length === 0" class="no-data">
                No word data available.
            </div>

            <div v-else class="matching-game">
                <div class="game-status">
                    <div class="score">
                        <span class="score-icon">🎯</span>
                        <span class="score-text">Cards: {{ wordMatchingData.length }}</span>
                    </div>
                    <div class="button-group">
                        <button @click="fetchNewCards" class="action-button new-cards-button">
                            <span class="button-icon">🔄</span>
                            New Cards
                        </button>
                        <button @click="resetCards" class="action-button reset-button">Reset All Cards</button>
                    </div>
                </div>

                <div class="cards-grid">
                    <div v-for="item in wordMatchingData" :key="item.id" class="card-container">
                        <div class="card" @click="flipCard(item.id)" :class="{ 'is-flipped': flippedCards[item.id] }">
                            <div class="card-face card-front">
                                <div class="word">{{ item.malayalam_word }}</div>
                                <div class="hint">Click to reveal</div>
                            </div>
                            <div class="card-face card-back">
                                <div class="word">{{ item.english_word }}</div>
                                <div class="hint">Click to hide</div>
                            </div>
                        </div>
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
const flippedCards = ref({})

const flipCard = (id) => {
    flippedCards.value[id] = !flippedCards.value[id]
}

const resetCards = () => {
    flippedCards.value = {}
}

const fetchNewCards = () => {
    resetCards()
    fetchWordMatchingData()
}

const fetchWordMatchingData = async () => {
    loading.value = true
    error.value = null

    try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/word-matching`)
        wordMatchingData.value = response.data.data
    } catch (err) {
        error.value = err.response?.data?.detail || 'Failed to fetch word data'
        console.error('Error fetching word data:', err)
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    fetchWordMatchingData()
})
</script>

<style scoped>
.flip-test-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    font-family: 'Nunito', 'Helvetica Neue', Arial, sans-serif;
}

h1 {
    color: var(--color-purple);
    margin-bottom: 1rem;
    text-align: center;
    font-size: 2.5rem;
    font-weight: 800;
}

.game-instructions {
    text-align: center;
    color: var(--color-text-light);
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
    color: white;
    background-color: var(--color-primary-dark);
    border-radius: 12px;
    border: 2px solid var(--color-primary);
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
    border-bottom: 2px solid var(--color-border);
}

.score {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.2rem;
    font-weight: bold;
    color: var(--color-text);
}

.score-icon {
    font-size: 1.5rem;
}

.score-text {
    color: var(--color-text);
}

.button-group {
    display: flex;
    gap: 1rem;
}

.action-button {
    color: white;
    border: none;
    padding: 0.7rem 1.5rem;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s;
    font-weight: bold;
    font-size: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.new-cards-button {
    background-color: var(--color-teal);
    box-shadow: 0 2px 0 #00d0b0;
}

.new-cards-button:hover {
    background-color: #00ffdd;
    transform: translateY(-2px);
}

.new-cards-button:active {
    transform: translateY(1px);
    box-shadow: 0 0 0 #00d0b0;
}

.reset-button {
    background-color: var(--color-yellow);
    color: #333;
    box-shadow: 0 2px 0 #d9c02c;
}

.reset-button:hover {
    background-color: #ffe85c;
    transform: translateY(-2px);
}

.reset-button:active {
    transform: translateY(1px);
    box-shadow: 0 0 0 #d9c02c;
}

.button-icon {
    font-size: 1.2rem;
}

.cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 2rem;
    margin-bottom: 1rem;
}

.card-container {
    height: 200px;
    perspective: 1000px;
}

.card {
    position: relative;
    width: 100%;
    height: 100%;
    cursor: pointer;
    transform-style: preserve-3d;
    transition: transform 0.6s;
}

.card.is-flipped {
    transform: rotateY(180deg);
}

.card-face {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 1.5rem;
    border-radius: 16px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-front {
    background-color: #fff;
    border: 2px solid var(--color-border);
    transform: rotateY(0deg);
}

.card-back {
    background-color: rgba(0, 187, 249, 0.1);
    border: 2px solid var(--color-blue);
    transform: rotateY(180deg);
}

.word {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--color-text);
    margin-bottom: 1rem;
    text-align: center;
}

.hint {
    font-size: 0.9rem;
    color: var(--color-text-light);
    text-align: center;
}

@media (max-width: 768px) {
    .flip-test-container {
        padding: 1rem;
    }

    h1 {
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
    }

    .game-instructions {
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }

    .matching-game {
        padding: 1rem;
    }

    .game-status {
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        flex-direction: column;
        gap: 1rem;
        align-items: flex-start;
    }

    .button-group {
        width: 100%;
        justify-content: space-between;
    }

    .action-button {
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
    }

    .cards-grid {
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 1rem;
    }

    .card-container {
        height: 180px;
    }

    .word {
        font-size: 1.2rem;
    }

    .hint {
        font-size: 0.8rem;
    }
}

@media (max-width: 375px) {
    .flip-test-container {
        padding: 0.5rem;
    }

    h1 {
        font-size: 1.5rem;
    }

    .game-instructions {
        font-size: 0.8rem;
    }

    .matching-game {
        padding: 0.8rem;
    }

    .button-group {
        flex-direction: column;
        gap: 0.5rem;
    }

    .action-button {
        width: 100%;
        justify-content: center;
    }

    .cards-grid {
        grid-template-columns: 1fr;
    }

    .card-container {
        height: 160px;
    }
}
</style>