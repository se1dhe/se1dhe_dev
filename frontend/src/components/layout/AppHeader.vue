<template>
  <header class="app-header">
    <div class="header-left">
      <el-button
        class="toggle-sidebar"
        circle
        @click="settingsStore.toggleSidebar"
      >
        <el-icon><Fold v-if="!settingsStore.sidebarCollapsed" /><Expand v-else /></el-icon>
      </el-button>
    </div>
    <div class="header-right">
      <el-button
        class="toggle-theme"
        circle
        @click="themeStore.toggleTheme"
      >
        <el-icon><Sunny v-if="!themeStore.isDark" /><Moon v-else /></el-icon>
      </el-button>
      <el-dropdown trigger="click">
        <span class="user-dropdown">
          {{ authStore.user?.name }}
          <el-icon><ArrowDown /></el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="router.push('/profile')">
              <el-icon><User /></el-icon>
              Профиль
            </el-dropdown-item>
            <el-dropdown-item divided @click="handleLogout">
              <el-icon><SwitchButton /></el-icon>
              Выйти
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import {
  Fold,
  Expand,
  Sunny,
  Moon,
  ArrowDown,
  User,
  SwitchButton
} from '@element-plus/icons-vue'
import { useAuthStore, useThemeStore, useSettingsStore } from '@/stores'

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()
const settingsStore = useSettingsStore()

const handleLogout = async () => {
  try {
    await authStore.logout()
    router.push('/login')
  } catch (error) {
    console.error('Logout error:', error)
  }
}
</script>

<style lang="scss" scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
  padding: 0 20px;
  background-color: var(--el-bg-color);
  border-bottom: 1px solid var(--border-color-light);

  .header-left,
  .header-right {
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .user-dropdown {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    color: var(--el-text-color-primary);
  }
}
</style> 