<script setup lang="ts">
import { CircleClose } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { computed, onMounted, ref } from 'vue'
import TaskForm from '../components/task/TaskForm.vue'
import TaskList from '../components/task/TaskList.vue'
import TaskToolbar from '../components/task/TaskToolbar.vue'
import { mockTasks } from '../mock/tasks'
import type { Task, TaskFilter, TaskFormData } from '../types/task'

const tasks = ref<Task[]>(mockTasks.map((task) => ({ ...task })))
const currentFilter = ref<TaskFilter>('all')
const isLoading = ref(true)
const hasError = ref(false)
const dialogVisible = ref(false)
const editingTask = ref<Task | null>(null)
const taskStats = computed(() => { const completedCount = tasks.value.filter((task) => task.completed).length; return { total: tasks.value.length, completedCount, activeCount: tasks.value.length - completedCount } })
const filteredTasks = computed(() => { if (currentFilter.value === 'active') return tasks.value.filter((task) => !task.completed); if (currentFilter.value === 'completed') return tasks.value.filter((task) => task.completed); return tasks.value })
const formMode = computed<'create' | 'edit'>(() => (editingTask.value ? 'edit' : 'create'))
onMounted(() => { window.setTimeout(() => { isLoading.value = false }, 550) })
function openCreateDialog() { editingTask.value = null; dialogVisible.value = true }
function openEditDialog(task: Task) { editingTask.value = { ...task }; dialogVisible.value = true }
function closeDialog() { dialogVisible.value = false; editingTask.value = null }
function toggleTask(id: number) { const task = tasks.value.find((item) => item.id === id); if (!task) return; task.completed = !task.completed; ElMessage.success(task.completed ? '任务已标记为完成' : '任务已恢复为待办') }
function saveTask(formData: TaskFormData) { if (editingTask.value) { const task = tasks.value.find((item) => item.id === editingTask.value?.id); if (task) Object.assign(task, formData); ElMessage.success('任务已更新') } else { tasks.value.unshift({ id: Math.max(0, ...tasks.value.map((task) => task.id)) + 1, ...formData, completed: false, createdAt: new Date().toISOString().slice(0, 10) }); ElMessage.success('任务已创建') } closeDialog() }
function completeAll() {
  tasks.value.forEach((task) => {
    task.completed = true
  })
}
async function removeTask(task: Task) { try { await ElMessageBox.confirm(`确定删除“${task.title}”吗？删除后无法恢复。`, '删除任务', { confirmButtonText: '确认删除', cancelButtonText: '取消', type: 'warning' }); tasks.value = tasks.value.filter((item) => item.id !== task.id); ElMessage.success('任务已删除') } catch { /* 用户取消删除时无需提示。 */ } }
</script>

<template>
  
  <el-container class="task-page">
    <main class="task-page__main">
      <TaskToolbar v-model:filter="currentFilter" :total="taskStats.total" :active-count="taskStats.activeCount" @complete-all="completeAll"
        :completed-count="taskStats.completedCount" @create="openCreateDialog" />
      <section class="task-page__content" aria-label="任务列表">
        <el-alert v-if="hasError" title="任务暂时无法加载，请稍后重试。" type="error" :closable="false" show-icon
          class="task-page__error" />
        <el-skeleton v-else-if="isLoading" :rows="6" animated class="task-page__loading" />
        <template v-else>
          <TaskList v-if="filteredTasks.length" :tasks="filteredTasks" @toggle="toggleTask" @edit="openEditDialog"
            @remove="removeTask" /><el-empty v-else :image-size="92" description="这里还没有任务"><template #image><el-icon
                class="empty-icon">
                <CircleClose />
              </el-icon></template><el-button type="primary" @click="openCreateDialog">创建第一条任务</el-button></el-empty>
        </template>
      </section>
    </main>
  </el-container>
  <TaskForm :visible="dialogVisible" :mode="formMode" :initial-task="editingTask" @close="closeDialog"
    @submit="saveTask" />
</template>

<style scoped>
.task-page {
  min-height: 100vh;
  padding: 40px 24px;
}

.task-page__main {
  width: min(1120px, 100%);
  margin: 0 auto;
  overflow: hidden;
  border: 1px solid #dfe4de;
  border-radius: 10px;
  background: #fff;
  box-shadow: 0 12px 30px rgba(45, 59, 52, .07);
}

.task-page__content {
  min-height: 440px;
}

.task-page__loading {
  padding: 26px 32px;
}

.task-page__error {
  width: auto;
  margin: 20px 32px;
}

.empty-icon {
  color: #a2ada6;
  font-size: 76px;
}

@media (max-width: 700px) {
  .task-page {
    padding: 0;
  }

  .task-page__main {
    min-height: 100vh;
    border: 0;
    border-radius: 0;
    box-shadow: none;
  }

  .task-page__loading {
    padding: 24px 20px;
  }

  .task-page__content {
    padding: 0 20px;
  }

  .task-page__error {
    margin: 18px 0;
  }
}
</style>
