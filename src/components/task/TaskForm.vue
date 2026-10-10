<script setup lang="ts">
import type { FormInstance, FormRules } from 'element-plus'
import { computed, reactive, ref, watch } from 'vue'
import type { Task, TaskFormData, TaskPriority } from '../../types/task'

interface Props { visible: boolean; mode: 'create' | 'edit'; initialTask: Task | null }
const props = defineProps<Props>()
const emit = defineEmits<{ close: []; submit: [formData: TaskFormData] }>()
const formRef = ref<FormInstance>()
const form = reactive<TaskFormData>({ title: '', priority: 'medium', deadline: '' })
const rules: FormRules<TaskFormData> = { title: [{ required: true, message: '请输入任务标题', trigger: 'blur' }, { min: 2, max: 60, message: '标题长度应为 2 到 60 个字符', trigger: 'blur' }], priority: [{ required: true, message: '请选择优先级', trigger: 'change' }], deadline: [{ required: true, message: '请选择截止日期', trigger: 'change' }] }
const dialogTitle = computed(() => (props.mode === 'create' ? '新增任务' : '编辑任务'))

function syncForm() { form.title = props.initialTask?.title ?? ''; form.priority = props.initialTask?.priority ?? 'medium'; form.deadline = props.initialTask?.deadline ?? '' }
watch(() => [props.visible, props.initialTask] as const, ([visible]) => { if (visible) { syncForm(); void formRef.value?.clearValidate() } }, { immediate: true })
function close() { emit('close') }
function handleVisibleChange(value: boolean) { if (!value) close() }
async function submitForm() { const valid = await formRef.value?.validate().catch(() => false); if (!valid) return; emit('submit', { title: form.title.trim(), priority: form.priority as TaskPriority, deadline: form.deadline }) }
</script>

<template>
  <el-dialog :model-value="visible" :title="dialogTitle" width="440px" :close-on-click-modal="false" @update:model-value="handleVisibleChange">
    <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent="submitForm">
      <el-form-item label="任务标题" prop="title"><el-input v-model="form.title" maxlength="60" show-word-limit placeholder="例如：完成任务列表页面" /></el-form-item>
      <div class="form-grid">
        <el-form-item label="优先级" prop="priority"><el-select v-model="form.priority" class="form-control"><el-option label="高优先级" value="high" /><el-option label="中优先级" value="medium" /><el-option label="低优先级" value="low" /></el-select></el-form-item>
        <el-form-item label="截止日期" prop="deadline"><el-date-picker v-model="form.deadline" type="date" value-format="YYYY-MM-DD" class="form-control" placeholder="选择日期" /></el-form-item>
      </div>
    </el-form>
    <template #footer><el-button @click="close">取消</el-button><el-button type="primary" @click="submitForm">{{ mode === 'create' ? '创建任务' : '保存修改' }}</el-button></template>
  </el-dialog>
</template>

<style scoped>
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }.form-control { width: 100%; }
@media (max-width: 460px) { .form-grid { grid-template-columns: 1fr; gap: 0; } }
</style>
