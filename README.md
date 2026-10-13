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

## 3. MySQL 与 SQLAlchemy

第三阶段将 FastAPI 后端从 Python 内存列表改造为 MySQL 持久化存储，并使用 SQLAlchemy ORM 完成任务数据的增删改查。任务保存后不会因为 FastAPI 服务重启而丢失。

### 技术与职责

- MySQL：保存任务数据，提供 `task_manager` 数据库和 `tasks` 表。
- SQLAlchemy：负责 Python 对象与 MySQL 表之间的映射，以及查询和事务操作。
- PyMySQL：作为 SQLAlchemy 连接 MySQL 使用的数据库驱动。
- python-dotenv：从 `.env` 读取本地数据库连接地址。
- Pydantic：继续负责请求数据校验和响应数据序列化。

### 后端目录更新

```text
backend/
├─ sql/
│  └─ init_database.sql  # 创建 task_manager 数据库
├─ .env                  # 本地数据库连接信息，不提交到 Git
├─ .env.example          # 数据库连接配置示例
├─ database.py           # Engine、SessionLocal、Base 和 get_db
├─ models.py             # SQLAlchemy Task 数据库模型
├─ schemas.py            # Pydantic 请求与响应模型
├─ seed.py               # 写入本地示例任务
├─ main.py               # FastAPI 应用和数据库 CRUD 接口
├─ test_main.http        # HTTP 接口测试
└─ requirements.txt      # 后端直接依赖
```

### 数据库初始化

`sql/init_database.sql` 负责创建数据库：

```sql
CREATE DATABASE IF NOT EXISTS task_manager
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

`models.py` 中的 `Task` 类负责描述 `tasks` 表。FastAPI 启动时执行：

```python
Base.metadata.create_all(bind=engine)
```

SQLAlchemy 会检查表是否存在，并根据模型创建缺少的表。当前字段包括：

| 字段 | 作用 |
| --- | --- |
| `id` | 自增主键 |
| `title` | 任务标题 |
| `completed` | 是否完成 |
| `priority` | 高、中、低优先级 |
| `deadline` | 截止日期 |
| `created_at` | 创建时间 |

### 数据库连接

`.env.example` 提供连接格式：

```dotenv
DATABASE_URL=mysql+pymysql://username:password@127.0.0.1:3306/task_manager?charset=utf8mb4
```

实际账号和密码只保存在本地 `.env`。`database.py` 读取连接地址并创建：

- `engine`：管理应用与 MySQL 的连接。
- `SessionLocal`：为每次数据库操作创建会话。
- `Base`：所有 SQLAlchemy 模型的基类。
- `get_db()`：向接口提供 Session，并在请求结束后自动关闭。

### 数据库 CRUD

接口通过 `Depends(get_db)` 获取数据库 Session：

| 操作 | SQLAlchemy 处理流程 |
| --- | --- |
| 查询 | `select(Task)` 查询任务并按 ID 排序 |
| 创建 | `db.add()` 添加对象，`db.commit()` 提交，`db.refresh()` 读取生成字段 |
| 更新 | `db.get()` 根据主键查询，`setattr()` 修改实际提交的字段，再提交事务 |
| 删除 | `db.get()` 查询任务，`db.delete()` 标记删除，再提交事务 |

更新接口使用：

```python
task_data.model_dump(exclude_unset=True, exclude_none=True)
```

这样只会更新客户端实际提交且不为 `null` 的字段。更新或删除不存在的任务时返回 `404 Not Found`。

当前数据流为：

```text
HTTP 请求
  → FastAPI 路由
  → Pydantic 数据校验
  → SQLAlchemy Session
  → MySQL tasks 表
  → Pydantic 响应模型
```

### 初始化示例数据

确认已经创建 `task_manager` 数据库后，可以手动执行：

```powershell
cd D:\LTM\backend
.\.venv\Scripts\Activate.ps1
python seed.py
```

`seed.py` 会创建 4 条示例任务；如果数据库已有任务则跳过，避免重复插入。

### 启动与验证

使用明确的模块入口启动当前后端：

```powershell
cd D:\LTM\backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload --port 8000
```

打开 Swagger：`http://127.0.0.1:8000/docs`，依次测试 `GET`、`POST`、`PUT` 和 `DELETE`。重启 FastAPI 后再次查询，如果任务仍然存在，就说明数据已经成功持久化到 MySQL。
