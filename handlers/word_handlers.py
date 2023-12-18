import asyncio
import random
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config.database import data_collection
from config import keyboards as kb
from handlers.start_handlers import cmd_start

router = Router()

user_progress = {}


class AnswerQuestion(StatesGroup):
    choosing_answer = State()


@router.message(F.text.lower() == "тренировка")
@router.message(F.text.lower() == "повторить")
async def start_training(message: types.Message):
    user_id = message.from_user.id
    num_words_to_learn = 5
    words_to_learn = random.sample(list(data_collection.find()), k=num_words_to_learn)
    user_progress[user_id] = {"words_to_learn": words_to_learn, "current_word_index": 0}
    current_word = words_to_learn[0]['word']

    await message.answer(f"Переведите слово: {current_word}")


@router.message(lambda message: message.text)
async def handle_answer(message: types.Message):
    user_id = message.from_user.id

    words_to_learn = user_progress.get(user_id, {}).get("words_to_learn")
    current_word_index = user_progress.get(user_id, {}).get("current_word_index")
    current_translation = words_to_learn[current_word_index]['translate'].lower()
    user_answer = message.text.lower()
    if current_word_index < len(words_to_learn):

        if user_answer == current_translation:
            await message.answer(f"Правильно")
        else:
            await message.reply(f"Неправильно. Правильный ответ: {current_translation}")
        current_word_index += 1
        if current_word_index < len(words_to_learn):
            await message.answer(f"Следующее слово: {words_to_learn[current_word_index]['word']}")
        else:
            await finish_training(message)
        user_progress[user_id]["current_word_index"] = current_word_index


async def finish_training(message: types.Message):
    await message.answer("Повторить тренировку?", reply_markup=kb.FINISH_KEYBOARD)
