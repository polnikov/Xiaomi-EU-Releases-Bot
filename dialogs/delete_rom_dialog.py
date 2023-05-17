from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from db import DataBase
from logger import logger

from keyboards.list_keyboard import get_list_kb
from keyboards.main_keyboard import get_main_kb
from messages import MESSAGE


router = Router()
db = DataBase()


class DeleteRomStep(StatesGroup):
    delete_rom = State()


@router.callback_query(Text('delete-rom'))
async def show_roms(callback: CallbackQuery, state: FSMContext):
    logger.info('[HANDLER] show_roms')

    user_id = callback.from_user.id
    lang = callback.from_user.language_code.upper()
    match lang:
        case 'RU':
            lang = 'RU'
        case _:
            lang = 'EN'

    roms = db.get_my_roms(user_id)
    if not roms:
        text = getattr(MESSAGE, f'{lang}_NO_ROMS')
        await callback.message.answer(
            text=text,
            reply_markup=get_main_kb(lang),
        )
        await state.clear()
    else:
        roms = [rom[0] for rom in roms]
        text = getattr(MESSAGE, f'{lang}_CHOOSE')
        await callback.message.answer(
            text=text,
            reply_markup=get_list_kb(roms, 'delete'),
        )
        await callback.answer()
        await state.set_state(DeleteRomStep.delete_rom)


@router.callback_query(DeleteRomStep.delete_rom)
async def delete_rom(callback: CallbackQuery, state: FSMContext):
    logger.info('[HANDLER] delete_rom')

    user_id = callback.from_user.id
    rom_to_delete = callback.data.split()[1]
    lang = callback.from_user.language_code.upper()
    match lang:
        case 'RU':
            lang = 'RU'
        case _:
            lang = 'EN'

    if db.delete_rom(user_id, rom_to_delete):
        await callback.answer()
        await show_roms(callback, state)
    else:
        text = getattr(MESSAGE, f'{lang}_WRONG')
        await callback.message.answer(
            text=text,
        )
        logger.error('[HANDLER] delete_rom')
        await state.clear()
