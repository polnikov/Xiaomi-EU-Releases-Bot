from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from messages import MESSAGE


def get_stop_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=MESSAGE.KB_STOP[0],
        callback_data=MESSAGE.KB_STOP[1]
    )
    return builder.as_markup()
