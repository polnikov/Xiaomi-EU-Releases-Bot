from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hlink

from db import DataBase
from logger import logger
from keyboards.main_keyboard import get_main_kb
from check_rom_support import check_rom_support
from functions import get_list_of_firmwares
from messages import MESSAGE


router = Router()
db = DataBase()


class FirstStep(StatesGroup):
    set_rom = State()


@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    logger.info('[HANDLER] start')
    await state.clear()
    user_id = message.from_user.id
    lang = message.from_user.language_code.upper()
    match lang:
        case 'RU':
            lang = 'RU'
        case _:
            lang = 'EN'

    if message.from_user.is_bot:
        logger.error(f'User [{message.from_user.username}] is BOT')
        return

    if not db.check_user(user_id):
        link = 'https://xiaomi.eu/community/threads/miui-14-stable-release.67685/'
        supported_list = f"{hlink('List', link)} of supported devices."
        input_text = hbold("Please input your phone\'s model ROM")
        await message.answer(
            parse_mode='HTML',
            text=f'Hi! I can help you keep track of new Xiaomi.EU MiUIv14 Stable firmware for your phone.\n{supported_list}\n{input_text}'
        )
        await state.set_state(FirstStep.set_rom)
    else:
        text = getattr(MESSAGE, f'MESSAGE.{lang}_WELCOME')
        await message.answer(
            text=text,
            reply_markup=get_main_kb(lang)
        )
        await state.clear()


@router.message(FirstStep.set_rom)
async def set_rom(message: Message, state: FSMContext):
    logger.info('[HANDLER] set_rom')
    user_id = message.from_user.id
    chat_id = message.chat.id
    lang = message.from_user.language_code.upper()
    match lang:
        case 'RU':
            lang = 'RU'
        case _:
            lang = 'EN'
    rom = message.text.strip().lower()

    if not check_rom_support(rom):
        text = getattr(MESSAGE, f'MESSAGE.{lang}_SORRY')
        await message.answer(
            text=text,
        )
    else:
        last_versions = get_list_of_firmwares()
        last_version_data = list(filter(lambda x: rom == x.get('rom'), last_versions))[0]

        version = last_version_data['data'][0] if last_version_data['data'][0] else 'Not exist❗'
        version_link = last_version_data['data'][1] if last_version_data['data'][1] else ''
        version = '.'.join(list(map(str, version)))
        add_to_db = db.add_rom(user_id, chat_id, rom, version, version_link)

        if add_to_db:
            await message.answer(
                parse_mode='HTML',
                text=f'ROM {hbold(rom)} was successfully added.\nLast version ➙ {hlink(version, version_link)}🔗',
                reply_markup=get_main_kb(lang),
            )
            await state.clear()
        else:
            text = getattr(MESSAGE, f'MESSAGE.{lang}_WRONG')
            await message.answer(
                text=text,
            )
            logger.error('[HANDLER] set_rom')
            await state.clear()
