import { defineStore } from 'pinia'
import { supabase } from '../lib/supabase'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
    loading: false,
    error: null,
    magicword: null,
    guestMode: false
  }),

  actions: {
    async signup(email, password) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/auth/signup`, {
          email,
          password
        })
        this.user = response.data.user
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'An error occurred during signup'
        throw error
      } finally {
        this.loading = false
      }
    },

    async login(email, password) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/auth/login`, {
          email,
          password
        })
        this.user = response.data.user
        this.token = response.data.access_token
        localStorage.setItem('token', this.token)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'An error occurred during login'
        throw error
      } finally {
        this.loading = false
      }
    },

    async logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
    },

    async checkAuth() {
      const token = localStorage.getItem('token')
      if (token) {
        try {
          const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/auth/user`, {
            headers: { Authorization: `Bearer ${token}` }
          })
          this.user = response.data.user
          this.token = token
        } catch (error) {
          this.logout()
        }
      }
    },

    async checkMagicword(magicword) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/auth/magicword`, {
          magicword
        })
        this.token = response.data.access_token
        localStorage.setItem('token', this.token)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'An error occurred during magicword check'
        throw error
      }
      finally {
        this.loading = false
      }
    }
  }
}) 