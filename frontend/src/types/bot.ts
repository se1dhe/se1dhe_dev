export interface Bot {
  id: number
  name: string
  description: string
  price: number
  category_id: number
  features: string[]
  images: string[]
  videos: string[]
  readme: string
  created_at: string
  updated_at: string
  discount?: number
  rating: number
  reviews_count: number
  sales_count: number
  reviews?: BotReview[]
}

export interface BotCategory {
  id: number
  name: string
  description: string
  image: string
  discount?: number
  created_at: string
  updated_at: string
}

export interface BotReview {
  id: number
  bot_id: number
  user_id: number
  rating: number
  comment: string
  created_at: string
  updated_at: string
  user: {
    id: number
    name: string
    avatar: string
  }
}

export interface BotSubscription {
  id: number
  bot_id: number
  user_id: number
  status: 'active' | 'expired' | 'cancelled'
  start_date: string
  end_date: string
  created_at: string
  updated_at: string
  bot: Bot
  stats: {
    uptime: number
    users_count: number
  }
} 