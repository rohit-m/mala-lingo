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
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { title: 'Mala Lingo - Login' }
  },
  {
    path: '/signup',
    name: 'Signup',
    component: () => import('../views/Signup.vue'),
    meta: { title: 'Mala Lingo - Sign Up' }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { requiresAuth: true, title: 'Mala Lingo - Dashboard' }
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
  {
    path: '/lessons',
    name: 'Lessons',
    component: () => import('../views/Lessons.vue'),
    meta: { title: 'Mala Lingo - Lessons' }
  },
  {
    path: '/lesson/:id',
    name: 'LessonDetail',
    component: () => import('../views/LessonDetail.vue'),
    meta: { title: 'Mala Lingo - Lesson Details' }
  },
  {
    path: '/practice/:id',
    name: 'WordPool',
    component: () => import('../views/WordPool.vue'),
    meta: { title: 'Mala Lingo - Practice' }
  }
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