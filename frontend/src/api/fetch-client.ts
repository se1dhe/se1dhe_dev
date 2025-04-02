import { API_ENDPOINTS, STORAGE_KEYS } from '@/constants'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

interface RequestOptions extends RequestInit {
  params?: Record<string, string>
}

interface Headers {
  'Content-Type': string
  'Accept': string
  'Authorization'?: string
}

interface User {
  id: number
  name: string
  email: string
  role: string
  created_at: string
  updated_at: string
}

class ApiClient {
  async request<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
    const { params = {}, ...init } = options

    // Add query parameters if they exist
    const queryParams = new URLSearchParams(params).toString()
    const url = `${API_URL}${endpoint}${queryParams ? `?${queryParams}` : ''}`

    const defaultHeaders: Headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }

    // Add authorization header if token exists
    const token = localStorage.getItem(STORAGE_KEYS.TOKEN)
    if (token) {
      defaultHeaders['Authorization'] = `Bearer ${token}`
    }

    try {
      const response = await fetch(url, {
        ...init,
        headers: {
          ...defaultHeaders,
          ...init.headers
        },
        credentials: 'include'
      })

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'An error occurred' }))
        throw new Error(error.detail || 'An error occurred')
      }

      return response.json()
    } catch (error) {
      if (error instanceof Error) {
        throw new Error(error.message)
      }
      throw new Error('An unexpected error occurred')
    }
  }

  async login(email: string, password: string) {
    return this.request<{ access_token: string; token_type: string }>(API_ENDPOINTS.AUTH.LOGIN, {
      method: 'POST',
      body: JSON.stringify({ email, password })
    })
  }

  async register(data: { name: string; email: string; password: string }) {
    return this.request<User>(API_ENDPOINTS.AUTH.REGISTER, {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  async logout() {
    return this.request<void>(API_ENDPOINTS.AUTH.LOGOUT, {
      method: 'POST'
    })
  }

  async getMe() {
    return this.request<User>(API_ENDPOINTS.AUTH.ME, {
      method: 'GET'
    })
  }

  async updateProfile(data: {
    name: string
    email: string
    current_password: string
    new_password: string
  }) {
    return this.request<User>(API_ENDPOINTS.AUTH.PROFILE, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  }

  async forgotPassword(email: string) {
    return this.request<{ message: string }>(API_ENDPOINTS.AUTH.FORGOT_PASSWORD, {
      method: 'POST',
      body: JSON.stringify({ email })
    })
  }

  async resetPassword(token: string, password: string) {
    return this.request<{ message: string }>(API_ENDPOINTS.AUTH.RESET_PASSWORD, {
      method: 'POST',
      body: JSON.stringify({ token, password })
    })
  }
}

export const api = new ApiClient() 