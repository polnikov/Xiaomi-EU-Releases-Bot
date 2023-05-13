from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold, hlink

from db import DataBase
from logger import logger
from keyboards.main_keyboard import get_main_kb
from messages import MESSAGE


router = Router()
db = DataBase()


@router.callback_query(Text('get-user-data'))
async def get_user_info(callback: CallbackQuery, state: FSMContext):
    logger.info('[HANDLER] get_user_info')

    user_id = callback.from_user.id

    user_data = db.get_user_data(user_id)
    user_data = [f'{hbold(rom[0])} ➙ {hlink(rom[1], rom[2])}' for rom in user_data]
    user_data = '\n'.join(user_data)
    if user_data:
        await callback.message.answer(
            parse_mode='HTML',
            disable_web_page_preview=True,
            text=user_data,
            reply_markup=get_main_kb(),
        )
        await callback.answer()
    else:
        await callback.message.answer(
            text=MESSAGE.DIALOGS.NO_ROMS,
            reply_markup=get_main_kb(),
        )
