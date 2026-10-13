from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel,ConfigDict, Field


class TaskPriority(str, Enum):
    """任务优先级，只允许以下三个值。"""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskCreate(BaseModel):
    """创建任务时客户端需要提交的数据。"""

    title: str = Field(min_length=1, max_length=100)
    priority: TaskPriority
    deadline: date


class TaskUpdate(BaseModel):
    """更新任务时允许修改的数据；未提交的字段保持不变。"""

    title: str | None = Field(default=None, min_length=1, max_length=100)
    completed: bool | None = None
    priority: TaskPriority | None = None
    deadline: date | None = None


class TaskResponse(BaseModel):
    """接口返回给客户端的完整任务结构。"""
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    completed: bool
    priority: TaskPriority
    deadline: date
    created_at: datetime
