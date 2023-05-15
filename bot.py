import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

from dotenv import load_dotenv
from logger import logger
from db import DataBase

from dialogs import first_dialog, add_rom_dialog, delete_rom_dialog
from handlers import common, get_data, delete_data
from tasks import send_notifications

load_dotenv()

TOKEN = os.getenv('TOKEN')

db = DataBase()


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(
        common.router,
        get_data.router,
        delete_data.router,
        first_dialog.router,
        add_rom_dialog.router,
        delete_rom_dialog.router,
    )
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_notifications,
        trigger='cron',
        day_of_week='mon-sun',
        hour=6,
        timezone=timezone('Europe/Moscow'),
        kwargs={'bot': bot}
    )
    scheduler.start()

    logger.info('Bot is running')
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    asyncio.run(main())
