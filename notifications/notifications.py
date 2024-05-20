import datetime
import asyncio
from aiogram.enums.parse_mode import ParseMode
from aiogram import Bot

import config
import logic.utils as utils
import logic.tasks as tsk
import logic.schedule as schdl
from db.data import weekly_schedule, tasks

time_event_notify = 15
time_task_notify = 30


async def send_notify(user_id, text):
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    await bot.send_message(user_id, text)
    await bot.session.close()

async def notify_upcoming_events():
    while True:
        current_time = datetime.datetime.now()
        day_of_week = schdl.days[current_time.weekday()]
        for user_id, user_weekly_schedule in weekly_schedule.items():
            day_schedule = user_weekly_schedule.days[day_of_week]
            for event in day_schedule.events:
                event_time = datetime.datetime.strptime(event.time, "%H:%M")
                event_datetime = datetime.datetime.combine(current_time.date(), event_time.time())
                if time_event_notify - 1 <= (event_datetime - current_time).total_seconds() / 60 <= time_event_notify:
                    await send_notify(user_id, f"{event.time} {event.title}")
                    
        await asyncio.sleep(60)

async def start_notify_events():
    asyncio.create_task(notify_upcoming_events())

async def notify_upcoming_tasks():
    while True:
        current_time = datetime.datetime.now()
        for user_id, user_tasks in tasks.items():
            for task in user_tasks.tasks:
                task_datetime = datetime.datetime.strptime(task.time, '%d.%m.%y %H:%M')
                if time_task_notify - 1 <= (task_datetime - current_time).total_seconds() / 60 <= time_task_notify:
                    await send_notify(user_id, f"{task.time} {task.description}")
                    
        await asyncio.sleep(60)

async def start_notify_tasks():
    asyncio.create_task(notify_upcoming_tasks())

