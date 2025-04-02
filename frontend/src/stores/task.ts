import { defineStore } from 'pinia'
import { ref } from 'vue'
import { apiClient } from '@/api'
import type { Task } from '@/types/task'

export const useTaskStore = defineStore('task', () => {
  const tasks = ref<Task[]>([])
  const selectedTask = ref<Task | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const fetchTasks = async (params?: { [key: string]: any }) => {
    try {
      isLoading.value = true
      const response = await apiClient.get('/tasks', { params })
      tasks.value = response.data
      return response.data
    } catch (err) {
      error.value = 'Failed to fetch tasks'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const fetchTask = async (id: number) => {
    try {
      isLoading.value = true
      const response = await apiClient.get(`/tasks/${id}`)
      selectedTask.value = response.data
      return response.data
    } catch (err) {
      error.value = 'Failed to fetch task'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const createTask = async (task: Partial<Task>) => {
    try {
      isLoading.value = true
      const response = await apiClient.post('/tasks', task)
      const newTask = response.data
      tasks.value.push(newTask)
      return newTask
    } catch (err) {
      error.value = 'Failed to create task'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const updateTask = async (id: number, task: Partial<Task>) => {
    try {
      isLoading.value = true
      const response = await apiClient.put(`/tasks/${id}`, task)
      const updatedTask = response.data

      // Update task in the tasks list
      const index = tasks.value.findIndex(t => t.id === id)
      if (index !== -1) {
        tasks.value[index] = updatedTask
      }

      // Update selected task if it's the same one
      if (selectedTask.value?.id === id) {
        selectedTask.value = updatedTask
      }

      return updatedTask
    } catch (err) {
      error.value = 'Failed to update task'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const deleteTask = async (id: number) => {
    try {
      isLoading.value = true
      await apiClient.delete(`/tasks/${id}`)

      // Remove task from the tasks list
      tasks.value = tasks.value.filter(t => t.id !== id)

      // Clear selected task if it's the same one
      if (selectedTask.value?.id === id) {
        selectedTask.value = null
      }
    } catch (err) {
      error.value = 'Failed to delete task'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  return {
    tasks,
    selectedTask,
    isLoading,
    error,
    fetchTasks,
    fetchTask,
    createTask,
    updateTask,
    deleteTask
  }
}) 