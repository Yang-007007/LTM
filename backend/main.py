from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Response, status

from schemas import TaskCreate, TaskResponse, TaskUpdate

# 这一行就是创建 FastAPI 实例
app = FastAPI(
    title="任务管理 API",
    description="使用内存列表练习任务 CRUD",
    version="1.0.0",
)

# 暂时使用 Python 列表模拟数据库。服务重启后，数据会被清空。
tasks: list[TaskResponse] = []
next_id = 1

def find_task_index(task_id: int) -> int:
    """根据任务 ID 查找列表下标，不存在时返回 404。"""
    for index, task in enumerate(tasks):
        if task.id == task_id:
            return index
    raise HTTPException(status_code=404, detail="任务不存在")


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks():
    """获取全部任务。"""
    return tasks


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate):
    """创建一条新任务。"""
    global next_id

    new_task = TaskResponse(
        id=next_id,
        title=task_data.title,
        completed=False,
        priority=task_data.priority,
        deadline=task_data.deadline,
        created_at=datetime.now(timezone.utc),
    )
    tasks.append(new_task)
    next_id += 1
    return new_task


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate):
    """根据 ID 更新任务中实际传入的字段。"""
    task_index = find_task_index(task_id)
    current_task = tasks[task_index]
    update_data = task_data.model_dump(exclude_unset=True)
    updated_task = current_task.model_copy(update=update_data)
    tasks[task_index] = updated_task
    return updated_task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    """根据 ID 删除任务。"""
    task_index = find_task_index(task_id)
    tasks.pop(task_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
