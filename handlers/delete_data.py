import re

from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from db import DataBase
from logger import logger
from keyboards.main_keyboard import get_main_kb
from messages import MESSAGE


router = Router()
db = DataBase()


@router.callback_query(Text('delete-user-data'))
async def delete_user_data(callback: CallbackQuery, state: FSMContext):
    logger.info('[HANDLER] delete_user_data')

    user_id = callback.from_user.id
    lang = callback.from_user.language_code.upper()
    match lang:
        case 'RU':
            lang = 'RU'
        case _:
            lang = 'EN'

    user_data = db.get_user_data(user_id)
    is_user_data_delete = db.delete_user_data(user_id)

    if not user_data:
        text = getattr(MESSAGE, f'{lang}_NO_ROMS')
        await callback.message.answer(
            text=text,
            reply_markup=get_main_kb(lang),
        )
        await callback.answer()
    elif is_user_data_delete:
        text = getattr(MESSAGE, f'{lang}_ALL_REMOVED')
        await callback.message.answer(
            text=text,
            reply_markup=get_main_kb(lang),
        )
        await callback.answer()
        await state.clear()
    else:
        text = getattr(MESSAGE, f'{lang}_WRONG')
        await callback.message.answer(
            text=text,
        )
