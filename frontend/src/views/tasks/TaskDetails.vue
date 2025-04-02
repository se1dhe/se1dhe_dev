<template>
  <div class="task-details">
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
              :loading="deleting"
            >
              Delete
            </el-button>
          </el-button-group>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="Status">
          <el-tag :type="getStatusType(task?.status)">
            {{ task?.status }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="Priority">
          <el-tag :type="getPriorityType(task?.priority)">
            {{ task?.priority }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="Due Date">
          {{ task?.due_date ? formatDate(task.due_date) : 'N/A' }}
        </el-descriptions-item>
        <el-descriptions-item label="Project">
          <el-link
            v-if="project"
            type="primary"
            @click="router.push(`/projects/${project.id}`)"
          >
            {{ project.name }}
          </el-link>
          <span v-else>N/A</span>
        </el-descriptions-item>
        <el-descriptions-item label="Description" :span="2">
          {{ task?.description }}
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useTaskStore } from '@/stores/task'
import { useProjectStore } from '@/stores/project'
import { formatDate } from '@/utils/date'
import { ElMessageBox } from 'element-plus'

const router = useRouter()
const route = useRoute()
const taskStore = useTaskStore()
const projectStore = useProjectStore()

const loading = ref(false)
const deleting = ref(false)
const task = ref(taskStore.currentTask)
const project = ref<{
  id: number
  name: string
  description: string
  status: string
  created_by: number
  created_at: string
  updated_at: string
} | null>(null)

const getStatusType = (status?: string) => {
  const types: Record<string, string> = {
    todo: 'info',
    in_progress: 'warning',
    done: 'success'
  }
  return (status ? types[status] || 'info' : 'info') as 'success' | 'warning' | 'info' | 'primary' | 'danger'
}

const getPriorityType = (priority?: string) => {
  const types: Record<string, string> = {
    low: 'info',
    medium: 'warning',
    high: 'danger'
  }
  return (priority ? types[priority] || 'info' : 'info') as 'success' | 'warning' | 'info' | 'primary' | 'danger'
}

const handleDelete = async () => {
  if (!task.value) return

  try {
    await ElMessageBox.confirm(
      'Are you sure you want to delete this task?',
      'Warning',
      {
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }
    )

    deleting.value = true
    await taskStore.deleteTask(task.value.id)
    router.push('/tasks')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Error deleting task:', error)
    }
  } finally {
    deleting.value = false
  }
}

onMounted(async () => {
  const id = route.params.id
  if (!id) {
    router.push('/tasks')
    return
  }

  loading.value = true
  try {
    await taskStore.fetchTask(Number(id))
    task.value = taskStore.currentTask
    if (task.value?.project_id) {
      await projectStore.fetchProject(task.value.project_id)
      project.value = projectStore.currentProject
    }
  } catch (error) {
    console.error('Error fetching task details:', error)
    router.push('/tasks')
  } finally {
    loading.value = false
  }
})
</script>

<style lang="scss" scoped>
.task-details {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}
</style> 