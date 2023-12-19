import random
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards import keyboards as kb
from keyboards.keyboards_functions import make_keyboard
from config.constants import WORDS
from trainers.trainer import Trainer

router = Router()


class TrainingState(StatesGroup):
    CHOOSING = State()


@router.message(F.text.lower() == "тренировка" or F.text.lower() == "повторить")
async def start_training(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    num_words_to_learn = 5
    words_to_learn = random.sample(WORDS, k=num_words_to_learn)
    training_instance = Trainer(user_id, words_to_learn)
    await state.set_state(TrainingState.CHOOSING)
    await state.update_data(training_instance=training_instance)

    await show_next_word(message, state)


@router.message(TrainingState.CHOOSING, lambda message: message.text)
async def handle_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    training_instance: Trainer = data['training_instance']
    user_answer = message.text.lower()

    if training_instance.check_answer(user_answer):
        await message.reply("Правильно!")
    else:
        correct_translation = training_instance.get_current_word()['translate']
        await message.reply(f"Неправильно. Правильный ответ: {correct_translation}")

    training_instance.current_word_index += 1
    if training_instance.current_word_index < len(training_instance.words_to_learn):
        await show_next_word(message, state)
    else:
        await finish_training(message, state)


async def show_next_word(message: types.Message, state: FSMContext):
    data = await state.get_data()
    training_instance: Trainer = data['training_instance']
    current_word = training_instance.get_current_word()['word']
    current_translation = training_instance.get_current_translation()
    await message.answer(f"Переведите слово: {current_word}", reply_markup=make_keyboard(current_translation))


async def finish_training(message: types.Message, state: FSMContext):
    await message.answer("Повторить тренировку?", reply_markup=kb.FINISH_KEYBOARD)
    await state.clear()
