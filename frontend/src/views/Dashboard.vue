<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <h1>Добро пожаловать, {{ user?.name }}!</h1>
      <p class="text-secondary">Ваша панель управления</p>
    </header>

    <div class="stats-grid">
      <div class="stat-card" v-for="stat in stats" :key="stat.id">
        <div class="stat-icon" :class="stat.color">
          <i :class="stat.icon"></i>
        </div>
        <div class="stat-content">
          <h3>{{ stat.title }}</h3>
          <div class="stat-value">{{ stat.value }}</div>
          <div class="stat-change" :class="stat.trend > 0 ? 'positive' : 'negative'">
            <i :class="stat.trend > 0 ? 'fas fa-arrow-up' : 'fas fa-arrow-down'"></i>
            {{ Math.abs(stat.trend) }}% с прошлой недели
          </div>
        </div>
      </div>
    </div>

    <div class="recent-tasks">
      <div class="card">
        <div class="card-header">
          <h2>Недавние задачи</h2>
          <router-link to="/tasks" class="btn-secondary">
            Все задачи
            <i class="fas fa-arrow-right"></i>
          </router-link>
        </div>

        <div v-if="isLoading" class="loading-spinner">
          <i class="fas fa-spinner fa-spin"></i>
          Загрузка...
        </div>

        <div v-else-if="error" class="error-message">
          <i class="fas fa-exclamation-circle"></i>
          {{ error }}
        </div>

        <div v-else class="task-list">
          <div v-for="task in recentTasks" :key="task.id" class="task-item">
            <div class="task-status" :class="task.status">
              <i :class="getStatusIcon(task.status)"></i>
            </div>
            <div class="task-content">
              <h4>{{ task.title }}</h4>
              <p>{{ task.description }}</p>
              <div class="task-meta">
                <span class="task-date">
                  <i class="far fa-calendar"></i>
                  {{ formatDate(task.due_date) }}
                </span>
                <span class="task-priority" :class="task.priority">
                  {{ task.priority }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores'
import { apiClient } from '@/api'
import { formatDistanceToNow } from 'date-fns'
import { ru } from 'date-fns/locale'
import { Task, TaskStatus, DashboardStats } from '@/types/task'

const authStore = useAuthStore()
const user = computed(() => authStore.user)

const isLoading = ref(true)
const error = ref<string | null>(null)
const recentTasks = ref<Task[]>([])
const stats = ref([
  {
    id: 1,
    title: 'Активные задачи',
    value: 0,
    trend: 0,
    icon: 'fas fa-tasks',
    color: 'blue'
  },
  {
    id: 2,
    title: 'Завершенные задачи',
    value: 0,
    trend: 0,
    icon: 'fas fa-check-circle',
    color: 'green'
  },
  {
    id: 3,
    title: 'Часы работы',
    value: '0',
    trend: 0,
    icon: 'fas fa-clock',
    color: 'purple'
  },
  {
    id: 4,
    title: 'Эффективность',
    value: '0%',
    trend: 0,
    icon: 'fas fa-chart-line',
    color: 'orange'
  }
])

const fetchDashboardData = async () => {
  try {
    isLoading.value = true
    error.value = null

    // Fetch stats
    const statsResponse = await apiClient.get('/dashboard/stats')
    const statsData = statsResponse.data

    stats.value = [
      {
        id: 1,
        title: 'Активные задачи',
        value: statsData.active_tasks,
        trend: statsData.active_tasks_trend,
        icon: 'fas fa-tasks',
        color: 'blue'
      },
      {
        id: 2,
        title: 'Завершенные задачи',
        value: statsData.completed_tasks,
        trend: statsData.completed_tasks_trend,
        icon: 'fas fa-check-circle',
        color: 'green'
      },
      {
        id: 3,
        title: 'Часы работы',
        value: `${statsData.work_hours}ч`,
        trend: statsData.work_hours_trend,
        icon: 'fas fa-clock',
        color: 'purple'
      },
      {
        id: 4,
        title: 'Эффективность',
        value: `${statsData.efficiency}%`,
        trend: statsData.efficiency_trend,
        icon: 'fas fa-chart-line',
        color: 'orange'
      }
    ]

    // Fetch recent tasks
    const tasksResponse = await apiClient.get('/tasks/recent')
    recentTasks.value = tasksResponse.data

  } catch (err) {
    error.value = 'Ошибка при загрузке данных'
    console.error('Dashboard data fetch error:', err)
  } finally {
    isLoading.value = false
  }
}

const getStatusIcon = (status: TaskStatus) => {
  const icons: Record<TaskStatus, string> = {
    'pending': 'fas fa-clock',
    'in_progress': 'fas fa-spinner',
    'completed': 'fas fa-check',
    'cancelled': 'fas fa-times'
  }
  return icons[status]
}

const formatDate = (date: string) => {
  return formatDistanceToNow(new Date(date), { addSuffix: true, locale: ru })
}

onMounted(() => {
  fetchDashboardData()
})
</script>

<style scoped>
.dashboard {
  padding: var(--spacing-8);
}

.dashboard-header {
  margin-bottom: var(--spacing-8);
}

.dashboard-header h1 {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: var(--spacing-2);
}

.text-secondary {
  color: var(--text-secondary);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: var(--spacing-6);
  margin-bottom: var(--spacing-8);
}

.stat-card {
  background: var(--bg-dark-secondary);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-6);
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-4);
  transition: transform var(--transition-fast);
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--border-radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.stat-icon.blue { background: rgba(59, 130, 246, 0.1); color: var(--primary); }
.stat-icon.green { background: rgba(34, 197, 94, 0.1); color: var(--success); }
.stat-icon.purple { background: rgba(139, 92, 246, 0.1); color: var(--accent); }
.stat-icon.orange { background: rgba(245, 158, 11, 0.1); color: var(--warning); }

.stat-content h3 {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: var(--spacing-2);
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: var(--spacing-2);
}

.stat-change {
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: var(--spacing-1);
}

.stat-change.positive { color: var(--success); }
.stat-change.negative { color: var(--error); }

.card {
  background: var(--bg-dark-secondary);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-6);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--spacing-6);
}

.card-header h2 {
  font-size: 1.25rem;
  font-weight: 600;
}

.btn-secondary {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  padding: var(--spacing-2) var(--spacing-4);
  border-radius: var(--border-radius-md);
  background: var(--bg-dark-tertiary);
  color: var(--text-primary);
  text-decoration: none;
  transition: all var(--transition-fast);
}

.btn-secondary:hover {
  background: var(--primary);
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
}

.task-item {
  display: flex;
  gap: var(--spacing-4);
  padding: var(--spacing-4);
  background: var(--bg-dark-tertiary);
  border-radius: var(--border-radius-lg);
  transition: transform var(--transition-fast);
}

.task-item:hover {
  transform: translateX(4px);
}

.task-status {
  width: 40px;
  height: 40px;
  border-radius: var(--border-radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.task-status.pending { background: rgba(245, 158, 11, 0.1); color: var(--warning); }
.task-status.in_progress { background: rgba(59, 130, 246, 0.1); color: var(--primary); }
.task-status.completed { background: rgba(34, 197, 94, 0.1); color: var(--success); }
.task-status.cancelled { background: rgba(239, 68, 68, 0.1); color: var(--error); }

.task-content {
  flex: 1;
}

.task-content h4 {
  font-size: 1rem;
  font-weight: 500;
  margin-bottom: var(--spacing-1);
}

.task-content p {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: var(--spacing-2);
}

.task-meta {
  display: flex;
  align-items: center;
  gap: var(--spacing-4);
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.task-date {
  display: flex;
  align-items: center;
  gap: var(--spacing-1);
}

.task-priority {
  padding: var(--spacing-1) var(--spacing-2);
  border-radius: var(--border-radius-sm);
  text-transform: capitalize;
}

.task-priority.high { background: rgba(239, 68, 68, 0.1); color: var(--priority-high); }
.task-priority.medium { background: rgba(245, 158, 11, 0.1); color: var(--priority-medium); }
.task-priority.low { background: rgba(34, 197, 94, 0.1); color: var(--priority-low); }

.loading-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-2);
  padding: var(--spacing-8);
  color: var(--text-secondary);
}

.error-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-2);
  padding: var(--spacing-8);
  color: var(--error);
}

@media (max-width: 768px) {
  .dashboard {
    padding: var(--spacing-4);
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .task-item {
    flex-direction: column;
  }

  .task-status {
    width: 32px;
    height: 32px;
    font-size: 1rem;
  }
}
</style> 