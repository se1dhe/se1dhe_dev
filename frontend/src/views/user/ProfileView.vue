<template>
  <div class="profile">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>Profile</h2>
          <el-button type="primary" @click="handleEdit" plain>Edit Profile</el-button>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="Username">
          {{ user.username }}
        </el-descriptions-item>
        <el-descriptions-item label="Email">
          {{ user.email }}
        </el-descriptions-item>
        <el-descriptions-item label="First Name">
          {{ user.first_name }}
        </el-descriptions-item>
        <el-descriptions-item label="Last Name">
          {{ user.last_name }}
        </el-descriptions-item>
        <el-descriptions-item label="Created At">
          {{ formatDate(user.created_at) }}
        </el-descriptions-item>
        <el-descriptions-item label="Last Updated">
          {{ formatDate(user.updated_at) }}
        </el-descriptions-item>
      </el-descriptions>

      <div class="stats-section">
        <h3>Activity Statistics</h3>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card shadow="hover">
              <template #header>
                <div class="stat-header">
                  <span>Projects</span>
                </div>
              </template>
              <div class="stat-value">{{ stats.projects_count }}</div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover">
              <template #header>
                <div class="stat-header">
                  <span>Tasks</span>
                </div>
              </template>
              <div class="stat-value">{{ stats.tasks_count }}</div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover">
              <template #header>
                <div class="stat-header">
                  <span>Completed Tasks</span>
                </div>
              </template>
              <div class="stat-value">{{ stats.completed_tasks_count }}</div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <div class="recent-activity">
        <h3>Recent Activity</h3>
        <el-timeline>
          <el-timeline-item
            v-for="activity in recentActivity"
            :key="activity.id"
            :timestamp="formatDate(activity.created_at)"
            :type="getActivityType(activity.type)"
          >
            {{ activity.description }}
          </el-timeline-item>
        </el-timeline>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { formatDate } from '@/utils/date'

const router = useRouter()
const authStore = useAuthStore()

const user = ref(authStore.user)
const stats = ref({
  projects_count: 0,
  tasks_count: 0,
  completed_tasks_count: 0
})
const recentActivity = ref([])

const getActivityType = (type: string): 'primary' | 'success' | 'warning' | 'info' => {
  const types: Record<string, 'primary' | 'success' | 'warning' | 'info'> = {
    project_created: 'primary',
    project_updated: 'primary',
    task_created: 'success',
    task_completed: 'success',
    task_updated: 'warning',
    task_deleted: 'info'
  }
  return types[type] || 'info'
}

const fetchStats = async () => {
  try {
    // TODO: Implement API call to fetch user stats
    stats.value = {
      projects_count: 0,
      tasks_count: 0,
      completed_tasks_count: 0
    }
  } catch (error) {
    console.error('Error fetching user stats:', error)
    ElMessage.error('Failed to fetch user statistics')
  }
}

const fetchRecentActivity = async () => {
  try {
    // TODO: Implement API call to fetch user activity
    recentActivity.value = []
  } catch (error) {
    console.error('Error fetching recent activity:', error)
    ElMessage.error('Failed to fetch recent activity')
  }
}

const handleEdit = () => {
  router.push({ name: 'profile-edit' })
}

onMounted(() => {
  fetchStats()
  fetchRecentActivity()
})
</script>

<style scoped lang="scss">
.profile {
  padding: 20px;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    h2 {
      margin: 0;
    }
  }

  .stats-section {
    margin-top: 30px;

    h3 {
      margin-bottom: 20px;
    }

    .stat-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .stat-value {
      font-size: 24px;
      font-weight: bold;
      text-align: center;
      color: var(--el-color-primary);
    }
  }

  .recent-activity {
    margin-top: 30px;

    h3 {
      margin-bottom: 20px;
    }
  }
}
</style> 