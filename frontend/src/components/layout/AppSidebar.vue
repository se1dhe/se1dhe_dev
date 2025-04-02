<template>
  <aside class="sidebar">
    <el-menu
      :default-active="activeMenu"
      class="sidebar-menu"
      :router="true"
      :collapse="isCollapsed"
    >
      <el-menu-item index="/dashboard">
        <el-icon><Monitor /></el-icon>
        <template #title>Дашборд</template>
      </el-menu-item>
      
      <el-menu-item index="/projects">
        <el-icon><Folder /></el-icon>
        <template #title>Проекты</template>
      </el-menu-item>

      <el-menu-item index="/tasks">
        <el-icon><List /></el-icon>
        <template #title>Задачи</template>
      </el-menu-item>

      <el-menu-item index="/users">
        <el-icon><User /></el-icon>
        <template #title>Пользователи</template>
      </el-menu-item>

      <el-menu-item index="/settings">
        <el-icon><Setting /></el-icon>
        <template #title>Настройки</template>
      </el-menu-item>
    </el-menu>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { Monitor, Folder, List, User, Setting } from '@element-plus/icons-vue'

const route = useRoute()
const activeMenu = computed(() => route.path)
const isCollapsed = computed(() => false) // Можно добавить состояние для сворачивания
</script>

<style lang="scss" scoped>
.sidebar {
  width: 240px;
  height: 100%;
  background-color: var(--el-menu-bg-color);
  border-right: 1px solid var(--el-border-color-light);
  transition: width 0.3s;

  &-menu {
    height: 100%;
    border-right: none;
  }
}
</style> 