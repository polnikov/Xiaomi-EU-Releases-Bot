from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from messages import MESSAGE


def get_main_kb(lang) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=getattr(MESSAGE, f'MESSAGE.{lang}_ADD_ROM')[0],
                callback_data=getattr(MESSAGE, f'MESSAGE.{lang}_ADD_ROM')[1]
            ),
        ], [
            InlineKeyboardButton(
                text=getattr(MESSAGE, f'MESSAGE.{lang}_DEL_ROM')[0],
                callback_data=getattr(MESSAGE, f'MESSAGE.{lang}_DEL_ROM')[1]
            ),
        ], [
            InlineKeyboardButton(
                text=getattr(MESSAGE, f'MESSAGE.{lang}_GET_DATA')[0],
                callback_data=getattr(MESSAGE, f'MESSAGE.{lang}_GET_DATA')[1]
            ),
        ], [
            InlineKeyboardButton(
                text=getattr(MESSAGE, f'MESSAGE.{lang}_DEL_DATA')[0],
                callback_data=getattr(MESSAGE, f'MESSAGE.{lang}_DEL_DATA')[1]
            ),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
