<template>
  <div class="bot-detail" v-if="bot">
    <div class="bot-header">
      <div class="bot-gallery">
        <div class="main-image">
          <img :src="currentImage" :alt="bot.name">
          <div v-if="bot.discount" class="discount-badge">
            -{{ bot.discount }}%
          </div>
        </div>
        <div class="thumbnail-list">
          <div 
            v-for="(image, index) in bot.images" 
            :key="index"
            class="thumbnail"
            :class="{ active: currentImageIndex === index }"
            @click="currentImageIndex = index"
          >
            <img :src="image" :alt="bot.name">
          </div>
        </div>
      </div>

      <div class="bot-info">
        <div class="bot-title">
          <h1>{{ bot.name }}</h1>
          <div class="rating">
            <i class="fas fa-star"></i>
            <span>{{ bot.rating.toFixed(1) }}</span>
            <span class="reviews-count">({{ bot.reviews_count }} отзывов)</span>
          </div>
        </div>

        <div class="price-section">
          <div class="price">
            <span class="current-price">
              {{ formatPrice(bot.price, bot.discount) }}
            </span>
            <span v-if="bot.discount" class="original-price">
              {{ formatPrice(bot.price) }}
            </span>
          </div>
          <div class="sales-count">
            <i class="fas fa-shopping-cart"></i>
            <span>{{ bot.sales_count }} продаж</span>
          </div>
        </div>

        <div class="features">
          <h3>Основные функции</h3>
          <ul>
            <li v-for="feature in bot.features" :key="feature">
              <i class="fas fa-check"></i>
              {{ feature }}
            </li>
          </ul>
        </div>

        <div class="actions">
          <button 
            class="btn-primary"
            @click="handlePurchase"
            :disabled="isLoading || hasActiveSubscription"
          >
            <i class="fas fa-shopping-cart"></i>
            {{ hasActiveSubscription ? 'Уже куплено' : 'Купить сейчас' }}
          </button>
          <button 
            class="btn-secondary"
            @click="showReportBugModal = true"
          >
            <i class="fas fa-bug"></i>
            Сообщить о проблеме
          </button>
        </div>
      </div>
    </div>

    <div class="bot-content">
      <div class="tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          class="tab-button"
          :class="{ active: activeTab === tab.id }"
          @click="activeTab = tab.id"
        >
          {{ tab.name }}
        </button>
      </div>

      <div class="tab-content">
        <div v-if="activeTab === 'description'" class="description">
          <div class="readme" v-html="formattedReadme"></div>
        </div>

        <div v-if="activeTab === 'reviews'" class="reviews">
          <div class="reviews-header">
            <div class="rating-summary">
              <div class="average-rating">
                <span class="rating-number">{{ bot.rating.toFixed(1) }}</span>
                <div class="stars">
                  <i 
                    v-for="n in 5" 
                    :key="n"
                    class="fas fa-star"
                    :class="{ filled: n <= Math.round(bot.rating) }"
                  ></i>
                </div>
                <span class="reviews-count">{{ bot.reviews_count }} отзывов</span>
              </div>
            </div>
            <button 
              class="btn-primary"
              @click="showReviewModal = true"
              v-if="hasActiveSubscription"
            >
              <i class="fas fa-star"></i>
              Оставить отзыв
            </button>
          </div>

          <div class="reviews-list">
            <div v-if="bot.reviews?.length" class="review-card" v-for="review in bot.reviews" :key="review.id">
              <div class="review-header">
                <div class="user-info">
                  <img :src="review.user.avatar" :alt="review.user.name" class="user-avatar">
                  <span class="user-name">{{ review.user.name }}</span>
                </div>
                <div class="review-rating">
                  <i 
                    v-for="n in 5" 
                    :key="n"
                    class="fas fa-star"
                    :class="{ filled: n <= review.rating }"
                  ></i>
                </div>
              </div>
              <p class="review-comment">{{ review.comment }}</p>
              <span class="review-date">{{ formatDate(review.created_at) }}</span>
            </div>
            <div v-else class="empty-reviews">
              <i class="fas fa-comments"></i>
              <p>Пока нет отзывов</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальные окна -->
    <div v-if="showReviewModal" class="modal">
      <div class="modal-content">
        <h2>Оставить отзыв</h2>
        <form @submit.prevent="handleSubmitReview">
          <div class="rating-input">
            <i 
              v-for="n in 5" 
              :key="n"
              class="fas fa-star"
              :class="{ filled: n <= reviewForm.rating }"
              @click="reviewForm.rating = n"
            ></i>
          </div>
          <textarea 
            v-model="reviewForm.comment"
            placeholder="Опишите ваш опыт использования бота..."
            required
          ></textarea>
          <div class="modal-actions">
            <button type="button" class="btn-secondary" @click="showReviewModal = false">
              Отмена
            </button>
            <button type="submit" class="btn-primary" :disabled="isLoading">
              Отправить
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showReportBugModal" class="modal">
      <div class="modal-content">
        <h2>Сообщить о проблеме</h2>
        <form @submit.prevent="handleSubmitBug">
          <div class="form-group">
            <label>Заголовок</label>
            <input 
              v-model="bugForm.title"
              type="text"
              placeholder="Краткое описание проблемы"
              required
            >
          </div>
          <div class="form-group">
            <label>Описание</label>
            <textarea 
              v-model="bugForm.description"
              placeholder="Подробно опишите проблему..."
              required
            ></textarea>
          </div>
          <div class="modal-actions">
            <button type="button" class="btn-secondary" @click="showReportBugModal = false">
              Отмена
            </button>
            <button type="submit" class="btn-primary" :disabled="isLoading">
              Отправить
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <div v-else-if="isLoading" class="loading-state">
    <i class="fas fa-circle-notch fa-spin"></i>
    <p>Загрузка информации о боте...</p>
  </div>

  <div v-else class="error-state">
    <i class="fas fa-exclamation-circle"></i>
    <p>Бот не найден</p>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBotStore } from '@/stores/bot'
import { useAuthStore } from '@/stores/auth'
import type { Bot } from '@/types/bot'
import { marked } from 'marked'

const route = useRoute()
const router = useRouter()
const botStore = useBotStore()
const authStore = useAuthStore()

const bot = computed(() => botStore.selectedBot)
const isLoading = computed(() => botStore.isLoading)
const userSubscriptions = computed(() => botStore.userSubscriptions)

const currentImageIndex = ref(0)
const currentImage = computed(() => bot.value?.images[currentImageIndex.value] || '')
const activeTab = ref('description')
const showReviewModal = ref(false)
const showReportBugModal = ref(false)

const tabs = [
  { id: 'description', name: 'Описание' },
  { id: 'reviews', name: 'Отзывы' }
]

const reviewForm = ref({
  rating: 5,
  comment: ''
})

const bugForm = ref({
  title: '',
  description: ''
})

const hasActiveSubscription = computed(() => {
  return userSubscriptions.value.some(
    sub => sub.bot_id === bot.value?.id && sub.status === 'active'
  )
})

const formattedReadme = computed(() => {
  return marked(bot.value?.readme || '')
})

const handlePurchase = async () => {
  if (!authStore.isAuthenticated) {
    router.push('/auth/login')
    return
  }

  try {
    await botStore.purchaseBot(bot.value!.id)
    router.push('/dashboard')
  } catch (error) {
    console.error('Purchase failed:', error)
  }
}

const handleSubmitReview = async () => {
  try {
    await botStore.submitReview(bot.value!.id, reviewForm.value)
    showReviewModal.value = false
    reviewForm.value = { rating: 5, comment: '' }
  } catch (error) {
    console.error('Review submission failed:', error)
  }
}

const handleSubmitBug = async () => {
  try {
    await botStore.reportBug(bot.value!.id, bugForm.value)
    showReportBugModal.value = false
    bugForm.value = { title: '', description: '' }
  } catch (error) {
    console.error('Bug report submission failed:', error)
  }
}

const formatPrice = (price: number, discount?: number) => {
  if (discount) {
    price = price * (1 - discount / 100)
  }
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB'
  }).format(price)
}

const formatDate = (date: string) => {
  return new Intl.DateTimeFormat('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(new Date(date))
}

onMounted(async () => {
  const botId = Number(route.params.id)
  if (isNaN(botId)) {
    router.push('/bots')
    return
  }

  await Promise.all([
    botStore.fetchBot(botId),
    botStore.fetchUserSubscriptions()
  ])
})
</script>

<style scoped>
.bot-detail {
  padding: var(--space-6);
}

.bot-header {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-8);
  margin-bottom: var(--space-8);
}

.bot-gallery {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.main-image {
  position: relative;
  aspect-ratio: 16/9;
  border-radius: var(--radius-xl);
  overflow: hidden;
}

.main-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.thumbnail-list {
  display: flex;
  gap: var(--space-2);
  overflow-x: auto;
  padding-bottom: var(--space-2);
}

.thumbnail {
  width: 80px;
  height: 60px;
  border-radius: var(--radius-lg);
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all var(--transition-fast);
}

.thumbnail.active {
  border-color: var(--color-primary);
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.bot-info {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.bot-title {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.bot-title h1 {
  font-size: var(--font-size-3xl);
  margin: 0;
}

.rating {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  color: var(--accent-yellow);
}

.reviews-count {
  color: var(--text-tertiary);
  font-size: var(--font-size-sm);
}

.price-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-4);
  background: var(--bg-elevated);
  border-radius: var(--radius-lg);
}

.price {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.current-price {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
}

.original-price {
  font-size: var(--font-size-sm);
  color: var(--text-tertiary);
  text-decoration: line-through;
}

.sales-count {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  color: var(--text-secondary);
}

.features {
  background: var(--bg-elevated);
  padding: var(--space-4);
  border-radius: var(--radius-lg);
}

.features h3 {
  margin-bottom: var(--space-4);
}

.features ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-3);
}

.features li {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  color: var(--text-secondary);
}

.features li i {
  color: var(--status-success);
}

.actions {
  display: flex;
  gap: var(--space-4);
}

.bot-content {
  background: var(--bg-elevated);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
}

.tabs {
  display: flex;
  gap: var(--space-4);
  margin-bottom: var(--space-6);
  border-bottom: 1px solid var(--border-primary);
  padding-bottom: var(--space-4);
}

.tab-button {
  padding: var(--space-2) var(--space-4);
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  position: relative;
}

.tab-button.active {
  color: var(--text-primary);
}

.tab-button.active::after {
  content: '';
  position: absolute;
  bottom: calc(-1 * var(--space-4));
  left: 0;
  width: 100%;
  height: 2px;
  background: var(--color-primary);
}

.tab-content {
  min-height: 400px;
}

.description {
  color: var(--text-secondary);
}

.readme {
  line-height: 1.6;
}

.readme :deep(h1),
.readme :deep(h2),
.readme :deep(h3),
.readme :deep(h4),
.readme :deep(h5),
.readme :deep(h6) {
  color: var(--text-primary);
  margin: var(--space-4) 0 var(--space-2);
}

.readme :deep(p) {
  margin-bottom: var(--space-4);
}

.readme :deep(code) {
  background: var(--bg-surface);
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-sm);
  font-family: monospace;
}

.readme :deep(pre) {
  background: var(--bg-surface);
  padding: var(--space-4);
  border-radius: var(--radius-lg);
  overflow-x: auto;
  margin: var(--space-4) 0;
}

.readme :deep(ul),
.readme :deep(ol) {
  margin: var(--space-4) 0;
  padding-left: var(--space-4);
}

.readme :deep(li) {
  margin-bottom: var(--space-2);
}

.reviews-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-6);
}

.rating-summary {
  display: flex;
  align-items: center;
  gap: var(--space-6);
}

.average-rating {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
}

.rating-number {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
}

.stars {
  display: flex;
  gap: var(--space-1);
}

.stars i {
  color: var(--text-tertiary);
}

.stars i.filled {
  color: var(--accent-yellow);
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.review-card {
  background: var(--bg-surface);
  padding: var(--space-4);
  border-radius: var(--radius-lg);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-2);
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.user-name {
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
}

.review-rating {
  display: flex;
  gap: var(--space-1);
  color: var(--accent-yellow);
}

.review-comment {
  color: var(--text-secondary);
  margin-bottom: var(--space-2);
}

.review-date {
  font-size: var(--font-size-sm);
  color: var(--text-tertiary);
}

.empty-reviews {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-8);
  color: var(--text-tertiary);
}

.empty-reviews i {
  font-size: var(--font-size-4xl);
  margin-bottom: var(--space-4);
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: var(--bg-surface);
  padding: var(--space-6);
  border-radius: var(--radius-xl);
  width: 100%;
  max-width: 500px;
}

.modal-content h2 {
  margin-bottom: var(--space-4);
}

.form-group {
  margin-bottom: var(--space-4);
}

.form-group label {
  display: block;
  margin-bottom: var(--space-2);
  color: var(--text-secondary);
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: var(--space-3);
  background: var(--bg-elevated);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-lg);
  color: var(--text-primary);
}

.form-group textarea {
  min-height: 120px;
  resize: vertical;
}

.rating-input {
  display: flex;
  gap: var(--space-2);
  margin-bottom: var(--space-4);
}

.rating-input i {
  font-size: var(--font-size-2xl);
  color: var(--text-tertiary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.rating-input i.filled {
  color: var(--accent-yellow);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-4);
  margin-top: var(--space-6);
}

.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-12);
  color: var(--text-tertiary);
}

.loading-state i,
.error-state i {
  font-size: var(--font-size-4xl);
  margin-bottom: var(--space-4);
}

@media (max-width: 768px) {
  .bot-header {
    grid-template-columns: 1fr;
  }
  
  .actions {
    flex-direction: column;
  }
  
  .modal-content {
    margin: var(--space-4);
  }
}
</style> 