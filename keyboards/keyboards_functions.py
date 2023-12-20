import random

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from config.constants import ANSWERS, WORDS, TRANSLATE_DIRECTIONS


def make_words_keyboard() -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками выбора количества слов
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in ['10', '20', '30']]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def make_answer_keyboard(direction: str, answer: str) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками выбора правильного ответа
    :param direction: направление перевода
    :param answer: текст правильного ответа
    :return: объект реплай-клавиатуры
    """
    data = ANSWERS if direction == TRANSLATE_DIRECTIONS[0].lower() else WORDS
    items = set(random.sample(data, 3) + [answer])
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)