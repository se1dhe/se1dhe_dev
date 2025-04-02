<template>
  <div class="profile">
    <div class="profile-header">
      <h1>Профиль</h1>
      <p class="text-secondary">Управление личной информацией</p>
    </div>

    <div class="profile-content">
      <div class="card profile-info">
        <div class="profile-avatar">
          <img :src="userAvatar" alt="User avatar" class="avatar-img">
          <button class="change-avatar-btn">
            <i class="fas fa-camera"></i>
          </button>
        </div>
        
        <form class="profile-form" @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="name">Имя</label>
            <input 
              type="text" 
              id="name" 
              v-model="form.name"
              class="form-control"
              placeholder="Введите ваше имя"
            >
          </div>

          <div class="form-group">
            <label for="email">Email</label>
            <input 
              type="email" 
              id="email" 
              v-model="form.email"
              class="form-control"
              placeholder="Введите ваш email"
            >
          </div>

          <div class="form-group">
            <label for="role">Роль</label>
            <input 
              type="text" 
              id="role" 
              v-model="form.role"
              class="form-control"
              disabled
            >
          </div>

          <div class="form-group">
            <label for="bio">О себе</label>
            <textarea 
              id="bio" 
              v-model="form.bio"
              class="form-control"
              rows="4"
              placeholder="Расскажите о себе"
            ></textarea>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-primary" :disabled="isLoading">
              <i class="fas fa-save"></i>
              Сохранить изменения
            </button>
          </div>
        </form>
      </div>

      <div class="card security-settings">
        <h2>Безопасность</h2>
        <div class="settings-list">
          <div class="setting-item">
            <div class="setting-info">
              <h3>Двухфакторная аутентификация</h3>
              <p>Дополнительный уровень защиты для вашего аккаунта</p>
            </div>
            <div class="setting-action">
              <label class="switch">
                <input type="checkbox" v-model="security.twoFactor">
                <span class="slider"></span>
              </label>
            </div>
          </div>

          <div class="setting-item">
            <div class="setting-info">
              <h3>Изменить пароль</h3>
              <p>Регулярно меняйте пароль для безопасности</p>
            </div>
            <div class="setting-action">
              <button class="btn-secondary" @click="showChangePassword = true">
                <i class="fas fa-key"></i>
                Изменить
              </button>
            </div>
          </div>

          <div class="setting-item">
            <div class="setting-info">
              <h3>История входов</h3>
              <p>Просмотр последних входов в систему</p>
            </div>
            <div class="setting-action">
              <button class="btn-secondary" @click="showLoginHistory = true">
                <i class="fas fa-history"></i>
                Просмотреть
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useAuthStore } from '@/stores'

const authStore = useAuthStore()
const isLoading = ref(false)
const showChangePassword = ref(false)
const showLoginHistory = ref(false)

const userAvatar = computed(() => authStore.user?.avatar || '/default-avatar.png')

const form = reactive({
  name: authStore.user?.name || '',
  email: authStore.user?.email || '',
  role: authStore.user?.role || '',
  bio: ''
})

const security = reactive({
  twoFactor: false
})

const handleSubmit = async () => {
  try {
    isLoading.value = true
    // Implement profile update logic
    await new Promise(resolve => setTimeout(resolve, 1000))
    // Show success message
  } catch (error) {
    // Handle error
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.profile {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.profile-header {
  margin-bottom: 1rem;
}

.profile-header h1 {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.text-secondary {
  color: var(--text-secondary);
}

.profile-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

.card {
  background: var(--bg-dark-secondary);
  border-radius: var(--border-radius-lg);
  padding: 2rem;
}

.profile-avatar {
  position: relative;
  width: 128px;
  height: 128px;
  margin: 0 auto 2rem;
}

.avatar-img {
  width: 100%;
  height: 100%;
  border-radius: var(--border-radius-full);
  object-fit: cover;
}

.change-avatar-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 32px;
  height: 32px;
  border-radius: var(--border-radius-full);
  background: var(--primary);
  border: none;
  color: var(--text-primary);
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
}

.change-avatar-btn:hover {
  background: var(--primary-light);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.form-control {
  width: 100%;
  padding: 0.75rem 1rem;
  background: var(--bg-dark-tertiary);
  border: 1px solid transparent;
  border-radius: var(--border-radius-lg);
  color: var(--text-primary);
  transition: all var(--transition-fast);
}

.form-control:focus {
  border-color: var(--primary);
  box-shadow: var(--shadow-glow);
  outline: none;
}

.form-control:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 2rem;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: var(--primary);
  border: none;
  border-radius: var(--border-radius-full);
  color: var(--text-primary);
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-primary:hover:not(:disabled) {
  background: var(--primary-light);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.security-settings h2 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.settings-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.setting-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.setting-info h3 {
  font-size: 1rem;
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.setting-info p {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.btn-secondary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: var(--bg-dark-tertiary);
  border: none;
  border-radius: var(--border-radius-full);
  color: var(--text-primary);
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-secondary:hover {
  background: var(--bg-dark-primary);
}

/* Switch styles */
.switch {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 24px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--bg-dark-tertiary);
  transition: var(--transition-fast);
  border-radius: var(--border-radius-full);
}

.slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 2px;
  bottom: 2px;
  background-color: var(--text-primary);
  transition: var(--transition-fast);
  border-radius: 50%;
}

input:checked + .slider {
  background-color: var(--primary);
}

input:checked + .slider:before {
  transform: translateX(24px);
}

@media (max-width: 768px) {
  .profile-content {
    grid-template-columns: 1fr;
  }
}
</style> 