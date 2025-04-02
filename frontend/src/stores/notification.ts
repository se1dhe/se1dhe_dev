import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Notification } from '@/types'

export const useNotificationStore = defineStore('notification', () => {
  const notifications = ref<Notification[]>([])

  function addNotification(notification: Omit<Notification, 'id' | 'created_at'>) {
    const id = Date.now().toString()
    const newNotification: Notification = {
      ...notification,
      id,
      created_at: new Date().toISOString()
    }
    notifications.value.push(newNotification)
    return id
  }

  function removeNotification(id: string) {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index !== -1) {
      notifications.value.splice(index, 1)
    }
  }

  function showSuccess(message: string, title: string = 'Успех') {
    return addNotification({
      title,
      message,
      type: 'success'
    })
  }

  function showError(message: string, title: string = 'Ошибка') {
    return addNotification({
      title,
      message,
      type: 'error'
    })
  }

  function showWarning(message: string, title: string = 'Предупреждение') {
    return addNotification({
      title,
      message,
      type: 'warning'
    })
  }

  function showInfo(message: string, title: string = 'Информация') {
    return addNotification({
      title,
      message,
      type: 'info'
    })
  }

  return {
    notifications,
    addNotification,
    removeNotification,
    showSuccess,
    showError,
    showWarning,
    showInfo
  }
}) 