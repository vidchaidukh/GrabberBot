from os.path import exists
from datetime import datetime
import sqlite3
from threading import Thread

import checker
import telebot

print(__name__ == '__main__')


def write_to_users(id_user, username, name):
    '''Функція додавання запису в таблицю users'''

    try:
        conn = sqlite3.connect('db/database.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (id_user, username) VALUES (?, ?)',
                       (id_user, username))
        cursor.close()
        conn.commit()
        bot.send_message(id_user, "Привіт, " + name + "! Я допоможу тобі в моніторингу дошок оголошень.\n"
                                                      "Просто надішли мені посилання з потрібними тобі фільтрами\n\n"
                                                      "Підтримувані дошки:\nOLX", reply_markup=greet_kb)
    except Exception:
        bot.send_message(id_user, "Привіт, " + name + ", радий тебе бачити!", reply_markup=greet_kb)


def write_to_requests(id_user, url, board_name):
    '''Функція додавання запису в таблицю requests'''

    conn = sqlite3.connect('db/database.db', check_same_thread=False)
    cursor = conn.cursor()
    try:
        time_now = datetime.now()
        cursor.execute('INSERT INTO requests (id_user, url, board_name, last_advert) VALUES (?, ?, ?, ?)',
                       (id_user, url + '?search[order]=created_at%3Adesc',
                        board_name, time_now.strftime("%Y,%m,%d,%H,%M")))
        cursor.close()
        conn.commit()
        bot.send_message(id_user, "Твій запит додано до бази, тепер ти будеш отримувати нові оголошення першим!\n\n"
                                  "Щоб переглянути та керувати своїми запитами перейди на вкладку \"Мої запити\"",
                         reply_markup=greet_kb)
    except Exception:
        bot.send_message(id_user, "Такий пошуковий запит вже створено, переглянь вкладку \"Мої запити\"",
                         reply_markup=greet_kb)


def send_new():
    '''Функція перевірки таблиці adverts та відправки нових повідомлень'''

    while True:
        conn = sqlite3.connect('db/database.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM adverts WHERE is_sended is False")
        new_adv = cursor.fetchall()
        cursor.close()
        for adv in new_adv:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT id_user FROM requests WHERE id =?", (adv[0],))
                user_id = cursor.fetchone()
                str_to_send = '\n'.join(adv[3:-2])
                if exists('img/' + str(adv[1]) + '.png'):
                    bot.send_photo(user_id, open('img/' + str(adv[1]) + '.png', 'rb'), caption=str_to_send[:1020],
                                   reply_markup=greet_kb)
                else:
                    bot.send_message(user_id, str_to_send[:1020], reply_markup=greet_kb)
            except:
                pass
            cursor.execute("UPDATE adverts SET is_sended = True WHERE id_advert=?", (adv[1],))
            cursor.close()
            conn.commit()


if __name__ == "__main__":
    button = telebot.types.KeyboardButton('Мої запити🔍')

    greet_kb = telebot.types.ReplyKeyboardMarkup(True).add(button)

    API = "1743404670:AAFUGxgr_Vbc47c7pxOhbUBhphQ4NLfDU3Y"

    bot = telebot.TeleBot(API)
    boards = ['olx', 'izi']

    checker_thread = Thread(target=checker.check)
    checker_thread.start()


    @bot.message_handler(commands=['start'])
    def starter(message):
        '''Функція активації, викликувана командою start'''

        write_to_users(message.from_user.id, message.from_user.username, message.from_user.first_name)


    @bot.message_handler(func=lambda message: message.text=='Мої запити🔍')
    def show_reqs(message):
        '''Функція відправляє повідомлення користувачу зі списком його запитів'''

        conn = sqlite3.connect('db/database.db', check_same_thread=False)
        cursor = conn.cursor()
        id_user = message.from_user.id
        cursor.execute('SELECT * FROM requests WHERE id_user=?', (id_user,))
        reqs = cursor.fetchall()
        cursor.close()
        temp = ['Ваші запити:']
        markup = telebot.types.InlineKeyboardMarkup()
        for req in reqs:
            temp.append(str(req[0]) + '\n' + req[2])
            markup.add(telebot.types.InlineKeyboardButton(text='Видалити' + str(req[0]), callback_data=req[0]))
        str_to_send = '\n\n'.join(temp)
        bot.send_message(id_user, str_to_send, reply_markup=markup)


    @bot.message_handler(content_types=["text"])
    def text_handler(message):
        '''Функція отримання посилання'''

        text = message.text
        if text.startswith('https'):
            for name in boards:
                if name in text:
                    write_to_requests(message.from_user.id, text, name)


    @bot.callback_query_handler(func=lambda call: True)
    def query_handler(call):
        '''Функція видалення пошукового запиту'''

        conn = sqlite3.connect('db/database.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM adverts WHERE id_request=?", (call.data,))
        cursor.execute("DELETE FROM requests WHERE id=?", (call.data,))
        cursor.close()
        conn.commit()

        bot.answer_callback_query(callback_query_id=call.id, text='Ваш запит видалено!')


    sender_thread = Thread(target=send_new)
    sender_thread.start()

    bot.polling(none_stop=True, timeout=60)