export interface User {
  id: number
  name: string
  email: string
  role: 'user' | 'admin'
  avatar?: string
  created_at: string
  updated_at: string
  last_login?: string
  is_active: boolean
  settings?: UserSettings
}

export interface UserSettings {
  theme: 'light' | 'dark'
  notifications: {
    email: boolean
    push: boolean
    telegram: boolean
  }
  language: string
  timezone: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  name: string
  email: string
  password: string
  password_confirm: string
}

export interface UpdateProfileRequest {
  name?: string
  email?: string
  avatar?: string
  bio?: string
}

export interface ChangePasswordRequest {
  current_password: string
  new_password: string
  new_password_confirm: string
}

export interface ForgotPasswordRequest {
  email: string
}

export interface ResetPasswordRequest {
  token: string
  password: string
  password_confirm: string
} 