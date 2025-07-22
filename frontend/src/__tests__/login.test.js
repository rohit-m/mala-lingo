import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import Login from '../components/layout/login.vue'
import { useAuthStore } from '../stores/auth'
import { flushPromises } from '@vue/test-utils'

describe('Login Component', () => {
  beforeEach(() => {
    // Create a fresh pinia instance for each test
    setActivePinia(createPinia())
  })

  it('renders login form when authStore token is not set', async () => {
    const authStore = useAuthStore()
    authStore.token = null
    await flushPromises()
    // Mount the component
    const wrapper = mount(Login)
    
    // Check that the login container is rendered
    expect(wrapper.find('[data-testid="login-container"]').exists()).toBe(true)
  })
}) 