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
    user = callback.from_user.username
    logger.info(f'User [{user}] canceled the conversation')
    lang = callback.from_user.language_code.upper()
    match lang:
        case 'RU':
            lang = 'RU'
        case _:
            lang = 'EN'
    text = getattr(MESSAGE, f'{lang}_WELCOME')
    await callback.message.answer(
        text=text,
        reply_markup=get_main_kb(lang)
    )
    await callback.answer()
    await state.clear()
