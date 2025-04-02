import { defineStore } from 'pinia'
import { ref } from 'vue'
import { apiClient } from '@/api'
import type { Bot, BotCategory, BotReview, BotSubscription } from '@/types/bot'

export const useBotStore = defineStore('bot', () => {
  const bots = ref<Bot[]>([])
  const categories = ref<BotCategory[]>([])
  const selectedBot = ref<Bot | null>(null)
  const userSubscriptions = ref<BotSubscription[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const fetchBots = async (categoryId?: number) => {
    try {
      isLoading.value = true
      const response = await apiClient.get('/bots', {
        params: { category_id: categoryId }
      })
      bots.value = response.data
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка при загрузке ботов'
    } finally {
      isLoading.value = false
    }
  }

  const fetchBot = async (id: number) => {
    try {
      isLoading.value = true
      const response = await apiClient.get(`/bots/${id}`)
      selectedBot.value = response.data
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка при загрузке бота'
    } finally {
      isLoading.value = false
    }
  }

  const fetchCategories = async () => {
    try {
      isLoading.value = true
      const response = await apiClient.get('/bot-categories')
      categories.value = response.data
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка при загрузке категорий'
    } finally {
      isLoading.value = false
    }
  }

  const fetchUserSubscriptions = async () => {
    try {
      isLoading.value = true
      const response = await apiClient.get('/user/subscriptions')
      userSubscriptions.value = response.data
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка при загрузке подписок'
    } finally {
      isLoading.value = false
    }
  }

  const purchaseBot = async (botId: number) => {
    try {
      isLoading.value = true
      const response = await apiClient.post(`/bots/${botId}/purchase`)
      await fetchUserSubscriptions()
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка при покупке бота'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const submitReview = async (botId: number, data: { rating: number; comment: string }) => {
    try {
      isLoading.value = true
      const response = await apiClient.post(`/bots/${botId}/reviews`, data)
      await fetchBot(botId)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка при отправке отзыва'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const reportBug = async (botId: number, data: { title: string; description: string }) => {
    try {
      isLoading.value = true
      const response = await apiClient.post(`/bots/${botId}/bugs`, data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Ошибка при отправке баг-репорта'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  return {
    bots,
    categories,
    selectedBot,
    userSubscriptions,
    isLoading,
    error,
    fetchBots,
    fetchBot,
    fetchCategories,
    fetchUserSubscriptions,
    purchaseBot,
    submitReview,
    reportBug
  }
}) 