<template>
  <div class="app">
    <nav class="navbar">
      <router-link to="/" class="nav-link">Home</router-link>
      <template v-if="!authStore.user">
        <router-link to="/login" class="nav-link">Login</router-link>
        <router-link to="/signup" class="nav-link">Sign Up</router-link>
      </template>
      <template v-else>
        <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
        <router-link to="/matching-words" class="nav-link">Word Matching</router-link>
        <button @click="handleLogout" class="nav-link logout-btn">Logout</button>
      </template>
    </nav>
    
    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<script setup>
import { useAuthStore } from './stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

<style>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background-color: #2c3e50;
  padding: 1rem;
  display: flex;
  gap: 1rem;
  align-items: center;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-link:hover {
  background-color: #34495e;
}

.logout-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  color: white;
}

.main-content {
  flex: 1;
  padding: 2rem;
}
</style>
