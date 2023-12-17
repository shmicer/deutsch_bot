import random
from aiogram import Router, types, F


from config.database import data_collection
from handlers.start_handlers import cmd_start

router = Router()

user_progress = {}


@router.message(F.text.lower() == "тренировка")
async def start_training(message: types.Message):
    user_id = message.from_user.id
    num_words_to_learn = 5
    current_word_index = 0

    words_to_learn = random.sample(list(data_collection.find()), k=num_words_to_learn)
    user_progress[user_id] = {"words_to_learn": words_to_learn, "current_word_index": 0}
    current_word = words_to_learn[current_word_index]['word']

    await message.reply(f"Переведите слово: {current_word}")


@router.message(lambda message: message.text)
async def handle_answer(message: types.Message):
    user_id = message.from_user.id

    words_to_learn = user_progress.get(user_id, {}).get("words_to_learn")
    current_word_index = user_progress.get(user_id, {}).get("current_word_index", 0)
    current_translation = words_to_learn[current_word_index]['translate']

    if words_to_learn and current_word_index < len(words_to_learn):

        user_answer = message.text.lower()
        correct_answer = current_translation.lower()
        if current_word_index < len(words_to_learn) - 1:
            current_word_index += 1
            if user_answer == correct_answer:
                await message.reply(f"Правильно")
            else:
                await message.reply(f"Неправильно. Правильный ответ: {correct_answer}")

            await message.answer(f"Следующее слово: {words_to_learn[current_word_index]['word']}")
        else:
            await message.answer(f"Отлично. Вы повторили сегодняшние {len(words_to_learn)} слов")
            await finish_training(message)

        user_progress[user_id]["current_word_index"] = current_word_index
    else:
        await start_training(message)


async def finish_training(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Главное меню"),
            types.KeyboardButton(text="Повторить"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    await message.answer("Повторить тренировку?", reply_markup=keyboard)


@router.message(F.text.lower() == "повторить")
async def repeat_training(message: types.Message):
    await start_training(message)