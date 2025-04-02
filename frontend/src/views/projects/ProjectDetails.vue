<template>
  <div class="project-details">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <h2>{{ project?.name }}</h2>
          <el-button-group>
            <el-button
              type="primary"
              @click="router.push(`/projects/${project?.id}/edit`)"
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
          <el-tag :type="getStatusType(project?.status)">
            {{ project?.status }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="Created">
          {{ project?.created_at ? formatDate(project.created_at) : 'N/A' }}
        </el-descriptions-item>
        <el-descriptions-item label="Description" :span="2">
          {{ project?.description }}
        </el-descriptions-item>
      </el-descriptions>

      <div class="mt-4">
        <h3>Tasks</h3>
        <el-table :data="tasks" style="width: 100%">
          <el-table-column prop="title" label="Title" />
          <el-table-column prop="status" label="Status">
            <template #default="{ row }">
              <el-tag :type="getTaskStatusType(row.status)">
                {{ row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="due_date" label="Due Date">
            <template #default="{ row }">
              {{ formatDate(row.due_date) }}
            </template>
          </el-table-column>
          <el-table-column label="Actions" width="150">
            <template #default="{ row }">
              <el-button
                size="small"
                @click="router.push(`/tasks/${row.id}`)"
              >
                View
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useProjectStore } from '@/stores/project'
import { useTaskStore } from '@/stores/task'
import { formatDate } from '@/utils/date'
import { ElMessageBox } from 'element-plus'

const router = useRouter()
const route = useRoute()
const projectStore = useProjectStore()
const taskStore = useTaskStore()

const loading = ref(false)
const deleting = ref(false)
const project = ref(projectStore.currentProject)
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
}>>([])

const getStatusType = (status?: string) => {
  const types: Record<string, string> = {
    active: 'success',
    completed: 'info',
    on_hold: 'warning',
    cancelled: 'danger'
  }
  return (status ? types[status] || 'info' : 'info') as 'success' | 'warning' | 'info' | 'primary' | 'danger'
}

const getTaskStatusType = (status: string) => {
  const types: Record<string, string> = {
    todo: 'info',
    in_progress: 'warning',
    done: 'success'
  }
  return (types[status] || 'info') as 'success' | 'warning' | 'info' | 'primary' | 'danger'
}

const handleDelete = async () => {
  if (!project.value) return

  try {
    await ElMessageBox.confirm(
      'Are you sure you want to delete this project?',
      'Warning',
      {
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }
    )

    deleting.value = true
    await projectStore.deleteProject(project.value.id)
    router.push('/projects')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Error deleting project:', error)
    }
  } finally {
    deleting.value = false
  }
}

onMounted(async () => {
  const id = route.params.id
  if (!id) {
    router.push('/projects')
    return
  }

  loading.value = true
  try {
    await projectStore.fetchProject(Number(id))
    project.value = projectStore.currentProject
    if (project.value) {
      await taskStore.fetchTasks(Number(project.value.id))
      tasks.value = taskStore.tasks
    }
  } catch (error) {
    console.error('Error fetching project details:', error)
    router.push('/projects')
  } finally {
    loading.value = false
  }
})
</script>

<style lang="scss" scoped>
.project-details {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .mt-4 {
    margin-top: 1rem;
  }
}
</style> 