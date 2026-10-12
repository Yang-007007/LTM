<script setup lang="ts">
import { Calendar, Delete, EditPen } from '@element-plus/icons-vue'
import type { Task } from '../../types/task'

defineProps<{ task: Task }>()
const emit = defineEmits<{ toggle: [id: number]; edit: [task: Task]; remove: [task: Task] }>()
const priorityMap = { high: { label: '高优先级', type: 'danger' as const }, medium: { label: '中优先级', type: 'warning' as const }, low: { label: '低优先级', type: 'info' as const } }
</script>

<template>
  <article class="task-item" :class="{ 'task-item--completed': task.completed }">
    <el-checkbox :model-value="task.completed" :aria-label="`${task.completed ? '标记为未完成' : '标记为已完成'}：${task.title}`" @change="emit('toggle', task.id)" />
    <div class="task-item__body">
      <p class="task-item__title">{{ task.title }}</p>
      <div class="task-item__meta"><el-tag size="small" effect="plain" :type="priorityMap[task.priority].type">{{ priorityMap[task.priority].label }}</el-tag><span><el-icon><Calendar /></el-icon>{{ task.deadline }}</span></div>
    </div>
    <div class="task-item__actions"><el-button text circle :icon="EditPen" aria-label="编辑任务" @click="emit('edit', task)" /><el-button text circle type="danger" :icon="Delete" aria-label="删除任务" @click="emit('remove', task)" /></div>
  </article>
</template>

<style scoped>
.task-item { display: grid; grid-template-columns: auto minmax(0, 1fr) auto; align-items: center; gap: 12px; padding: 16px 0; border-bottom: 1px solid #e5e9e4; }
.task-item__title { margin: 0; color: #2a3731; font-size: 14px; font-weight: 600; line-height: 1.45; }
.task-item__meta { display: flex; align-items: center; gap: 10px; margin-top: 8px; color: #7c8781; font-size: 12px; }
.task-item__meta span { display: inline-flex; align-items: center; gap: 4px; }.task-item__actions { display: flex; }
.task-item--completed .task-item__title { color: #9ba39e; font-weight: 500; text-decoration: line-through; }
</style>
