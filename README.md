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

## 2.FastAPI初步

第二天完成任务管理应用的 FastAPI 内存版后端。当前前后端保持独立，后端暂不连接 Vue 和 MySQL，主要用于理解 FastAPI 请求流程、Pydantic 数据校验和 CRUD 操作。

### 开发环境

- 使用 `.venv` 为后端创建独立的 Python 虚拟环境，避免项目之间发生依赖冲突。
- 使用 `requirements.txt` 记录后端依赖，目前主要依赖 `fastapi[standard]`。
- `.venv`、`__pycache__`、IDE 配置和环境变量文件通过 `.gitignore` 排除，不提交到 Git。

### 后端目录

```text
backend/
├─ .venv/              # Python 虚拟环境，不提交到 Git
├─ main.py             # FastAPI 实例、内存数据和 CRUD 接口
├─ schemas.py          # Pydantic 请求与响应模型
├─ test_main.http      # PyCharm HTTP 接口测试文件
├─ requirements.txt    # Python 依赖
└─ .gitignore          # Git 忽略规则
```

### Pydantic 数据模型

`schemas.py` 用于规定接口接收和返回的数据格式，并在运行时自动校验客户端提交的数据。

- `TaskPriority`：将优先级限制为 `high`、`medium`、`low`。
- `TaskCreate`：规定创建任务时需要提交的标题、优先级和截止日期。
- `TaskUpdate`：规定更新任务时允许修改的字段，字段均为可选。
- `TaskResponse`：规定接口返回的完整任务结构，包括 `id`、完成状态和创建时间。

### 内存数据

当前使用 Python 列表临时代替数据库：

```python
tasks: list[TaskResponse] = []
next_id = 1
```

`tasks` 保存任务，`next_id` 模拟数据库的自增主键。服务重启后列表会重新变为空，这是内存版后端的正常行为。

辅助函数 `find_task_index(task_id)` 根据任务 ID 查找其在列表中的下标；找不到时抛出 `404`，供更新和删除接口共同使用。

### CRUD 接口

| 操作 | 请求方法和路径 | 作用 |
| --- | --- | --- |
| 查询 | `GET /tasks` | 返回全部任务 |
| 创建 | `POST /tasks` | 生成 ID 和创建时间，并将新任务加入列表 |
| 更新 | `PUT /tasks/{task_id}` | 根据 ID 找到任务，只更新客户端实际提交的字段 |
| 删除 | `DELETE /tasks/{task_id}` | 根据 ID 从列表中删除任务 |

更新任务时使用：

```python
task_data.model_dump(exclude_unset=True)
```

它只提取客户端实际提交的字段。随后使用 `model_copy(update=update_data)` 在原任务基础上生成更新后的任务，并替换列表中的旧任务。

删除任务时先通过 ID 找到列表下标，再使用 `tasks.pop(task_index)` 删除对应任务。删除成功返回 `204 No Content`。

### 状态码和校验

- `200 OK`：查询或更新成功。
- `201 Created`：任务创建成功。
- `204 No Content`：任务删除成功，不返回响应体。
- `404 Not Found`：任务 ID 不存在。
- `422 Unprocessable Entity`：请求数据不符合 Pydantic 模型，例如优先级或日期格式错误。

### 启动和测试

进入后端目录并激活虚拟环境：

```powershell
cd D:\LTM\backend
.\.venv\Scripts\Activate.ps1
fastapi dev main.py
```

启动后可以使用以下方式测试：

- Swagger 文档：`http://127.0.0.1:8000/docs`
- PyCharm：打开 `test_main.http`，依次执行新增、查询、更新和删除请求。

建议的 CRUD 测试顺序：

```text
POST 新增任务
  ↓
GET 查看任务
  ↓
PUT 修改任务
  ↓
GET 检查修改结果
  ↓
DELETE 删除任务
  ↓
GET 确认任务已经删除
```
