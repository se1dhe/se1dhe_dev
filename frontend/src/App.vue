<template>
  <el-config-provider :locale="locale">
    <div class="app">
      <AppHeader v-if="isAuthenticated" />
      <div class="app-content">
        <AppSidebar v-if="isAuthenticated" />
        <main class="main-content">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </main>
      </div>
      <AppFooter v-if="isAuthenticated" />
      <AppLoading v-if="isLoading" />
      <AppNotification />
    </div>
  </el-config-provider>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores'
import { useUIStore } from '@/stores'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import AppLoading from '@/components/common/AppLoading.vue'
import AppNotification from '@/components/common/AppNotification.vue'
import ru from 'element-plus/es/locale/lang/ru'
import '@/assets/styles/variables.css'
import '@/assets/styles/global.css'

const authStore = useAuthStore()
const uiStore = useUIStore()

const isAuthenticated = computed(() => authStore.isAuthenticated)
const isLoading = computed(() => uiStore.isLoading)
const locale = ru

// Initialize theme from localStorage or system preference
onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme) {
    document.documentElement.classList.add(savedTheme)
  } else {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    document.documentElement.classList.add(prefersDark ? 'dark' : 'light')
    localStorage.setItem('theme', prefersDark ? 'dark' : 'light')
  }
})
</script>

<style lang="scss">
@use '@/assets/styles/_main' as *;

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-base);
  color: var(--text-primary);
}

.app-content {
  flex: 1;
  display: flex;
}

.main-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--transition-normal);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Ensure proper scrollbar styling across the app */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: var(--bg-surface);
}

::-webkit-scrollbar-thumb {
  background: var(--bg-elevated);
  border-radius: var(--radius-full);
}

::-webkit-scrollbar-thumb:hover {
  background: var(--text-tertiary);
}

/* Selection styling */
::selection {
  background: var(--color-primary);
  color: var(--text-primary);
}

/* Focus outline */
:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

:focus:not(:focus-visible) {
  outline: none;
}

/* Ensure proper font rendering */
body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}
</style> 