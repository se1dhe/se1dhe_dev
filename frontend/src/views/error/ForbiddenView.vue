<template>
  <div class="forbidden">
    <el-result
      icon="error"
      title="403"
      sub-title="Sorry, you don't have permission to access this page."
    >
      <template #extra>
        <el-button type="primary" @click="router.push('/')">
          Back to Home
        </el-button>
      </template>
    </el-result>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<style scoped lang="scss">
.forbidden {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style> 