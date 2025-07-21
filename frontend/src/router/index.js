import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { title: 'Mala Lingo - Home' }
  },
  {
    path: '/matching-words',
    name: 'MatchingWords',
    component: () => import('../views/MatchingWords.vue'),
    meta: { title: 'Mala Lingo - Word Matching' }
  },
  {
    path: '/flip-test',
    name: 'FlipTest',
    component: () => import('../views/FlipTest.vue'),
    meta: { title: 'Mala Lingo - Flip Test' }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Set page title
  document.title = to.meta.title || 'Mala Lingo'
  
  if (to.meta.requiresAuth) {
    if (!authStore.user) {
      await authStore.checkAuth()
      if (!authStore.user) {
        next('/login')
        return
      }
    }
  }
  
  next()
})

export default router 