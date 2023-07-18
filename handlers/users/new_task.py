from datetime import datetime

from aiogram import types

from db.tasks import Tasks
from loader import dp
from db import db_session


async def new_task(message: types.Message, task_text: str, task_date: datetime, task_author: int):
    try:
        task = Tasks(
            task_text=task_text,
            task_date=task_date,
            task_author=task_author
        )
        active_session = db_session.create_session()
        active_session.add(task)
        active_session.commit()
        await message.answer(f"Задача на {task_date.strftime('%d.%m.%Y %H:%M')} сохранена:\n{task_text}")
    except Exception as er:
        print(er)
        await message.answer(f"Что-то не так:\n{er}")


@dp.message_handler(regexp=r"\d\d.\d\d.\d\d\s\d\d.\d\d\s[\S\s]*")  # DD.MM.YY HH.MM task
async def new_task_1(message: types.Message):
    day, month, year = map(int, message.text.split()[0].split("."))
    year += 2000
    hour, minute = map(int, message.text.split()[1].split("."))
    await new_task(
        message=message,
        task_text=message.text[15:].strip(),
        task_author=message.from_user.id,
        task_date=datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute
        )
    )


@dp.message_handler(regexp=r"\d\d.\d\d.\d\d\s[\S\s]*")  # DD.MM.YY task
async def new_task_2(message: types.Message):
    day, month, year = map(int, message.text.split()[0].split("."))
    year += 2000
    hour, minute = 18, 0
    await new_task(
        message=message,
        task_text=message.text[9:].strip(),
        task_author=message.from_user.id,
        task_date=datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute
        )
    )


@dp.message_handler(regexp=r"\d\d.\d\d\s[\S\s]*")  # HH.MM task
async def new_task_3(message: types.Message):
    today = datetime.now()
    year, month, day = today.year, today.month, today.day
    hour, minute = map(int, message.text.split()[0].split("."))
    await new_task(
        message=message,
        task_text=message.text[6:].strip(),
        task_author=message.from_user.id,
        task_date=datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute
        )
    )


@dp.message_handler()  # task
async def new_task_4(message: types.Message):
    today = datetime.now()
    year, month, day = today.year, today.month, today.day
    hour, minute = 18, 0
    await new_task(
        message=message,
        task_text=message.text.strip(),
        task_author=message.from_user.id,
        task_date=datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute
        )
    )

# @dp.message_handler()
# async def new_task0(message: types.Message):
#     templ_1 = r'\d\d.\d\d.\d\d\s\d\d.\d\d\s[\S\s]*'  # DD.MM.YY HH.MM task
#     templ_2 = r"\d\d.\d\d.\d\d\s[\S\s]*"  # DD.MM.YY task
#     templ_3 = r"\d\d.\d\d\s[\S\s]*"  # HH.MM task
#     today = datetime.now()
#     year, month, day, hour, minute = today.year, today.month, today.day, 18, 0
#     if fullmatch(templ_1, message.text):
#         day, month, year = map(int, message.text.split()[0].split("."))
#         year += 2000
#         hour, minute = map(int, message.text.split()[1].split("."))
#         task_text = message.text
#     elif fullmatch(templ_2, message.text):
#         day, month, year = map(int, message.text.split()[0].split("."))
#         year += 2000
#         task_text = message.text
#     elif fullmatch(templ_2, message.text):
#         hour, minute = map(int, message.text.split()[1].split("."))
#         task_text = message.text
#     else:
#         task_text = message.text
#     task = Tasks(
#         task_text=task_text,
#         task_date=datetime(year=year, month=month, day=day, hour=hour, minute=minute),
#         task_author=message.from_user.id
#     )
#     active_session = db_session.create_session()
#     active_session.add(task)
#     active_session.commit()
#
#     await message.answer(f"Задача сохранена:\n{task_text}")
