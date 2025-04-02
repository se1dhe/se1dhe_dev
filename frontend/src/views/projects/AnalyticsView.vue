<template>
  <div class="projects-analytics">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="mb-4">
          <template #header>
            <div class="card-header">
              <h2>Project Analytics</h2>
            </div>
          </template>
          
          <el-row :gutter="20">
            <el-col :span="8">
              <el-card shadow="hover">
                <template #header>
                  <div class="card-header">
                    <span>Total Projects</span>
                  </div>
                </template>
                <div class="stat-value">{{ totalProjects }}</div>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card shadow="hover">
                <template #header>
                  <div class="card-header">
                    <span>Active Projects</span>
                  </div>
                </template>
                <div class="stat-value">{{ activeProjects }}</div>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card shadow="hover">
                <template #header>
                  <div class="card-header">
                    <span>Completed Projects</span>
                  </div>
                </template>
                <div class="stat-value">{{ completedProjects }}</div>
              </el-card>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useProjectStore } from '@/stores/project'

const projectStore = useProjectStore()

const totalProjects = ref(0)
const activeProjects = ref(0)
const completedProjects = ref(0)

onMounted(async () => {
  try {
    await projectStore.fetchProjects()
    const projects = projectStore.projects
    totalProjects.value = projects.length
    activeProjects.value = projects.filter(p => p.status === 'active').length
    completedProjects.value = projects.filter(p => p.status === 'completed').length
  } catch (error) {
    console.error('Error fetching project analytics:', error)
  }
})
</script>

<style lang="scss" scoped>
.projects-analytics {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .stat-value {
    font-size: 2rem;
    font-weight: bold;
    text-align: center;
    color: var(--el-color-primary);
  }
}
</style> 