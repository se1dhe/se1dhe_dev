<template>
  <div class="notification-list">
    <el-empty v-if="!loading && notifications.length === 0" description="No notifications" />
    
    <div v-else class="notifications">
      <div v-for="notification in notifications" :key="notification.id" class="notification-item">
        <div class="notification-content" :class="{ unread: !notification.read }">
          <div class="notification-icon">
            <el-icon :size="24">
              <component :is="getNotificationIcon(notification.type)" />
            </el-icon>
          </div>
          
          <div class="notification-details">
            <div class="notification-title">{{ notification.title }}</div>
            <div class="notification-message">{{ notification.message }}</div>
            <div class="notification-meta">
              <span class="time">{{ formatTime(notification.created_at) }}</span>
              <span v-if="notification.type === 'task'" class="project">
                Project: {{ notification.project_name }}
              </span>
            </div>
          </div>
        </div>

        <div class="notification-actions">
          <el-button
            v-if="!notification.read"
            type="primary"
            link
            @click="$emit('mark-read', notification.id)"
          >
            Mark as Read
          </el-button>
          <el-button type="danger" link @click="$emit('delete', notification.id)">
            Delete
          </el-button>
        </div>
      </div>
    </div>

    <el-skeleton v-if="loading" :rows="5" animated />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Bell, Document, User, Warning } from '@element-plus/icons-vue'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'

dayjs.extend(relativeTime)

interface Notification {
  id: number
  type: 'task' | 'project' | 'system' | 'user'
  title: string
  message: string
  read: boolean
  created_at: string
  project_name?: string
}

const props = defineProps<{
  notifications: Notification[]
  loading: boolean
}>()

const emit = defineEmits<{
  (e: 'mark-read', id: number): void
  (e: 'delete', id: number): void
}>()

const getNotificationIcon = (type: string) => {
  const icons: Record<string, any> = {
    task: Document,
    project: Document,
    system: Warning,
    user: User
  }
  return icons[type] || Bell
}

const formatTime = (timestamp: string) => {
  return dayjs(timestamp).fromNow()
}
</script>

<style scoped lang="scss">
.notification-list {
  .notifications {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .notification-item {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 16px;
    border-radius: 8px;
    background-color: var(--el-bg-color);
    border: 1px solid var(--el-border-color-light);
    transition: all 0.3s ease;

    &:hover {
      box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    }

    .notification-content {
      display: flex;
      gap: 16px;
      flex: 1;

      &.unread {
        background-color: var(--el-color-primary-light-9);
      }

      .notification-icon {
        color: var(--el-color-primary);
      }

      .notification-details {
        flex: 1;

        .notification-title {
          font-weight: 600;
          margin-bottom: 4px;
        }

        .notification-message {
          color: var(--el-text-color-regular);
          margin-bottom: 8px;
        }

        .notification-meta {
          display: flex;
          gap: 16px;
          font-size: 12px;
          color: var(--el-text-color-secondary);

          .project {
            color: var(--el-color-primary);
          }
        }
      }
    }

    .notification-actions {
      display: flex;
      gap: 8px;
    }
  }
}
</style> 