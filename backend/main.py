from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Task
from schemas import TaskCreate, TaskResponse, TaskUpdate

Base.metadata.create_all(bind=engine)

# 这一行就是创建 FastAPI 实例
app = FastAPI(
    title="任务管理 API",
    description="使用 FastAPI、SQLAlchemy 和 MySQL 实现任务 CRUD",
    version="1.0.0",
)


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    """获取全部任务。"""
    return db.scalars(select(Task).order_by(Task.id)).all()


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    """创建一条新任务。"""
    new_task = Task(
        title=task_data.title,
        completed=False,
        priority=task_data.priority.value,
        deadline=task_data.deadline,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
):
    """根据 ID 更新任务中实际传入的字段。"""
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="任务不存在")

    update_data = task_data.model_dump(exclude_unset=True, exclude_none=True)
    if "priority" in update_data:
        update_data["priority"] = update_data["priority"].value

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """根据 ID 删除任务。"""
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="任务不存在")

    db.delete(task)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
