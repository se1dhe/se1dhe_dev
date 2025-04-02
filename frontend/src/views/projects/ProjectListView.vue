<template>
  <div class="project-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>Projects</h2>
          <el-button type="primary" @click="handleCreate">New Project</el-button>
        </div>
      </template>

      <el-table
        v-loading="loading"
        :data="projects"
        style="width: 100%"
      >
        <el-table-column prop="name" label="Name" min-width="200">
          <template #default="{ row }">
            <router-link :to="{ name: 'project-detail', params: { id: row.id }}">
              {{ row.name }}
            </router-link>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="Description" min-width="300" show-overflow-tooltip />
        <el-table-column prop="status" label="Status" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="Created" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="Actions" width="200" fixed="right">
          <template #default="{ row }">
            <el-button-group>
              <el-button
                size="small"
                @click="handleView(row)"
                type="primary"
                plain
              >
                View
              </el-button>
              <el-button
                size="small"
                @click="handleEdit(row)"
                type="warning"
                plain
              >
                Edit
              </el-button>
              <el-button
                size="small"
                @click="handleDelete(row)"
                type="danger"
                plain
              >
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
import { useProjectStore } from '@/stores/project'
import { formatDate } from '@/utils/date'

const router = useRouter()
const projectStore = useProjectStore()

const loading = ref(false)
const projects = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

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

const fetchProjects = async () => {
  loading.value = true
  try {
    const success = await projectStore.fetchProjects({
      page: currentPage.value,
      per_page: pageSize.value
    })
    if (success) {
      projects.value = projectStore.projects
      total.value = projectStore.pagination.total
    }
  } catch (error) {
    console.error('Error fetching projects:', error)
    ElMessage.error('Failed to fetch projects')
  } finally {
    loading.value = false
  }
}

const handleCreate = () => {
  router.push({ name: 'project-create' })
}

const handleView = (project: any) => {
  router.push({ name: 'project-detail', params: { id: project.id } })
}

const handleEdit = (project: any) => {
  router.push({ name: 'project-edit', params: { id: project.id } })
}

const handleDelete = async (project: any) => {
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
    
    const success = await projectStore.deleteProject(project.id)
    if (success) {
      ElMessage.success('Project deleted successfully')
      fetchProjects()
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Error deleting project:', error)
      ElMessage.error('Failed to delete project')
    }
  }
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  fetchProjects()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchProjects()
}

onMounted(() => {
  fetchProjects()
})
</script>

<style scoped lang="scss">
.project-list {
  padding: 20px;

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