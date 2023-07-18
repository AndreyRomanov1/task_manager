from datetime import datetime, timedelta

from aiogram import types

from db import db_session
from db.tasks import Tasks
from loader import dp


async def tasks_of_specified_day(message: types.Message, date: datetime):
    next_date = date + timedelta(days=1)
    active_session = db_session.create_session()
    tasks: list[Tasks] = active_session.query(Tasks).filter(
        Tasks.task_author == message.from_user.id,
        Tasks.task_date >= date,
        Tasks.task_date < next_date
    ).all()
    if tasks:
        tasks = sorted(tasks, key=lambda task: task.task_date)
        str_tasks = "\n".join(list(map(str, tasks)))
        await message.answer(f"Задачи на {date.strftime('%d.%m.%Y')}:\n{str_tasks}")
    else:
        await message.answer("На указанную дату задач нет")


@dp.message_handler(regexp=r"\d\d.\d\d.\d\d$")  # DD.MM.YY
async def tasks_of_specified_day_handler_0(message: types.Message):
    try:
        day, month, year = map(int, message.text.split("."))
        year += 2000
        await tasks_of_specified_day(message, datetime(
            year=year,
            month=month,
            day=day
        ))
    except ValueError:
        await message.answer("Неверный формат даты или времени")


@dp.message_handler(regexp=r"\d\d.\d\d.\d\d\d\d$")  # DD.MM.YYYY
async def tasks_of_specified_day_handler_0(message: types.Message):
    try:
        day, month, year = map(int, message.text.split("."))
        await tasks_of_specified_day(message, datetime(
            year=year,
            month=month,
            day=day
        ))
    except ValueError:
        await message.answer("Неверный формат даты или времени")


@dp.message_handler(commands=["today"])
async def tasks_of_today_handler(message: types.Message):
    today = datetime.now().replace(minute=0, hour=0, second=0, microsecond=0)
    await tasks_of_specified_day(message, today)


@dp.message_handler(commands=["tomorrow"])
async def tasks_of_tomorrow_handler(message: types.Message):
    tomorrow = datetime.now().replace(minute=0, hour=0, second=0, microsecond=0) + timedelta(days=1)
    await tasks_of_specified_day(message, tomorrow)
