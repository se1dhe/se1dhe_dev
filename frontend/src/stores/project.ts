import { defineStore } from 'pinia'
import { ref } from 'vue'
import { apiClient } from '@/api'
import type { Project } from '@/types/project'

export const useProjectStore = defineStore('project', () => {
  const projects = ref<Project[]>([])
  const selectedProject = ref<Project | null>(null)
  const recentProjects = ref<Project[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const fetchProjects = async (params?: { [key: string]: any }) => {
    try {
      isLoading.value = true
      const response = await apiClient.get('/projects', { params })
      projects.value = response.data
      return response.data
    } catch (err) {
      error.value = 'Failed to fetch projects'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const fetchProject = async (id: number) => {
    try {
      isLoading.value = true
      const response = await apiClient.get(`/projects/${id}`)
      selectedProject.value = response.data
      return response.data
    } catch (err) {
      error.value = 'Failed to fetch project'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const createProject = async (project: Partial<Project>) => {
    try {
      isLoading.value = true
      const response = await apiClient.post('/projects', project)
      const newProject = response.data
      projects.value.push(newProject)
      return newProject
    } catch (err) {
      error.value = 'Failed to create project'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const updateProject = async (id: number, project: Partial<Project>) => {
    try {
      isLoading.value = true
      const response = await apiClient.put(`/projects/${id}`, project)
      const updatedProject = response.data

      // Update project in the projects list
      const index = projects.value.findIndex(p => p.id === id)
      if (index !== -1) {
        projects.value[index] = updatedProject
      }

      // Update selected project if it's the same one
      if (selectedProject.value?.id === id) {
        selectedProject.value = updatedProject
      }

      return updatedProject
    } catch (err) {
      error.value = 'Failed to update project'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const deleteProject = async (id: number) => {
    try {
      isLoading.value = true
      await apiClient.delete(`/projects/${id}`)

      // Remove project from the projects list
      projects.value = projects.value.filter(p => p.id !== id)

      // Clear selected project if it's the same one
      if (selectedProject.value?.id === id) {
        selectedProject.value = null
      }

      // Remove from recent projects if present
      recentProjects.value = recentProjects.value.filter(p => p.id !== id)
    } catch (err) {
      error.value = 'Failed to delete project'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const fetchRecentProjects = async () => {
    try {
      isLoading.value = true
      const response = await apiClient.get('/projects/recent')
      recentProjects.value = response.data
      return response.data
    } catch (err) {
      error.value = 'Failed to fetch recent projects'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  return {
    projects,
    selectedProject,
    recentProjects,
    isLoading,
    error,
    fetchProjects,
    fetchProject,
    createProject,
    updateProject,
    deleteProject,
    fetchRecentProjects
  }
}) 