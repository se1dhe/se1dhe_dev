<template>
  <div class="projects">
    <div class="projects-header">
      <h1>Проекты</h1>
      <el-button type="primary" @click="showCreateDialog = true">
        <el-icon><Plus /></el-icon>
        Новый проект
      </el-button>
    </div>

    <el-table
      v-loading="loading"
      :data="projects"
      style="width: 100%"
      border
    >
      <el-table-column prop="name" label="Название" />
      <el-table-column prop="description" label="Описание" show-overflow-tooltip />
      <el-table-column prop="status" label="Статус" width="120">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="Создан" width="180">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="Действия" width="200" fixed="right">
        <template #default="{ row }">
          <el-button-group>
            <el-button
              type="primary"
              :icon="Edit"
              circle
              @click="handleEdit(row)"
            />
            <el-button
              type="danger"
              :icon="Delete"
              circle
              @click="handleDelete(row)"
            />
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- Диалог создания/редактирования проекта -->
    <el-dialog
      v-model="showCreateDialog"
      :title="editingProject ? 'Редактирование проекта' : 'Новый проект'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="projectForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="Название" prop="name">
          <el-input v-model="projectForm.name" />
        </el-form-item>
        <el-form-item label="Описание" prop="description">
          <el-input
            v-model="projectForm.description"
            type="textarea"
            :rows="3"
          />
        </el-form-item>
        <el-form-item label="Статус" prop="status">
          <el-select v-model="projectForm.status" style="width: 100%">
            <el-option label="Активный" value="active" />
            <el-option label="Завершен" value="completed" />
            <el-option label="Отменен" value="cancelled" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreateDialog = false">Отмена</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">
            {{ editingProject ? 'Сохранить' : 'Создать' }}
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- Диалог подтверждения удаления -->
    <el-dialog
      v-model="showDeleteDialog"
      title="Подтверждение удаления"
      width="400px"
    >
      <p>Вы уверены, что хотите удалить проект "{{ projectToDelete?.name }}"?</p>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showDeleteDialog = false">Отмена</el-button>
          <el-button
            type="danger"
            @click="confirmDelete"
            :loading="deleting"
          >
            Удалить
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Plus, Edit, Delete } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'
import { useProjectStore } from '@/stores'
import { useUIStore } from '@/stores'
import { useNotificationStore } from '@/stores'

interface Project {
  id: number
  name: string
  description: string
  status: string
  created_by: number
  created_at: string
  updated_at: string
}

const projectStore = useProjectStore()
const uiStore = useUIStore()
const notificationStore = useNotificationStore()

const loading = ref(false)
const submitting = ref(false)
const deleting = ref(false)
const showCreateDialog = ref(false)
const showDeleteDialog = ref(false)
const editingProject = ref<Project | null>(null)
const projectToDelete = ref<Project | null>(null)
const formRef = ref<FormInstance>()

const projectForm = ref<Omit<Project, 'id' | 'created_at' | 'updated_at'>>({
  name: '',
  description: '',
  status: 'active',
  created_by: 1 // TODO: Заменить на ID текущего пользователя
})

const rules: FormRules = {
  name: [
    { required: true, message: 'Введите название проекта', trigger: 'blur' },
    { min: 3, message: 'Название должно содержать минимум 3 символа', trigger: 'blur' }
  ],
  description: [
    { required: true, message: 'Введите описание проекта', trigger: 'blur' }
  ],
  status: [
    { required: true, message: 'Выберите статус проекта', trigger: 'change' }
  ]
}

const { projects } = projectStore

function getStatusType(status: string): 'success' | 'warning' | 'info' | 'danger' | 'primary' {
  switch (status.toLowerCase()) {
    case 'active':
      return 'success'
    case 'completed':
      return 'info'
    case 'cancelled':
      return 'danger'
    default:
      return 'warning'
  }
}

function formatDate(date: string): string {
  return new Date(date).toLocaleString('ru-RU')
}

async function fetchProjects() {
  loading.value = true
  try {
    await projectStore.fetchProjects()
  } catch (error) {
    console.error('Error fetching projects:', error)
    notificationStore.showError('Ошибка при загрузке проектов')
  } finally {
    loading.value = false
  }
}

function handleEdit(project: any) {
  editingProject.value = project
  projectForm.value = { ...project }
  showCreateDialog.value = true
}

function handleDelete(project: any) {
  projectToDelete.value = project
  showDeleteDialog.value = true
}

async function handleSubmit() {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        if (editingProject.value) {
          await projectStore.updateProject(editingProject.value.id, projectForm.value)
          notificationStore.showSuccess('Проект успешно обновлен')
        } else {
          await projectStore.createProject(projectForm.value)
          notificationStore.showSuccess('Проект успешно создан')
        }
        showCreateDialog.value = false
        await fetchProjects()
      } catch (error) {
        console.error('Error saving project:', error)
        notificationStore.showError('Ошибка при сохранении проекта')
      } finally {
        submitting.value = false
      }
    }
  })
}

async function confirmDelete() {
  if (!projectToDelete.value) return

  deleting.value = true
  try {
    await projectStore.deleteProject(projectToDelete.value.id)
    notificationStore.showSuccess('Проект успешно удален')
    showDeleteDialog.value = false
    await fetchProjects()
  } catch (error) {
    console.error('Error deleting project:', error)
    notificationStore.showError('Ошибка при удалении проекта')
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  fetchProjects()
})
</script>

<style lang="scss" scoped>
.projects {
  &-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-lg);
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-md);
}
</style> 