<template>
  <div class="task-create">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <h2>Create Task</h2>
            </div>
          </template>
          
          <TaskForm @submit="handleSubmit" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useTaskStore } from '@/stores/task'
import { useAuthStore } from '@/stores/auth'
import TaskForm from './TaskForm.vue'

const router = useRouter()
const taskStore = useTaskStore()
const authStore = useAuthStore()

const handleSubmit = async (formData: {
  title: string
  description: string
  status: string
  priority: string
  project_id: number
  assigned_to: number
  due_date: string
}) => {
  try {
    await taskStore.createTask({
      ...formData,
      created_by: authStore.user?.id || 0
    })
    router.push('/tasks')
  } catch (error) {
    console.error('Error creating task:', error)
  }
}
</script>

<style lang="scss" scoped>
.task-create {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}
</style> 