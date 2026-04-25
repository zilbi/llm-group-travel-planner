from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Прослушка", callback_data="listen")],
        # [InlineKeyboardButton(text="Прошлые планы", callback_data="past_trip")],
    ],
)

keyboard_listen = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Включить"),
            KeyboardButton(text="Выключить"),
        ],
    ],
)
