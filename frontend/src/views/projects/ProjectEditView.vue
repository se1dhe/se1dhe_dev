<template>
  <div class="project-edit">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <h2>Edit Project</h2>
        </div>
      </template>

      <el-form
        v-if="project"
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
          <el-button type="primary" @click="handleSubmit" :loading="submitting">
            Save Changes
          </el-button>
          <el-button @click="handleCancel">Cancel</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useProjectStore } from '@/stores/project'

const router = useRouter()
const route = useRoute()
const projectStore = useProjectStore()

const formRef = ref()
const loading = ref(false)
const submitting = ref(false)
const project = ref<any>(null)

const form = reactive({
  name: '',
  description: '',
  status: ''
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

const fetchProject = async () => {
  loading.value = true
  try {
    const success = await projectStore.fetchProject(Number(route.params.id))
    if (success) {
      project.value = projectStore.currentProject
      Object.assign(form, {
        name: project.value.name,
        description: project.value.description,
        status: project.value.status
      })
    }
  } catch (error) {
    console.error('Error fetching project:', error)
    ElMessage.error('Failed to fetch project')
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    submitting.value = true

    const success = await projectStore.updateProject(Number(route.params.id), form)
    if (success) {
      ElMessage.success('Project updated successfully')
      router.push({ name: 'project-detail', params: { id: route.params.id } })
    }
  } catch (error) {
    console.error('Error updating project:', error)
    ElMessage.error('Failed to update project')
  } finally {
    submitting.value = false
  }
}

const handleCancel = () => {
  router.back()
}

onMounted(() => {
  fetchProject()
})
</script>

<style scoped lang="scss">
.project-edit {
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