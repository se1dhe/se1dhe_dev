import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSettingsStore = defineStore('settings', () => {
  const language = ref('ru')
  const notificationsEnabled = ref(true)
  const sidebarCollapsed = ref(false)

  function setLanguage(lang: string) {
    language.value = lang
    // TODO: Добавить логику смены языка
  }

  function toggleNotifications() {
    notificationsEnabled.value = !notificationsEnabled.value
  }

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  return {
    language,
    notificationsEnabled,
    sidebarCollapsed,
    setLanguage,
    toggleNotifications,
    toggleSidebar
  }
}) 