<template>
  <div class="auth-container">
    <div class="auth-content">
      <div class="auth-card">
        <div class="auth-header">
          <img src="@/assets/logo.svg" alt="Logo" class="auth-logo">
          <h1>Регистрация</h1>
          <p class="text-secondary">Создайте новый аккаунт для доступа к системе.</p>
        </div>

        <form class="auth-form" @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="name">Имя</label>
            <div class="input-group">
              <i class="fas fa-user"></i>
              <input 
                type="text" 
                id="name" 
                v-model="form.name"
                :class="{ 'has-error': errors.name }"
                placeholder="Введите ваше имя"
                required
                @focus="clearError('name')"
              >
              <span v-if="errors.name" class="error-message">{{ errors.name }}</span>
            </div>
          </div>

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
                placeholder="Введите пароль"
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

          <div class="form-group">
            <label for="password_confirm">Подтверждение пароля</label>
            <div class="input-group">
              <i class="fas fa-lock"></i>
              <input 
                :type="showPassword ? 'text' : 'password'"
                id="password_confirm" 
                v-model="form.password_confirm"
                :class="{ 'has-error': errors.password_confirm }"
                placeholder="Повторите пароль"
                required
                @focus="clearError('password_confirm')"
              >
              <span v-if="errors.password_confirm" class="error-message">{{ errors.password_confirm }}</span>
            </div>
          </div>

          <div class="form-options">
            <label class="checkbox-container">
              <input 
                type="checkbox" 
                v-model="form.terms"
                :class="{ 'has-error': errors.terms }"
                @focus="clearError('terms')"
              >
              <span class="checkmark"></span>
              <span class="label-text">
                Я согласен с <a href="#" class="terms-link" @click.prevent="showTerms">условиями использования</a>
              </span>
            </label>
            <span v-if="errors.terms" class="error-message">{{ errors.terms }}</span>
          </div>

          <button type="submit" class="btn btn-primary w-full" :disabled="isLoading">
            <i class="fas fa-user-plus" v-if="!isLoading"></i>
            <i class="fas fa-circle-notch fa-spin" v-else></i>
            {{ isLoading ? 'Регистрация...' : 'Зарегистрироваться' }}
          </button>

          <div class="auth-divider">
            <span>или зарегистрируйтесь через</span>
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
          <p>Уже есть аккаунт? <router-link to="/login">Войти</router-link></p>
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
  name: '',
  email: '',
  password: '',
  password_confirm: '',
  terms: false
})

const errors = reactive({
  name: '',
  email: '',
  password: '',
  password_confirm: '',
  terms: ''
})

const clearError = (field: keyof typeof errors) => {
  errors[field] = ''
}

const validateForm = () => {
  let isValid = true

  if (!form.name) {
    errors.name = 'Имя обязательно'
    isValid = false
  } else if (form.name.length < 2) {
    errors.name = 'Имя должно содержать не менее 2 символов'
    isValid = false
  }

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

  if (!form.password_confirm) {
    errors.password_confirm = 'Подтвердите пароль'
    isValid = false
  } else if (form.password !== form.password_confirm) {
    errors.password_confirm = 'Пароли не совпадают'
    isValid = false
  }

  if (!form.terms) {
    errors.terms = 'Необходимо принять условия использования'
    isValid = false
  }

  return isValid
}

const handleSubmit = async () => {
  if (!validateForm()) return

  try {
    isLoading.value = true
    await authStore.register(form)
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

const showTerms = () => {
  // Implement terms modal
  console.log('Show terms modal')
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-4);
  background: var(--bg-base);
  position: relative;
  overflow: hidden;
}

.auth-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 200px;
  background: var(--gradient-primary);
  transform: skewY(-6deg) translateY(-100px);
  filter: blur(50px);
  opacity: 0.5;
}

.auth-content {
  position: relative;
  width: 100%;
  max-width: 420px;
}

.auth-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-xl);
  padding: var(--space-8);
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
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
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
  pointer-events: none;
}

.input-group input {
  width: 100%;
  padding: var(--space-3) var(--space-4) var(--space-3) var(--space-10);
  background: var(--bg-elevated);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-lg);
  color: var(--text-primary);
  transition: all var(--transition-fast);
}

.input-group input:focus {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-glow);
}

.input-group input.has-error {
  border-color: var(--status-error);
}

.error-message {
  color: var(--status-error);
  font-size: var(--font-size-sm);
  margin-top: var(--space-1);
}

.password-toggle {
  position: absolute;
  right: var(--space-4);
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--text-tertiary);
  cursor: pointer;
  transition: color var(--transition-fast);
}

.password-toggle:hover {
  color: var(--text-primary);
}

.form-options {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.checkbox-container {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  cursor: pointer;
}

.checkbox-container input {
  display: none;
}

.checkmark {
  width: 18px;
  height: 18px;
  border: 2px solid var(--border-primary);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
}

.checkbox-container input:checked ~ .checkmark {
  background: var(--color-primary);
  border-color: var(--color-primary);
}

.checkbox-container input:checked ~ .checkmark::after {
  content: '✓';
  color: var(--text-primary);
  font-size: 12px;
}

.label-text {
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.terms-link {
  color: var(--color-primary);
  text-decoration: none;
  transition: color var(--transition-fast);
}

.terms-link:hover {
  color: var(--color-primary-light);
}

.auth-divider {
  position: relative;
  text-align: center;
  margin: var(--space-4) 0;
}

.auth-divider::before,
.auth-divider::after {
  content: '';
  position: absolute;
  top: 50%;
  width: calc(50% - 120px);
  height: 1px;
  background: var(--border-primary);
}

.auth-divider::before {
  left: 0;
}

.auth-divider::after {
  right: 0;
}

.auth-divider span {
  background: var(--bg-surface);
  padding: 0 var(--space-4);
  color: var(--text-tertiary);
  font-size: var(--font-size-sm);
}

.social-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
}

.btn-telegram,
.btn-google {
  padding: var(--space-3);
  border: 1px solid var(--border-primary);
  background: var(--bg-elevated);
  color: var(--text-primary);
}

.btn-telegram:hover {
  background: #0088cc;
  border-color: #0088cc;
}

.btn-google:hover {
  background: #db4437;
  border-color: #db4437;
}

.auth-footer {
  text-align: center;
  margin-top: var(--space-6);
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.auth-footer a {
  color: var(--color-primary);
  font-weight: var(--font-weight-medium);
}

.auth-footer a:hover {
  color: var(--color-primary-light);
}

@media (max-width: 640px) {
  .auth-card {
    padding: var(--space-6);
  }
  
  .social-buttons {
    grid-template-columns: 1fr;
  }
}
</style> 