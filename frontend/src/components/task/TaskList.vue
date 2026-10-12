<script setup lang="ts">
import { Calendar, Delete, EditPen } from '@element-plus/icons-vue'
import TaskItem from './TaskItem.vue'
import type { Task } from '../../types/task'

defineProps<{ tasks: Task[] }>()
const emit = defineEmits<{ toggle: [id: number]; edit: [task: Task]; remove: [task: Task] }>()
const priorityMap = { high: { label: '高优先级', type: 'danger' as const }, medium: { label: '中优先级', type: 'warning' as const }, low: { label: '低优先级', type: 'info' as const } }
</script>

<template>
  <div class="task-list">
    <div class="task-list__desktop">
      <el-table :data="tasks" row-key="id" class="task-table" table-layout="fixed">
        <el-table-column label="状态" width="72" align="center"><template #default="{ row }: { row: Task }"><el-checkbox :model-value="row.completed" :aria-label="`${row.completed ? '标记为未完成' : '标记为已完成'}：${row.title}`" @change="emit('toggle', row.id)" /></template></el-table-column>
        <el-table-column label="任务" min-width="290"><template #default="{ row }: { row: Task }"><span class="task-title" :class="{ 'task-title--completed': row.completed }">{{ row.title }}</span></template></el-table-column>
        <el-table-column label="优先级" width="120"><template #default="{ row }: { row: Task }"><el-tag size="small" effect="plain" :type="priorityMap[row.priority].type">{{ priorityMap[row.priority].label }}</el-tag></template></el-table-column>
        <el-table-column label="截止日期" width="144"><template #default="{ row }: { row: Task }"><span class="date-cell"><el-icon><Calendar /></el-icon>{{ row.deadline }}</span></template></el-table-column>
        <el-table-column label="创建于" width="118"><template #default="{ row }: { row: Task }">{{ row.createdAt }}</template></el-table-column>
        <el-table-column label="操作" width="112" align="right"><template #default="{ row }: { row: Task }"><el-button text :icon="EditPen" @click="emit('edit', row)">编辑</el-button><el-button text type="danger" :icon="Delete" @click="emit('remove', row)">删除</el-button></template></el-table-column>
      </el-table>
    </div>
    <div class="task-list__mobile"><TaskItem v-for="task in tasks" :key="task.id" :task="task" @toggle="emit('toggle', $event)" @edit="emit('edit', $event)" @remove="emit('remove', $event)" /></div>
  </div>
</template>

<style scoped>
.task-list__mobile { display: none; }
:deep(.task-table) { --el-table-header-bg-color: #fafbf8; --el-table-border-color: #e5e9e4; --el-table-row-hover-bg-color: #f7faf6; --el-table-text-color: #6e7b74; --el-table-header-text-color: #7d8882; font-size: 13px; }
:deep(.task-table th.el-table__cell) { height: 46px; font-size: 12px; font-weight: 650; }:deep(.task-table td.el-table__cell) { height: 62px; }
.task-title { color: #2b3832; font-weight: 600; }.task-title--completed { color: #9ba39e; font-weight: 500; text-decoration: line-through; }
.date-cell { display: inline-flex; align-items: center; gap: 5px; }
@media (max-width: 700px) { .task-list__desktop { display: none; }.task-list__mobile { display: block; } }
</style>
