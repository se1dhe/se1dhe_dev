<template>
  <div class="bot-list">
    <div class="bot-list-header">
      <h1>Телеграм боты</h1>
      <div class="filters">
        <div class="search-box">
          <i class="fas fa-search"></i>
          <input 
            type="text" 
            v-model="searchQuery"
            placeholder="Поиск ботов..."
            @input="handleSearch"
          >
        </div>
        <div class="category-filter">
          <select v-model="selectedCategory" @change="handleCategoryChange">
            <option value="">Все категории</option>
            <option 
              v-for="category in categories" 
              :key="category.id" 
              :value="category.id"
            >
              {{ category.name }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <div class="bot-grid" v-if="!isLoading">
      <div 
        v-for="bot in filteredBots" 
        :key="bot.id" 
        class="bot-card"
        @click="navigateToBot(bot.id)"
      >
        <div class="bot-image">
          <img :src="bot.images[0]" :alt="bot.name">
          <div v-if="bot.discount" class="discount-badge">
            -{{ bot.discount }}%
          </div>
        </div>
        <div class="bot-info">
          <h3>{{ bot.name }}</h3>
          <p class="description">{{ bot.description }}</p>
          <div class="features">
            <span 
              v-for="feature in bot.features.slice(0, 3)" 
              :key="feature"
              class="feature-tag"
            >
              {{ feature }}
            </span>
          </div>
          <div class="bot-footer">
            <div class="price">
              <span class="current-price">
                {{ formatPrice(bot.price, bot.discount) }}
              </span>
              <span v-if="bot.discount" class="original-price">
                {{ formatPrice(bot.price) }}
              </span>
            </div>
            <div class="rating">
              <i class="fas fa-star"></i>
              <span>{{ bot.rating.toFixed(1) }}</span>
              <span class="reviews-count">({{ bot.reviews_count }})</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="loading-state">
      <i class="fas fa-circle-notch fa-spin"></i>
      <p>Загрузка ботов...</p>
    </div>

    <div v-if="!isLoading && filteredBots.length === 0" class="empty-state">
      <i class="fas fa-robot"></i>
      <p>Боты не найдены</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBotStore } from '@/stores/bot'
import type { Bot } from '@/types/bot'

const router = useRouter()
const botStore = useBotStore()
const searchQuery = ref('')
const selectedCategory = ref<number | ''>('')

const isLoading = computed(() => botStore.isLoading)
const categories = computed(() => botStore.categories)
const bots = computed(() => botStore.bots)

const filteredBots = computed(() => {
  return bots.value.filter(bot => {
    const matchesSearch = bot.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         bot.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesCategory = !selectedCategory.value || bot.category_id === selectedCategory.value
    return matchesSearch && matchesCategory
  })
})

const handleSearch = () => {
  // Debounce search if needed
}

const handleCategoryChange = () => {
  botStore.fetchBots(selectedCategory.value as number)
}

const navigateToBot = (id: number) => {
  router.push(`/bots/${id}`)
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

onMounted(async () => {
  await Promise.all([
    botStore.fetchBots(),
    botStore.fetchCategories()
  ])
})
</script>

<style scoped>
.bot-list {
  padding: var(--space-6);
}

.bot-list-header {
  margin-bottom: var(--space-8);
}

.bot-list-header h1 {
  font-size: var(--font-size-3xl);
  margin-bottom: var(--space-6);
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.filters {
  display: flex;
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.search-box {
  position: relative;
  flex: 1;
  max-width: 400px;
}

.search-box i {
  position: absolute;
  left: var(--space-4);
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-tertiary);
}

.search-box input {
  width: 100%;
  padding: var(--space-3) var(--space-4) var(--space-3) var(--space-10);
  background: var(--bg-elevated);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-lg);
  color: var(--text-primary);
  transition: all var(--transition-fast);
}

.search-box input:focus {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-glow);
}

.category-filter select {
  padding: var(--space-3) var(--space-4);
  background: var(--bg-elevated);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-lg);
  color: var(--text-primary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.category-filter select:focus {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-glow);
}

.bot-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--space-6);
}

.bot-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-xl);
  overflow: hidden;
  transition: all var(--transition-fast);
  cursor: pointer;
}

.bot-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.bot-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.bot-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition-fast);
}

.bot-card:hover .bot-image img {
  transform: scale(1.05);
}

.discount-badge {
  position: absolute;
  top: var(--space-4);
  right: var(--space-4);
  background: var(--status-error);
  color: var(--text-primary);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-lg);
  font-weight: var(--font-weight-bold);
}

.bot-info {
  padding: var(--space-6);
}

.bot-info h3 {
  font-size: var(--font-size-xl);
  margin-bottom: var(--space-2);
}

.description {
  color: var(--text-secondary);
  margin-bottom: var(--space-4);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.features {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin-bottom: var(--space-4);
}

.feature-tag {
  background: var(--bg-elevated);
  color: var(--text-secondary);
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
}

.bot-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.current-price {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
}

.original-price {
  font-size: var(--font-size-sm);
  color: var(--text-tertiary);
  text-decoration: line-through;
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

.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-12);
  color: var(--text-tertiary);
}

.loading-state i,
.empty-state i {
  font-size: var(--font-size-4xl);
  margin-bottom: var(--space-4);
}

@media (max-width: 768px) {
  .filters {
    flex-direction: column;
  }
  
  .search-box {
    max-width: none;
  }
  
  .bot-grid {
    grid-template-columns: 1fr;
  }
}
</style> 