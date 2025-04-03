// Bot types
export type BotStatus = 'active' | 'inactive';

export interface Bot {
  id: number;
  name: string;
  description: string;
  status: BotStatus;
  users: number;
  price: number;
  category: string;
}

// User types
export type UserRole = 'admin' | 'user';
export type UserStatus = 'active' | 'inactive';

export interface User {
  id: number;
  name: string;
  email: string;
  role: UserRole;
  status: UserStatus;
  telegramUsername?: string;
  createdAt: string;
}

// Category types
export interface Category {
  id: number;
  name: string;
  description: string;
}

// Subscription types
export type SubscriptionStatus = 'active' | 'expired' | 'cancelled';

export interface Subscription {
  id: number;
  botId: number;
  userId: number;
  startDate: string;
  endDate: string;
  status: SubscriptionStatus;
} 