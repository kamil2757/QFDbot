import sqlite3
import telebot
from telebot import types
import time
import random

bot = telebot.TeleBot('6606153195:AAGJFy_W_ejzna2LzF_hKdAdyhW00ZeTL30')

@bot.message_handler(commands=['start'])
def greeting(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Продолжить', callback_data='menu')
    markup.row(button1)

    conn = sqlite3.connect('QFD.db')
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
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Дела', callback_data='tasks')
        button2 = types.InlineKeyboardButton('Профиль', callback_data='profile')
        site = types.WebAppInfo('https://www.donationalerts.com/r/kamil42658')
        button3 = types.InlineKeyboardButton('Поддержать монеткой', web_app=site)
        markup.row(button1)
        markup.row(button2)
        markup.row(button3)

        photo = open('меню.png', 'rb')
        bot.send_photo(call.message.chat.id, photo, reply_markup=markup)

        if random.randint(1, 4) == 1:
            conn = sqlite3.connect('QFD.db')
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
                cur.execute('''SELECT DATE('now') - ?''', (db_info1[0],))
                db_info2 = cur.fetchone()
                bot.send_message(call.message.chat.id, f'ты в нашем боте уже дней {db_info2[0]} :>')
                conn.close()

    elif call.data == 'take_past':
        conn = sqlite3.connect('QFD.db')

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
            button3 = types.InlineKeyboardButton('Меню', callback_data='menu')
            markup.row(button1, button2)
            markup.row(button3)
            bot.send_message(call.message.chat.id, str_tasks, reply_markup=markup)
            conn.close()


    elif call.data == 'tasks':
        conn = sqlite3.connect('QFD.db')
        cur = conn.cursor()
        cur.execute('''SELECT work FROM works WHERE id_user_tg = ? AND date = CURRENT_DATE''', (call.from_user.id, ))
        db_info = cur.fetchall()

        if db_info == []:
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('Составить', callback_data='create_tasks')
            button2 = types.InlineKeyboardButton('Взять прошлые', callback_data='take_past')
            button3 = types.InlineKeyboardButton('меню', callback_data='menu')
            markup.row(button1,button2)
            markup.row(button3)
            photo = open('дела.png', 'rb')
            bot.send_photo(call.message.chat.id, photo, reply_markup=markup)
        else:
            photo = open('дела.png', 'rb')
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
            button3 = types.InlineKeyboardButton('Меню', callback_data='menu')
            markup.row(button1, button2)
            markup.row(button3)
            bot.send_message(call.message.chat.id, str_tasks, reply_markup=markup)
            conn.close()


    elif call.data == 'mark_tasks':
        bot.send_message(call.message.chat.id, 'Какое?')
        bot.register_next_step_handler(call.message, mark_tasks2)

    elif call.data == 'create_tasks':
        bot.send_message(call.message.chat.id, 'Напиши свои дела. Если ты закончил, напиши ready')
        bot.send_message(call.message.chat.id, 'в таком ввиде:')
        photo = open('пример сообщение.png', 'rb')
        bot.send_photo(call.message.chat.id, photo)

        bot.register_next_step_handler(call.message, create_tasks2)

    elif call.data == 'reset_tasks':
        conn = sqlite3.connect('QFD.db')

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
        photo = open('дефолт ава.png', 'rb')
        bot.send_photo(call.message.chat.id, photo)

        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton('меню', callback_data='menu')
        markup.add(button)

        conn = sqlite3.connect('QFD.db')
        cur = conn.cursor()

        cur.execute('''SELECT sum_time,date_regist FROM users WHERE id_tg = ?''', (call.from_user.id,))
        bd_info = cur.fetchone()
        time_h = bd_info[0] // 60
        time_m = bd_info[0] % 60
        cur.execute('''SELECT DATE('now') - ?''', (bd_info[1],))
        bd_info2 = cur.fetchone()

        if call.from_user.id == 1450823762:
            bot.send_message(call.message.chat.id,
                             f'Самое красивое имя: {call.from_user.first_name}\nВы с нами уже дней: {bd_info2[0]}\n\nВсего времени: {time_h}ч {time_m}мин ',
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
                             f'Ник: {call.from_user.first_name}\nВы с нами уже дней: {bd_info2[0]}\n\nВсего времени: {time_h}ч {time_m}мин ',
                             reply_markup=markup)
            conn.close()



def mark_tasks2(message):
    conn = sqlite3.connect('QFD.db')

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
        conn = sqlite3.connect('QFD.db')
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
            button3 = types.InlineKeyboardButton('Меню', callback_data='menu')
            markup.row(button1, button2)
            markup.row(button3)
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
    conn = sqlite3.connect('QFD.db')

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
        button3 = types.InlineKeyboardButton('Меню', callback_data='menu')
        markup.row(button1, button2)
        markup.row(button3)
        bot.send_message(message.chat.id, str_tasks, reply_markup=markup)
        conn.close()
    else:

        cur.execute('''INSERT INTO works(work,id_user) VALUES(?,?)''', (user_task, message.from_user.id))
        conn.commit()
        conn.close()
        bot.register_next_step_handler(message, create_tasks2)





def create_tasks2(message):
    user_task = message.text.title()
    conn = sqlite3.connect('QFD.db')

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
        button3 = types.InlineKeyboardButton('Меню', callback_data='menu')
        markup.row(button1, button2)
        markup.row(button3)
        bot.send_message(message.chat.id, str_tasks, reply_markup=markup)
        conn.close()
    else:

        cur.execute('''INSERT INTO works(work,id_user_tg) VALUES(?,?)''', [user_task, message.from_user.id])
        conn.commit()
        conn.close()
        bot.register_next_step_handler(message, create_tasks2)



bot.polling(none_stop=True)