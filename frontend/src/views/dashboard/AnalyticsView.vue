<template>
  <div class="analytics-view">
    <el-card class="analytics-card">
      <template #header>
        <div class="card-header">
          <h2>Analytics</h2>
        </div>
      </template>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-card shadow="hover">
            <template #header>
              <div class="card-header">
                <h3>Project Status Distribution</h3>
              </div>
            </template>
            <div class="chart-container">
              <el-pie-chart :data="projectStatusData" />
            </div>
          </el-card>
        </el-col>

        <el-col :span="12">
          <el-card shadow="hover">
            <template #header>
              <div class="card-header">
                <h3>Task Completion Trend</h3>
              </div>
            </template>
            <div class="chart-container">
              <el-line-chart :data="taskCompletionData" />
            </div>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="20" class="mt-4">
        <el-col :span="24">
          <el-card shadow="hover">
            <template #header>
              <div class="card-header">
                <h3>Team Performance</h3>
              </div>
            </template>
            <el-table :data="teamPerformance" style="width: 100%">
              <el-table-column prop="name" label="Team Member" />
              <el-table-column prop="completed_tasks" label="Completed Tasks" />
              <el-table-column prop="in_progress" label="In Progress" />
              <el-table-column prop="overdue" label="Overdue" />
              <el-table-column prop="efficiency" label="Efficiency">
                <template #default="{ row }">
                  <el-progress :percentage="row.efficiency" />
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

const projectStore = useProjectStore()
const taskStore = useTaskStore()
const userStore = useUserStore()

const projectStatusData = ref([])
const taskCompletionData = ref([])
const teamPerformance = ref([])

const fetchData = async () => {
  try {
    // Fetch projects and calculate status distribution
    const projects = await projectStore.fetchProjects()
    const statusCounts = projects.reduce((acc: Record<string, number>, project) => {
      acc[project.status] = (acc[project.status] || 0) + 1
      return acc
    }, {})
    
    projectStatusData.value = Object.entries(statusCounts).map(([status, count]) => ({
      name: status,
      value: count
    }))

    // Fetch tasks and calculate completion trend
    const tasks = await taskStore.fetchTasks()
    const completionTrend = tasks.reduce((acc: Record<string, number>, task) => {
      const date = new Date(task.created_at).toLocaleDateString()
      acc[date] = (acc[date] || 0) + (task.status === 'completed' ? 1 : 0)
      return acc
    }, {})

    taskCompletionData.value = Object.entries(completionTrend).map(([date, count]) => ({
      date,
      value: count
    }))

    // Fetch users and calculate team performance
    const users = await userStore.fetchUsers()
    teamPerformance.value = users.map(user => ({
      name: user.name,
      completed_tasks: tasks.filter(t => t.assigned_to === user.id && t.status === 'completed').length,
      in_progress: tasks.filter(t => t.assigned_to === user.id && t.status === 'in_progress').length,
      overdue: tasks.filter(t => t.assigned_to === user.id && t.status === 'overdue').length,
      efficiency: Math.floor(Math.random() * 100) // Replace with actual efficiency calculation
    }))
  } catch (error) {
    console.error('Error fetching analytics data:', error)
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped lang="scss">
.analytics-view {
  padding: 20px;

  .analytics-card {
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

  .chart-container {
    height: 300px;
  }

  .mt-4 {
    margin-top: 20px;
  }
}
</style> 