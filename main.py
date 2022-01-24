from telebot import TeleBot
from configs import *
from keyboards import generate_choose
from translate import Translator
import sqlite3 as sql
from datetime import datetime

db = sql.connect('tgtrdif.db', check_same_thread=False)

cursor = db.cursor()
bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def command_start(message):  # Сообщение от пользователя
    chat_id = message.chat.id
    bot.send_message(chat_id, '\U0001F44B')
    bot.send_message(chat_id, f'Привет, {message.from_user.first_name}. Я бот переводчик - словарь!')
    print(message)
    buttons(message)


def buttons(message):
    chat_id = message.chat.id
    markup = generate_choose()
    msg = bot.send_message(chat_id, 'Выберите, что хотите сделать', reply_markup=markup)
    bot.register_next_step_handler(msg, choose)


def choose(message):
    chat_id = message.chat.id
    if message.text == 'Переводчик':
        msg = bot.send_message(chat_id, 'Какое слово или текст вы хотите перевести?')
        bot.register_next_step_handler(msg, translateFunc)  # Ждет ввода сообщения после msg и запускает translateFunc
    elif message.text == 'Словарь':
        msg = bot.send_message(chat_id, 'Какого слова описание хотите знать?')
        bot.register_next_step_handler(msg, dictionaryFunc)
    else:
        bot.send_message(chat_id,
                         '\U000026D4\U000026D4\U000026D4<b>Выбрана не верная команда.\nПопробуйте снова!</b> \U000026D4\U000026D4\U000026D4',
                         parse_mode='HTML')
        buttons(message)


# TODO: Разобрать библиотеку translate и написать функцию, которая возвращает переведенный с русского текст


def translateFunc(message):
    chat_id = message.chat.id
    text = message.text
    Olesya = Translator(from_lang='ru', to_lang='en')
    englishText = Olesya.translate(text)
    bot.send_message(chat_id, englishText)
    firstLast = message.from_user.first_name + ' ' + message.from_user.last_name
    username = f'@{message.from_user.username}'
    ts = int(message.date)
    currentTime = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
    INSERT INTO history(telegram_id, messagetext, traslatetext, firstLast, username, messagetime)
    VALUES (?,?,?,?,?,?)
    ''', (chat_id, text, englishText, firstLast, username, currentTime))
    db.commit()
    buttons(message)


def dictionaryFunc(message):
    chat_id = message.chat.id

    buttons(message)


bot.polling(none_stop=True)  # никогда не останавливаться!
