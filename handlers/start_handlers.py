from aiogram import Router, types, F
from aiogram.filters import Command
from keyboards import keyboards as kb

router = Router()


@router.message(Command("start"))
@router.message(F.text.lower() == "главное меню")
async def cmd_start(message: types.Message):
    await message.answer("Выберите тренировку или посмотрите свой прогресс", reply_markup=kb.START_KEYBOARD)


@router.message(F.text.lower() == "прогресс")
async def show_progress(message: types.Message):
    await message.reply("Вот ваш прогресс")
