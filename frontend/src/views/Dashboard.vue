<template>
  <div class="dashboard-container">
    <h1>Dashboard</h1>
    <div class="user-info" v-if="authStore.user">
      <h2>Welcome, {{ authStore.user.email }}</h2>
      <div class="info-card">
        <h3>Account Information</h3>
        <p><strong>Email:</strong> {{ authStore.user.email }}</p>
        <p><strong>User ID:</strong> {{ authStore.user.id }}</p>
        <p><strong>Last Sign In:</strong> {{ formatDate(authStore.user.last_sign_in_at) }}</p>
      </div>
    </div>
    <div v-else class="loading">
      Loading user information...
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
import { onMounted } from 'vue'

const authStore = useAuthStore()

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleString()
}

onMounted(async () => {
  if (!authStore.user) {
    await authStore.checkAuth()
  }
})
</script>

<style scoped>
.dashboard-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.user-info {
  margin-top: 2rem;
}

.info-card {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-top: 1rem;
}

.info-card h3 {
  margin-top: 0;
  color: #2c3e50;
}

.info-card p {
  margin: 0.5rem 0;
  color: #34495e;
}

.loading {
  text-align: center;
  color: #666;
  margin-top: 2rem;
}
</style> 