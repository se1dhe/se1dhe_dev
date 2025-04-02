<template>
  <div class="project-create">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>Create Project</h2>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
        class="project-form"
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
            <el-option label="Completed" value="completed" />
            <el-option label="On Hold" value="on_hold" />
            <el-option label="Cancelled" value="cancelled" />
            <el-option label="Draft" value="draft" />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="loading">
            Create Project
          </el-button>
          <el-button @click="handleCancel">Cancel</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useProjectStore } from '@/stores/project'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const projectStore = useProjectStore()
const authStore = useAuthStore()

const formRef = ref()
const loading = ref(false)

const form = reactive({
  name: '',
  description: '',
  status: 'draft',
  created_by: authStore.user?.id || 0
})

const rules = {
  name: [
    { required: true, message: 'Please enter project name', trigger: 'blur' },
    { min: 3, max: 100, message: 'Length should be 3 to 100 characters', trigger: 'blur' }
  ],
  description: [
    { required: true, message: 'Please enter project description', trigger: 'blur' },
    { max: 1000, message: 'Length should not exceed 1000 characters', trigger: 'blur' }
  ],
  status: [
    { required: true, message: 'Please select project status', trigger: 'change' }
  ]
}

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    loading.value = true

    const success = await projectStore.createProject(form)
    if (success) {
      ElMessage.success('Project created successfully')
      router.push({ name: 'projects' })
    }
  } catch (error) {
    console.error('Error creating project:', error)
    ElMessage.error('Failed to create project')
  } finally {
    loading.value = false
  }
}

const handleCancel = () => {
  router.back()
}
</script>

<style scoped lang="scss">
.project-create {
  padding: 20px;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    h2 {
      margin: 0;
    }
  }

  .project-form {
    max-width: 600px;
    margin: 0 auto;
  }
}
</style> 