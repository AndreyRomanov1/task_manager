from datetime import datetime, timedelta

from db import db_session
from db.tasks import Tasks


async def get_tasks_of_specified_day(date: datetime, task_author: int) -> list[Tasks]:
    """Получает отсортированный по времени список задач на день date для пользователя task_author"""
    next_date = date + timedelta(days=1)
    active_session = db_session.create_session()
    tasks = active_session.query(Tasks).filter(
        Tasks.task_author == task_author,
        Tasks.task_date >= date,
        Tasks.task_date < next_date
    ).all()
    tasks = sorted(tasks, key=lambda task: task.task_date)
    return tasks


async def add_new_task(task_text: str, task_date: datetime, task_author: int) -> None:
    """Создаёт новую задачу для пользователя с идентификатором task_author в базе данных на дату task_date с
    содержанием task_text """
    task = Tasks(
        task_text=task_text,
        task_date=task_date,
        task_author=task_author
    )
    active_session = db_session.create_session()
    active_session.add(task)
    active_session.commit()
