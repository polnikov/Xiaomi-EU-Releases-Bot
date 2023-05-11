from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_back_kb() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(
            text='back to top',
            callback_data='start'
        ),
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
