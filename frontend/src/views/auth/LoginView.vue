<template>
  <div class="login-view">
    <el-card class="login-card">
      <template #header>
        <h1 class="text-center">Вход в систему</h1>
      </template>
      
      <el-form
        ref="loginForm"
        :model="loginData"
        :rules="rules"
        @submit.prevent="handleSubmit"
      >
        <el-form-item prop="email">
          <el-input
            v-model="loginData.email"
            placeholder="Email"
            type="email"
            autocomplete="email"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="loginData.password"
            placeholder="Пароль"
            type="password"
            autocomplete="current-password"
            show-password
          />
        </el-form-item>

        <div class="form-actions">
          <el-button type="primary" native-type="submit" :loading="isLoading">
            Войти
          </el-button>
          <router-link to="/auth/forgot-password" class="forgot-password">
            Забыли пароль?
          </router-link>
        </div>
      </el-form>

      <div class="register-link">
        <span>Нет аккаунта?</span>
        <router-link to="/auth/register">Зарегистрироваться</router-link>
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

const loginForm = ref<FormInstance>()
const isLoading = ref(false)

const loginData = reactive({
  email: '',
  password: ''
})

const rules: FormRules = {
  email: [
    { required: true, message: 'Введите email', trigger: ['blur', 'change'] },
    { type: 'email', message: 'Введите корректный email', trigger: ['blur', 'change'] }
  ],
  password: [
    { required: true, message: 'Введите пароль', trigger: ['blur', 'change'] },
    { min: 6, message: 'Минимум 6 символов', trigger: ['blur', 'change'] }
  ]
}

const handleSubmit = async () => {
  if (!loginForm.value) return

  try {
    await loginForm.value.validate()
    isLoading.value = true
    
    await authStore.login(loginData.email, loginData.password)
    notificationStore.showSuccess('Вы успешно вошли в систему', 'Успешно')
    
    router.push('/dashboard')
  } catch (error: any) {
    if (error.response?.data?.detail) {
      notificationStore.showError(error.response.data.detail, 'Ошибка')
    } else {
      notificationStore.showError(error.message || 'Произошла ошибка при входе', 'Ошибка')
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style lang="scss" scoped>
.login-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-md);
  background-color: var(--bg-color-dark);
}

.login-card {
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
  justify-content: space-between;
  margin-top: var(--spacing-lg);
}

.forgot-password {
  color: var(--primary-color);
  text-decoration: none;
  transition: opacity var(--transition-duration) var(--transition-timing-function);

  &:hover {
    opacity: 0.8;
  }
}

.register-link {
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