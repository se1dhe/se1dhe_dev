<template>
  <div class="forgot-password">
    <div class="card">
      <div class="card-header">
        <h1 class="card-title">Forgot Password</h1>
      </div>
      <div class="card-body">
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="email">Email</label>
            <input
              type="email"
              id="email"
              v-model="email"
              class="form-control"
              required
              placeholder="Enter your email"
            />
          </div>
          <button type="submit" class="btn btn-primary mt-3" :disabled="loading">
            {{ loading ? 'Sending...' : 'Send Reset Link' }}
          </button>
        </form>
        <p class="mt-3">
          Remember your password?
          <router-link to="/login">Login here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useNotificationStore } from '@/stores/notification'

const authStore = useAuthStore()
const notificationStore = useNotificationStore()

const email = ref('')
const loading = ref(false)

const handleSubmit = async () => {
  try {
    loading.value = true
    await authStore.forgotPassword(email.value)
    notificationStore.showSuccess('Password reset link has been sent to your email')
    email.value = ''
  } catch (error: any) {
    notificationStore.showError(error.message || 'Failed to send reset link')
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.forgot-password {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: var(--spacing-md);
  background-color: var(--color-background);

  .card {
    width: 100%;
    max-width: 400px;
  }

  .form-group {
    margin-bottom: var(--spacing-md);
  }

  label {
    display: block;
    margin-bottom: var(--spacing-xs);
  }

  .btn {
    width: 100%;
  }
}
</style> 