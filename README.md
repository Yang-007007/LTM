# 任务管理应用

## 1.前端内容部分

本阶段完成一个使用 Vue 3、TypeScript、Vite 和 Element Plus 实现的任务管理前端页面。当前使用本地假数据练习 Vue 的基础能力，暂未连接 FastAPI 和 MySQL。

### 技术栈

- Vue 3：使用 Composition API 和 `<script setup lang="ts">` 编写组件。
- TypeScript：在 `src/types/task.ts` 中定义 `Task`、`TaskPriority`、`TaskFilter` 等数据类型。
- Vite：提供本地开发服务和生产构建能力。
- Element Plus：提供表格、标签、表单、弹窗、按钮、加载骨架屏、空状态和消息提示等组件。

### 已完成的功能

- 展示包含标题、完成状态、优先级、截止日期、创建时间的任务列表。
- 使用 `ref<Task[]>` 保存本地任务数据。
- 使用 `computed` 计算任务总数、已完成数、未完成数，以及筛选后的任务列表。
- 按“全部、未完成、已完成”状态筛选任务。
- 切换任务完成/未完成状态。
- 使用弹窗表单新增和编辑任务。
- 删除任务前使用二次确认弹窗。
- 展示 loading、空数据状态，并预留请求失败提示。
- 适配桌面表格和移动端任务卡片两种展示方式。

### 组件与数据流

`TaskPage.vue` 是当前页面的核心组件，负责持有任务数据并处理新增、编辑、删除、筛选等业务逻辑。`TaskToolbar.vue`、`TaskList.vue`、`TaskItem.vue` 和 `TaskForm.vue` 负责展示界面或接收用户输入。

项目通过父子组件通信保持清晰的数据流：父组件使用 `props` 向子组件传递任务数据；子组件使用 `emits` 向父组件通知筛选、切换状态、新增、编辑或删除等用户操作。任务数据最终统一由 `TaskPage.vue` 修改。

```text
TaskPage.vue（持有并修改任务数据）
  ├─ TaskToolbar.vue（筛选、新增）
  ├─ TaskList.vue（任务表格）
  │    └─ TaskItem.vue（移动端单条任务）
  └─ TaskForm.vue（新增、编辑表单）
```

### 当前目录说明

```text
src/
├─ components/task/  # 任务相关的可复用组件
├─ mock/             # 本地假数据
├─ types/            # TypeScript 类型定义
├─ views/            # 页面级组件和业务逻辑
├─ App.vue           # 根组件
├─ main.ts           # Vue 和 Element Plus 的应用入口
└─ style.css         # 全局样式
```

### 启动项目

```bash
npm install
npm run dev
```

生产构建：

```bash
npm run build
```
