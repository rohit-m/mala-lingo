<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Button from '../components/ui/Button.vue'

const router = useRouter()

// Reactive text references for each paragraph
const text1 = ref('')
const text2 = ref('')
const text3 = ref('')
const text4 = ref('')

// Full text content for each paragraph
const fullTexts = [
  "You're back here again?!",
  "You're really good at Malayalam from what the data tells me!",
  "What would you like to do today?"
]

// Typing animation function
const typeText = (targetRef, fullText, delay = 0) => {
  setTimeout(() => {
    let currentIndex = 0
    const typeInterval = setInterval(() => {
      if (currentIndex <= fullText.length) {
        targetRef.value = fullText.slice(0, currentIndex)
        currentIndex++
      } else {
        clearInterval(typeInterval)
      }
    }, 50) // 50ms between each character
  }, delay)
}

onMounted(() => {
  // Start typing animations with staggered delays
  typeText(text1, fullTexts[0], 500)      // Start after 500ms
  typeText(text2, fullTexts[1], 2000)     // Start after 2000ms
  typeText(text3, fullTexts[2], 4500)     // Start after 4500ms
})
</script>
<template>
  <div class="home-container">
    <div class="content">
      <h1>Hey Trixy!</h1>
      <p class="typing-text">{{ text1 }}<span class="cursor" v-if="text1.length < fullTexts[0].length">|</span></p>
      <p class="typing-text">{{ text2 }}<span class="cursor" v-if="text2.length < fullTexts[1].length">|</span></p>
      <p class="typing-text">{{ text3 }}<span class="cursor" v-if="text3.length < fullTexts[2].length">|</span></p>
      <div class="buttons-container">
        <Button label="Word matching" :onClick="() => {
          router.push('/matching-words')
        }" />
        <Button label="Flip cards" :onClick="() => {
          router.push('/flip-test')
        }" />
      </div>
    </div>
  </div>
</template>
<style scoped>
.home-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.content {
  text-align: center;
  max-width: 600px;
  width: 100%;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 2rem;
  color: #333;
}

.typing-text {
  min-height: 1.5em;
  margin: 1rem 0;
  font-size: 1.2rem;
  line-height: 1.6;
}

.cursor {
  animation: blink 1s infinite;
  color: #333;
  font-weight: bold;
}

@keyframes blink {
  0%, 50% {
    opacity: 1;
  }
  51%, 100% {
    opacity: 0;
  }
}

.buttons-container {
  margin-top: 3rem;
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}
</style>