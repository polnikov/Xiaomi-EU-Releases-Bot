import os
import asyncio
import traceback

from aiogram import Bot, Dispatcher
from aiogram import exceptions
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.methods.send_message import SendMessage
from aiogram.utils.markdown import hbold, hlink
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from dotenv import load_dotenv
from logger import logger
from db import DataBase

from dialogs import first_dialog, add_rom_dialog, delete_rom_dialog
from handlers import common, get_data, delete_data
from functions import get_list_of_firmwares


load_dotenv()

TOKEN = os.getenv('TOKEN')

db = DataBase()


async def main():
    scheduler = AsyncIOScheduler()
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


    async def check_updates_and_notify():
        logger.info('[CHECKING UPDATE]')
        try:
            last_versions = get_list_of_firmwares()
            users = db.get_users()
            if users:
                users = list(map(lambda x: x[0], users))

                for user in users:
                    update_data = []
                    user_roms = db.get_my_roms(user)
                    if user_roms:
                        user_roms = list(map(lambda x: x[0], user_roms))
                        for rom in user_roms:
                            rom_data = list(filter(lambda x: rom in x.get('rom'), last_versions))[0]
                            new_version = rom_data['data'][0]
                            new_link = rom_data['data'][1]

                            current_version = db.get_user_rom_version(user, rom)[0].split('.')
                            current_version = list(map(int, current_version))

                            if new_version > current_version:
                                version = '.'.join(list(map(str, new_version)))
                                db.update_version(user, rom, version, new_link)
                                update_data.append([rom, version, new_link])

                    chat_id = db.get_user_chat_id(user)[0]
                    for upd in update_data:
                        version = upd[1]
                        link = upd[2]
                        rom = upd[0]
                        try:
                            await bot(SendMessage(
                                parse_mode='HTML',
                                chat_id=chat_id,
                                text=f'📮 New release {hlink(version, link)} for {hbold(rom)}'
                            ))
                        except exceptions.BotBlocked:
                            logger.error(f'User {user}]: blocked by user')
                        except exceptions.ChatNotFound:
                            logger.error(f'invalid user ID {user}')
                        except exceptions.RetryAfter as e:
                            logger.error(f'Flood limit is exceeded. Sleep {e.timeout} seconds.')
                            await asyncio.sleep(e.timeout)
                            return await bot(SendMessage(
                                parse_mode='HTML',
                                chat_id=chat_id,
                                text=f'📮 New release {hlink(version, link)} for {hbold(rom)}'
                            ))
                        except exceptions.UserDeactivated:
                            logger.error(f'User {user} is deactivated')
                        except exceptions.TelegramAPIError:
                            logger.exception(f'User {user} failed')
                        else:
                            logger.info(f'Send to user {user} success')
        except Exception as e:
            logger.error(f"Can'\t check update: {e}")
    
    scheduler.add_job(check_updates_and_notify, 'interval', days=1)
    scheduler.start()

    DELAY = 30
    while True:
        try:
            logger.info('Bot is running')
            await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
        except exceptions.NetworkError as e:
            logger.error(f"Network error occurred: {e}")
            asyncio.sleep(DELAY)
        except exceptions.TerminatedByOtherGetUpdates:
            logger.error('Bot terminated by other getUpdates request')
            break
        except Exception as e:
            logger.error(f"Exception occurred: {e}")
            logger.error(traceback.format_exc())
            asyncio.sleep(DELAY)

if __name__ == '__main__':
    asyncio.run(main())
