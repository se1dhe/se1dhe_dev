import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores'
import { ROUTES } from '@/constants'
import MainLayout from '@/layouts/MainLayout.vue'
import Login from '@/views/auth/Login.vue'
import Register from '@/views/auth/Register.vue'
import Dashboard from '@/views/Dashboard.vue'
import Profile from '@/views/Profile.vue'
import Settings from '@/views/Settings.vue'

// Auth views
import ForgotPasswordView from '@/views/auth/ForgotPasswordView.vue'
import ResetPasswordView from '@/views/auth/ResetPasswordView.vue'

// Dashboard views
import OverviewView from '@/views/dashboard/OverviewView.vue'
import AnalyticsView from '@/views/dashboard/AnalyticsView.vue'
import ReportsView from '@/views/dashboard/ReportsView.vue'

// Project views
import ProjectsView from '@/views/projects/ProjectsView.vue'
import ProjectListView from '@/views/projects/ProjectListView.vue'
import ProjectDetailView from '@/views/projects/ProjectDetailView.vue'
import ProjectCreateView from '@/views/projects/ProjectCreateView.vue'
import ProjectEditView from '@/views/projects/ProjectEditView.vue'

// Task views
import TasksView from '@/views/tasks/TasksView.vue'
import TaskListView from '@/views/tasks/TaskListView.vue'
import TaskDetailView from '@/views/tasks/TaskDetailView.vue'
import TaskCreateView from '@/views/tasks/TaskCreateView.vue'
import TaskEditView from '@/views/tasks/TaskEditView.vue'

// User views
import NotificationsView from '@/views/user/NotificationsView.vue'
import SecurityView from '@/views/user/SecurityView.vue'

// Error views
import NotFoundView from '@/views/error/NotFoundView.vue'
import ForbiddenView from '@/views/error/ForbiddenView.vue'
import ServerErrorView from '@/views/error/ServerErrorView.vue'

const routes = [
  {
    path: '/',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'dashboard',
        component: Dashboard
      },
      {
        path: 'profile',
        name: 'profile',
        component: Profile
      },
      {
        path: 'settings',
        name: 'settings',
        component: Settings
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'register',
    component: Register,
    meta: { guest: true }
  },
  {
    path: '/forgot-password',
    name: 'forgot-password',
    component: ForgotPasswordView,
    meta: { requiresAuth: false },
  },
  {
    path: '/reset-password',
    name: 'reset-password',
    component: ResetPasswordView,
    meta: { requiresAuth: false },
  },
  {
    path: ROUTES.PROJECTS,
    name: 'projects',
    component: ProjectsView,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'project-list',
        component: ProjectListView,
      },
      {
        path: 'create',
        name: 'project-create',
        component: ProjectCreateView,
      },
      {
        path: ':id',
        name: 'project-detail',
        component: ProjectDetailView,
      },
      {
        path: ':id/edit',
        name: 'project-edit',
        component: ProjectEditView,
      },
    ],
  },
  {
    path: ROUTES.TASKS,
    name: 'tasks',
    component: TasksView,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'task-list',
        component: TaskListView,
      },
      {
        path: 'create',
        name: 'task-create',
        component: TaskCreateView,
      },
      {
        path: ':id',
        name: 'task-detail',
        component: TaskDetailView,
      },
      {
        path: ':id/edit',
        name: 'task-edit',
        component: TaskEditView,
      },
    ],
  },
  {
    path: '/notifications',
    name: 'notifications',
    component: NotificationsView,
    meta: { requiresAuth: true },
  },
  {
    path: '/security',
    name: 'security',
    component: SecurityView,
    meta: { requiresAuth: true },
  },
  {
    path: '/403',
    name: 'forbidden',
    component: ForbiddenView,
    meta: { requiresAuth: false },
  },
  {
    path: '/500',
    name: 'server-error',
    component: ServerErrorView,
    meta: { requiresAuth: false },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFoundView,
    meta: { requiresAuth: false },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = authStore.isAuthenticated

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next({ name: 'login' })
    } else {
      next()
    }
  } else if (to.matched.some(record => record.meta.guest)) {
    if (isAuthenticated) {
      next({ name: 'dashboard' })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router 