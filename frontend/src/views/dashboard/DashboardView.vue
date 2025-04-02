<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>Dashboard</h1>
      <div class="dashboard-actions">
        <button class="btn btn-primary" @click="createProject">
          Create Project
        </button>
      </div>
    </div>

    <div class="dashboard-content">
      <div class="row">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h2 class="card-title">Recent Projects</h2>
            </div>
            <div class="card-body">
              <div v-if="loading" class="text-center">
                <div class="spinner-border" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
              </div>
              <div v-else-if="projects.length === 0" class="text-center">
                <p>No projects found</p>
                <button class="btn btn-primary" @click="createProject">
                  Create your first project
                </button>
              </div>
              <ul v-else class="list-group">
                <li v-for="project in projects" :key="project.id" class="list-group-item">
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <h3 class="h5 mb-1">{{ project.name }}</h3>
                      <p class="text-muted mb-0">{{ project.description }}</p>
                    </div>
                    <router-link :to="'/projects/' + project.id" class="btn btn-sm btn-outline-primary">
                      View
                    </router-link>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h2 class="card-title">Recent Tasks</h2>
            </div>
            <div class="card-body">
              <div v-if="loading" class="text-center">
                <div class="spinner-border" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
              </div>
              <div v-else-if="tasks.length === 0" class="text-center">
                <p>No tasks found</p>
              </div>
              <ul v-else class="list-group">
                <li v-for="task in tasks" :key="task.id" class="list-group-item">
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <h3 class="h5 mb-1">{{ task.title }}</h3>
                      <p class="text-muted mb-0">
                        Due: {{ new Date(task.due_date).toLocaleDateString() }}
                      </p>
                    </div>
                    <span :class="getStatusBadgeClass(task.status)">
                      {{ task.status }}
                    </span>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProjectStore } from '@/stores/project'
import { useTaskStore } from '@/stores/task'
import type { Project, Task } from '@/types'

const router = useRouter()
const projectStore = useProjectStore()
const taskStore = useTaskStore()

const loading = ref(true)
const projects = ref<Project[]>([])
const tasks = ref<Task[]>([])

const getStatusBadgeClass = (status: string) => {
  const classes = {
    'TO_DO': 'badge bg-secondary',
    'IN_PROGRESS': 'badge bg-primary',
    'DONE': 'badge bg-success',
    'BLOCKED': 'badge bg-danger'
  }
  return classes[status as keyof typeof classes] || 'badge bg-secondary'
}

const createProject = () => {
  router.push('/projects/new')
}

const fetchData = async () => {
  try {
    loading.value = true
    const [projectsData, tasksData] = await Promise.all([
      projectStore.getRecentProjects(),
      taskStore.getRecentTasks()
    ])
    projects.value = projectsData
    tasks.value = tasksData
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style lang="scss" scoped>
.dashboard {
  padding: var(--spacing-md);

  &-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-lg);
  }

  &-content {
    .row {
      margin: calc(var(--spacing-md) * -1);
      
      > [class*="col-"] {
        padding: var(--spacing-md);
      }
    }
  }

  .card {
    height: 100%;
  }

  .list-group-item {
    border-left: none;
    border-right: none;

    &:first-child {
      border-top: none;
    }

    &:last-child {
      border-bottom: none;
    }
  }

  .badge {
    font-size: 0.75rem;
    padding: 0.5em 0.75em;
  }
}
</style> 