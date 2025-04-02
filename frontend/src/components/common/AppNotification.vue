<template>
  <div class="notifications-container">
    <transition-group name="notification">
      <div
        v-for="notification in notifications"
        :key="notification.id"
        class="notification"
        :class="notification.type"
      >
        <el-icon class="notification-icon">
          <component :is="getIcon(notification.type)" />
        </el-icon>
        <div class="notification-content">
          <div class="notification-title">{{ notification.title }}</div>
          <div class="notification-message">{{ notification.message }}</div>
        </div>
        <el-button
          class="notification-close"
          circle
          @click="removeNotification(notification.id)"
        >
          <el-icon><Close /></el-icon>
        </el-button>
      </div>
    </transition-group>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Close, CircleCheck, CircleClose, Warning, InfoFilled } from '@element-plus/icons-vue'
import { useNotificationStore } from '@/stores'

const notificationStore = useNotificationStore()
const notifications = computed(() => notificationStore.notifications)

const getIcon = (type: string) => {
  switch (type) {
    case 'success':
      return CircleCheck
    case 'warning':
      return Warning
    case 'error':
      return CircleClose
    default:
      return InfoFilled
  }
}

const removeNotification = (id: string) => {
  notificationStore.removeNotification(id)
}
</script>

<style lang="scss" scoped>
.notifications-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.notification {
  display: flex;
  align-items: flex-start;
  padding: 12px 16px;
  border-radius: 4px;
  background-color: var(--el-bg-color);
  box-shadow: var(--el-box-shadow-light);
  min-width: 300px;
  max-width: 400px;

  &.success {
    border-left: 4px solid var(--el-color-success);
  }

  &.warning {
    border-left: 4px solid var(--el-color-warning);
  }

  &.error {
    border-left: 4px solid var(--el-color-danger);
  }

  &.info {
    border-left: 4px solid var(--el-color-info);
  }

  &-icon {
    margin-right: 12px;
    font-size: 20px;
  }

  &-content {
    flex: 1;
  }

  &-title {
    font-weight: 500;
    margin-bottom: 4px;
  }

  &-message {
    font-size: 14px;
    color: var(--el-text-color-secondary);
  }

  &-close {
    margin-left: 12px;
    padding: 0;
  }
}

.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style> 