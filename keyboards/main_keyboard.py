from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from messages import MESSAGE


def get_main_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=MESSAGE.KB_MAIN.ADD_ROM[0],
                callback_data=MESSAGE.KB_MAIN.ADD_ROM[1]
            ),
        ], [
            InlineKeyboardButton(
                text=MESSAGE.KB_MAIN.DEL_ROM[0],
                callback_data=MESSAGE.KB_MAIN.DEL_ROM[1]
            ),
        ], [
            InlineKeyboardButton(
                text=MESSAGE.KB_MAIN.GET_DATA[0],
                callback_data=MESSAGE.KB_MAIN.GET_DATA[1]
            ),
        ], [
            InlineKeyboardButton(
                text=MESSAGE.KB_MAIN.DEL_DATA[0],
                callback_data=MESSAGE.KB_MAIN.DEL_DATA[1]
            ),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
