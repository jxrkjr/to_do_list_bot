import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from aiogram.types import Message
from dotenv import load_dotenv

from handlers.menu import menu_router
from handlers.register import register_router
from handlers.start import start_router
from keyboards.inline import inline_router
from utils.notify_admins import bot_start_up, bot_shut_down

load_dotenv()
TOKEN = getenv("BOT_TOKEN")


dp = Dispatcher()





async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_routers(start_router , register_router , menu_router , inline_router)
    dp.startup.register(bot_start_up)
    dp.shutdown.register(bot_shut_down)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())