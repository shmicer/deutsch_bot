import asyncio
import logging
from aiogram import Bot, Dispatcher
from pymongo import MongoClient

from config import bot_config
from handlers import start_handlers, word_handlers

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=bot_config.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_routers(start_handlers.router, word_handlers.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())