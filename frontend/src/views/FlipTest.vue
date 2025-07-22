
<script setup>
import { onMounted, computed } from 'vue'
import { useWordData } from '../composables/useWordData'
import { useFlipCardGame } from '../composables/useGameState'
import { useAuthStore } from '../stores/auth'

// UI Components
import LoadingSpinner from '../components/ui/LoadingSpinner.vue'
import ErrorMessage from '../components/ui/ErrorMessage.vue'
import GameHeader from '../components/ui/GameHeader.vue'
import GameStatus from '../components/game/GameStatus.vue'
import FlipCard from '../components/game/FlipCard.vue'
import Login from '../components/layout/login.vue'

// Composables
const { loading, error, wordMatchingData, fetchWordData, retryFetch } = useWordData()
const { flippedCards, flippedCount, flipCard, resetCards } = useFlipCardGame()

const authStore = useAuthStore()

// Game score for GameStatus
const gameScore = computed(() => ({
    current: flippedCount.value,
    total: wordMatchingData.value.length
}))

// Game actions for GameStatus component
const gameActions = computed(() => [
    {
        label: 'New Cards',
        onClick: () => {
            resetCards()
            fetchWordData()
        },
        variant: 'filled',
        icon: '🔄'
    },
    {
        label: 'Reset All Cards',
        onClick: resetCards,
        variant: 'outlined'
    }
])

// Load data on mount
onMounted(() => {
    fetchWordData()
})
</script>

<template>
    <Login />
    <div class="flip-test-container">
        <GameHeader
            title="Flip Test"
            instructions="Click on a card to reveal its English translation."
        />

        <LoadingSpinner
            v-if="loading"
            text="Loading word data..."
        />

        <ErrorMessage
            v-else-if="error"
            :message="error"
            :showRetry="true"
            :onRetry="retryFetch"
        />

        <div v-else-if="wordMatchingData.length === 0" class="no-data">
            <ErrorMessage
                message="No word data available."
                severity="info"
            />
        </div>

        <div v-else class="flip-test-content">
            <GameStatus
                :score="gameScore"
                scoreIcon="🎯"
                scoreLabel="Cards Flipped"
                :actions="gameActions"
            />

            <div class="cards-grid">
                <FlipCard
                    v-for="item in wordMatchingData"
                    :key="item.id"
                    :frontText="item.malayalam_word"
                    :backText="item.english_word"
                    :isFlipped="!!flippedCards[item.id]"
                    :onFlip="() => flipCard(item.id)"
                />
            </div>
        </div>
    </div>
</template>


<style scoped>
.flip-test-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

.flip-test-content {
    margin-top: 2rem;
}

.no-data {
    text-align: center;
    margin: 2rem 0;
}

.cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
    padding: 1rem;
}

@media (max-width: 768px) {
    .flip-test-container {
        padding: 1rem;
    }

    .cards-grid {
        grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
        gap: 1rem;
        padding: 0.5rem;
    }
}

@media (max-width: 480px) {
    .cards-grid {
        grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
        gap: 0.75rem;
    }
}
</style>