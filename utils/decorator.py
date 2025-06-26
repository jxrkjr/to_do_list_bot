from functools import wraps
from keyboards.reply import menu_buttons
from utils.database import Users, session
from aiogram.utils.i18n import gettext as _

def check_register(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        message = args[0]
        chat_id = message.chat.id

        if Users.check_register(session, chat_id):
            await message.answer(('Botdan foydalanishga xush kelibsiz!'), reply_markup=menu_buttons())
        else:
            return await func(*args, **kwargs)

    return wrapper