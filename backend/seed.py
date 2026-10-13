from datetime import date

from sqlalchemy import select

from database import Base, SessionLocal, engine
from models import Task


def seed_tasks() -> None:
    """为本地开发数据库添加一组初始任务。"""
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        # 数据库已有任务时跳过，避免重复运行后反复插入相同数据。
        existing_task_id = db.scalar(select(Task.id).limit(1))
        if existing_task_id is not None:
            print("数据库中已经存在任务，跳过初始化")
            return

        tasks = [
            Task(
                title="学习 SQLAlchemy 基础",
                completed=False,
                priority="high",
                deadline=date(2026, 10, 15),
            ),
            Task(
                title="改造任务查询接口",
                completed=False,
                priority="high",
                deadline=date(2026, 10, 16),
            ),
            Task(
                title="完成任务新增接口",
                completed=False,
                priority="medium",
                deadline=date(2026, 10, 17),
            ),
            Task(
                title="复习 Vue 父子通信",
                completed=True,
                priority="low",
                deadline=date(2026, 10, 12),
            ),
        ]

        db.add_all(tasks)
        db.commit()

        print(f"初始化完成，共添加 {len(tasks)} 条任务")


if __name__ == "__main__":
    seed_tasks()
