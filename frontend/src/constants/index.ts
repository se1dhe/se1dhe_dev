export * from './api'
export * from './routes'

export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  PROJECTS: '/projects',
  TASKS: '/tasks',
  PROFILE: '/profile',
  SETTINGS: '/settings',
  NOTIFICATIONS: '/notifications',
  SECURITY: '/security',
} as const

export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    LOGOUT: '/auth/logout',
    ME: '/auth/me',
    PROFILE: '/auth/profile',
    FORGOT_PASSWORD: '/auth/forgot-password',
    RESET_PASSWORD: '/auth/reset-password',
  },
  PROJECTS: {
    LIST: '/projects',
    DETAIL: (id: number) => `/projects/${id}`,
    CREATE: '/projects',
    UPDATE: (id: number) => `/projects/${id}`,
    DELETE: (id: number) => `/projects/${id}`,
  },
  TASKS: {
    LIST: '/tasks',
    DETAIL: (id: number) => `/tasks/${id}`,
    CREATE: '/tasks',
    UPDATE: (id: number) => `/tasks/${id}`,
    DELETE: (id: number) => `/tasks/${id}`,
  },
} as const

export const STORAGE_KEYS = {
  TOKEN: 'token',
  USER: 'user',
} as const 