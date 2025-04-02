<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <div class="welcome-section">
        <h1>Добро пожаловать, {{ user?.name }}</h1>
        <p class="subtitle">Управляйте вашими ботами и отслеживайте статистику</p>
      </div>
      
      <div class="stats-cards">
        <div class="stat-card">
          <div class="stat-icon">
            <i class="fas fa-robot"></i>
          </div>
          <div class="stat-info">
            <span class="stat-value">{{ activeSubscriptions.length }}</span>
            <span class="stat-label">Активные боты</span>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <i class="fas fa-clock"></i>
          </div>
          <div class="stat-info">
            <span class="stat-value">{{ totalUsageTime }}</span>
            <span class="stat-label">Общее время использования</span>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <i class="fas fa-users"></i>
          </div>
          <div class="stat-info">
            <span class="stat-value">{{ totalUsers }}</span>
            <span class="stat-label">Пользователей обработано</span>
          </div>
        </div>
      </div>
    </div>

    <div class="dashboard-content">
      <div class="section-header">
        <h2>Мои боты</h2>
        <router-link to="/bots" class="btn btn-primary">
          <i class="fas fa-plus"></i>
          Добавить бота
        </router-link>
      </div>

      <div v-if="isLoading" class="loading-state">
        <i class="fas fa-circle-notch fa-spin"></i>
        <p>Загрузка ботов...</p>
      </div>

      <div v-else-if="activeSubscriptions.length === 0" class="empty-state">
        <i class="fas fa-robot"></i>
        <h3>У вас пока нет ботов</h3>
        <p>Выберите и приобретите бота из нашего каталога</p>
        <router-link to="/bots" class="btn btn-primary">
          Перейти в каталог
        </router-link>
      </div>

      <div v-else class="bots-grid">
        <div v-for="sub in activeSubscriptions" :key="sub.id" class="bot-card">
          <div class="bot-header">
            <img :src="sub.bot.images[0]" :alt="sub.bot.name">
            <div class="bot-status" :class="{ active: sub.status === 'active' }">
              {{ sub.status === 'active' ? 'Активен' : 'Неактивен' }}
            </div>
          </div>

          <div class="bot-info">
            <h3>{{ sub.bot.name }}</h3>
            <p class="description">{{ sub.bot.description }}</p>
            
            <div class="bot-stats">
              <div class="stat">
                <i class="fas fa-users"></i>
                <span>{{ sub.stats.users_count }} польз.</span>
              </div>
              <div class="stat">
                <i class="fas fa-clock"></i>
                <span>{{ formatUptime(sub.stats.uptime) }}</span>
              </div>
            </div>

            <div class="subscription-info">
              <div class="date-info">
                <span>Активен до:</span>
                <strong>{{ formatDate(sub.end_date) }}</strong>
              </div>
              <button 
                class="btn btn-secondary"
                @click="showBotDetails(sub.bot.id)"
              >
                Управление
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useBotStore } from '@/stores/bot'
import type { BotSubscription } from '@/types/bot'

const router = useRouter()
const authStore = useAuthStore()
const botStore = useBotStore()

const user = computed(() => authStore.user)
const isLoading = computed(() => botStore.isLoading)
const activeSubscriptions = computed(() => 
  botStore.userSubscriptions.filter(sub => sub.status === 'active')
)

const totalUsageTime = computed(() => {
  const totalSeconds = activeSubscriptions.value.reduce((acc, sub) => {
    return acc + (sub.stats?.uptime || 0)
  }, 0)
  return formatUptime(totalSeconds)
})

const totalUsers = computed(() => {
  return activeSubscriptions.value.reduce((acc, sub) => {
    return acc + (sub.stats?.users_count || 0)
  }, 0)
})

const formatUptime = (seconds: number) => {
  const days = Math.floor(seconds / (24 * 3600))
  const hours = Math.floor((seconds % (24 * 3600)) / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)

  if (days > 0) {
    return days + 'д ' + hours + 'ч'
  }
  if (hours > 0) {
    return hours + 'ч ' + minutes + 'м'
  }
  return minutes + 'м'
}

const formatDate = (date: string) => {
  return new Intl.DateTimeFormat('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  }).format(new Date(date))
}

const showBotDetails = (botId: number) => {
  router.push('/dashboard/bots/' + botId)
}

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  await botStore.fetchUserSubscriptions()
})
</script>

<style scoped>
.dashboard {
  padding: var(--space-6);
  min-height: 100vh;
  background: var(--bg-base);
}

.dashboard-header {
  margin-bottom: var(--space-8);
}

.welcome-section {
  margin-bottom: var(--space-8);
}

.welcome-section h1 {
  font-size: var(--font-size-3xl);
  margin-bottom: var(--space-2);
}

.subtitle {
  color: var(--text-secondary);
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--space-4);
  margin-bottom: var(--space-8);
}

.stat-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  background: var(--bg-elevated);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-primary);
  font-size: var(--font-size-2xl);
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
}

.stat-label {
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-6);
}

.section-header h2 {
  font-size: var(--font-size-2xl);
}

.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-12);
  text-align: center;
  background: var(--bg-surface);
  border-radius: var(--radius-xl);
  border: 1px solid var(--border-primary);
}

.loading-state i,
.empty-state i {
  font-size: var(--font-size-4xl);
  color: var(--text-tertiary);
  margin-bottom: var(--space-4);
}

.empty-state h3 {
  margin-bottom: var(--space-2);
}

.empty-state p {
  margin-bottom: var(--space-6);
  color: var(--text-secondary);
}

.bots-grid {
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
}

.bot-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.bot-header {
  position: relative;
  height: 160px;
}

.bot-header img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.bot-status {
  position: absolute;
  top: var(--space-4);
  right: var(--space-4);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  background: var(--bg-elevated);
  color: var(--text-secondary);
}

.bot-status.active {
  background: var(--status-success);
  color: white;
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

.bot-stats {
  display: flex;
  gap: var(--space-4);
  margin-bottom: var(--space-4);
}

.stat {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.subscription-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: var(--space-4);
  border-top: 1px solid var(--border-primary);
}

.date-info {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.date-info span {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.date-info strong {
  color: var(--text-primary);
}

@media (max-width: 768px) {
  .dashboard {
    padding: var(--space-4);
  }
  
  .stats-cards {
    grid-template-columns: 1fr;
  }
  
  .bots-grid {
    grid-template-columns: 1fr;
  }
}
</style> 