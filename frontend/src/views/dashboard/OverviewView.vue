<template>
  <div class="overview-view">
    <el-card class="overview-card">
      <template #header>
        <div class="card-header">
          <h2>Overview</h2>
        </div>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="8">
          <el-card shadow="hover">
            <template #header>
              <div class="stat-header">
                <span>Total Projects</span>
              </div>
            </template>
            <div class="stat-value">{{ stats.totalProjects }}</div>
          </el-card>
        </el-col>
        
        <el-col :span="8">
          <el-card shadow="hover">
            <template #header>
              <div class="stat-header">
                <span>Active Tasks</span>
              </div>
            </template>
            <div class="stat-value">{{ stats.activeTasks }}</div>
          </el-card>
        </el-col>
        
        <el-col :span="8">
          <el-card shadow="hover">
            <template #header>
              <div class="stat-header">
                <span>Team Members</span>
              </div>
            </template>
            <div class="stat-value">{{ stats.teamMembers }}</div>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="20" class="mt-4">
        <el-col :span="12">
          <el-card shadow="hover">
            <template #header>
              <div class="card-header">
                <h3>Recent Projects</h3>
              </div>
            </template>
            <el-table :data="recentProjects" style="width: 100%">
              <el-table-column prop="name" label="Name" />
              <el-table-column prop="status" label="Status">
                <template #default="{ row }">
                  <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="progress" label="Progress">
                <template #default="{ row }">
                  <el-progress :percentage="row.progress" />
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>
        
        <el-col :span="12">
          <el-card shadow="hover">
            <template #header>
              <div class="card-header">
                <h3>Recent Tasks</h3>
              </div>
            </template>
            <el-table :data="recentTasks" style="width: 100%">
              <el-table-column prop="title" label="Title" />
              <el-table-column prop="status" label="Status">
                <template #default="{ row }">
                  <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="due_date" label="Due Date">
                <template #default="{ row }">
                  {{ formatDate(row.due_date) }}
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useProjectStore } from '@/stores/project'
import { useTaskStore } from '@/stores/task'
import { useUserStore } from '@/stores/user'
import { formatDate } from '@/utils/date'

const projectStore = useProjectStore()
const taskStore = useTaskStore()
const userStore = useUserStore()

const stats = ref({
  totalProjects: 0,
  activeTasks: 0,
  teamMembers: 0
})

const recentProjects = ref([])
const recentTasks = ref([])

const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    'active': 'success',
    'completed': 'info',
    'on_hold': 'warning',
    'cancelled': 'danger'
  }
  return types[status.toLowerCase()] || 'info'
}

const fetchData = async () => {
  try {
    // Fetch projects
    const projects = await projectStore.fetchProjects()
    stats.value.totalProjects = projects.length
    recentProjects.value = projects.slice(0, 5).map(project => ({
      ...project,
      progress: Math.floor(Math.random() * 100) // Replace with actual progress calculation
    }))

    // Fetch tasks
    const tasks = await taskStore.fetchTasks()
    stats.value.activeTasks = tasks.filter(task => task.status === 'active').length
    recentTasks.value = tasks.slice(0, 5)

    // Fetch users
    const users = await userStore.fetchUsers()
    stats.value.teamMembers = users.length
  } catch (error) {
    console.error('Error fetching overview data:', error)
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped lang="scss">
.overview-view {
  padding: 20px;

  .overview-card {
    margin-bottom: 20px;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    h2, h3 {
      margin: 0;
    }
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

  .mt-4 {
    margin-top: 20px;
  }
}
</style> 