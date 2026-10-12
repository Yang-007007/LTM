export type TaskPriority = 'high' | 'medium' | 'low'

export type TaskFilter = 'all' | 'active' | 'completed'

export interface Task {
  id: number
  title: string
  completed: boolean
  priority: TaskPriority
  deadline: string
  createdAt: string
}

export interface TaskFormData {
  title: string
  priority: TaskPriority
  deadline: string
}
