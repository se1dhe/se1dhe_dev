<template>
  <div class="server-error">
    <el-result
      icon="error"
      title="500"
      sub-title="Sorry, something went wrong on our servers."
    >
      <template #extra>
        <el-button type="primary" @click="handleRetry">
          Try Again
        </el-button>
        <el-button @click="router.push('/')">
          Back to Home
        </el-button>
      </template>
    </el-result>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const handleRetry = () => {
  window.location.reload()
}
</script>

<style scoped lang="scss">
.server-error {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style> 