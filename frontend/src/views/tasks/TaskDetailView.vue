<template>
  <div class="task-detail">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card v-loading="loading">
          <template #header>
            <div class="card-header">
              <h2>{{ task?.title }}</h2>
              <el-button-group>
                <el-button
                  type="primary"
                  @click="router.push(`/tasks/${task?.id}/edit`)"
                >
                  Edit
                </el-button>
                <el-button
                  type="danger"
                  @click="handleDelete"
                >
                  Delete
                </el-button>
              </el-button-group>
            </div>
          </template>

          <div v-if="task" class="task-info">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="Status">
                <el-tag :type="getStatusType(task.status)">
                  {{ task.status }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="Priority">
                <el-tag :type="getPriorityType(task.priority)">
                  {{ task.priority }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="Due Date">
                {{ formatDate(task.due_date) }}
              </el-descriptions-item>
              <el-descriptions-item label="Project">
                <el-link
                  v-if="task.project"
                  type="primary"
                  @click="router.push(`/projects/${task.project.id}`)"
                >
                  {{ task.project.name }}
                </el-link>
                <span v-else>N/A</span>
              </el-descriptions-item>
              <el-descriptions-item label="Created At">
                {{ formatDate(task.created_at) }}
              </el-descriptions-item>
              <el-descriptions-item label="Updated At">
                {{ formatDate(task.updated_at) }}
              </el-descriptions-item>
              <el-descriptions-item :span="2" label="Description">
                {{ task.description }}
              </el-descriptions-item>
            </el-descriptions>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useTaskStore } from '@/stores/task'
import { formatDate } from '@/utils/date'
import { ElMessageBox } from 'element-plus'

const router = useRouter()
const route = useRoute()
const taskStore = useTaskStore()

const loading = ref(false)
const task = ref<{
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
} | null>(null)

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

const handleDelete = async () => {
  try {
    await ElMessageBox.confirm(
      'Are you sure you want to delete this task?',
      'Warning',
      {
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel',
        type: 'warning',
      }
    )
    
    loading.value = true
    await taskStore.deleteTask(task.value!.id)
    router.push('/tasks')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Error deleting task:', error)
    }
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  const taskId = parseInt(route.params.id as string)
  if (isNaN(taskId)) {
    router.push('/tasks')
    return
  }

  loading.value = true
  try {
    await taskStore.fetchTask(taskId)
    task.value = taskStore.currentTask
  } catch (error) {
    console.error('Error fetching task:', error)
    router.push('/tasks')
  } finally {
    loading.value = false
  }
})
</script>

<style lang="scss" scoped>
.task-detail {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .task-info {
    margin-top: 1rem;
  }
}
</style> 