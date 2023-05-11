from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from logger import logger
from keyboards.main_keyboard import get_main_kb
from messages import MESSAGE


router = Router()


@router.callback_query(Text('stop'))
async def stop(callback: CallbackQuery, state: FSMContext):
    user = callback.message.from_user.username
    logger.info(f'User [{user}] canceled the conversation')
    await callback.message.answer(
        text=MESSAGE.DIALOGS.WELCOME,
        reply_markup=get_main_kb()
    )
    await state.clear()
