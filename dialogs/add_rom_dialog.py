from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold, hlink

from db import DataBase
from logger import logger
from keyboards.main_keyboard import get_main_kb
from keyboards.stop_keyboard import get_stop_kb
from check_rom_support import check_rom_support
from functions import get_list_of_firmwares
from messages import MESSAGE


router = Router()
db = DataBase()


class AddRomStep(StatesGroup):
    set_new_rom = State()


@router.callback_query(Text(MESSAGE.KB_MAIN.ADD_ROM[1]))
async def ask_new_rom(callback: CallbackQuery, state: FSMContext):
    logger.info('[HANDLER] ask_new_rom')
    lang = callback.from_user.language_code.upper()
    match lang:
        case 'RU':
            lang = 'RU'
        case _:
            lang = 'EN'

    text = getattr(MESSAGE, f'MESSAGE.{lang}_INPUT_ROM')
    await callback.message.answer(
        text=text,
        reply_markup=get_stop_kb(),
    )
    if callback.message.text:
        await callback.answer()
        await state.set_state(AddRomStep.set_new_rom)


@router.message(AddRomStep.set_new_rom)
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
            reply_markup=get_stop_kb(),
        )
    elif db.check_rom_exist(user_id, rom):
        text = getattr(MESSAGE, f'MESSAGE.{lang}_ALREADY_FOLLOW')
        await message.answer(
            text=text,
            reply_markup=get_stop_kb(),
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
            await state.clear()
