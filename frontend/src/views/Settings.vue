<template>
  <div class="settings">
    <div class="settings-header">
      <h1>Настройки</h1>
      <p class="text-secondary">Настройте приложение под себя</p>
    </div>

    <div class="settings-content">
      <div class="card">
        <h2>Внешний вид</h2>
        <div class="settings-list">
          <div class="setting-item">
            <div class="setting-info">
              <h3>Тема</h3>
              <p>Выберите тему оформления</p>
            </div>
            <div class="setting-action">
              <select v-model="appearance.theme" class="form-control">
                <option value="dark">Темная</option>
                <option value="light">Светлая</option>
                <option value="system">Системная</option>
              </select>
            </div>
          </div>

          <div class="setting-item">
            <div class="setting-info">
              <h3>Акцентный цвет</h3>
              <p>Выберите основной цвет интерфейса</p>
            </div>
            <div class="setting-action">
              <div class="color-picker">
                <button 
                  v-for="color in accentColors" 
                  :key="color.value"
                  class="color-btn"
                  :class="{ active: appearance.accentColor === color.value }"
                  :style="{ '--color': color.value }"
                  @click="appearance.accentColor = color.value"
                ></button>
              </div>
            </div>
          </div>

          <div class="setting-item">
            <div class="setting-info">
              <h3>Анимации</h3>
              <p>Включить анимации интерфейса</p>
            </div>
            <div class="setting-action">
              <label class="switch">
                <input type="checkbox" v-model="appearance.animations">
                <span class="slider"></span>
              </label>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <h2>Уведомления</h2>
        <div class="settings-list">
          <div class="setting-item">
            <div class="setting-info">
              <h3>Push-уведомления</h3>
              <p>Получать уведомления в браузере</p>
            </div>
            <div class="setting-action">
              <label class="switch">
                <input type="checkbox" v-model="notifications.push">
                <span class="slider"></span>
              </label>
            </div>
          </div>

          <div class="setting-item">
            <div class="setting-info">
              <h3>Email-уведомления</h3>
              <p>Получать уведомления на почту</p>
            </div>
            <div class="setting-action">
              <label class="switch">
                <input type="checkbox" v-model="notifications.email">
                <span class="slider"></span>
              </label>
            </div>
          </div>

          <div class="setting-item">
            <div class="setting-info">
              <h3>Звуковые уведомления</h3>
              <p>Проигрывать звук при уведомлениях</p>
            </div>
            <div class="setting-action">
              <label class="switch">
                <input type="checkbox" v-model="notifications.sound">
                <span class="slider"></span>
              </label>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <h2>Язык и регион</h2>
        <div class="settings-list">
          <div class="setting-item">
            <div class="setting-info">
              <h3>Язык интерфейса</h3>
              <p>Выберите язык приложения</p>
            </div>
            <div class="setting-action">
              <select v-model="localization.language" class="form-control">
                <option value="ru">Русский</option>
                <option value="en">English</option>
              </select>
            </div>
          </div>

          <div class="setting-item">
            <div class="setting-info">
              <h3>Формат даты</h3>
              <p>Выберите формат отображения дат</p>
            </div>
            <div class="setting-action">
              <select v-model="localization.dateFormat" class="form-control">
                <option value="DD.MM.YYYY">DD.MM.YYYY</option>
                <option value="MM/DD/YYYY">MM/DD/YYYY</option>
                <option value="YYYY-MM-DD">YYYY-MM-DD</option>
              </select>
            </div>
          </div>

          <div class="setting-item">
            <div class="setting-info">
              <h3>Часовой пояс</h3>
              <p>Выберите ваш часовой пояс</p>
            </div>
            <div class="setting-action">
              <select v-model="localization.timezone" class="form-control">
                <option value="UTC+3">Москва (UTC+3)</option>
                <option value="UTC+0">Лондон (UTC+0)</option>
                <option value="UTC-5">Нью-Йорк (UTC-5)</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'

const appearance = reactive({
  theme: 'dark',
  accentColor: '#6C63FF',
  animations: true
})

const notifications = reactive({
  push: true,
  email: true,
  sound: true
})

const localization = reactive({
  language: 'ru',
  dateFormat: 'DD.MM.YYYY',
  timezone: 'UTC+3'
})

const accentColors = [
  { value: '#6C63FF' }, // Default purple
  { value: '#2D7FF9' }, // Blue
  { value: '#22C55E' }, // Green
  { value: '#EAB308' }, // Yellow
  { value: '#EF4444' }, // Red
  { value: '#EC4899' }, // Pink
]
</script>

<style scoped>
.settings {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.settings-header {
  margin-bottom: 1rem;
}

.settings-header h1 {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.text-secondary {
  color: var(--text-secondary);
}

.settings-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.card {
  background: var(--bg-dark-secondary);
  border-radius: var(--border-radius-lg);
  padding: 2rem;
}

.card h2 {
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

.form-control {
  min-width: 200px;
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

/* Color picker styles */
.color-picker {
  display: flex;
  gap: 0.5rem;
}

.color-btn {
  width: 32px;
  height: 32px;
  border-radius: var(--border-radius-full);
  border: 2px solid transparent;
  background: var(--color);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.color-btn:hover {
  transform: scale(1.1);
}

.color-btn.active {
  border-color: var(--text-primary);
  transform: scale(1.1);
}

@media (max-width: 768px) {
  .setting-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .setting-action {
    width: 100%;
  }

  .form-control {
    width: 100%;
  }
}
</style> 