<template>
  <div id="app">
    <el-container>
      <el-header>
        <nav-menu />
      </el-header>
      
      <el-main>
        <router-view />
      </el-main>
      
      <el-footer>
        <app-footer />
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import NavMenu from './components/NavMenu.vue'
import AppFooter from './components/AppFooter.vue'

export default {
  name: 'App',
  components: {
    NavMenu,
    AppFooter
  }
}
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.el-container {
  flex: 1;
}

.el-header {
  background-color: #2c3e50;
  color: white;
  padding: 0;
}

.el-main {
  padding: 20px;
  background-color: #f5f7fa;
}

.el-footer {
  background-color: #2c3e50;
  color: white;
  padding: 20px;
}
</style> 