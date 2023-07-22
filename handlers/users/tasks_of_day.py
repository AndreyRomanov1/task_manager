from datetime import datetime, timedelta

from aiogram import types

from loader import dp
from utils.task_services import create_message_for_tasks_of_day, get_all_tasks_for_period_from_db


async def tasks_of_specified_day_base_handler(message: types.Message, date: datetime):
    tasks = await get_all_tasks_for_period_from_db(
        task_author=message.from_user.id,
        start_date_of_period=date,
        period_length_in_days=1
    )
    if tasks:
        answer_message = await create_message_for_tasks_of_day(tasks_of_days=tasks, date=date)
        await message.answer(answer_message)
    else:
        await message.answer("На указанную дату задач нет")


@dp.message_handler(regexp=r"\d\d.\d\d.\d\d$")  # DD.MM.YY
async def tasks_of_specified_day_0_handler(message: types.Message):
    try:
        day, month, year = map(int, message.text.split("."))
        year += 2000
        await tasks_of_specified_day_base_handler(message, datetime(
            year=year,
            month=month,
            day=day
        ))
    except ValueError:
        await message.answer("Неверный формат даты или времени")


@dp.message_handler(regexp=r"\d\d.\d\d.\d\d\d\d$")  # DD.MM.YYYY
async def tasks_of_specified_day_1_handler(message: types.Message):
    try:
        day, month, year = map(int, message.text.split("."))
        await tasks_of_specified_day_base_handler(message, datetime(
            year=year,
            month=month,
            day=day
        ))
    except ValueError:
        await message.answer("Неверный формат даты или времени")


@dp.message_handler(commands=["today"])
async def tasks_of_today_handler(message: types.Message):
    today = datetime.now()
    await tasks_of_specified_day_base_handler(message, today)


@dp.message_handler(commands=["tomorrow"])
async def tasks_of_tomorrow_handler(message: types.Message):
    tomorrow = datetime.now() + timedelta(days=1)
    await tasks_of_specified_day_base_handler(message, tomorrow)
