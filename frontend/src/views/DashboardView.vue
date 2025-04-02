<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>Дашборд</h1>
      <el-button type="primary" @click="refreshData">
        <el-icon><Refresh /></el-icon>
        Обновить
      </el-button>
    </div>

    <div class="dashboard-grid">
      <el-card class="dashboard-card">
        <template #header>
          <div class="card-header">
            <span>Проекты</span>
            <el-tag type="info">{{ projects.length }}</el-tag>
          </div>
        </template>
        <div class="card-content">
          <el-table :data="projects.slice(0, 5)" style="width: 100%">
            <el-table-column prop="name" label="Название" />
            <el-table-column prop="status" label="Статус">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-card>

      <el-card class="dashboard-card">
        <template #header>
          <div class="card-header">
            <span>Задачи</span>
            <el-tag type="info">{{ tasks.length }}</el-tag>
          </div>
        </template>
        <div class="card-content">
          <el-table :data="tasks.slice(0, 5)" style="width: 100%">
            <el-table-column prop="title" label="Название" />
            <el-table-column prop="status" label="Статус">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-card>

      <el-card class="dashboard-card">
        <template #header>
          <div class="card-header">
            <span>Пользователи</span>
            <el-tag type="info">{{ users.length }}</el-tag>
          </div>
        </template>
        <div class="card-content">
          <el-table :data="users.slice(0, 5)" style="width: 100%">
            <el-table-column prop="name" label="Имя" />
            <el-table-column prop="email" label="Email" />
            <el-table-column prop="role" label="Роль">
              <template #default="{ row }">
                <el-tag>{{ row.role }}</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { Refresh } from '@element-plus/icons-vue'
import { useProjectStore } from '@/stores'
import { useTaskStore } from '@/stores'
import { useUserStore } from '@/stores'
import { useUIStore } from '@/stores'
import { useNotificationStore } from '@/stores'

const projectStore = useProjectStore()
const taskStore = useTaskStore()
const userStore = useUserStore()
const uiStore = useUIStore()
const notificationStore = useNotificationStore()

const { projects } = projectStore
const { tasks } = taskStore
const { users } = userStore

async function refreshData() {
  uiStore.setLoading(true, 'Обновление данных...')
  try {
    await Promise.all([
      projectStore.fetchProjects(),
      taskStore.fetchTasks(),
      userStore.fetchUsers()
    ])
    notificationStore.showSuccess('Данные успешно обновлены')
  } catch (error) {
    console.error('Error refreshing data:', error)
    notificationStore.showError('Ошибка при обновлении данных')
  } finally {
    uiStore.setLoading(false)
  }
}

function getStatusType(status: string): 'success' | 'warning' | 'info' | 'danger' | 'primary' {
  switch (status.toLowerCase()) {
    case 'active':
    case 'completed':
      return 'success'
    case 'pending':
      return 'warning'
    case 'cancelled':
      return 'danger'
    default:
      return 'info'
  }
}

onMounted(() => {
  refreshData()
})
</script>

<style lang="scss" scoped>
.dashboard {
  &-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-lg);
  }

  &-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: var(--spacing-lg);
  }
}

.dashboard-card {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .card-content {
    min-height: 200px;
  }
}
</style> 