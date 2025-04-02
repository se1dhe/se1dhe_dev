<template>
  <div class="login-view">
    <div class="login-container">
      <div class="login-header">
        <h1>SE1DHE Development</h1>
        <p>Войдите в свой аккаунт</p>
      </div>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        class="login-form"
        @submit.prevent="handleSubmit"
      >
        <el-form-item prop="email">
          <el-input
            v-model="form.email"
            placeholder="Email"
            :prefix-icon="User"
            @change="() => formRef?.validateField('email')"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="Пароль"
            :prefix-icon="Lock"
            show-password
            @change="() => formRef?.validateField('password')"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            native-type="submit"
            :loading="isLoading"
            class="submit-button"
          >
            Войти
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'
import { useAuthStore } from '@/stores'
import { useNotificationStore } from '@/stores'

const router = useRouter()
const authStore = useAuthStore()
const notificationStore = useNotificationStore()

const formRef = ref<FormInstance>()
const isLoading = ref(false)

const form = reactive({
  email: '',
  password: ''
})

const rules: FormRules = {
  email: [
    { required: true, message: 'Пожалуйста, введите email', trigger: 'change' },
    { type: 'email', message: 'Пожалуйста, введите корректный email', trigger: 'change' }
  ],
  password: [
    { required: true, message: 'Пожалуйста, введите пароль', trigger: 'change' },
    { min: 6, message: 'Пароль должен содержать минимум 6 символов', trigger: 'change' }
  ]
}

async function handleSubmit() {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    isLoading.value = true

    const success = await authStore.login(form.email, form.password)
    if (success) {
      notificationStore.showSuccess('Вы успешно вошли в систему')
      router.push('/dashboard')
    }
  } catch (error: any) {
    console.error('Form validation error:', error)
    if (error.response?.data?.detail) {
      notificationStore.showError(error.response.data.detail)
    } else if (error.message) {
      notificationStore.showError(error.message)
    } else {
      notificationStore.showError('Ошибка при входе в систему')
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
  background-color: var(--background-color-base);
}

.login-container {
  width: 100%;
  max-width: 400px;
  padding: var(--spacing-xl);
  background-color: white;
  border-radius: var(--border-radius-base);
  box-shadow: var(--box-shadow-light);
}

.login-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);

  h1 {
    color: var(--primary-color);
    margin-bottom: var(--spacing-sm);
  }

  p {
    color: var(--text-secondary);
  }
}

.login-form {
  .submit-button {
    width: 100%;
  }
}
</style> 