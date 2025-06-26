from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command

from keyboards.reply import contact_button, confirm_button, menu_buttons
from states.register import Register

from aiogram import Router , html

from utils.database import Users, session
from utils.decorator import check_register

register_router = Router()

@register_router.message(Command('register'))
@check_register
async def register_command(message: Message , state: FSMContext):
    await message.answer('To`liq ismingizni kiriting: ')
    await state.set_state(Register.fullname)
@register_router.message(Register.fullname)
async def register_fullname(message: Message , state: FSMContext):
    fullname = message.text
    await message.answer('Telefon raqamingizni kiritish uchun tugmani bosing: ' , reply_markup=contact_button())
    await state.update_data(fullname=fullname)
    await state.set_state(Register.phone_number)
@register_router.message(Register.phone_number)
async def register_phone_number(message: Message , state: FSMContext):
    phone_number = message.text
    await message.answer('Parol kiriting: ' , reply_markup=ReplyKeyboardRemove())
    await state.update_data(phone_number=phone_number)
    await state.set_state(Register.password)
@register_router.message(Register.password)
async def register_password(message: Message , state: FSMContext):
    password = message.text
    data = await state.get_data()
    fullname = data.get("fullname")
    phone_number = data.get("phone_number")


    await message.answer(f'To`liq ismingiz: {html.bold(fullname)}\n'
                         f'Telefon raqamingiz: {html.bold(phone_number)}\n'
                         f'Parolingiz: {html.bold(password)}\n'
                         f'Tasdiqlaysizmi?' , reply_markup=confirm_button())
    await state.update_data(password=password)
    await state.set_state(Register.confirm)
@register_router.message(Register.confirm)
async def register_confimed(message: Message , state: FSMContext):
    confirm = message.text
    data = await state.get_data()
    fullname = data.get("fullname")
    phone_number = data.get("phone_number")
    password = data.get("password")

    if confirm.casefold() == 'ha':
        user = Users(fullname=fullname, phone_number=phone_number , password=password , chat_id=message.chat.id)
        user.save(session)
        await state.clear()
        await message.answer('Tabriklaymiz siz muvafaqiyatli royxatdan otdingiz' , reply_markup=menu_buttons())
    elif confirm.casefold() == 'yoq':
        await message.answer('Qayta ro`yxatdan o`tish uchun /register ni bosing')
    else:
        await message.answer('Tugmalarda birini tanlang')





