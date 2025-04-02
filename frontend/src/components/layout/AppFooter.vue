<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-left">
        <span>© {{ currentYear }} SE1DHE Development</span>
      </div>
      <div class="footer-right">
        <el-dropdown>
          <span class="language-selector">
            {{ currentLanguage }}
            <el-icon><ArrowDown /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="changeLanguage('ru')">Русский</el-dropdown-item>
              <el-dropdown-item @click="changeLanguage('en')">English</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ArrowDown } from '@element-plus/icons-vue'
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

const currentYear = computed(() => new Date().getFullYear())
const currentLanguage = computed(() => locale.value === 'ru' ? 'Русский' : 'English')

const changeLanguage = (lang: string) => {
  locale.value = lang
}
</script>

<style lang="scss" scoped>
.footer {
  height: 60px;
  background-color: var(--el-bg-color);
  border-top: 1px solid var(--el-border-color-light);
  padding: 0 20px;

  &-content {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .language-selector {
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 4px;
  }
}
</style> 