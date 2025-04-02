<template>
  <div class="task-list-view">
    <el-card class="task-card">
      <template #header>
        <div class="card-header">
          <h2>Tasks</h2>
          <el-button type="primary" @click="handleCreateTask">New Task</el-button>
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
            <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="priority" label="Priority">
          <template #default="{ row }">
            <el-tag :type="getPriorityType(row.priority)">{{ row.priority }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="project.name" label="Project" />
        <el-table-column prop="due_date" label="Due Date">
          <template #default="{ row }">
            {{ formatDate(row.due_date) }}
          </template>
        </el-table-column>
        <el-table-column label="Actions">
          <template #default="{ row }">
            <el-button-group>
              <el-button type="primary" size="small" @click="handleViewTask(row)">
                View
              </el-button>
              <el-button type="warning" size="small" @click="handleEditTask(row)">
                Edit
              </el-button>
              <el-button type="danger" size="small" @click="handleDeleteTask(row)">
                Delete
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useTaskStore } from '@/stores/task'
import { formatDate } from '@/utils/date'

const router = useRouter()
const taskStore = useTaskStore()

const loading = ref(false)
const tasks = ref<any[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const getStatusType = (status: string): 'success' | 'warning' | 'info' | 'primary' | 'danger' => {
  const types: Record<string, 'success' | 'warning' | 'info' | 'primary' | 'danger'> = {
    'todo': 'info',
    'in_progress': 'warning',
    'completed': 'success',
    'cancelled': 'danger'
  }
  return types[status?.toLowerCase() || ''] || 'info'
}

const getPriorityType = (priority: string): 'success' | 'warning' | 'info' | 'primary' | 'danger' => {
  const types: Record<string, 'success' | 'warning' | 'info' | 'primary' | 'danger'> = {
    'low': 'info',
    'medium': 'warning',
    'high': 'danger'
  }
  return types[priority?.toLowerCase() || ''] || 'info'
}

const fetchTasks = async () => {
  try {
    loading.value = true
    const success = await taskStore.fetchTasks(undefined, currentPage.value)
    if (success) {
      tasks.value = taskStore.tasks
      total.value = taskStore.pagination.total
    }
  } catch (error) {
    console.error('Error fetching tasks:', error)
    ElMessage.error('Failed to load tasks')
  } finally {
    loading.value = false
  }
}

const handleCreateTask = () => {
  router.push('/tasks/create')
}

const handleViewTask = (task: any) => {
  router.push(`/tasks/${task.id}`)
}

const handleEditTask = (task: any) => {
  router.push(`/tasks/${task.id}/edit`)
}

const handleDeleteTask = async (task: any) => {
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

    await taskStore.deleteTask(task.id)
    ElMessage.success('Task deleted successfully')
    await fetchTasks()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Error deleting task:', error)
      ElMessage.error('Failed to delete task')
    }
  }
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  fetchTasks()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchTasks()
}

onMounted(() => {
  fetchTasks()
})
</script>

<style scoped lang="scss">
.task-list-view {
  padding: 20px;

  .task-card {
    margin-bottom: 20px;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    h2 {
      margin: 0;
    }
  }

  .pagination-container {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
}
</style> 