<template>
  <aside 
    class="sidebar" 
    :class="{ 
      'sidebar-collapsed': isCollapsed,
      'sidebar-mobile-open': isMobileOpen 
    }"
  >
    <div class="sidebar-header">
      <div class="logo-container">
        <img src="@/assets/logo.svg" alt="Logo" class="logo" />
        <span v-if="!isCollapsed" class="logo-text">SE1DHE</span>
      </div>
      <button class="collapse-btn" @click="toggleCollapse">
        <i class="fas" :class="isCollapsed ? 'fa-chevron-right' : 'fa-chevron-left'"></i>
      </button>
    </div>

    <nav class="sidebar-nav">
      <router-link
        v-for="item in menuItems"
        :key="item.path"
        :to="item.path"
        class="nav-item"
        :class="{ active: isCurrentRoute(item.path) }"
        :title="isCollapsed ? item.name : ''"
      >
        <div class="nav-icon">
          <i :class="['fas', item.icon]"></i>
        </div>
        <span v-if="!isCollapsed" class="nav-text">{{ item.name }}</span>
        <div 
          v-if="!isCollapsed && item.badge" 
          class="badge" 
          :class="item.badge.type"
        >
          {{ item.badge.text }}
        </div>
      </router-link>
    </nav>

    <div class="sidebar-footer">
      <div class="user-info" v-if="!isCollapsed">
        <img :src="userAvatar" alt="User avatar" class="user-avatar" />
        <div class="user-details">
          <span class="user-name">{{ userName }}</span>
          <span class="user-role">{{ userRole }}</span>
        </div>
      </div>
      <button 
        v-if="!isCollapsed" 
        class="settings-btn" 
        @click="navigateToSettings"
      >
        <i class="fas fa-cog"></i>
        <span>Настройки</span>
      </button>
    </div>

    <div v-if="isMobileOpen" class="sidebar-overlay" @click="closeMobileSidebar"></div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useSidebarStore } from '@/stores/sidebar'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const sidebarStore = useSidebarStore()

const isCollapsed = computed(() => sidebarStore.isCollapsed)
const isMobileOpen = computed(() => sidebarStore.isMobileOpen)

const menuItems = [
  { 
    name: 'Дашборд', 
    path: '/', 
    icon: 'fa-home' 
  },
  { 
    name: 'Проекты', 
    path: '/projects', 
    icon: 'fa-project-diagram',
    badge: { text: 'Новый', type: 'success' }
  },
  { 
    name: 'Задачи', 
    path: '/tasks', 
    icon: 'fa-tasks',
    badge: { text: '3', type: 'primary' }
  },
  { 
    name: 'Команда', 
    path: '/team', 
    icon: 'fa-users' 
  },
  { 
    name: 'Календарь', 
    path: '/calendar', 
    icon: 'fa-calendar-alt' 
  },
  { 
    name: 'Аналитика', 
    path: '/analytics', 
    icon: 'fa-chart-line' 
  },
  { 
    name: 'Отчеты', 
    path: '/reports', 
    icon: 'fa-file-alt' 
  },
]

const userName = computed(() => authStore.user?.name || 'Гость')
const userRole = computed(() => {
  const role = authStore.user?.role
  return role === 'admin' ? 'Администратор' : 'Пользователь'
})
const userAvatar = computed(() => authStore.user?.avatar || '/default-avatar.png')

const isCurrentRoute = (path: string) => {
  if (path === '/') {
    return route.path === '/'
  }
  return route.path.startsWith(path)
}

const toggleCollapse = () => {
  sidebarStore.toggle()
}

const closeMobileSidebar = () => {
  sidebarStore.closeMobile()
}

const navigateToSettings = () => {
  router.push('/settings')
}
</script>

<style scoped>
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  width: var(--sidebar-width);
  background: var(--bg-surface);
  border-right: 1px solid var(--border-primary);
  display: flex;
  flex-direction: column;
  transition: all var(--transition-normal);
  z-index: var(--z-drawer);
}

.sidebar-collapsed {
  width: var(--sidebar-width-collapsed);
}

.sidebar-header {
  height: var(--header-height);
  padding: var(--space-4);
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-primary);
}

.logo-container {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.logo {
  width: 32px;
  height: 32px;
}

.logo-text {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.collapse-btn {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-lg);
  background: var(--bg-elevated);
  border: 1px solid var(--border-secondary);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
}

.collapse-btn:hover {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: var(--text-primary);
}

.sidebar-nav {
  flex: 1;
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-lg);
  color: var(--text-secondary);
  transition: all var(--transition-fast);
  text-decoration: none;
  gap: var(--space-3);
  position: relative;
}

.nav-item:hover {
  background: var(--bg-elevated);
  color: var(--text-primary);
}

.nav-item.active {
  background: var(--color-primary);
  color: var(--text-primary);
}

.nav-icon {
  width: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-text {
  font-weight: var(--font-weight-medium);
  font-size: var(--font-size-sm);
}

.badge {
  position: absolute;
  right: var(--space-4);
  padding: 2px var(--space-2);
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
}

.badge.primary {
  background: var(--color-primary);
  color: var(--text-primary);
}

.badge.success {
  background: var(--status-success);
  color: var(--text-primary);
}

.sidebar-footer {
  padding: var(--space-4);
  border-top: 1px solid var(--border-primary);
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  object-fit: cover;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.user-name {
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  font-size: var(--font-size-sm);
}

.user-role {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
}

.settings-btn {
  width: 100%;
  padding: var(--space-3);
  border-radius: var(--radius-lg);
  background: var(--bg-elevated);
  border: 1px solid var(--border-secondary);
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: var(--space-3);
  cursor: pointer;
  transition: all var(--transition-fast);
  font-size: var(--font-size-sm);
}

.settings-btn:hover {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: var(--text-primary);
}

/* Scrollbar styles */
.sidebar-nav {
  scrollbar-width: thin;
  scrollbar-color: var(--bg-elevated) transparent;
}

.sidebar-nav::-webkit-scrollbar {
  width: 4px;
}

.sidebar-nav::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background-color: var(--bg-elevated);
  border-radius: var(--radius-full);
}

/* Mobile styles */
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
  }
  
  .sidebar-mobile-open {
    transform: translateX(0);
  }
  
  .sidebar-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--bg-overlay);
    z-index: var(--z-negative);
  }
  
  .collapse-btn {
    display: none;
  }
}
</style> 