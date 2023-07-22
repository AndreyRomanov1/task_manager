from datetime import datetime

from aiogram import types


from loader import dp
from utils.task_services import add_new_task


async def new_task_base_handler(message: types.Message, task_text: str, task_date: datetime, task_author: int):
    try:
        await add_new_task(task_text, task_date, task_author)
        await message.answer(f"Задача на {task_date.strftime('%d.%m.%Y %H:%M')} сохранена:\n{task_text}")
    except Exception as er:
        print(er)
        await message.answer(f"Не получилось сохранить запись")


@dp.message_handler(regexp=r"\d\d.\d\d.\d\d\s\d\d.\d\d\s[\S\s]*")  # DD.MM.YY HH.MM task
async def new_task_0_handler(message: types.Message):
    try:
        day, month, year = map(int, message.text.split()[0].split("."))
        year += 2000
        hour, minute = map(int, message.text.split()[1].split("."))
        await new_task_base_handler(
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
    except ValueError:
        await message.answer("Неверный формат даты или времени")


@dp.message_handler(regexp=r"\d\d.\d\d.\d\d\d\d\s\d\d.\d\d\s[\S\s]*")  # DD.MM.YYYY HH.MM task
async def new_task_1_handler(message: types.Message):
    try:
        day, month, year = map(int, message.text.split()[0].split("."))
        hour, minute = map(int, message.text.split()[1].split("."))
        await new_task_base_handler(
            message=message,
            task_text=message.text[17:].strip(),
            task_author=message.from_user.id,
            task_date=datetime(
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute
            )
        )
    except ValueError:
        await message.answer("Неверный формат даты или времени")


@dp.message_handler(regexp=r"\d\d.\d\d.\d\d\s[\S\s]*")  # DD.MM.YY task
async def new_task_2_handler(message: types.Message):
    try:
        day, month, year = map(int, message.text.split()[0].split("."))
        year += 2000
        hour, minute = 18, 0
        await new_task_base_handler(
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
    except ValueError:
        await message.answer("Неверный формат даты или времени")


@dp.message_handler(regexp=r"\d\d.\d\d.\d\d\d\d\s[\S\s]*")  # DD.MM.YYYY task
async def new_task_3_handler(message: types.Message):
    try:
        day, month, year = map(int, message.text.split()[0].split("."))
        hour, minute = 18, 0
        await new_task_base_handler(
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
    except ValueError:
        await message.answer("Неверный формат даты или времени")


@dp.message_handler(regexp=r"\d\d.\d\d\s[\S\s]*")  # HH.MM task
async def new_task_4_handler(message: types.Message):
    try:
        today = datetime.now()
        year, month, day = today.year, today.month, today.day
        hour, minute = map(int, message.text.split()[0].split("."))
        await new_task_base_handler(
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
    except ValueError:
        await message.answer("Неверный формат даты или времени")


@dp.message_handler()  # task
async def new_task_5_handler(message: types.Message):
    today = datetime.now()
    year, month, day = today.year, today.month, today.day
    hour, minute = 18, 0
    await new_task_base_handler(
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
