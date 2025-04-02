<template>
  <div class="tasks">
    <div class="tasks-header">
      <h1>Задачи</h1>
      <el-button type="primary" @click="showCreateDialog = true">
        <el-icon><Plus /></el-icon>
        Новая задача
      </el-button>
    </div>

    <el-table
      v-loading="loading"
      :data="tasks"
      style="width: 100%"
      border
    >
      <el-table-column prop="title" label="Название" />
      <el-table-column prop="description" label="Описание" show-overflow-tooltip />
      <el-table-column prop="project.name" label="Проект" width="150" />
      <el-table-column prop="status" label="Статус" width="120">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="priority" label="Приоритет" width="120">
        <template #default="{ row }">
          <el-tag :type="getPriorityType(row.priority)">
            {{ row.priority }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="due_date" label="Срок" width="180">
        <template #default="{ row }">
          {{ formatDate(row.due_date) }}
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

    <!-- Диалог создания/редактирования задачи -->
    <el-dialog
      v-model="showCreateDialog"
      :title="editingTask ? 'Редактирование задачи' : 'Новая задача'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="taskForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="Название" prop="title">
          <el-input v-model="taskForm.title" />
        </el-form-item>
        <el-form-item label="Описание" prop="description">
          <el-input
            v-model="taskForm.description"
            type="textarea"
            :rows="3"
          />
        </el-form-item>
        <el-form-item label="Проект" prop="project_id">
          <el-select v-model="taskForm.project_id" style="width: 100%">
            <el-option
              v-for="project in projects"
              :key="project.id"
              :label="project.name"
              :value="project.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Статус" prop="status">
          <el-select v-model="taskForm.status" style="width: 100%">
            <el-option label="Новая" value="new" />
            <el-option label="В работе" value="in_progress" />
            <el-option label="На проверке" value="in_review" />
            <el-option label="Завершена" value="completed" />
          </el-select>
        </el-form-item>
        <el-form-item label="Приоритет" prop="priority">
          <el-select v-model="taskForm.priority" style="width: 100%">
            <el-option label="Низкий" value="low" />
            <el-option label="Средний" value="medium" />
            <el-option label="Высокий" value="high" />
            <el-option label="Срочный" value="urgent" />
          </el-select>
        </el-form-item>
        <el-form-item label="Срок" prop="due_date">
          <el-date-picker
            v-model="taskForm.due_date"
            type="datetime"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreateDialog = false">Отмена</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">
            {{ editingTask ? 'Сохранить' : 'Создать' }}
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
      <p>Вы уверены, что хотите удалить задачу "{{ taskToDelete?.title }}"?</p>
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
import { useTaskStore } from '@/stores'
import { useProjectStore } from '@/stores'
import { useUIStore } from '@/stores'
import { useNotificationStore } from '@/stores'

interface Task {
  id: number
  title: string
  description: string
  project_id: number
  project: {
    id: number
    name: string
  }
  status: string
  priority: string
  due_date: string
  created_by: number
  assigned_to: number
  created_at: string
  updated_at: string
}

interface Project {
  id: number
  name: string
}

const taskStore = useTaskStore()
const projectStore = useProjectStore()
const uiStore = useUIStore()
const notificationStore = useNotificationStore()

const loading = ref(false)
const submitting = ref(false)
const deleting = ref(false)
const showCreateDialog = ref(false)
const showDeleteDialog = ref(false)
const editingTask = ref<Task | null>(null)
const taskToDelete = ref<Task | null>(null)
const formRef = ref<FormInstance>()

const taskForm = ref<Omit<Task, 'id' | 'created_at' | 'updated_at' | 'project'>>({
  title: '',
  description: '',
  project_id: 0,
  status: 'new',
  priority: 'medium',
  due_date: '',
  created_by: 1, // TODO: Заменить на ID текущего пользователя
  assigned_to: 1 // TODO: Заменить на ID текущего пользователя
})

const rules: FormRules = {
  title: [
    { required: true, message: 'Введите название задачи', trigger: 'blur' },
    { min: 3, message: 'Название должно содержать минимум 3 символа', trigger: 'blur' }
  ],
  description: [
    { required: true, message: 'Введите описание задачи', trigger: 'blur' }
  ],
  project_id: [
    { required: true, message: 'Выберите проект', trigger: 'change' }
  ],
  status: [
    { required: true, message: 'Выберите статус задачи', trigger: 'change' }
  ],
  priority: [
    { required: true, message: 'Выберите приоритет задачи', trigger: 'change' }
  ],
  due_date: [
    { required: true, message: 'Выберите срок выполнения', trigger: 'change' }
  ]
}

const { tasks } = taskStore
const { projects } = projectStore

function getStatusType(status: string): 'success' | 'warning' | 'info' | 'danger' | 'primary' {
  switch (status.toLowerCase()) {
    case 'completed':
      return 'success'
    case 'in_progress':
      return 'primary'
    case 'in_review':
      return 'warning'
    case 'new':
      return 'info'
    default:
      return 'info'
  }
}

function getPriorityType(priority: string): 'success' | 'warning' | 'info' | 'danger' | 'primary' {
  switch (priority.toLowerCase()) {
    case 'urgent':
      return 'danger'
    case 'high':
      return 'warning'
    case 'medium':
      return 'primary'
    case 'low':
      return 'info'
    default:
      return 'info'
  }
}

function formatDate(date: string): string {
  return new Date(date).toLocaleString('ru-RU')
}

async function fetchTasks() {
  loading.value = true
  try {
    await taskStore.fetchTasks()
  } catch (error) {
    console.error('Error fetching tasks:', error)
    notificationStore.showError('Ошибка при загрузке задач')
  } finally {
    loading.value = false
  }
}

async function fetchProjects() {
  try {
    await projectStore.fetchProjects()
  } catch (error) {
    console.error('Error fetching projects:', error)
    notificationStore.showError('Ошибка при загрузке проектов')
  }
}

function handleEdit(task: Task) {
  editingTask.value = task
  taskForm.value = {
    title: task.title,
    description: task.description,
    project_id: task.project_id,
    status: task.status,
    priority: task.priority,
    due_date: task.due_date,
    created_by: task.created_by,
    assigned_to: task.assigned_to
  }
  showCreateDialog.value = true
}

function handleDelete(task: Task) {
  taskToDelete.value = task
  showDeleteDialog.value = true
}

async function handleSubmit() {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        if (editingTask.value) {
          await taskStore.updateTask(editingTask.value.id, taskForm.value)
          notificationStore.showSuccess('Задача успешно обновлена')
        } else {
          await taskStore.createTask(taskForm.value)
          notificationStore.showSuccess('Задача успешно создана')
        }
        showCreateDialog.value = false
        await fetchTasks()
      } catch (error) {
        console.error('Error saving task:', error)
        notificationStore.showError('Ошибка при сохранении задачи')
      } finally {
        submitting.value = false
      }
    }
  })
}

async function confirmDelete() {
  if (!taskToDelete.value) return

  deleting.value = true
  try {
    await taskStore.deleteTask(taskToDelete.value.id)
    notificationStore.showSuccess('Задача успешно удалена')
    showDeleteDialog.value = false
    await fetchTasks()
  } catch (error) {
    console.error('Error deleting task:', error)
    notificationStore.showError('Ошибка при удалении задачи')
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  fetchTasks()
  fetchProjects()
})
</script>

<style lang="scss" scoped>
.tasks {
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