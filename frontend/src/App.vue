<template>
  <div class="app">
    <nav class="navbar">
      <div class="logo">Mala-Lingo</div>

      <div class="menu-icon" @click="toggleMenu">
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
      </div>

      <div class="nav-links" :class="{ 'active': menuOpen }">
        <router-link to="/" class="nav-link" @click="closeMenu">Home</router-link>
        <router-link to="/matching-words" class="nav-link" @click="closeMenu">Word Matching</router-link>
        <router-link to="/flip-test" class="nav-link" @click="closeMenu">Flip Test</router-link>
        <router-link to="/lessons" class="nav-link" @click="closeMenu">Lessons</router-link>
        <template v-if="authStore.user">
          <router-link to="/dashboard" class="nav-link" @click="closeMenu">Dashboard</router-link>
          <button @click="handleLogout" class="nav-link logout-btn">Logout</button>
        </template>
      </div>
    </nav>

    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<script setup>
import { useAuthStore } from './stores/auth'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

const authStore = useAuthStore()
const router = useRouter()
const menuOpen = ref(false)

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}

const closeMenu = () => {
  menuOpen.value = false
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
  closeMenu()
}
</script>

<style>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background-color: var(--color-purple);
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
}

.logo {
  color: white;
  font-weight: bold;
  font-size: 1.2rem;
}

.nav-links {
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
  background-color: rgba(255, 255, 255, 0.2);
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

.menu-icon {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 30px;
  height: 21px;
  cursor: pointer;
}

.bar {
  height: 3px;
  width: 100%;
  background-color: white;
  border-radius: 10px;
}

@media (max-width: 768px) {
  .menu-icon {
    display: flex;
    z-index: 102;
  }

  .nav-links {
    position: fixed;
    flex-direction: column;
    top: 0;
    right: -250px;
    width: 250px;
    height: 100vh;
    background-color: var(--color-purple);
    padding: 80px 1rem 1rem;
    transition: right 0.3s ease;
    z-index: 101;
    gap: 1.5rem;
  }

  .nav-links.active {
    right: 0;
  }

  .nav-link {
    width: 100%;
    text-align: left;
  }
}
</style>
