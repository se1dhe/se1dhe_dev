export interface User {
  id: number
  name: string
  email: string
  role: string
  created_at: string
  updated_at: string
}

export interface Project {
  id: number
  name: string
  description: string
  status: string
  created_by: number
  created_at: string
  updated_at: string
}

export interface Task {
  id: number
  title: string
  description: string
  status: string
  priority: string
  project_id: number
  assigned_to: number
  created_by: number
  due_date: string
  created_at: string
  updated_at: string
}

export interface Notification {
  id: string
  title: string
  message: string
  type: 'success' | 'warning' | 'error' | 'info'
  created_at: string
}

export interface Pagination {
  page: number
  per_page: number
  total: number
  total_pages: number
}

export interface ApiResponse<T> {
  data: T
  message?: string
  pagination?: Pagination
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  size: number
  pages: number
} 