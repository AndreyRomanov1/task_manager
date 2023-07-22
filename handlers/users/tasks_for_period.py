from datetime import datetime, timedelta

from aiogram import types

from loader import dp
from utils.task_services import create_message_for_tasks_for_period, get_all_tasks_for_period_from_db, \
    distribution_of_all_tasks_by_day


async def tasks_for_period_base_handler(message: types.Message, start_date_of_period: datetime, period_length_in_days):
    tasks_for_this_week_by_day = await distribution_of_all_tasks_by_day(
        all_tasks=await get_all_tasks_for_period_from_db(
            task_author=message.from_user.id,
            start_date_of_period=start_date_of_period,
            period_length_in_days=period_length_in_days),
        start_date_of_period=start_date_of_period,
        period_length_in_days=period_length_in_days
    )
    answer_message = await create_message_for_tasks_for_period(tasks_for_period=tasks_for_this_week_by_day,
                                                               start_date_of_period=start_date_of_period)
    await message.answer(answer_message)


@dp.message_handler(commands=["week"])
async def tasks_for_this_week_handler(message: types.Message):
    today = datetime.today()
    start_date_of_week = today - timedelta(days=today.weekday())
    await tasks_for_period_base_handler(
        message=message,
        start_date_of_period=start_date_of_week,
        period_length_in_days=7
    )


@dp.message_handler(commands=["nweek"])
async def tasks_for_next_week_handler(message: types.Message):
    today = datetime.today()
    start_date_of_next_week = today - timedelta(days=today.weekday()) + timedelta(days=7)
    await tasks_for_period_base_handler(
        message=message,
        start_date_of_period=start_date_of_next_week,
        period_length_in_days=7
    )
