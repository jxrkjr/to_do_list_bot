from aiogram import Router, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.database import SessionLocal, Tasks

inline_router = Router()

def get_tasks_keyboard(chat_id: int):
    session = SessionLocal()
    tasks = session.query(Tasks).filter(Tasks.chat_id == chat_id).all()
    session.close()

    keyboard = [
        [
            InlineKeyboardButton(
                text=f"{'✅' if task.is_done else '❌'} {task.task_text}",
                callback_data=f"toggle_task_{task.id}"
            )
        ] for task in tasks
    ]
    # Tasdiqlash tugmasi
    keyboard.append(
        [InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm_tasks")]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@inline_router.callback_query(F.data.startswith("toggle_task_"))
async def toggle_task(callback: types.CallbackQuery):
    task_id = int(callback.data.split("_")[2])
    session = SessionLocal()
    task = session.query(Tasks).get(task_id)
    if task:
        task.is_done = not task.is_done
        session.commit()
    session.close()

    await callback.message.edit_reply_markup(
        reply_markup=get_tasks_keyboard(callback.message.chat.id)
    )
    await callback.answer("Holat o'zgartirildi!")


@inline_router.callback_query(F.data == "confirm_tasks")
async def confirm_tasks(callback: types.CallbackQuery):
    # Inline tugmalarni olib tashlaymiz
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("Ma'lumotlar o'zgardi ✅")
    await callback.answer()