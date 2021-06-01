from datetime import datetime
import sqlite3
from threading import Thread

import checker
import telebot

API = "1743404670:AAFUGxgr_Vbc47c7pxOhbUBhphQ4NLfDU3Y"

bot = telebot.TeleBot(API)
boards = ['olx', 'izi']

checker_thread = Thread(target=checker.check)
checker_thread.start()

@bot.message_handler(commands=['start'])
def starter(message):
    write_to_users(message.from_user.id, message.from_user.username, message.from_user.first_name)


@bot.message_handler(content_types=["text"])
def text_handler(message):
    text = message.text
    if text.startswith('https'):
        for name in boards:
            if name in text:
                write_to_requests(message.from_user.id, text, name)


def write_to_users(id_user, username, name):
    try:
        conn = sqlite3.connect('db/database.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (id_user, username) VALUES (?, ?)',
                   (id_user, username))
        conn.commit()
        bot.send_message(id, "Привіт, " + name +  "! Я допоможу тобі в моніторингу дошок оголошень.\n"
                             "Просто надішли мені посилання з потрібними тобі фільтрами\n\n"
                             "Підтримувані дошки:\n")
    except Exception:
        bot.send_message(id_user, "Привіт, " + name + ", радий тебе бачити!")


def write_to_requests(id_user, url, board_name):
    conn = sqlite3.connect('db/database.db', check_same_thread=False)
    cursor = conn.cursor()
    try:
        time_now = datetime.now()
        cursor.execute('INSERT INTO requests (id_user, url, board_name, last_advert) VALUES (?, ?, ?, ?)',
                       (id_user, url.split("&search[order]")[0] + "&search[order]=created_at%3Adesc",
                        board_name, time_now.strftime("%Y/%m/%d %H:%M")))
        conn.commit()
        bot.send_message(id_user, "Твій запит додано до бази, тепер ти будеш отримувати нові оголошення першим!\n\n"
                                  "Щоб переглянути та керувати своїми запитами перейди на вкладку \"Мої запити\"")
    except Exception:
        bot.send_message(id_user, "Такий пошуковий запит вже створено, переглянь вкладку \"Мої запити\"")


bot.polling(none_stop=True, timeout=60)