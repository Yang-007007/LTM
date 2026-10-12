import type { Task } from '../types/task'

export const mockTasks: Task[] = [
  { id: 1, title: '整理 Vue 3 Composition API 学习笔记', completed: false, priority: 'high', deadline: '2026-10-11', createdAt: '2026-10-09' },
  { id: 2, title: '完成任务列表的筛选交互', completed: false, priority: 'high', deadline: '2026-10-10', createdAt: '2026-10-09' },
  { id: 3, title: '为任务表单补充 TypeScript 类型', completed: false, priority: 'medium', deadline: '2026-10-12', createdAt: '2026-10-09' },
  { id: 4, title: '复习 ref 与 computed 的区别', completed: true, priority: 'medium', deadline: '2026-10-09', createdAt: '2026-10-08' },
  { id: 5, title: '设计 FastAPI 的 tasks 接口字段', completed: false, priority: 'medium', deadline: '2026-10-13', createdAt: '2026-10-09' },
  { id: 6, title: '阅读 Element Plus Form 文档', completed: true, priority: 'low', deadline: '2026-10-08', createdAt: '2026-10-08' },
  { id: 7, title: '规划 MySQL tasks 表结构', completed: false, priority: 'low', deadline: '2026-10-15', createdAt: '2026-10-09' },
  { id: 8, title: '检查任务页的移动', completed: true, priority: 'low', deadline: '2026-10-09', createdAt: '2026-10-09' },
]
