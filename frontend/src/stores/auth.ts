import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiClient } from '@/api'
import type { User } from '@/types/user'
import { useRouter } from 'vue-router'
import { ROUTES } from '../constants'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  const setToken = (newToken: string | null) => {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${newToken}`
    } else {
      localStorage.removeItem('token')
      delete apiClient.defaults.headers.common['Authorization']
    }
  }

  const login = async (credentials: { email: string; password: string; remember?: boolean }) => {
    const response = await apiClient.post('/auth/login', credentials)
    setToken(response.data.token)
    user.value = response.data.user
    return response.data.user
  }

  const register = async (data: any) => {
    const response = await apiClient.post('/auth/register', data)
    setToken(response.data.token)
    user.value = response.data.user
    return response.data.user
  }

  const logout = async () => {
    try {
      await apiClient.post('/auth/logout')
    } finally {
      setToken(null)
      user.value = null
    }
  }

  const getMe = async () => {
    try {
      const response = await apiClient.get('/auth/me')
      user.value = response.data
      return response.data
    } catch (error) {
      console.error('Failed to fetch user:', error)
      setToken(null)
      user.value = null
      throw error
    }
  }

  const updateProfile = async (data: Partial<User>) => {
    const response = await apiClient.put('/auth/profile', data)
    user.value = response.data
    return response.data
  }

  const forgotPassword = async (email: string) => {
    return await apiClient.post('/auth/forgot-password', { email })
  }

  const resetPassword = async (token: string, password: string) => {
    return await apiClient.post('/auth/reset-password', { token, password })
  }

  const telegramLogin = async (data: { id: number; first_name: string; username: string; photo_url?: string; auth_date: number; hash: string }) => {
    const response = await apiClient.post('/auth/telegram', data)
    setToken(response.data.token)
    user.value = response.data.user
    return response.data.user
  }

  const googleLogin = async (token: string) => {
    const response = await apiClient.post('/auth/google', { token })
    setToken(response.data.token)
    user.value = response.data.user
    return response.data.user
  }

  // Initialize auth state
  if (token.value) {
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
    getMe().catch(() => {
      setToken(null)
      user.value = null
    })
  }

  return {
    user,
    token,
    isAuthenticated,
    isAdmin,
    login,
    register,
    logout,
    getMe,
    updateProfile,
    forgotPassword,
    resetPassword,
    telegramLogin,
    googleLogin
  }
}) 