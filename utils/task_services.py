from datetime import datetime, timedelta

from db import db_session
from db.tasks import Tasks


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


async def get_all_tasks_for_period_from_db(task_author: int, start_date_of_period: datetime,
                                           period_length_in_days: int) -> list[Tasks]:
    """Возвращает все задачи пользователя task_author с start_date_of_period по
    end_date_of_period отсортированные по времени"""
    start_date_of_period = start_date_of_period.replace(minute=0, hour=0, second=0, microsecond=0)
    end_date_of_period = start_date_of_period + timedelta(days=period_length_in_days)
    active_session = db_session.create_session()
    all_tasks = active_session.query(Tasks).filter(
        Tasks.task_author == task_author,
        Tasks.task_date >= start_date_of_period,
        Tasks.task_date < end_date_of_period
    ).all()
    all_tasks = sorted(all_tasks, key=lambda task: task.task_date)
    return all_tasks


async def distribution_of_all_tasks_by_day(all_tasks: list[Tasks], start_date_of_period: datetime,
                                           period_length_in_days: int) -> list[list[Tasks]]:
    start_date_of_period = start_date_of_period.replace(minute=0, hour=0, second=0, microsecond=0)
    """Распределяет список задач на список списков задач по дням"""
    tasks_for_period = [[] for _ in range(period_length_in_days)]
    days_from_start_period, i = 0, 0
    while i < len(all_tasks):
        if all_tasks[i].task_date.replace(minute=0, hour=0, second=0, microsecond=0) == start_date_of_period + \
                timedelta(days=days_from_start_period):
            tasks_for_period[days_from_start_period].append(all_tasks[i])
            i += 1
        else:
            days_from_start_period += 1
    return tasks_for_period


async def create_message_for_tasks_of_day(tasks_of_days: list[Tasks], date: datetime) -> str:
    """Формирует сообщение для пользователя с выводом задач tasks_of_days на указанный день"""
    str_tasks = "\n".join(list(map(str, tasks_of_days)))
    message_for_tasks_of_day = f"Задачи на {date.strftime('%d.%m.%Y')}:\n{str_tasks}"
    return message_for_tasks_of_day


async def create_message_for_tasks_for_period(tasks_for_period: list[list[Tasks]],
                                              start_date_of_period: datetime) -> str:
    """Формирует сообщение для пользователя с выводом задач tasks_for_period на указанный период
    начиная с start_date_of_period"""
    message_for_tasks_for_period = ""
    for days_from_start_period, tasks_of_day in enumerate(tasks_for_period):
        date = start_date_of_period + timedelta(days=days_from_start_period)
        message_for_tasks_for_period += await create_message_for_tasks_of_day(tasks_of_days=tasks_of_day,
                                                                              date=date) + "\n"
    return message_for_tasks_for_period
