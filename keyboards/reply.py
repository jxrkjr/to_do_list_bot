from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def confirm_button():
    keyboards = [
        [
            KeyboardButton(text='Ha'),
            KeyboardButton(text='Yoq'),
        ]
    ]
    kbs = ReplyKeyboardMarkup(resize_keyboard=True,
                              keyboard=keyboards,
                              input_keyboard='tugmalardan foydalaning')
    return kbs
def contact_button():
    keyboards = [
        [
            KeyboardButton(text='Telefon raqamingizni uzatish uchun bosing📱' , request_contact=True),
        ]
    ]
    kbs = ReplyKeyboardMarkup(resize_keyboard=True,
                              keyboard=keyboards,
                              input_keyboard='tugmalardan foydalaning')
    return kbs
def menu_buttons():
    keyboards = [
        [
            KeyboardButton(text='Bugungi vazifalarni ko`rish'),
            KeyboardButton(text='Vazifalarni kiritish'),
            KeyboardButton(text='Vazifalarni tahrirlash')

        ]
    ]
    kbs = ReplyKeyboardMarkup(resize_keyboard=True,
                              keyboard=keyboards,
                              )
    return kbs