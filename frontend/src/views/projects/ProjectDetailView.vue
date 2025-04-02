<template>
  <div class="project-detail">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <h2>{{ project.name }}</h2>
          <div class="header-actions">
            <el-button type="warning" @click="handleEdit" plain>Edit</el-button>
            <el-button type="danger" @click="handleDelete" plain>Delete</el-button>
          </div>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="Status">
          <el-tag :type="getStatusType(project.status)">
            {{ project.status }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="Created By">
          {{ project.created_by }}
        </el-descriptions-item>
        <el-descriptions-item label="Created At">
          {{ formatDate(project.created_at) }}
        </el-descriptions-item>
        <el-descriptions-item label="Updated At">
          {{ formatDate(project.updated_at) }}
        </el-descriptions-item>
      </el-descriptions>

      <div class="description-section">
        <h3>Description</h3>
        <p>{{ project.description || 'No description provided' }}</p>
      </div>

      <div class="tasks-section">
        <div class="section-header">
          <h3>Tasks</h3>
          <el-button type="primary" @click="handleCreateTask">New Task</el-button>
        </div>

        <el-table :data="tasks" style="width: 100%">
          <el-table-column prop="title" label="Title" min-width="200">
            <template #default="{ row }">
              <router-link :to="{ name: 'task-detail', params: { id: row.id }}">
                {{ row.title }}
              </router-link>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="Status" width="120">
            <template #default="{ row }">
              <el-tag :type="getTaskStatusType(row.status)">
                {{ row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="priority" label="Priority" width="120">
            <template #default="{ row }">
              <el-tag :type="getTaskPriorityType(row.priority)">
                {{ row.priority }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="due_date" label="Due Date" width="180">
            <template #default="{ row }">
              {{ formatDate(row.due_date) }}
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
import { ElMessage, ElMessageBox } from 'element-plus'
import { useProjectStore } from '@/stores/project'
import { useTaskStore } from '@/stores/task'
import { formatDate } from '@/utils/date'

const router = useRouter()
const route = useRoute()
const projectStore = useProjectStore()
const taskStore = useTaskStore()

const loading = ref(false)
const project = ref<any>({})
const tasks = ref<any[]>([])

const getStatusType = (status: string): 'success' | 'warning' | 'info' | 'primary' | 'danger' => {
  const types: Record<string, 'success' | 'warning' | 'info' | 'primary' | 'danger'> = {
    active: 'success',
    completed: 'primary',
    on_hold: 'warning',
    cancelled: 'danger',
    draft: 'info'
  }
  return types[status.toLowerCase()] || 'info'
}

const getTaskStatusType = (status: string): 'success' | 'warning' | 'info' | 'primary' | 'danger' => {
  const types: Record<string, 'success' | 'warning' | 'info' | 'primary' | 'danger'> = {
    todo: 'info',
    in_progress: 'warning',
    done: 'success',
    cancelled: 'danger'
  }
  return types[status.toLowerCase()] || 'info'
}

const getTaskPriorityType = (priority: string): 'success' | 'warning' | 'info' | 'primary' | 'danger' => {
  const types: Record<string, 'success' | 'warning' | 'info' | 'primary' | 'danger'> = {
    low: 'info',
    medium: 'warning',
    high: 'danger',
    urgent: 'danger'
  }
  return types[priority.toLowerCase()] || 'info'
}

const fetchProject = async () => {
  loading.value = true
  try {
    const success = await projectStore.fetchProject(Number(route.params.id))
    if (success) {
      project.value = projectStore.currentProject
      await fetchTasks()
    }
  } catch (error) {
    console.error('Error fetching project:', error)
    ElMessage.error('Failed to fetch project')
  } finally {
    loading.value = false
  }
}

const fetchTasks = async () => {
  try {
    const success = await taskStore.fetchTasks({
      project_id: Number(route.params.id)
    })
    if (success) {
      tasks.value = taskStore.tasks
    }
  } catch (error) {
    console.error('Error fetching tasks:', error)
    ElMessage.error('Failed to fetch tasks')
  }
}

const handleEdit = () => {
  router.push({ name: 'project-edit', params: { id: project.value.id } })
}

const handleDelete = async () => {
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
    
    const success = await projectStore.deleteProject(project.value.id)
    if (success) {
      ElMessage.success('Project deleted successfully')
      router.push({ name: 'projects' })
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Error deleting project:', error)
      ElMessage.error('Failed to delete project')
    }
  }
}

const handleCreateTask = () => {
  router.push({
    name: 'task-create',
    query: { project_id: project.value.id }
  })
}

onMounted(() => {
  fetchProject()
})
</script>

<style scoped lang="scss">
.project-detail {
  padding: 20px;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    h2 {
      margin: 0;
    }

    .header-actions {
      display: flex;
      gap: 10px;
    }
  }

  .description-section {
    margin-top: 20px;

    h3 {
      margin-bottom: 10px;
    }

    p {
      margin: 0;
      white-space: pre-wrap;
    }
  }

  .tasks-section {
    margin-top: 30px;

    .section-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;

      h3 {
        margin: 0;
      }
    }
  }
}
</style> 