<template>
  <div class="auth-container">
    <div class="auth-content">
      <div class="auth-card">
        <div class="auth-header">
          <img src="@/assets/logo.svg" alt="Logo" class="auth-logo">
          <h1>{{ $t('auth.login.title') }}</h1>
          <p>{{ $t('auth.login.subtitle') }}</p>
        </div>

        <form class="auth-form" @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="email">Email</label>
            <div class="input-group">
              <i class="fas fa-envelope"></i>
              <input 
                type="email" 
                id="email" 
                v-model="form.email"
                :class="{ 'has-error': errors.email }"
                placeholder="Введите ваш email"
                required
                @focus="clearError('email')"
              >
              <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
            </div>
          </div>

          <div class="form-group">
            <label for="password">Пароль</label>
            <div class="input-group">
              <i class="fas fa-lock"></i>
              <input 
                :type="showPassword ? 'text' : 'password'"
                id="password" 
                v-model="form.password"
                :class="{ 'has-error': errors.password }"
                placeholder="Введите ваш пароль"
                required
                @focus="clearError('password')"
              >
              <button 
                type="button"
                class="password-toggle"
                @click="togglePassword"
                :title="showPassword ? 'Скрыть пароль' : 'Показать пароль'"
              >
                <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </button>
              <span v-if="errors.password" class="error-message">{{ errors.password }}</span>
            </div>
          </div>

          <div class="form-options">
            <label class="checkbox-container">
              <input type="checkbox" v-model="form.remember">
              <span class="checkmark"></span>
              <span class="label-text">Запомнить меня</span>
            </label>
            <router-link to="/forgot-password" class="forgot-password">
              Забыли пароль?
            </router-link>
          </div>

          <button type="submit" class="btn btn-primary w-full" :disabled="isLoading">
            <i class="fas fa-sign-in-alt" v-if="!isLoading"></i>
            <i class="fas fa-circle-notch fa-spin" v-else></i>
            {{ isLoading ? 'Вход...' : 'Войти' }}
          </button>

          <div class="auth-divider">
            <span>или войдите через</span>
          </div>

          <div class="social-buttons">
            <button type="button" class="btn btn-telegram" @click="handleTelegramLogin">
              <i class="fab fa-telegram"></i>
              Telegram
            </button>
            <button type="button" class="btn btn-google" @click="handleGoogleLogin">
              <i class="fab fa-google"></i>
              Google
            </button>
          </div>
        </form>

        <div class="auth-footer">
          <p>Нет аккаунта? <router-link to="/register">Зарегистрироваться</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const isLoading = ref(false)
const showPassword = ref(false)

const form = reactive({
  email: '',
  password: '',
  remember: false
})

const errors = reactive({
  email: '',
  password: ''
})

const clearError = (field: keyof typeof errors) => {
  errors[field] = ''
}

const validateForm = () => {
  let isValid = true

  if (!form.email) {
    errors.email = 'Email обязателен'
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = 'Введите корректный email'
    isValid = false
  }

  if (!form.password) {
    errors.password = 'Пароль обязателен'
    isValid = false
  } else if (form.password.length < 6) {
    errors.password = 'Пароль должен быть не менее 6 символов'
    isValid = false
  }

  return isValid
}

const handleSubmit = async () => {
  if (!validateForm()) return

  try {
    isLoading.value = true
    await authStore.login(form)
    router.push('/')
  } catch (error: any) {
    if (error.response?.data?.message) {
      if (error.response.data.message.includes('email')) {
        errors.email = error.response.data.message
      } else if (error.response.data.message.includes('password')) {
        errors.password = error.response.data.message
      }
    }
  } finally {
    isLoading.value = false
  }
}

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const handleTelegramLogin = async () => {
  try {
    isLoading.value = true
    await authStore.telegramLogin()
  } catch (error) {
    console.error('Telegram login error:', error)
  } finally {
    isLoading.value = false
  }
}

const handleGoogleLogin = async () => {
  try {
    isLoading.value = true
    await authStore.googleLogin()
  } catch (error) {
    console.error('Google login error:', error)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-base);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.auth-content {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: var(--space-4);
}

.auth-card {
  width: 100%;
  max-width: 400px;
  padding: var(--space-8);
  background: var(--bg-surface);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
}

.auth-header {
  text-align: center;
  margin-bottom: var(--space-8);
}

.auth-logo {
  width: 64px;
  height: 64px;
  margin-bottom: var(--space-4);
}

.auth-header h1 {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  margin-bottom: var(--space-2);
  color: var(--text-primary);
}

.auth-header p {
  color: var(--text-secondary);
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.form-group label {
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
}

.input-group {
  position: relative;
}

.input-group i {
  position: absolute;
  left: var(--space-4);
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-tertiary);
  font-size: var(--font-size-lg);
}

.input-group input {
  padding-left: var(--space-10);
}

.input-group .password-toggle {
  position: absolute;
  right: var(--space-4);
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--text-tertiary);
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color var(--transition-fast);
}

.input-group .password-toggle:hover {
  color: var(--text-primary);
}

.form-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
}

.checkbox-container {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  cursor: pointer;
}

.checkbox-container input[type="checkbox"] {
  width: 16px;
  height: 16px;
  margin: 0;
}

.label-text {
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.forgot-password {
  font-size: var(--font-size-sm);
}

.auth-divider {
  display: flex;
  align-items: center;
  text-align: center;
  margin: var(--space-4) 0;
}

.auth-divider::before,
.auth-divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid var(--border-primary);
}

.auth-divider span {
  padding: 0 var(--space-4);
  color: var(--text-tertiary);
  font-size: var(--font-size-sm);
}

.social-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
}

.auth-footer {
  margin-top: var(--space-6);
  text-align: center;
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.error-message {
  color: var(--status-error);
  font-size: var(--font-size-sm);
  margin-top: var(--space-1);
}

.has-error {
  border-color: var(--status-error) !important;
}

.has-error:focus {
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.35) !important;
}

@media (max-width: 640px) {
  .auth-card {
    margin: var(--space-4);
  }
  
  .form-options {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .social-buttons {
    grid-template-columns: 1fr;
  }
}
</style> 