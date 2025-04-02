import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import i18n from './i18n'
import { useAuthStore } from './stores'
import { useUIStore } from './stores'
import { useThemeStore } from './stores'
import { useSettingsStore } from './stores'
import { useNotificationStore } from './stores'
import { useProjectStore } from './stores'
import { useTaskStore } from './stores'
import { useUserStore } from './stores'
import './assets/styles/variables.css'
import './assets/styles/global.css'

// Create app instance
const app = createApp(App)

// Create Pinia instance
const pinia = createPinia()

// Use plugins
app.use(pinia)
app.use(router)
app.use(ElementPlus)
app.use(i18n)

// Initialize stores
const authStore = useAuthStore()
const uiStore = useUIStore()
const themeStore = useThemeStore()
const settingsStore = useSettingsStore()
const notificationStore = useNotificationStore()
const projectStore = useProjectStore()
const taskStore = useTaskStore()
const userStore = useUserStore()

// Mount app
app.mount('#app') 