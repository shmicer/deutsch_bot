from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

START_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Тренировка')],
        [KeyboardButton(text='Прогресс')]
    ],
    resize_keyboard=True,
    )

FINISH_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Главное меню')],
        [KeyboardButton(text='Повторить')],
    ],
    resize_keyboard=True,
)

TRANSLATE_DIRECTION_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='DE-RU')],
        [KeyboardButton(text='RU-DE')],
    ],
    resize_keyboard=True,
)