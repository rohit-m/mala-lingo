<template>
  <div class="home-container">
    <h1>Welcome to Mala Lingo</h1>
    <p class="subtitle">Your language learning platform</p>
    
    <div class="cta-container">
      <router-link to="/matching-words" class="cta-button primary">Try Word Matching</router-link>
      <template v-if="authStore.user">
        <router-link to="/dashboard" class="cta-button secondary">Go to Dashboard</router-link>
      </template>
    </div>
    
    <div class="features">
      <div class="feature-card">
        <h3>Learn Languages</h3>
        <p>Access comprehensive language learning materials</p>
      </div>
      <div class="feature-card">
        <h3>Track Progress</h3>
        <p>Monitor your learning journey with detailed analytics</p>
      </div>
      <div class="feature-card">
        <h3>Practice Speaking</h3>
        <p>Improve your pronunciation with interactive exercises</p>
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
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

h1 {
  font-size: 3rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.subtitle {
  font-size: 1.5rem;
  color: #666;
  margin-bottom: 3rem;
}

.cta-container {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 4rem;
}

.cta-button {
  padding: 1rem 2rem;
  border-radius: 4px;
  font-size: 1.1rem;
  text-decoration: none;
  transition: transform 0.3s, box-shadow 0.3s;
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.primary {
  background-color: #42b883;
  color: white;
}

.secondary {
  background-color: #2c3e50;
  color: white;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 4rem;
}

.feature-card {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.feature-card h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #666;
}
</style> 