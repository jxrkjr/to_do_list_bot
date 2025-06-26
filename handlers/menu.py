from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from keyboards.inline import get_tasks_keyboard
from keyboards.reply import menu_buttons
from states.register import AddTaskState  # yangi fayl states.py yaratamiz
from utils.database import session, Tasks

menu_router = Router()

@menu_router.message(F.text == "Bugungi vazifalarni ko`rish")
async def show_tasks(message: Message):
    chat_id = message.chat.id
    tasks = Tasks.get_user_tasks(session, chat_id)
    if not tasks:
        await message.answer("Bugun hech qanday vazifa topilmadi!")
    else:
        text = "Bugungi vazifalaringiz:\n\n"
        for t in tasks:
            status = "✅" if t.is_done else "❌"
            text += f"{status} {t.task_text}\n"
        await message.answer(text)

@menu_router.message(F.text == "Vazifalarni kiritish")
async def add_task_start(message: Message, state: FSMContext):
    await message.answer(
        "Iltimos, yangi vazifa matnini yozing:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AddTaskState.text)

@menu_router.message(AddTaskState.text)
async def save_task(message: Message, state: FSMContext):
    new_task = Tasks(
        chat_id=message.chat.id,
        task_text=message.text
    )
    new_task.save(session)

    await message.answer(
        "Vazifa saqlandi! 🎯",
        reply_markup=menu_buttons()  # asosiy menyuga qaytaramiz
    )
    await state.clear()





@menu_router.message(F.text == "Vazifalarni tahrirlash")
async def edit_tasks(message: Message):
    # Foydalanuvchiga mavjud vazifalar ro'yxatini tugmalar bilan yuboramiz
    keyboard = get_tasks_keyboard(chat_id=message.chat.id)
    await message.answer(
        "Bajargan vazifalaringizni tanlang:",
        reply_markup=keyboard
    )