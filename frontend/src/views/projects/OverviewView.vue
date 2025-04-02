<template>
  <div class="projects-overview">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="mb-4">
          <template #header>
            <div class="card-header">
              <h2>Projects Overview</h2>
              <el-button type="primary" @click="router.push('/projects/new')">
                New Project
              </el-button>
            </div>
          </template>
          
          <el-table
            v-loading="loading"
            :data="projects"
            style="width: 100%"
          >
            <el-table-column prop="name" label="Name" />
            <el-table-column prop="description" label="Description" />
            <el-table-column prop="status" label="Status">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status) as 'success' | 'warning' | 'info' | 'primary' | 'danger'">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="Created">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="Actions" width="200">
              <template #default="{ row }">
                <el-button-group>
                  <el-button
                    size="small"
                    @click="router.push(`/projects/${row.id}`)"
                  >
                    View
                  </el-button>
                  <el-button
                    size="small"
                    type="primary"
                    @click="router.push(`/projects/${row.id}/edit`)"
                  >
                    Edit
                  </el-button>
                </el-button-group>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProjectStore } from '@/stores/project'
import { formatDate } from '@/utils/date'

const router = useRouter()
const projectStore = useProjectStore()

const loading = ref(false)
const projects = ref<Array<{
  id: number
  name: string
  description: string
  status: string
  created_by: number
  created_at: string
  updated_at: string
}>>([])

const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    active: 'success',
    completed: 'info',
    on_hold: 'warning',
    cancelled: 'danger'
  }
  return types[status] || 'info'
}

onMounted(async () => {
  loading.value = true
  try {
    await projectStore.fetchProjects()
    projects.value = projectStore.projects
  } catch (error) {
    console.error('Error fetching projects:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style lang="scss" scoped>
.projects-overview {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}
</style> 