from aiogram.fsm.state import State , StatesGroup

class Register(StatesGroup):
    fullname = State()
    phone_number = State()
    password = State()
    confirm = State()


class AddTaskState(StatesGroup):
    text = State()