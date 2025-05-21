<template>
  <div class="home-container">
    <div class="home-content">
      <div class="text-section">
        <h1>Make learning Malayalam fun and easy!</h1>

        <div class="action-buttons">
          <router-link to="/signup" class="cta-button primary">GET STARTED</router-link>
          <router-link to="/login" class="cta-button secondary">I ALREADY HAVE AN ACCOUNT</router-link>
        </div>
      </div>

      <div class="image-section">
        <div class="mascot-container">
          <div class="mascot-group">
            <div class="mascot mascot-main">🦉</div>
            <div class="mascot mascot-1">🐻</div>
            <div class="mascot mascot-2">🦊</div>
            <div class="mascot mascot-3">🐶</div>
            <div class="mascot mascot-4">🐱</div>
            <div class="coin coin-1">🔶</div>
            <div class="coin coin-2">🔶</div>
          </div>
        </div>
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
  min-height: calc(100vh - 4rem);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.home-content {
  max-width: 1200px;
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
}

.text-section {
  flex: 1;
  max-width: 600px;
}

h1 {
  font-size: 2.5rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 2.5rem;
  line-height: 1.2;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
}

.cta-button {
  padding: 1rem;
  border-radius: 8px;
  font-size: 1rem;
  text-decoration: none;
  text-align: center;
  font-weight: bold;
  transition: background-color 0.3s;
  width: 100%;
}

.primary {
  background-color: #58cc02;
  color: white;
  border: 2px solid #58a700;
  box-shadow: 0 4px 0 #58a700;
}

.primary:hover {
  background-color: #61e002;
}

.secondary {
  background-color: white;
  color: #1cb0f6;
  border: 2px solid #e5e5e5;
  box-shadow: 0 4px 0 #e5e5e5;
}

.secondary:hover {
  background-color: #f7f7f7;
}

.image-section {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.mascot-container {
  position: relative;
  width: 350px;
  height: 350px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.mascot-group {
  position: relative;
  width: 100%;
  height: 100%;
}

.mascot {
  position: absolute;
  font-size: 5rem;
  filter: drop-shadow(0 3px 3px rgba(0, 0, 0, 0.2));
}

.mascot-main {
  bottom: 40%;
  right: 40%;
  font-size: 7rem;
  z-index: 5;
  color: #58cc02;
}

.mascot-1 {
  top: 5%;
  left: 15%;
  font-size: 4rem;
  transform: rotate(-15deg);
  z-index: 4;
}

.mascot-2 {
  bottom: 10%;
  right: 10%;
  font-size: 4.5rem;
  transform: rotate(10deg);
  z-index: 3;
}

.mascot-3 {
  top: 20%;
  right: 15%;
  font-size: 3.5rem;
  transform: rotate(25deg);
  z-index: 2;
}

.mascot-4 {
  bottom: 15%;
  left: 15%;
  font-size: 3.8rem;
  transform: rotate(-20deg);
  z-index: 1;
}

.coin {
  position: absolute;
  font-size: 2.5rem;
  animation: float 3s ease-in-out infinite;
  filter: drop-shadow(0 2px 2px rgba(0, 0, 0, 0.1));
}

.coin-1 {
  top: 35%;
  left: 5%;
  animation-delay: 0.5s;
}

.coin-2 {
  bottom: 25%;
  right: 15%;
  animation-delay: 1.5s;
}

@keyframes float {

  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-15px);
  }
}

@media (max-width: 768px) {
  .home-content {
    flex-direction: column-reverse;
    text-align: center;
  }

  .text-section {
    max-width: 100%;
  }

  h1 {
    font-size: 2rem;
  }

  .mascot-container {
    width: 280px;
    height: 280px;
    margin-bottom: 2rem;
  }

  .mascot-main {
    font-size: 5.5rem;
  }

  .mascot-1,
  .mascot-2,
  .mascot-3,
  .mascot-4 {
    font-size: 3rem;
  }

  .coin {
    font-size: 2rem;
  }
}
</style>