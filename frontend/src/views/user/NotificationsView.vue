<template>
  <div class="notifications">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>Notifications</h2>
          <div class="header-actions">
            <el-button type="primary" @click="markAllAsRead" :loading="markingAsRead">
              Mark All as Read
            </el-button>
            <el-button type="danger" @click="clearAll" :loading="clearing">
              Clear All
            </el-button>
          </div>
        </div>
      </template>

      <el-tabs v-model="activeTab">
        <el-tab-pane label="All" name="all">
          <notification-list
            :notifications="notifications"
            :loading="loading"
            @mark-read="handleMarkAsRead"
            @delete="handleDelete"
          />
        </el-tab-pane>

        <el-tab-pane label="Unread" name="unread">
          <notification-list
            :notifications="unreadNotifications"
            :loading="loading"
            @mark-read="handleMarkAsRead"
            @delete="handleDelete"
          />
        </el-tab-pane>
      </el-tabs>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import NotificationList from '@/components/notifications/NotificationList.vue'

const activeTab = ref('all')
const loading = ref(false)
const markingAsRead = ref(false)
const clearing = ref(false)
const notifications = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

const unreadNotifications = computed(() => {
  return notifications.value.filter((notification: any) => !notification.read)
})

const fetchNotifications = async () => {
  loading.value = true
  try {
    // TODO: Implement API call to fetch notifications
    notifications.value = []
    total.value = 0
  } catch (error) {
    console.error('Error fetching notifications:', error)
    ElMessage.error('Failed to fetch notifications')
  } finally {
    loading.value = false
  }
}

const handleMarkAsRead = async (notificationId: number) => {
  try {
    // TODO: Implement API call to mark notification as read
    ElMessage.success('Notification marked as read')
    await fetchNotifications()
  } catch (error) {
    console.error('Error marking notification as read:', error)
    ElMessage.error('Failed to mark notification as read')
  }
}

const markAllAsRead = async () => {
  markingAsRead.value = true
  try {
    // TODO: Implement API call to mark all notifications as read
    ElMessage.success('All notifications marked as read')
    await fetchNotifications()
  } catch (error) {
    console.error('Error marking all notifications as read:', error)
    ElMessage.error('Failed to mark all notifications as read')
  } finally {
    markingAsRead.value = false
  }
}

const handleDelete = async (notificationId: number) => {
  try {
    // TODO: Implement API call to delete notification
    ElMessage.success('Notification deleted')
    await fetchNotifications()
  } catch (error) {
    console.error('Error deleting notification:', error)
    ElMessage.error('Failed to delete notification')
  }
}

const clearAll = async () => {
  clearing.value = true
  try {
    // TODO: Implement API call to clear all notifications
    ElMessage.success('All notifications cleared')
    await fetchNotifications()
  } catch (error) {
    console.error('Error clearing notifications:', error)
    ElMessage.error('Failed to clear notifications')
  } finally {
    clearing.value = false
  }
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  fetchNotifications()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchNotifications()
}

onMounted(() => {
  fetchNotifications()
})
</script>

<style scoped lang="scss">
.notifications {
  padding: 20px;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    h2 {
      margin: 0;
    }

    .header-actions {
      display: flex;
      gap: 10px;
    }
  }

  .pagination-container {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
}
</style> 