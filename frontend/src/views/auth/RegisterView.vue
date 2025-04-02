<template>
  <div class="register-view">
    <el-card class="register-card">
      <template #header>
        <h1 class="text-center">Регистрация</h1>
      </template>
      
      <el-form
        ref="registerForm"
        :model="registerData"
        :rules="rules"
        @submit.prevent="handleSubmit"
      >
        <el-form-item prop="name">
          <el-input
            v-model="registerData.name"
            placeholder="Имя"
            type="text"
            autocomplete="name"
          />
        </el-form-item>

        <el-form-item prop="email">
          <el-input
            v-model="registerData.email"
            placeholder="Email"
            type="email"
            autocomplete="email"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="registerData.password"
            placeholder="Пароль"
            type="password"
            autocomplete="new-password"
            show-password
          />
        </el-form-item>

        <el-form-item prop="confirmPassword">
          <el-input
            v-model="registerData.confirmPassword"
            placeholder="Подтвердите пароль"
            type="password"
            autocomplete="new-password"
            show-password
          />
        </el-form-item>

        <div class="form-actions">
          <el-button type="primary" native-type="submit" :loading="isLoading">
            Зарегистрироваться
          </el-button>
        </div>
      </el-form>

      <div class="login-link">
        <span>Уже есть аккаунт?</span>
        <router-link to="/auth/login">Войти</router-link>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore, useNotificationStore } from '@/stores'
import type { FormInstance, FormRules } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()
const notificationStore = useNotificationStore()

const registerForm = ref<FormInstance>()
const isLoading = ref(false)

const registerData = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const validatePass = (rule: any, value: string, callback: any) => {
  if (value === '') {
    callback(new Error('Пожалуйста, подтвердите пароль'))
  } else if (value !== registerData.password) {
    callback(new Error('Пароли не совпадают'))
  } else {
    callback()
  }
}

const rules: FormRules = {
  name: [
    { required: true, message: 'Введите имя', trigger: 'blur' },
    { min: 2, message: 'Минимум 2 символа', trigger: 'blur' }
  ],
  email: [
    { required: true, message: 'Введите email', trigger: 'blur' },
    { type: 'email', message: 'Введите корректный email', trigger: 'blur' }
  ],
  password: [
    { required: true, message: 'Введите пароль', trigger: 'blur' },
    { min: 6, message: 'Минимум 6 символов', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: 'Подтвердите пароль', trigger: 'blur' },
    { validator: validatePass, trigger: 'blur' }
  ]
}

const handleSubmit = async () => {
  if (!registerForm.value) return

  try {
    await registerForm.value.validate()
    isLoading.value = true
    
    await authStore.register({
      name: registerData.name,
      email: registerData.email,
      password: registerData.password
    })
    
    notificationStore.showSuccess('Вы успешно зарегистрировались', 'Успешно')
    router.push('/auth/login')
  } catch (error: any) {
    notificationStore.showError(error.message || 'Произошла ошибка при регистрации', 'Ошибка')
  } finally {
    isLoading.value = false
  }
}
</script>

<style lang="scss" scoped>
.register-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-md);
  background-color: var(--bg-color-dark);
}

.register-card {
  width: 100%;
  max-width: 400px;

  :deep(.el-card__header) {
    padding: var(--spacing-lg);
    border-bottom: 1px solid var(--border-color-light);
  }

  h1 {
    margin: 0;
    font-size: var(--font-size-xl);
    color: var(--text-color-primary);
  }
}

.form-actions {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: var(--spacing-lg);
}

.login-link {
  margin-top: var(--spacing-lg);
  text-align: center;
  color: var(--text-color-secondary);

  a {
    margin-left: var(--spacing-xs);
    color: var(--primary-color);
    text-decoration: none;
    transition: opacity var(--transition-duration) var(--transition-timing-function);

    &:hover {
      opacity: 0.8;
    }
  }
}
</style> 