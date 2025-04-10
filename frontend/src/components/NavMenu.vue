<template>
  <el-menu
    mode="horizontal"
    background-color="#2c3e50"
    text-color="#fff"
    active-text-color="#ffd04b"
    router
  >
    <el-menu-item index="/">
      <el-icon><HomeFilled /></el-icon>
      {{ $t('nav.home') }}
    </el-menu-item>
    
    <el-menu-item index="/catalog">
      <el-icon><List /></el-icon>
      {{ $t('nav.catalog') }}
    </el-menu-item>
    
    <el-menu-item index="/dashboard" v-if="isAuthenticated">
      <el-icon><User /></el-icon>
      {{ $t('nav.dashboard') }}
    </el-menu-item>
    
    <el-menu-item index="/login" v-if="!isAuthenticated">
      <el-icon><Login /></el-icon>
      {{ $t('nav.login') }}
    </el-menu-item>
    
    <el-menu-item @click="logout" v-if="isAuthenticated">
      <el-icon><Logout /></el-icon>
      {{ $t('nav.logout') }}
    </el-menu-item>
    
    <el-sub-menu index="language">
      <template #title>
        <el-icon><Globe /></el-icon>
        {{ $t('nav.language') }}
      </template>
      <el-menu-item @click="changeLanguage('ru')">Русский</el-menu-item>
      <el-menu-item @click="changeLanguage('en')">English</el-menu-item>
      <el-menu-item @click="changeLanguage('uk')">Українська</el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import {
  HomeFilled,
  List,
  User,
  Login,
  Logout,
  Globe
} from '@element-plus/icons-vue'

export default {
  name: 'NavMenu',
  components: {
    HomeFilled,
    List,
    User,
    Login,
    Logout,
    Globe
  },
  computed: {
    ...mapState(['isAuthenticated'])
  },
  methods: {
    ...mapActions(['logout']),
    changeLanguage(lang) {
      this.$i18n.locale = lang
      localStorage.setItem('language', lang)
    }
  }
}
</script>

<style lang="scss" scoped>
.el-menu {
  border-bottom: none;
}

.el-menu-item {
  height: 60px;
  line-height: 60px;
}

.el-sub-menu {
  float: right;
  margin-right: 20px;
}
</style> 