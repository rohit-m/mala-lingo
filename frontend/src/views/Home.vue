<template>
  <div class="home-container">
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">Make learning Malayalam fun and easy!</h1>
        <div class="hero-description">
          <p>Discover a colorful world of Malayalam language learning through interactive games and lessons</p>
        </div>

        <div class="hero-cta">
          <router-link to="/signup" class="cta-button primary">SIGN UP AND SAVE YOUR PROGRESS</router-link>
          <router-link to="/login" class="cta-button secondary">LOGIN</router-link>
        </div>
      </div>

      <div class="hero-visual">
        <div class="mascot-container">
          <div class="mascot-circle">
            <div class="mascot">🐕</div>
          </div>
          <div class="mascot-circle small circle-pink">
            <div class="mascot">🐱</div>
          </div>
          <div class="mascot-circle small circle-yellow">
            <div class="mascot">🦊</div>
          </div>
          <div class="mascot-circle small circle-teal">
            <div class="mascot">🐻</div>
          </div>
        </div>
      </div>
    </div>

    <div class="features-banner">
      <div class="feature-item">
        <span class="feature-emoji">🎮</span>
        <span class="feature-text">Interactive Games</span>
      </div>
      <div class="feature-item">
        <span class="feature-emoji">📚</span>
        <span class="feature-text">Structured Lessons</span>
      </div>
      <div class="feature-item">
        <span class="feature-emoji">📊</span>
        <span class="feature-text">Progress Tracking</span>
      </div>
      <div class="feature-item">
        <span class="feature-emoji">🔄</span>
        <span class="feature-text">Daily Practice</span>
      </div>
    </div>

    <div class="try-now-section">
      <h2>Start Learning Malayalam Today</h2>
      <p class="try-description">Try these activities without creating an account</p>

      <div class="try-buttons">
        <router-link to="/matching-words" class="try-button">
          <span class="try-icon">🎮</span>
          <h3>Word Matching</h3>
          <p>Match Malayalam words with their meanings</p>
        </router-link>
        <router-link to="/flip-test" class="try-button">
          <span class="try-icon">🔄</span>
          <h3>Flip Test</h3>
          <p>Test your memory with flashcards</p>
        </router-link>
        <router-link to="/lessons" class="try-button">
          <span class="try-icon">📚</span>
          <h3>Browse Lessons</h3>
          <p>Explore our lesson library</p>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
</script>

<style scoped>
.home-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 4rem;
}

.hero-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 3rem;
  padding: 2rem 0;
}

.hero-content {
  flex: 1;
  max-width: 600px;
}

.hero-title {
  font-size: 3.2rem;
  font-weight: bold;
  color: var(--color-purple);
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.hero-description {
  font-size: 1.5rem;
  color: var(--color-text-light);
  margin-bottom: 2.5rem;
}

.hero-visual {
  flex: 1;
  display: flex;
  justify-content: center;
}

.hero-cta {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 100%;
}

.cta-button {
  padding: 1rem;
  border-radius: 8px;
  font-size: 1rem;
  text-decoration: none;
  text-align: center;
  font-weight: bold;
  transition: transform 0.3s, box-shadow 0.3s;
  width: 100%;
}

.cta-button:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.primary {
  background-color: var(--color-pink);
  color: white;
  border: 2px solid var(--color-primary-dark);
  box-shadow: 0 4px 0 var(--color-primary-dark);
}

.primary:hover {
  background-color: #f56bbe;
}

.secondary {
  background-color: white;
  color: var(--color-blue);
  border: 2px solid var(--color-border);
  box-shadow: 0 4px 0 var(--color-border);
}

.secondary:hover {
  background-color: #f7f7f7;
}

.features-banner {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, var(--color-purple) 0%, var(--color-pink) 100%);
  border-radius: 12px;
  color: white;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.feature-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 0.5rem;
}

.feature-emoji {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.feature-text {
  font-weight: bold;
}

.mascot-container {
  position: relative;
  width: 300px;
  height: 300px;
}

.mascot-circle {
  position: absolute;
  width: 140px;
  height: 140px;
  background-color: var(--color-purple);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  z-index: 2;
}

.mascot-circle.small {
  width: 80px;
  height: 80px;
  z-index: 1;
}

.circle-pink {
  background-color: var(--color-pink);
  top: 20%;
  left: 20%;
}

.circle-yellow {
  background-color: var(--color-yellow);
  top: 20%;
  left: 80%;
}

.circle-teal {
  background-color: var(--color-teal);
  top: 75%;
  left: 25%;
}

.mascot {
  font-size: 4rem;
}

.mascot-circle.small .mascot {
  font-size: 2rem;
}

.try-now-section {
  text-align: center;
  padding: 2rem 0;
}

.try-now-section h2 {
  font-size: 2.5rem;
  color: var(--color-text);
  margin-bottom: 0.5rem;
}

.try-description {
  font-size: 1.2rem;
  color: var(--color-text-light);
  margin-bottom: 2.5rem;
}

.try-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.try-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  background-color: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  color: var(--color-text);
  text-decoration: none;
  transition: transform 0.3s;
  height: 100%;
}

.try-button:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
}

.try-icon {
  font-size: 3.5rem;
  margin-bottom: 1rem;
  display: block;
}

.try-button h3 {
  color: var(--color-purple);
  font-size: 1.5rem;
  margin-bottom: 0.75rem;
}

.try-button p {
  color: var(--color-text-light);
  line-height: 1.5;
}

@media (max-width: 768px) {
  .home-container {
    gap: 3rem;
    padding: 1.5rem;
  }

  .hero-section {
    flex-direction: column;
    padding: 1rem 0;
    text-align: center;
  }

  .hero-content {
    order: 2;
    max-width: 100%;
  }

  .hero-visual {
    order: 1;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .hero-description {
    font-size: 1.2rem;
    margin-bottom: 1.5rem;
  }

  .features-banner {
    flex-wrap: wrap;
    justify-content: center;
  }

  .feature-item {
    width: 45%;
    margin-bottom: 1rem;
  }

  .mascot-container {
    height: 250px;
    width: 250px;
    margin: 0 auto;
  }

  .try-buttons {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}
</style>