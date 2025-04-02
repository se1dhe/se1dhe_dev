<template>
  <div class="task-form">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>{{ isEdit ? 'Edit Task' : 'New Task' }}</h2>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
        @submit.prevent="handleSubmit"
      >
        <el-form-item label="Title" prop="title">
          <el-input v-model="form.title" placeholder="Enter task title" />
        </el-form-item>

        <el-form-item label="Description" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="4"
            placeholder="Enter task description"
          />
        </el-form-item>

        <el-form-item label="Status" prop="status">
          <el-select v-model="form.status" placeholder="Select status">
            <el-option label="To Do" value="todo" />
            <el-option label="In Progress" value="in_progress" />
            <el-option label="Done" value="done" />
          </el-select>
        </el-form-item>

        <el-form-item label="Priority" prop="priority">
          <el-select v-model="form.priority" placeholder="Select priority">
            <el-option label="Low" value="low" />
            <el-option label="Medium" value="medium" />
            <el-option label="High" value="high" />
          </el-select>
        </el-form-item>

        <el-form-item label="Due Date" prop="due_date">
          <el-date-picker
            v-model="form.due_date"
            type="date"
            placeholder="Select due date"
          />
        </el-form-item>

        <el-form-item label="Project" prop="project_id">
          <el-select v-model="form.project_id" placeholder="Select project">
            <el-option
              v-for="project in projects"
              :key="project.id"
              :label="project.name"
              :value="project.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="loading">
            {{ isEdit ? 'Update' : 'Create' }}
          </el-button>
          <el-button @click="router.back()">Cancel</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useTaskStore } from '@/stores/task'
import { useProjectStore } from '@/stores/project'
import type { FormInstance } from 'element-plus'

const router = useRouter()
const route = useRoute()
const taskStore = useTaskStore()
const projectStore = useProjectStore()

const formRef = ref<FormInstance>()
const loading = ref(false)
const isEdit = ref(false)
const projects = ref<Array<{
  id: number
  name: string
  description: string
  status: string
  created_by: number
  created_at: string
  updated_at: string
}>>([])

const form = ref({
  title: '',
  description: '',
  status: 'todo',
  priority: 'medium',
  due_date: '',
  project_id: 0,
  created_by: 1, // TODO: Replace with actual user ID from auth store
  assigned_to: 1 // TODO: Replace with actual user ID from auth store
})

const rules = {
  title: [
    { required: true, message: 'Please enter task title', trigger: 'blur' },
    { min: 3, max: 100, message: 'Length should be 3 to 100 characters', trigger: 'blur' }
  ],
  description: [
    { required: true, message: 'Please enter task description', trigger: 'blur' }
  ],
  status: [
    { required: true, message: 'Please select task status', trigger: 'change' }
  ],
  priority: [
    { required: true, message: 'Please select task priority', trigger: 'change' }
  ],
  due_date: [
    { required: true, message: 'Please select due date', trigger: 'change' }
  ],
  project_id: [
    { required: true, message: 'Please select project', trigger: 'change' }
  ]
}

const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        if (isEdit.value) {
          await taskStore.updateTask(Number(route.params.id), form.value)
        } else {
          await taskStore.createTask(form.value)
        }
        router.push('/tasks')
      } catch (error) {
        console.error('Error saving task:', error)
      } finally {
        loading.value = false
      }
    }
  })
}

onMounted(async () => {
  try {
    await projectStore.fetchProjects()
    projects.value = projectStore.projects

    const id = route.params.id
    if (id) {
      isEdit.value = true
      await taskStore.fetchTask(Number(id))
      if (taskStore.currentTask) {
        form.value = { ...taskStore.currentTask }
      }
    }
  } catch (error) {
    console.error('Error fetching data:', error)
    router.push('/tasks')
  }
})
</script>

<style lang="scss" scoped>
.task-form {
  max-width: 800px;
  margin: 0 auto;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}
</style> 