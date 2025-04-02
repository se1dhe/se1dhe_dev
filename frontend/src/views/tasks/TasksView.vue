<template>
  <div class="tasks">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="mb-4">
          <template #header>
            <div class="card-header">
              <h2>Tasks</h2>
              <el-button type="primary" @click="router.push('/tasks/new')">
                New Task
              </el-button>
            </div>
          </template>
          
          <el-table
            v-loading="loading"
            :data="tasks"
            style="width: 100%"
          >
            <el-table-column prop="title" label="Title" />
            <el-table-column prop="status" label="Status">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="priority" label="Priority">
              <template #default="{ row }">
                <el-tag :type="getPriorityType(row.priority)">
                  {{ row.priority }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="due_date" label="Due Date">
              <template #default="{ row }">
                {{ formatDate(row.due_date) }}
              </template>
            </el-table-column>
            <el-table-column prop="project.name" label="Project">
              <template #default="{ row }">
                <el-link
                  v-if="row.project"
                  type="primary"
                  @click="router.push(`/projects/${row.project.id}`)"
                >
                  {{ row.project.name }}
                </el-link>
                <span v-else>N/A</span>
              </template>
            </el-table-column>
            <el-table-column label="Actions" width="200">
              <template #default="{ row }">
                <el-button-group>
                  <el-button
                    size="small"
                    @click="router.push(`/tasks/${row.id}`)"
                  >
                    View
                  </el-button>
                  <el-button
                    size="small"
                    type="primary"
                    @click="router.push(`/tasks/${row.id}/edit`)"
                  >
                    Edit
                  </el-button>
                </el-button-group>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTaskStore } from '@/stores/task'
import { formatDate } from '@/utils/date'

const router = useRouter()
const taskStore = useTaskStore()

const loading = ref(false)
const tasks = ref<Array<{
  id: number
  title: string
  description: string
  status: string
  priority: string
  project_id: number
  assigned_to: number
  created_by: number
  due_date: string
  created_at: string
  updated_at: string
  project?: {
    id: number
    name: string
    description: string
    status: string
    created_by: number
    created_at: string
    updated_at: string
  }
}>>([])

const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    todo: 'info',
    in_progress: 'warning',
    done: 'success'
  }
  return (types[status] || 'info') as 'success' | 'warning' | 'info' | 'primary' | 'danger'
}

const getPriorityType = (priority: string) => {
  const types: Record<string, string> = {
    low: 'info',
    medium: 'warning',
    high: 'danger'
  }
  return (types[priority] || 'info') as 'success' | 'warning' | 'info' | 'primary' | 'danger'
}

onMounted(async () => {
  loading.value = true
  try {
    await taskStore.fetchTasks()
    tasks.value = taskStore.tasks
  } catch (error) {
    console.error('Error fetching tasks:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style lang="scss" scoped>
.tasks {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}
</style> 