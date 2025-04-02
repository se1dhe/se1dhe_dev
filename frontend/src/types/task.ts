export type TaskStatus = 'pending' | 'in_progress' | 'completed' | 'cancelled'
export type TaskPriority = 'low' | 'medium' | 'high'

export interface Task {
  id: number
  title: string
  description: string
  status: TaskStatus
  priority: TaskPriority
  due_date: string
  created_at: string
  updated_at: string
  user_id: number
  project_id: number | null
}

export interface DashboardStats {
  active_tasks: number
  active_tasks_trend: number
  completed_tasks: number
  completed_tasks_trend: number
  work_hours: number
  work_hours_trend: number
  efficiency: number
  efficiency_trend: number
} 