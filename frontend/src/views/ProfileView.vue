<template>
  <div class="profile">
    <div class="profile-header">
      <h1>Профиль</h1>
      <el-button type="primary" @click="showEditDialog = true">
        <el-icon><Edit /></el-icon>
        Редактировать
      </el-button>
    </div>

    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <span>Информация о пользователе</span>
        </div>
      </template>
      <div class="profile-info">
        <div class="info-item">
          <span class="label">Имя:</span>
          <span class="value">{{ user?.name }}</span>
        </div>
        <div class="info-item">
          <span class="label">Email:</span>
          <span class="value">{{ user?.email }}</span>
        </div>
        <div class="info-item">
          <span class="label">Роль:</span>
          <span class="value">
            <el-tag :type="getRoleType(user?.role)">
              {{ user?.role }}
            </el-tag>
          </span>
        </div>
        <div class="info-item">
          <span class="label">Дата регистрации:</span>
          <span class="value">{{ formatDate(user?.created_at) }}</span>
        </div>
      </div>
    </el-card>

    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <span>Статистика</span>
        </div>
      </template>
      <div class="profile-stats">
        <div class="stat-item">
          <div class="stat-value">{{ stats.projects }}</div>
          <div class="stat-label">Проектов</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ stats.tasks }}</div>
          <div class="stat-label">Задач</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ stats.completedTasks }}</div>
          <div class="stat-label">Завершенных задач</div>
        </div>
      </div>
    </el-card>

    <!-- Диалог редактирования профиля -->
    <el-dialog
      v-model="showEditDialog"
      title="Редактирование профиля"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="profileForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="Имя" prop="name">
          <el-input v-model="profileForm.name" />
        </el-form-item>
        <el-form-item label="Email" prop="email">
          <el-input v-model="profileForm.email" />
        </el-form-item>
        <el-form-item label="Текущий пароль" prop="currentPassword">
          <el-input v-model="profileForm.currentPassword" type="password" />
        </el-form-item>
        <el-form-item label="Новый пароль" prop="newPassword">
          <el-input v-model="profileForm.newPassword" type="password" />
        </el-form-item>
        <el-form-item label="Подтверждение" prop="confirmPassword">
          <el-input v-model="profileForm.confirmPassword" type="password" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showEditDialog = false">Отмена</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">
            Сохранить
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Edit } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'
import { useAuthStore } from '@/stores'
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

interface ProfileForm {
  name: string
  email: string
  currentPassword: string
  newPassword: string
  confirmPassword: string
}

interface Stats {
  projects: number
  tasks: number
  completedTasks: number
}

const authStore = useAuthStore()
const uiStore = useUIStore()
const notificationStore = useNotificationStore()

const loading = ref(false)
const submitting = ref(false)
const showEditDialog = ref(false)
const formRef = ref<FormInstance>()

const user = ref<User | null>(null)
const stats = ref<Stats>({
  projects: 0,
  tasks: 0,
  completedTasks: 0
})

const profileForm = ref<ProfileForm>({
  name: '',
  email: '',
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const validatePass = (rule: any, value: string, callback: any) => {
  if (value === '') {
    callback(new Error('Введите пароль'))
  } else {
    if (profileForm.value.confirmPassword !== '') {
      if (formRef.value) {
        formRef.value.validateField('confirmPassword')
      }
    }
    callback()
  }
}

const validatePass2 = (rule: any, value: string, callback: any) => {
  if (value === '') {
    callback(new Error('Пожалуйста, подтвердите пароль'))
  } else if (value !== profileForm.value.newPassword) {
    callback(new Error('Пароли не совпадают'))
  } else {
    callback()
  }
}

const rules: FormRules = {
  name: [
    { required: true, message: 'Введите имя', trigger: 'blur' },
    { min: 2, message: 'Имя должно содержать минимум 2 символа', trigger: 'blur' }
  ],
  email: [
    { required: true, message: 'Введите email', trigger: 'blur' },
    { type: 'email', message: 'Введите корректный email', trigger: 'blur' }
  ],
  currentPassword: [
    { required: true, message: 'Введите текущий пароль', trigger: 'blur' }
  ],
  newPassword: [
    { validator: validatePass, trigger: 'blur' },
    { min: 6, message: 'Пароль должен содержать минимум 6 символов', trigger: 'blur' }
  ],
  confirmPassword: [
    { validator: validatePass2, trigger: 'blur' }
  ]
}

function getRoleType(role?: string): 'success' | 'warning' | 'info' | 'danger' | 'primary' {
  switch (role?.toLowerCase()) {
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

function formatDate(date?: string): string {
  if (!date) return ''
  return new Date(date).toLocaleString('ru-RU')
}

async function fetchProfile() {
  loading.value = true
  try {
    const userData = await authStore.getCurrentUser()
    user.value = userData
    profileForm.value = {
      name: userData.name,
      email: userData.email,
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
    // TODO: Загрузить статистику пользователя
  } catch (error) {
    console.error('Error fetching profile:', error)
    notificationStore.showError('Ошибка при загрузке профиля')
  } finally {
    loading.value = false
  }
}

async function handleSubmit() {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        await authStore.updateProfile({
          name: profileForm.value.name,
          email: profileForm.value.email,
          current_password: profileForm.value.currentPassword,
          new_password: profileForm.value.newPassword
        })
        notificationStore.showSuccess('Профиль успешно обновлен')
        showEditDialog.value = false
        await fetchProfile()
      } catch (error) {
        console.error('Error updating profile:', error)
        notificationStore.showError('Ошибка при обновлении профиля')
      } finally {
        submitting.value = false
      }
    }
  })
}

onMounted(() => {
  fetchProfile()
})
</script>

<style lang="scss" scoped>
.profile {
  &-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-lg);
  }

  &-card {
    margin-bottom: var(--spacing-lg);
  }

  &-info {
    .info-item {
      display: flex;
      margin-bottom: var(--spacing-md);

      .label {
        width: 200px;
        color: var(--text-secondary);
      }

      .value {
        flex: 1;
      }
    }
  }

  &-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: var(--spacing-lg);

    .stat-item {
      text-align: center;

      .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: var(--primary-color);
        margin-bottom: var(--spacing-xs);
      }

      .stat-label {
        color: var(--text-secondary);
      }
    }
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-md);
}
</style> 