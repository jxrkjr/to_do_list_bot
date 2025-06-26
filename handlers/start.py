from aiogram import Router , html
from aiogram.types import Message, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters import CommandStart

from utils.decorator import check_register

start_router = Router()

@start_router.message(CommandStart())
@check_register
async def command_start_handler(message: Message):
    fullname = html.bold(message.from_user.full_name)
    await message.answer(
        ("Salom, {name}!\n\n Ro'yxatdan o'tish uchun 👉 /register kamandasini bosing").format(name=fullname)
    , reply_markup=ReplyKeyboardRemove())