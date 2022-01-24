from telebot.types import ReplyKeyboardMarkup, KeyboardButton



def generate_choose():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    translateButton = KeyboardButton(text='Переводчик')
    dictButton = KeyboardButton(text='Словарь')
    markup.add(translateButton, dictButton)
    return markup