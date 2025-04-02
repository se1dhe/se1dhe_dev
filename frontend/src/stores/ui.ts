import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUIStore = defineStore('ui', () => {
  const isLoading = ref(false)
  const loadingText = ref('')
  const isSidebarCollapsed = ref(false)
  const theme = ref<'light' | 'dark'>('light')

  function setLoading(loading: boolean, text: string = '') {
    isLoading.value = loading
    loadingText.value = text
  }

  function toggleSidebar() {
    isSidebarCollapsed.value = !isSidebarCollapsed.value
  }

  function setTheme(newTheme: 'light' | 'dark') {
    theme.value = newTheme
    document.documentElement.setAttribute('data-theme', newTheme)
  }

  return {
    isLoading,
    loadingText,
    isSidebarCollapsed,
    theme,
    setLoading,
    toggleSidebar,
    setTheme
  }
}) 