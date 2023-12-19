import random
from config.constants import ANSWERS
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_keyboard(answer: str) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками
    :param answer: текст правильного ответа
    :return: объект реплай-клавиатуры
    """
    items = set(random.sample(ANSWERS, 3) + [answer])
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)