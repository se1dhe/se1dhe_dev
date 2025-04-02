import { defineStore } from 'pinia'
import { ref } from 'vue'
import { apiClient } from '@/api'
import type { User } from '@/types/user'

export const useUserStore = defineStore('user', () => {
  const users = ref<User[]>([])
  const selectedUser = ref<User | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const fetchUsers = async () => {
    try {
      isLoading.value = true
      const response = await apiClient.get('/users')
      users.value = response.data
      return response.data
    } catch (err) {
      error.value = 'Failed to fetch users'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const fetchUser = async (id: number) => {
    try {
      isLoading.value = true
      const response = await apiClient.get(`/users/${id}`)
      selectedUser.value = response.data
      return response.data
    } catch (err) {
      error.value = 'Failed to fetch user'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const updateUser = async (id: number, data: Partial<User>) => {
    try {
      isLoading.value = true
      const response = await apiClient.put(`/users/${id}`, data)
      const updatedUser = response.data
      
      // Update the user in the users list
      const index = users.value.findIndex(u => u.id === id)
      if (index !== -1) {
        users.value[index] = updatedUser
      }
      
      // Update selected user if it's the same one
      if (selectedUser.value?.id === id) {
        selectedUser.value = updatedUser
      }
      
      return updatedUser
    } catch (err) {
      error.value = 'Failed to update user'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const deleteUser = async (id: number) => {
    try {
      isLoading.value = true
      await apiClient.delete(`/users/${id}`)
      
      // Remove user from the users list
      users.value = users.value.filter(u => u.id !== id)
      
      // Clear selected user if it's the same one
      if (selectedUser.value?.id === id) {
        selectedUser.value = null
      }
    } catch (err) {
      error.value = 'Failed to delete user'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  return {
    users,
    selectedUser,
    isLoading,
    error,
    fetchUsers,
    fetchUser,
    updateUser,
    deleteUser
  }
}) 