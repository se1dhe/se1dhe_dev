export interface Project {
  id: number
  title: string
  description: string
  status: 'active' | 'completed' | 'archived'
  priority: 'low' | 'medium' | 'high'
  start_date: string
  end_date: string
  created_at: string
  updated_at: string
  user_id: number
  team_id: number | null
} 