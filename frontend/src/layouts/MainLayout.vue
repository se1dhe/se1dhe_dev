<template>
  <div class="layout">
    <Sidebar />
    <div class="layout-content" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
      <Header />
      <main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import Sidebar from '@/components/Sidebar.vue'
import Header from '@/components/Header.vue'
import { useSidebarStore } from '@/stores/sidebar'

const sidebarStore = useSidebarStore()
const isSidebarCollapsed = computed(() => sidebarStore.isCollapsed)

// Handle escape key to close sidebar on mobile
const handleEscKey = (event: KeyboardEvent) => {
  if (event.key === 'Escape' && window.innerWidth < 768) {
    sidebarStore.collapse()
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleEscKey)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscKey)
})
</script>

<style scoped>
.layout {
  min-height: 100vh;
  display: flex;
  background: var(--bg-base);
  color: var(--text-primary);
}

.layout-content {
  flex: 1;
  margin-left: var(--sidebar-width);
  transition: margin-left var(--transition-normal);
  position: relative;
  overflow-x: hidden;
}

.layout-content.sidebar-collapsed {
  margin-left: var(--sidebar-width-collapsed);
}

.main-content {
  padding: calc(var(--header-height) + var(--space-8)) var(--space-8) var(--space-8);
  min-height: 100vh;
  max-width: var(--content-width);
  margin: 0 auto;
  width: 100%;
}

/* Page transition animations */
.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--transition-normal);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .layout-content {
    margin-left: 0;
  }
  
  .layout-content.sidebar-collapsed {
    margin-left: 0;
  }
  
  .main-content {
    padding: calc(var(--header-height) + var(--space-4)) var(--space-4) var(--space-4);
  }
}

/* Scrollbar styling */
.main-content {
  scrollbar-width: thin;
  scrollbar-color: var(--bg-elevated) var(--bg-surface);
}

.main-content::-webkit-scrollbar {
  width: 8px;
}

.main-content::-webkit-scrollbar-track {
  background: var(--bg-surface);
}

.main-content::-webkit-scrollbar-thumb {
  background-color: var(--bg-elevated);
  border-radius: var(--radius-full);
  border: 2px solid var(--bg-surface);
}

.main-content::-webkit-scrollbar-thumb:hover {
  background-color: var(--text-tertiary);
}
</style> 