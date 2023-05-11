from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from messages import MESSAGE


def get_list_kb(buttons_list: list, action: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for btn in buttons_list:
        builder.button(
            text=btn,
            callback_data=f'{action}-rom {btn}'
        )
    builder.button(
        text=MESSAGE.KB_STOP[0],
        callback_data=MESSAGE.KB_STOP[1]
    )
    builder.adjust(2)
    return builder.as_markup()
