<template>
  <header class="header" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
    <div class="header-left">
      <button class="menu-btn" @click="toggleSidebar">
        <i class="fas fa-bars"></i>
      </button>
      <div class="search-container">
        <i class="fas fa-search search-icon"></i>
        <input 
          type="text" 
          class="search-input" 
          placeholder="Поиск..."
          v-model="searchQuery"
          @input="handleSearch"
        >
      </div>
    </div>

    <div class="header-right">
      <div class="notifications" v-click-outside="closeNotifications">
        <button class="icon-btn" @click="toggleNotifications">
          <i class="fas fa-bell"></i>
          <span v-if="unreadNotifications" class="notification-badge">
            {{ unreadNotifications }}
          </span>
        </button>
        <transition name="dropdown">
          <div v-if="showNotifications" class="notifications-dropdown">
            <div class="notifications-header">
              <h3>Уведомления</h3>
              <button class="text-btn" @click="markAllAsRead">
                Отметить все как прочитанные
              </button>
            </div>
            <div class="notifications-list" v-if="notifications.length">
              <div 
                v-for="notification in notifications" 
                :key="notification.id" 
                class="notification-item"
                :class="{ unread: !notification.read }"
              >
                <div class="notification-icon" :class="notification.type">
                  <i :class="getNotificationIcon(notification.type)"></i>
                </div>
                <div class="notification-content">
                  <p class="notification-text">{{ notification.text }}</p>
                  <span class="notification-time">{{ formatTime(notification.time) }}</span>
                </div>
              </div>
            </div>
            <div v-else class="notifications-empty">
              <i class="fas fa-bell-slash"></i>
              <p>Нет новых уведомлений</p>
            </div>
          </div>
        </transition>
      </div>

      <div class="user-menu" v-click-outside="closeUserMenu">
        <button class="user-btn" @click="toggleUserMenu">
          <img :src="userAvatar" alt="User avatar" class="user-avatar">
          <span class="user-name">{{ userName }}</span>
          <i class="fas fa-chevron-down" :class="{ 'rotated': showUserMenu }"></i>
        </button>
        <transition name="dropdown">
          <div v-if="showUserMenu" class="user-dropdown">
            <router-link to="/profile" class="dropdown-item" @click="closeUserMenu">
              <i class="fas fa-user"></i>
              Профиль
            </router-link>
            <router-link to="/settings" class="dropdown-item" @click="closeUserMenu">
              <i class="fas fa-cog"></i>
              Настройки
            </router-link>
            <div class="dropdown-divider"></div>
            <button class="dropdown-item text-danger" @click="handleLogout">
              <i class="fas fa-sign-out-alt"></i>
              Выйти
            </button>
          </div>
        </transition>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useSidebarStore } from '@/stores/sidebar'
import { formatDistanceToNow } from 'date-fns'
import { ru } from 'date-fns/locale'
import { vClickOutside } from '@/directives/click-outside'

const router = useRouter()
const authStore = useAuthStore()
const sidebarStore = useSidebarStore()

const searchQuery = ref('')
const showNotifications = ref(false)
const showUserMenu = ref(false)

const isSidebarCollapsed = computed(() => sidebarStore.isCollapsed)

// Mock notifications data
const notifications = ref([
  {
    id: 1,
    type: 'info',
    text: 'Добро пожаловать в систему!',
    time: new Date(),
    read: false
  },
  {
    id: 2,
    type: 'success',
    text: 'Задача "Разработка UI" выполнена',
    time: new Date(Date.now() - 3600000),
    read: false
  },
  {
    id: 3,
    type: 'warning',
    text: 'Срок выполнения задачи истекает через 2 дня',
    time: new Date(Date.now() - 7200000),
    read: true
  }
])

const userName = computed(() => authStore.user?.name || 'Гость')
const userAvatar = computed(() => authStore.user?.avatar || '/default-avatar.png')
const unreadNotifications = computed(() => 
  notifications.value.filter(n => !n.read).length
)

const handleSearch = () => {
  // Implement search logic
}

const toggleSidebar = () => {
  sidebarStore.toggle()
}

const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value
  showUserMenu.value = false
}

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
  showNotifications.value = false
}

const closeNotifications = () => {
  showNotifications.value = false
}

const closeUserMenu = () => {
  showUserMenu.value = false
}

const markAllAsRead = () => {
  notifications.value = notifications.value.map(n => ({ ...n, read: true }))
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

const getNotificationIcon = (type: string) => {
  const icons = {
    info: 'fas fa-info-circle',
    success: 'fas fa-check-circle',
    warning: 'fas fa-exclamation-triangle',
    error: 'fas fa-times-circle'
  }
  return icons[type as keyof typeof icons]
}

const formatTime = (date: Date) => {
  return formatDistanceToNow(date, { addSuffix: true, locale: ru })
}
</script>

<style scoped>
.header {
  position: fixed;
  top: 0;
  right: 0;
  left: var(--sidebar-width);
  height: var(--header-height);
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-primary);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-6);
  z-index: var(--z-sticky);
  transition: all var(--transition-normal);
}

.header.sidebar-collapsed {
  left: var(--sidebar-width-collapsed);
}

.header-left {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.menu-btn {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-lg);
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
}

.menu-btn:hover {
  background: var(--bg-elevated);
  color: var(--text-primary);
}

.search-container {
  position: relative;
  width: 300px;
}

.search-icon {
  position: absolute;
  left: var(--space-4);
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-tertiary);
  pointer-events: none;
}

.search-input {
  width: 100%;
  height: 40px;
  padding: 0 var(--space-4) 0 var(--space-10);
  background: var(--bg-elevated);
  border: 1px solid var(--border-secondary);
  border-radius: var(--radius-lg);
  color: var(--text-primary);
  transition: all var(--transition-fast);
}

.search-input:focus {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-glow);
  outline: none;
}

.header-right {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.icon-btn {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-lg);
  background: var(--bg-elevated);
  border: 1px solid var(--border-secondary);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-btn:hover {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: var(--text-primary);
}

.notification-badge {
  position: absolute;
  top: -6px;
  right: -6px;
  background: var(--accent-red);
  color: var(--text-primary);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  padding: 2px 6px;
  border-radius: var(--radius-full);
  min-width: 20px;
}

.notifications-dropdown,
.user-dropdown {
  position: absolute;
  top: calc(100% + var(--space-4));
  right: 0;
  background: var(--bg-surface);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  min-width: 300px;
  max-width: 400px;
  overflow: hidden;
}

.notifications-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4);
  border-bottom: 1px solid var(--border-primary);
}

.notifications-header h3 {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin: 0;
}

.text-btn {
  background: none;
  border: none;
  color: var(--color-primary);
  font-size: var(--font-size-sm);
  cursor: pointer;
  transition: color var(--transition-fast);
}

.text-btn:hover {
  color: var(--color-primary-light);
}

.notifications-list {
  max-height: 400px;
  overflow-y: auto;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  padding: var(--space-4);
  border-bottom: 1px solid var(--border-secondary);
  transition: background var(--transition-fast);
}

.notification-item:hover {
  background: var(--bg-elevated);
}

.notification-item.unread {
  background: var(--bg-elevated);
}

.notification-icon {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.notification-icon.info {
  background: var(--status-info);
  color: var(--text-primary);
}

.notification-icon.success {
  background: var(--status-success);
  color: var(--text-primary);
}

.notification-icon.warning {
  background: var(--status-warning);
  color: var(--text-primary);
}

.notification-icon.error {
  background: var(--status-error);
  color: var(--text-primary);
}

.notification-content {
  flex: 1;
}

.notification-text {
  margin: 0 0 var(--space-2);
  color: var(--text-primary);
  font-size: var(--font-size-sm);
  line-height: var(--line-height-snug);
}

.notification-time {
  color: var(--text-tertiary);
  font-size: var(--font-size-xs);
}

.notifications-empty {
  padding: var(--space-8);
  text-align: center;
  color: var(--text-tertiary);
}

.notifications-empty i {
  font-size: var(--font-size-2xl);
  margin-bottom: var(--space-2);
}

.notifications-empty p {
  margin: 0;
  font-size: var(--font-size-sm);
}

.user-btn {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-3);
  background: var(--bg-elevated);
  border: 1px solid var(--border-secondary);
  border-radius: var(--radius-lg);
  color: var(--text-primary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.user-btn:hover {
  background: var(--bg-elevated);
  border-color: var(--color-primary);
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-full);
  object-fit: cover;
}

.user-name {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
}

.fa-chevron-down {
  color: var(--text-tertiary);
  transition: transform var(--transition-fast);
}

.fa-chevron-down.rotated {
  transform: rotate(180deg);
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  color: var(--text-primary);
  text-decoration: none;
  transition: background var(--transition-fast);
}

.dropdown-item:hover {
  background: var(--bg-elevated);
}

.dropdown-item i {
  color: var(--text-tertiary);
  width: 16px;
}

.dropdown-divider {
  height: 1px;
  background: var(--border-primary);
  margin: var(--space-2) 0;
}

.text-danger {
  color: var(--status-error) !important;
}

.text-danger:hover {
  background: var(--status-error) !important;
  color: var(--text-primary) !important;
}

.text-danger i {
  color: inherit !important;
}

/* Dropdown animations */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all var(--transition-normal);
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Responsive styles */
@media (max-width: 768px) {
  .header {
    left: 0;
    padding: 0 var(--space-4);
  }
  
  .header.sidebar-collapsed {
    left: 0;
  }
  
  .search-container {
    width: 100%;
    max-width: 300px;
  }
  
  .user-name {
    display: none;
  }
  
  .notifications-dropdown,
  .user-dropdown {
    position: fixed;
    top: var(--header-height);
    right: var(--space-4);
    left: var(--space-4);
    max-width: none;
  }
}
</style> 