import { createI18n } from 'vue-i18n'
import ru from './ru'

export default createI18n({
  legacy: false,
  locale: 'ru',
  fallbackLocale: 'ru',
  messages: {
    ru
  }
}) 