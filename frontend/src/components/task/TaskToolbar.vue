<script setup lang="ts">
import { Plus } from '@element-plus/icons-vue'
import { computed } from 'vue'
import type { TaskFilter } from '../../types/task'

interface Props {
  filter: TaskFilter
  total: number
  activeCount: number
  completedCount: number
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:filter': [filter: TaskFilter]
  completeAll: []
  create: []
}>()

const selectedFilter = computed({
  get: () => props.filter,
  set: (value: string) => emit('update:filter', value as TaskFilter),
})
</script>

<template>
  <section class="toolbar" aria-label="任务概览与筛选">
    <div class="toolbar__heading">
      <p class="toolbar__eyebrow">个人工作台</p>
      <div class="toolbar__title-row">
        <h1>我的任务</h1><span class="toolbar__date">本周安排</span>
      </div>
    </div>
    <div class="toolbar__actions">
      <div class="task-stats" aria-label="任务统计">
        <span><b>{{ total }}</b> 全部</span><span><b>{{ activeCount }}</b> 待办</span><span><b>{{ completedCount }}</b> 已完成</span>
      </div>
      <el-button type="primary" :icon="Plus" @click="emit('create')">新增任务</el-button>
    </div>
    <el-button @click="emit('completeAll')">
  全部完成
</el-button>
    <el-tabs v-model="selectedFilter" class="filter-tabs" aria-label="任务状态筛选">
      <el-tab-pane label="全部" name="all" /><el-tab-pane label="未完成" name="active" /><el-tab-pane label="已完成" name="completed" />
    </el-tabs>
  </section>
</template>

<style scoped>
.toolbar { display: grid; grid-template-columns: 1fr auto; gap: 22px 32px; padding: 30px 32px 0; }
.toolbar__eyebrow { margin: 0 0 6px; color: #76827c; font-size: 12px; font-weight: 700; letter-spacing: .12em; }
.toolbar__title-row { display: flex; align-items: baseline; gap: 12px; }
h1 { margin: 0; color: #24312c; font-size: 29px; letter-spacing: -.045em; line-height: 1.15; }
.toolbar__date { color: #89938e; font-size: 13px; }
.toolbar__actions { display: flex; align-items: center; gap: 18px; }
.task-stats { display: flex; gap: 12px; color: #7d8882; font-size: 12px; white-space: nowrap; }
.task-stats b { color: #2b3933; font-size: 14px; }
.filter-tabs { grid-column: 1 / -1; margin-bottom: -1px; }
:deep(.el-tabs__header) { margin: 0; }
:deep(.el-tabs__nav-wrap::after) { height: 1px; background-color: #dfe4de; }
:deep(.el-tabs__item) { height: 42px; color: #738079; font-size: 14px; }
:deep(.el-tabs__item.is-active) { color: #2a7c5e; font-weight: 650; }
:deep(.el-tabs__active-bar) { height: 2px; background: #2a7c5e; }
@media (max-width: 620px) { .toolbar { grid-template-columns: 1fr; gap: 18px; padding: 24px 20px 0; } .toolbar__actions { justify-content: space-between; gap: 10px; } .task-stats { gap: 8px; overflow: hidden; } .toolbar__date { display: none; } }
</style>
