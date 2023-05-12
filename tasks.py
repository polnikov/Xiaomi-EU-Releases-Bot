import asyncio

from aiogram import Bot
from aiogram.utils.markdown import hbold, hlink
from aiogram import exceptions

from functions import get_list_of_firmwares
from logger import logger
from db import DataBase


db = DataBase()


async def send_notifications(bot: Bot):
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
                        await bot.send_message(
                            chat_id=chat_id,
                            text=f'📮 New release {hlink(version, link)} for {hbold(rom)}',
                            parse_mode='HTML',
                        )
                    except exceptions.BotBlocked:
                        logger.error(f'User {user}]: blocked by user')
                    except exceptions.ChatNotFound:
                        logger.error(f'invalid user ID {user}')
                    except exceptions.RetryAfter as e:
                        logger.error(f'Flood limit is exceeded. Sleep {e.timeout} seconds.')
                        await asyncio.sleep(e.timeout)
                        return await bot.send_message(
                            chat_id=chat_id,
                            text=f'📮 New release {hlink(version, link)} for {hbold(rom)}',
                            parse_mode='HTML',
                        )
                    except exceptions.UserDeactivated:
                        logger.error(f'User {user} is deactivated')
                    except exceptions.TelegramAPIError:
                        logger.exception(f'User {user} failed')
                    else:
                        logger.info(f'Send to user {user} success')
    except Exception as e:
        logger.error(f"Can'\t check update: {e}")
