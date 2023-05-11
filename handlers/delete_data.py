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
    user_data = db.get_user_data(user_id)
    is_user_data_delete = db.delete_user_data(user_id)

    if not user_data:
        await callback.message.answer(
            text=MESSAGE.DIALOGS.NO_ROMS,
            reply_markup=get_main_kb(),
        )
        await callback.answer()
    elif is_user_data_delete:
        await callback.message.answer(
            text=MESSAGE.DIALOGS.ALL_REMOVED,
            reply_markup=get_main_kb(),
        )
        await callback.answer()
        await state.clear()
    else:
        await callback.message.answer(
            text=MESSAGE.DIALOGS.WRONG
        )
