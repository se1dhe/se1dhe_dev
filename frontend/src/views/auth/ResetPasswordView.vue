<template>
  <div class="reset-password">
    <div class="card">
      <div class="card-header">
        <h1 class="card-title">Reset Password</h1>
      </div>
      <div class="card-body">
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="password">New Password</label>
            <input
              type="password"
              id="password"
              v-model="password"
              class="form-control"
              required
              placeholder="Enter new password"
            />
          </div>
          <div class="form-group">
            <label for="confirmPassword">Confirm Password</label>
            <input
              type="password"
              id="confirmPassword"
              v-model="confirmPassword"
              class="form-control"
              required
              placeholder="Confirm new password"
            />
          </div>
          <button type="submit" class="btn btn-primary mt-3" :disabled="loading || !isValid">
            {{ loading ? 'Resetting...' : 'Reset Password' }}
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
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useNotificationStore } from '@/stores/notification'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const notificationStore = useNotificationStore()

const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)

const isValid = computed(() => {
  return password.value && confirmPassword.value && password.value === confirmPassword.value
})

const handleSubmit = async () => {
  if (!isValid.value) {
    notificationStore.showError('Passwords do not match')
    return
  }

  const token = route.query.token as string
  if (!token) {
    notificationStore.showError('Reset token is missing')
    return
  }

  try {
    loading.value = true
    await authStore.resetPassword(token, password.value)
    notificationStore.showSuccess('Password has been reset successfully')
    router.push('/login')
  } catch (error: any) {
    notificationStore.showError(error.message || 'Failed to reset password')
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.reset-password {
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