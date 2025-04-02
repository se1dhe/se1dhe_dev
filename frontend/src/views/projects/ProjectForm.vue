<template>
  <div class="project-form">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>{{ isEdit ? 'Edit Project' : 'New Project' }}</h2>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
        @submit.prevent="handleSubmit"
      >
        <el-form-item label="Name" prop="name">
          <el-input v-model="form.name" placeholder="Enter project name" />
        </el-form-item>

        <el-form-item label="Description" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="4"
            placeholder="Enter project description"
          />
        </el-form-item>

        <el-form-item label="Status" prop="status">
          <el-select v-model="form.status" placeholder="Select status">
            <el-option label="Active" value="active" />
            <el-option label="On Hold" value="on_hold" />
            <el-option label="Completed" value="completed" />
            <el-option label="Cancelled" value="cancelled" />
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
import { useProjectStore } from '@/stores/project'
import type { FormInstance } from 'element-plus'

const router = useRouter()
const route = useRoute()
const projectStore = useProjectStore()

const formRef = ref<FormInstance>()
const loading = ref(false)
const isEdit = ref(false)

const form = ref({
  name: '',
  description: '',
  status: 'active',
  created_by: 1 // TODO: Replace with actual user ID from auth store
})

const rules = {
  name: [
    { required: true, message: 'Please enter project name', trigger: 'blur' },
    { min: 3, max: 100, message: 'Length should be 3 to 100 characters', trigger: 'blur' }
  ],
  description: [
    { required: true, message: 'Please enter project description', trigger: 'blur' }
  ],
  status: [
    { required: true, message: 'Please select project status', trigger: 'change' }
  ]
}

const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        if (isEdit.value) {
          await projectStore.updateProject(Number(route.params.id), form.value)
        } else {
          await projectStore.createProject(form.value)
        }
        router.push('/projects')
      } catch (error) {
        console.error('Error saving project:', error)
      } finally {
        loading.value = false
      }
    }
  })
}

onMounted(async () => {
  const id = route.params.id
  if (id) {
    isEdit.value = true
    try {
      await projectStore.fetchProject(Number(id))
      if (projectStore.currentProject) {
        form.value = { ...projectStore.currentProject }
      }
    } catch (error) {
      console.error('Error fetching project:', error)
      router.push('/projects')
    }
  }
})
</script>

<style lang="scss" scoped>
.project-form {
  max-width: 800px;
  margin: 0 auto;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}
</style> 