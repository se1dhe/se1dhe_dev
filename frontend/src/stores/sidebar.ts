import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSidebarStore = defineStore('sidebar', () => {
  const isCollapsed = ref(false)
  const isMobileOpen = ref(false)

  // Toggle sidebar collapse state
  const toggle = () => {
    isCollapsed.value = !isCollapsed.value
    localStorage.setItem('sidebarCollapsed', String(isCollapsed.value))
  }

  // Collapse sidebar
  const collapse = () => {
    isCollapsed.value = true
    localStorage.setItem('sidebarCollapsed', 'true')
  }

  // Expand sidebar
  const expand = () => {
    isCollapsed.value = false
    localStorage.setItem('sidebarCollapsed', 'false')
  }

  // Toggle mobile sidebar
  const toggleMobile = () => {
    isMobileOpen.value = !isMobileOpen.value
  }

  // Close mobile sidebar
  const closeMobile = () => {
    isMobileOpen.value = false
  }

  // Initialize sidebar state from localStorage
  const initializeState = () => {
    const savedState = localStorage.getItem('sidebarCollapsed')
    if (savedState !== null) {
      isCollapsed.value = savedState === 'true'
    }
  }

  // Call initialize on store creation
  initializeState()

  return {
    isCollapsed,
    isMobileOpen,
    toggle,
    collapse,
    expand,
    toggleMobile,
    closeMobile
  }
}) 