import random

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from config.constants import ANSWERS


def make_words_keyboard() -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in ['10', '20', '30']]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def make_answer_keyboard(answer: str) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками
    :param answer: текст правильного ответа
    :return: объект реплай-клавиатуры
    """
    items = set(random.sample(ANSWERS, 3) + [answer])
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)