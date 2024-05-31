import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config
from notifications.notifications import NotificationChecker
from db.saver import Saver
from handlers import schedule, tasks



async def main():
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(schedule.router, tasks.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await Saver().start_scheduled_save()
    await NotificationChecker().start_notify_events()
    await NotificationChecker().start_notify_tasks()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())