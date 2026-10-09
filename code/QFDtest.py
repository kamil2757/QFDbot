import sqlite3
import telebot
from telebot import types
import schedule
import time
from datetime import datetime
import random
import functools

bot = telebot.TeleBot('7070138497:AAEBoWNnKOmyDHfEbdOejwyaz0Nq77HTjTM')
@bot.message_handler(commands=['start'])
def greeting(message):
    def notify():
        conn = sqlite3.connect('../data/QFDtest.db')
        cur = conn.cursor()
        cur.execute('''SELECT work FROM works WHERE id_user_tg = ? and time_m = 0 and date = CURRENT_DATE''',
                    (message.from_user.id,))
        db_info = cur.fetchall()

        for i in range(len(db_info)):
            max_num = 0
            if i > max_num:
                max_num = i

        random_num = random.randint(0, max_num)

        random_num2 = random.randint(1, 5)
        if random_num2 == 1:
            bot.send_message(message.chat.id, f'Не забудь сделать {db_info[random_num][0]}! >:0')
        elif random_num2 == 2:
            bot.send_message(message.chat.id, f'Тебе бы сделать {db_info[random_num][0]} :>')
        elif random_num2 == 3:
            bot.send_message(message.chat.id, f'Не забыл  {db_info[random_num][0]} сегодня поделать? :>>>>')
        elif random_num2 == 4:
            bot.send_message(message.chat.id, f'привеееет, а ты будш делать {db_info[random_num][0]} :>? ')
        elif random_num2 == 5:
            bot.send_message(message.chat.id, f'тебе бы {db_info[random_num][0]} поделать :)')

    schedule.every().day.at("15:00").do(notify)
    schedule.every().day.at("19:00").do(notify)

    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Продолжить', callback_data='menu')
    markup.row(button1)
    conn = sqlite3.connect('../data/QFDtest.db')
    cur = conn.cursor()




    cur.execute('''SELECT * FROM users WHERE id_tg = ?''', (message.from_user.id,))
    db_info = cur.fetchone()

    if db_info is None:
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
        bot.send_message(message.chat.id, f'Со мной ты можешь записывать свои дела на день и управлять ими в удобном формате.',
                         reply_markup=markup)
        cur.execute('''INSERT INTO users(id_tg, date_regist, name) VALUES(?,CURRENT_DATE, ?)''', (message.from_user.id, message.from_user.first_name))
        conn.commit()
        conn.close()
    else:
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!', reply_markup=markup)


@bot.callback_query_handler(func=lambda call:True)
def cal_fun(call):
    if call.data == 'menu':
        def notify():
            conn = sqlite3.connect('../data/QFDtest.db')
            cur = conn.cursor()
            cur.execute('''SELECT work FROM works WHERE id_user_tg = ? and time_m = 0 and date = CURRENT_DATE''', (call.from_user.id, ))
            db_info = cur.fetchall()

            max_num = 0
            for i in range(len(db_info)):
                if i > max_num:
                    max_num = i

            random_num = random.randint(0, max_num)

            random_num2 = random.randint(1, 5)
            if random_num2 == 1:
                bot.send_message(call.message.chat.id, f'Не забудь сделать {db_info[random_num][0]}! >:0')
            elif random_num2 == 2:
                bot.send_message(call.message.chat.id, f'Тебе бы сделать {db_info[random_num][0]} :>')
            elif random_num2 == 3:
                bot.send_message(call.message.chat.id, f'Не забыл  {db_info[random_num][0]} сегодня поделать? :>>>>')
            elif random_num2 == 4:
                bot.send_message(call.message.chat.id, f'привеееет, а ты будш делать {db_info[random_num][0]} :>? ')
            elif random_num2 == 5:
                bot.send_message(call.message.chat.id, f'тебе бы {db_info[random_num][0]} поделать :)')



        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Дела', callback_data='tasks')
        button2 = types.InlineKeyboardButton('Профиль', callback_data='profile')
        site = types.WebAppInfo('https://www.donationalerts.com/r/kamil42658')
        button3 = types.InlineKeyboardButton('Поддержать монеткой', web_app=site)
        markup.row(button1)
        markup.row(button2)
        markup.row(button3)

        photo = open('../data/меню.png', 'rb')
        bot.send_photo(call.message.chat.id, photo, reply_markup=markup)

        if random.randint(1, 1) == 1:
            conn = sqlite3.connect('../data/QFDtest.db')
            cur = conn.cursor()
            random_num = random.randint(1, 2)
            if random_num == 1:
                cur.execute('''SELECT sum(time_m) FROM works WHERE id_user_tg=? AND date = CURRENT_DATE''',
                            (call.from_user.id, ))

                db_info = cur.fetchone()
                if db_info[0] != None and db_info[0] // 60 >= 3:
                    bot.send_message(call.message.chat.id, f'Вау, у тебя уже {db_info[0] // 60}ч :0')
                    conn.close()
                else:
                    bot.send_message(call.message.chat.id, f'сможешь за сегодня 3 часа ;) ?')
                    conn.close()
            elif random_num == 2:
                cur.execute('''SELECT date_regist FROM users WHERE id_tg = ?''', (call.from_user.id, ))
                db_info1 = cur.fetchone()
                cur.execute('''SELECT julianday('now') - julianday(?)''', (db_info1[0],))
                db_info2 = cur.fetchone()
                days_difference = int(db_info2[0])
                bot.send_message(call.message.chat.id, f'ты в нашем боте уже дней {days_difference} :>')
                conn.close()


        while True:
            schedule.run_pending()
            time.sleep(1)
    elif call.data == 'delete_tasks':
        bot.send_message(call.message.chat.id, 'Напиши дело, которое ты хочешь удалить (время удалится)')
        bot.register_next_step_handler(call.message, delete_tasks2)
    elif call.data == 'take_past':
        conn = sqlite3.connect('../data/QFDtest.db')

        cur = conn.cursor()
        cur.execute('''SELECT work FROM works WHERE id_user_tg = ?''', (call.from_user.id, ))

        if cur.fetchone() is None:
            bot.send_message(call.message.chat.id, 'У тебя не было вчера записанно дел')
            conn.close()
        else:
            str_tasks = ''
            cur.execute(
                '''UPDATE works SET date = CURRENT_DATE, time_m = 0 WHERE id_user_tg = ? AND date = DATE('now', '-1 day')''',
                (call.from_user.id, ))
            conn.commit()

            cur.execute('''SELECT work FROM works WHERE id_user_tg = ? AND date = CURRENT_DATE''', (call.from_user.id, ))

            db_info = cur.fetchall()
            for i in range(len(db_info)):
                str_tasks += f'{db_info[i][0]}\n'

            str_tasks += f'\n'
            str_tasks += f'Время всего:'

            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('Отметить', callback_data='mark_tasks')
            button2 = types.InlineKeyboardButton('Сбросить', callback_data='reset_tasks')
            button3 = types.InlineKeyboardButton('Добавить', callback_data='create_tasks')
            button4 = types.InlineKeyboardButton('Удалить', callback_data='delete_tasks')
            button5 = types.InlineKeyboardButton('Меню', callback_data='menu')
            markup.row(button1, button2)
            markup.row(button3, button4)
            markup.row(button5)
            bot.send_message(call.message.chat.id, str_tasks, reply_markup=markup)
            conn.close()



    elif call.data == 'tasks':
        conn = sqlite3.connect('../data/QFDtest.db')
        cur = conn.cursor()
        cur.execute('''SELECT work FROM works WHERE id_user_tg = ? AND date = CURRENT_DATE''', (call.from_user.id, ))
        db_info = cur.fetchall()

        if db_info == []:
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('Составить', callback_data='create_tasks')
            button2 = types.InlineKeyboardButton('Взять прошлые', callback_data='take_past')
            button3 = types.InlineKeyboardButton('Меню', callback_data='menu')
            markup.row(button1, button2)
            photo = open('../data/дела.png', 'rb')
            bot.send_photo(call.message.chat.id, photo, reply_markup=markup)
        else:
            photo = open('../data/дела.png', 'rb')
            bot.send_photo(call.message.chat.id, photo)
            str_tasks = ''
            cur.execute('''SELECT work, time_m FROM works WHERE id_user_tg = ? AND date = CURRENT_DATE''',
                        (call.from_user.id, ))
            db_info = cur.fetchall()
            for i in range(len(db_info)):
                time_hours = db_info[i][1] // 60
                time_minutes = db_info[i][1] % 60
                str_tasks += f'{db_info[i][0]} '

                if db_info[i][1] >= 120:
                    str_tasks += f'✅✅✅'
                elif db_info[i][1] >= 60:
                    str_tasks += f'✅✅'
                elif db_info[i][1] > 0:
                    str_tasks += f'✅'

                if time_minutes == 0 and time_hours != 0:
                    str_tasks += f'({time_hours}ч)\n'
                elif time_minutes == 0 and time_hours == 0:
                    str_tasks += '\n'
                elif time_hours == 0:
                    str_tasks += f'({time_minutes}мин)\n'
                else:
                    str_tasks += f'({time_hours}ч {time_minutes}мин)\n'


            cur.execute('''SELECT sum(time_m) FROM works WHERE id_user_tg = ? AND date =  CURRENT_DATE''',
                        (call.from_user.id, ))

            db_info = cur.fetchone()
            str_tasks += f'\n'
            str_tasks += f'Время всего:  {db_info[0] // 60}ч {db_info[0] % 60}мин'

            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('Отметить', callback_data='mark_tasks')
            button2 = types.InlineKeyboardButton('Сбросить', callback_data='reset_tasks')
            button3 = types.InlineKeyboardButton('Добавить', callback_data='create_tasks')
            button4 = types.InlineKeyboardButton('Удалить', callback_data='delete_tasks')
            button5 = types.InlineKeyboardButton('Меню', callback_data='menu')
            markup.row(button1, button2)
            markup.row(button3, button4)
            markup.row(button5)
            bot.send_message(call.message.chat.id, str_tasks, reply_markup=markup)
            conn.close()


    elif call.data == 'mark_tasks':
        bot.send_message(call.message.chat.id, 'Какое?')
        bot.register_next_step_handler(call.message, mark_tasks2)

    elif call.data == 'create_tasks':
        bot.send_message(call.message.chat.id, 'Напиши дела. Если ты закончил, напиши ready')
        bot.send_message(call.message.chat.id, 'в таком ввиде:')
        photo = open('../data/пример сообщение.png', 'rb')
        bot.send_photo(call.message.chat.id, photo)

        bot.register_next_step_handler(call.message, create_tasks2)

    elif call.data == 'reset_tasks':
        conn = sqlite3.connect('data/QFDtest.db')

        cur = conn.cursor()
        cur.execute('''SELECT SUM(time_m) FROM works WHERE id_user_tg = ? AND date = CURRENT_DATE''', (call.from_user.id,))
        time_m_forreset = cur.fetchone()[0]
        cur.execute(
                    '''
                       UPDATE users
                       SET sum_time = sum_time - ?
                       WHERE id_tg = ?
                    ''', (time_m_forreset, call.from_user.id))
        conn.commit()
        cur.execute('''DELETE FROM works WHERE id_user_tg = ? AND date = CURRENT_DATE''', (call.from_user.id, ))
        conn.commit()

        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Меню', callback_data='menu')
        markup.row(button1)

        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, 'Дела обнулились', reply_markup=markup)

        cur.execute('''SELECT sum_time FROM users WHERE id_tg = ?''', (call.from_user.id,))
        if cur.fetchone()[0] is None:
            cur.execute(
                '''
                   UPDATE users
                   SET sum_time = 0
                   WHERE id_tg = ?
                ''', (call.from_user.id))
            conn.commit()
            conn.close()



    elif call.data == 'profile':
        photo = open('../data/дефолт ава.png', 'rb')
        bot.send_photo(call.message.chat.id, photo)

        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton('меню', callback_data='menu')
        markup.add(button)

        conn = sqlite3.connect('../data/QFDtest.db')
        cur = conn.cursor()

        cur.execute('''SELECT sum_time,date_regist FROM users WHERE id_tg = ?''', (call.from_user.id,))
        bd_info = cur.fetchone()
        time_h = bd_info[0] // 60
        time_m = bd_info[0] % 60
        cur.execute('''SELECT julianday('now') - julianday(?)''', (bd_info[1],))
        bd_info2 = cur.fetchone()
        days_difference = int(bd_info2[0])


        if call.from_user.id == 1450823762:
            bot.send_message(call.message.chat.id,
                             f'Самое красивое имя: {call.from_user.first_name}\nВы с нами уже дней: {(days_difference)}\n\nВсего времени: {time_h}ч {time_m}мин ',
                             reply_markup=markup)
            random_num = random.randint(1, 5)
            if random_num == 1:
                bot.send_message(call.message.chat.id, 'Я очень люблю тебя!')
            if random_num == 2:
                    bot.send_message(call.message.chat.id, 'Ты самая красивая девушка')
            if random_num == 3:
                bot.send_message(call.message.chat.id, 'Ты оооочень милая')
            if random_num == 4:
                    bot.send_message(call.message.chat.id, 'обнимаю, целую')
            if random_num == 5:
                    bot.send_message(call.message.chat.id, 'Ты моя умничка, оч люблю тя')
            if random_num == 6:
                    bot.send_message(call.message.chat.id, 'Я всегда рядом')
            if random_num == 7:
                bot.send_message(call.message.chat.id, 'ты у меня самый большой молодец')
            if random_num == 8:
                bot.send_message(call.message.chat.id, 'У тебя самые красивые глаза')
            if random_num == 9:
                bot.send_message(call.message.chat.id, 'Милее тя никогда никого не видел!')
            if random_num == 10:
                bot.send_message(call.message.chat.id, 'У тебя самая красивая улыбка')

            conn.close()


        else:
            bot.send_message(call.message.chat.id,
                             f'Ник: {call.from_user.first_name}\nВы с нами уже дней: {(days_difference)}\n\nВсего времени: {time_h}ч {time_m}мин ',
                             reply_markup=markup)
            conn.close()

def delete_tasks2(message):
    conn = sqlite3.connect('../data/QFDtest.db')
    cur = conn.cursor()

    cur.execute('''SELECT work FROM works WHERE work = ? AND id_user_tg = ?''',
                (message.text.title(), message.from_user.id))
    db_info = cur.fetchone()

    if db_info is None:
        bot.send_message(message.chat.id, 'не существует такого дело, напиши заново')
        bot.register_next_step_handler(message, mark_tasks2)
    else:
        cur.execute('''SELECT time_m FROM works WHERE work = ? AND id_user_tg = ?''',
                (message.text.title(), message.from_user.id))
        work_time = cur.fetchone()[0]

        cur.execute('''DELETE FROM works WHERE work = ? AND id_user_tg = ?''',
        (message.text.title(), message.from_user.id))
        cur.execute(
            '''
               UPDATE users
               SET sum_time = sum_time - ?
               WHERE id_tg = ?
            ''', (work_time, message.from_user.id))
        conn.commit()
        conn.close()

        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Продолжить', callback_data='tasks')
        markup.row(button1)
        bot.send_message(message.chat.id, 'Дело было удаленно', reply_markup=markup)


def mark_tasks2(message):
    conn = sqlite3.connect('../data/QFDtest.db')

    cur = conn.cursor()
    cur.execute('''SELECT work FROM works WHERE work = ? AND id_user_tg = ?''',
                (message.text.title(), message.from_user.id))
    db_info = cur.fetchone()

    if db_info is None:
        bot.send_message(message.chat.id, 'не существует такого дело, напиши заново')
        bot.register_next_step_handler(message, mark_tasks2)
    else:
        bot.send_message(message.chat.id, 'Сколько минут?')
        bot.register_next_step_handler(message, mark_tasks3, message.text)

def mark_tasks3(message, work):
    work_minutes = message.text
    if message.text.isdigit():
        conn = sqlite3.connect('../data/QFDtest.db')
        if message.text.isdigit():
            cur = conn.cursor()
            cur.execute('''
                        UPDATE works
                        SET time_m = time_m + ?
                        WHERE work = ? AND date = CURRENT_DATE AND id_user_tg = ?;
            ''', (work_minutes, work.title(), message.from_user.id))
            conn.commit()
            str_tasks = ''
            cur.execute('''SELECT work, time_m FROM works WHERE id_user_tg = ? AND date = CURRENT_DATE''',
                        (message.from_user.id,))
            db_info = cur.fetchall()
            for i in range(len(db_info)):
                time_hours = db_info[i][1] // 60
                time_minutes = db_info[i][1] % 60
                str_tasks += f'{db_info[i][0]} '

                if db_info[i][1] >= 120:
                    str_tasks += f'✅✅✅'
                elif db_info[i][1] >= 60:
                    str_tasks += f'✅✅'
                elif db_info[i][1] > 0:
                    str_tasks += f'✅'

                if time_minutes == 0 and time_hours != 0:
                    str_tasks += f'({time_hours}ч)\n'
                elif time_minutes == 0 and time_hours == 0:
                    str_tasks += '\n'
                elif time_hours == 0:
                    str_tasks += f'({time_minutes}мин)\n'
                else:
                    str_tasks += f'({time_hours}ч {time_minutes}мин)\n'

            cur.execute('''SELECT sum(time_m) FROM works WHERE id_user_tg = ? AND date =  CURRENT_DATE''',
                        (message.from_user.id, ))

            db_info = cur.fetchone()
            str_tasks += f'\n'
            str_tasks += f'Время всего:  {db_info[0] // 60}ч {db_info[0] % 60}мин'

            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('Отметить', callback_data='mark_tasks')
            button2 = types.InlineKeyboardButton('Сбросить', callback_data='reset_tasks')
            button3 = types.InlineKeyboardButton('Добавить', callback_data='create_tasks')
            button4 = types.InlineKeyboardButton('Удалить', callback_data='delete_tasks')
            button5 = types.InlineKeyboardButton('Меню', callback_data='menu')
            markup.row(button1, button2)
            markup.row(button3, button4)
            markup.row(button5)
            bot.send_message(message.chat.id, str_tasks, reply_markup=markup)

            cur.execute('''UPDATE users SET sum_time = sum_time + ? WHERE id_tg = ?''',
                        (work_minutes, message.from_user.id))
            conn.commit()
            conn.close()
    else:
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Продолжить', callback_data='tasks')
        markup.row(button1)
        bot.send_message(message.chat.id, 'Нужно писать время, а не текст', reply_markup=markup)






def create_tasks2(message):
    user_task = message.text.title()
    conn = sqlite3.connect('../data/QFDtest.db')

    cur = conn.cursor()

    if user_task.strip().lower() == 'ready':
        str_tasks = ''
        cur.execute('''SELECT work, time_m FROM works WHERE id_tg = ? AND date = CURRENT_DATE''',
                    (message.from_user.id, ))
        db_info = cur.fetchall()
        for i in range(len(db_info)):
            str_tasks += f'{db_info[i][0]} \n'

        cur.execute('''SELECT sum(time_m) FROM works WHERE id_tg = ? AND date =  CURRENT_DATE''',
                    (message.from_user.id, ))

        db_info = cur.fetchone()
        str_tasks += f'\n'
        str_tasks += f'Время всего:  {db_info[0] // 60}ч {db_info[0] % 60}мин'

        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Отметить', callback_data='mark_tasks')
        button2 = types.InlineKeyboardButton('Сбросить', callback_data='reset_tasks')
        button3 = types.InlineKeyboardButton('Добавить', callback_data='create_tasks')
        button4 = types.InlineKeyboardButton('Удалить', callback_data='delete_tasks')
        button5 = types.InlineKeyboardButton('Меню', callback_data='menu')
        markup.row(button1, button2)
        markup.row(button3, button4)
        markup.row(button5)
        bot.send_message(message.chat.id, str_tasks, reply_markup=markup)
        conn.close()
    else:

        cur.execute('''INSERT INTO works(work,id_user) VALUES(?,?)''', (user_task, message.from_user.id))
        conn.commit()
        conn.close()
        bot.register_next_step_handler(message, create_tasks2)





def create_tasks2(message):
    user_task = message.text.title()
    conn = sqlite3.connect('../data/QFDtest.db')

    cur = conn.cursor()

    if user_task.strip().lower() == 'ready':
        str_tasks = ''
        cur.execute('''SELECT work, time_m FROM works WHERE id_user_tg = ? AND date = CURRENT_DATE''',
                    (message.from_user.id, ))
        db_info = cur.fetchall()
        for i in range(len(db_info)):
            str_tasks += f'{db_info[i][0]} \n'

        cur.execute('''SELECT sum(time_m) FROM works WHERE id_user_tg = ? AND date =  CURRENT_DATE''',
                    (message.from_user.id, ))

        db_info = cur.fetchone()
        str_tasks += f'\n'
        str_tasks += f'Время всего:  {db_info[0] // 60}ч {db_info[0] % 60}мин'

        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Отметить', callback_data='mark_tasks')
        button2 = types.InlineKeyboardButton('Сбросить', callback_data='reset_tasks')
        button3 = types.InlineKeyboardButton('Добавить', callback_data='create_tasks')
        button4 = types.InlineKeyboardButton('Удалить', callback_data='delete_tasks')
        button5 = types.InlineKeyboardButton('Меню', callback_data='menu')
        markup.row(button1, button2)
        markup.row(button3, button4)
        markup.row(button5)
        bot.send_message(message.chat.id, str_tasks, reply_markup=markup)
        conn.close()
    else:

        cur.execute('''INSERT INTO works(work,id_user_tg) VALUES(?,?)''', [user_task, message.from_user.id])
        conn.commit()
        conn.close()
        bot.register_next_step_handler(message, create_tasks2)




bot.polling(none_stop=True)