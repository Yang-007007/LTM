from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    completed: Mapped[bool] = mapped_column(default=False)
    priority: Mapped[str] = mapped_column(String(10))
    deadline: Mapped[date]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())