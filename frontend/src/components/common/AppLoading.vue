<template>
  <div class="loading-overlay">
    <el-loading
      :full-screen="true"
      :text="loadingText"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useUIStore } from '@/stores'

const uiStore = useUIStore()
const loadingText = computed(() => uiStore.loadingText || 'Загрузка...')
</script>

<style lang="scss" scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 9999;
  background-color: rgba(0, 0, 0, 0.1);
}
</style> 