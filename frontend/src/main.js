import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { createI18n } from 'vue-i18n'
import axios from 'axios'
import VueChartJs from 'vue-chartjs'

// Настройка axios
axios.defaults.baseURL = process.env.VUE_APP_API_URL || 'http://localhost:8000'

// Настройка i18n
const i18n = createI18n({
  locale: 'ru',
  fallbackLocale: 'en',
  messages: {
    ru: require('./locales/ru.json'),
    en: require('./locales/en.json'),
    uk: require('./locales/uk.json')
  }
})

// Создание приложения
const app = createApp(App)

// Использование плагинов
app.use(router)
app.use(store)
app.use(ElementPlus)
app.use(i18n)
app.use(VueChartJs)

// Монтирование приложения
app.mount('#app') 