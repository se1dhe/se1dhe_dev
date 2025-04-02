<template>
  <div class="users">
    <div class="users-header">
      <h1>Пользователи</h1>
      <el-button type="primary" @click="showCreateDialog = true">
        <el-icon><Plus /></el-icon>
        Новый пользователь
      </el-button>
    </div>

    <el-table
      v-loading="loading"
      :data="users"
      style="width: 100%"
      border
    >
      <el-table-column prop="name" label="Имя" />
      <el-table-column prop="email" label="Email" />
      <el-table-column prop="role" label="Роль" width="120">
        <template #default="{ row }">
          <el-tag :type="getRoleType(row.role)">
            {{ row.role }}
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

    <!-- Диалог создания/редактирования пользователя -->
    <el-dialog
      v-model="showCreateDialog"
      :title="editingUser ? 'Редактирование пользователя' : 'Новый пользователь'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="userForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="Имя" prop="name">
          <el-input v-model="userForm.name" />
        </el-form-item>
        <el-form-item label="Email" prop="email">
          <el-input v-model="userForm.email" />
        </el-form-item>
        <el-form-item label="Пароль" prop="password" v-if="!editingUser">
          <el-input v-model="userForm.password" type="password" />
        </el-form-item>
        <el-form-item label="Роль" prop="role">
          <el-select v-model="userForm.role" style="width: 100%">
            <el-option label="Администратор" value="admin" />
            <el-option label="Менеджер" value="manager" />
            <el-option label="Пользователь" value="user" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreateDialog = false">Отмена</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">
            {{ editingUser ? 'Сохранить' : 'Создать' }}
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
      <p>Вы уверены, что хотите удалить пользователя "{{ userToDelete?.name }}"?</p>
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
import { useUserStore } from '@/stores'
import { useUIStore } from '@/stores'
import { useNotificationStore } from '@/stores'

interface User {
  id: number
  name: string
  email: string
  role: string
  created_at: string
  updated_at: string
}

const userStore = useUserStore()
const uiStore = useUIStore()
const notificationStore = useNotificationStore()

const loading = ref(false)
const submitting = ref(false)
const deleting = ref(false)
const showCreateDialog = ref(false)
const showDeleteDialog = ref(false)
const editingUser = ref<User | null>(null)
const userToDelete = ref<User | null>(null)
const formRef = ref<FormInstance>()

const userForm = ref<Omit<User, 'id' | 'created_at' | 'updated_at'> & { password?: string }>({
  name: '',
  email: '',
  password: '',
  role: 'user'
})

const rules: FormRules = {
  name: [
    { required: true, message: 'Введите имя пользователя', trigger: 'blur' },
    { min: 2, message: 'Имя должно содержать минимум 2 символа', trigger: 'blur' }
  ],
  email: [
    { required: true, message: 'Введите email пользователя', trigger: 'blur' },
    { type: 'email', message: 'Введите корректный email', trigger: 'blur' }
  ],
  password: [
    { required: true, message: 'Введите пароль', trigger: 'blur' },
    { min: 6, message: 'Пароль должен содержать минимум 6 символов', trigger: 'blur' }
  ],
  role: [
    { required: true, message: 'Выберите роль пользователя', trigger: 'change' }
  ]
}

const { users } = userStore

function getRoleType(role: string): 'success' | 'warning' | 'info' | 'danger' | 'primary' {
  switch (role.toLowerCase()) {
    case 'admin':
      return 'danger'
    case 'manager':
      return 'warning'
    case 'user':
      return 'info'
    default:
      return 'info'
  }
}

function formatDate(date: string): string {
  return new Date(date).toLocaleString('ru-RU')
}

async function fetchUsers() {
  loading.value = true
  try {
    await userStore.fetchUsers()
  } catch (error) {
    console.error('Error fetching users:', error)
    notificationStore.showError('Ошибка при загрузке пользователей')
  } finally {
    loading.value = false
  }
}

function handleEdit(user: User) {
  editingUser.value = user
  userForm.value = {
    name: user.name,
    email: user.email,
    role: user.role
  }
  showCreateDialog.value = true
}

function handleDelete(user: User) {
  userToDelete.value = user
  showDeleteDialog.value = true
}

async function handleSubmit() {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        if (editingUser.value) {
          await userStore.updateUser(editingUser.value.id, userForm.value)
          notificationStore.showSuccess('Пользователь успешно обновлен')
        } else {
          await userStore.createUser(userForm.value)
          notificationStore.showSuccess('Пользователь успешно создан')
        }
        showCreateDialog.value = false
        await fetchUsers()
      } catch (error) {
        console.error('Error saving user:', error)
        notificationStore.showError('Ошибка при сохранении пользователя')
      } finally {
        submitting.value = false
      }
    }
  })
}

async function confirmDelete() {
  if (!userToDelete.value) return

  deleting.value = true
  try {
    await userStore.deleteUser(userToDelete.value.id)
    notificationStore.showSuccess('Пользователь успешно удален')
    showDeleteDialog.value = false
    await fetchUsers()
  } catch (error) {
    console.error('Error deleting user:', error)
    notificationStore.showError('Ошибка при удалении пользователя')
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  fetchUsers()
})
</script>

<style lang="scss" scoped>
.users {
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