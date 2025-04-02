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
  project_id: number
  project: {
    id: number
    name: string
  }
  status: string
  priority: string
  due_date: string
  created_by: number
  assigned_to: number
  created_at: string
  updated_at: string
}

export interface Notification {
  id: string
  title: string
  message: string
  type: 'success' | 'error' | 'info' | 'warning'
  created_at: string
} 