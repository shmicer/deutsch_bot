import asyncio
import random

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config.constants import DATA, WORDS, TRANSLATE_DIRECTIONS
from keyboards import keyboards as kb
from keyboards.keyboards_functions import make_answer_keyboard, make_words_keyboard
from trainers.trainer import Trainer

router = Router()


class TrainingState(StatesGroup):
    TRANSLATE_DIRECTION = State()
    CHOOSING = State()


@router.message(F.text.lower() == 'тренировка')
async def start_training(message: types.Message, state: FSMContext):
    await message.answer(f'Сколько слов повторяем?', reply_markup=make_words_keyboard())


@router.message(lambda message: message.text.isdigit())
async def handle_number_of_words(message: types.Message, state: FSMContext):
    num_words = int(message.text)
    await state.update_data(num_words=num_words)
    await state.set_state(TrainingState.TRANSLATE_DIRECTION)
    await message.answer(f'Направление перевода', reply_markup=kb.TRANSLATE_DIRECTION_KEYBOARD)


@router.message(TrainingState.TRANSLATE_DIRECTION, F.text.in_(TRANSLATE_DIRECTIONS))
async def handle_training_options(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    num_words = data['num_words']
    translate_direction = message.text.lower()
    words_to_learn = random.sample(DATA, k=num_words)
    training_instance = Trainer(user_id, words_to_learn, translate_direction)
    await state.set_state(TrainingState.CHOOSING)
    await state.update_data(training_instance=training_instance, translate_direction=translate_direction)

    await show_next_word(message, state)


@router.message(TrainingState.CHOOSING, lambda message: message.text)
async def handle_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    training_instance: Trainer = data['training_instance']
    user_answer = message.text.lower()

    if training_instance.check_answer(user_answer):
        await message.reply('Правильно!')
    else:
        correct_translation = training_instance.get_current_translation()
        await message.reply(f'Неправильно. Правильный ответ: {correct_translation}')
    await asyncio.sleep(1)
    training_instance.current_word_index += 1
    if training_instance.current_word_index < len(training_instance.words_to_learn):
        await show_next_word(message, state)
    else:
        await finish_training(message, state)


async def show_next_word(message: types.Message, state: FSMContext):
    data = await state.get_data()
    training_instance: Trainer = data['training_instance']
    translate_direction = data['translate_direction']
    current_word = training_instance.get_current_word()
    current_translation = training_instance.get_current_translation()
    await message.answer(f'Переведите слово: {current_word}',
                         reply_markup=make_answer_keyboard(translate_direction, current_translation)
                         )


async def finish_training(message: types.Message, state: FSMContext):
    await message.answer('Повторить тренировку?', reply_markup=kb.FINISH_KEYBOARD)
    await state.clear()


@router.message(F.text.lower() == 'повторить')
async def repeat_training(message: types.Message, state: FSMContext):
    await start_training(message, state)