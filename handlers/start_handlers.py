import time

from aiogram import Router, types, F
from aiogram.filters import Command
from pymongo import MongoClient

from config.database import search_or_save_user, users

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Регистрация"),
            types.KeyboardButton(text="Тренировка"),
            types.KeyboardButton(text="Прогресс")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    await message.answer("Выберите тренировку или посмотрите свой прогресс?", reply_markup=keyboard)


@router.message(F.text.lower() == "регистрация")
async def show_progress(message: types.Message):
    search_or_save_user(message.from_user.id, message.from_user.username, time.time())
    await message.reply("Вот ваш прогресс", reply_markup=types.ReplyKeyboardRemove())


@router.message(F.text.lower() == "прогресс")
async def show_progress(message: types.Message):
    await message.reply("Вот ваш прогресс")
