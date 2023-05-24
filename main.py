import telebot, psycopg2, datetime
from telebot import types

token = "6066356979:AAFQPR7Rdy2YzkaHo0MrryWNqpVY5jx5WlA"

bot = telebot.TeleBot(token)

connection = psycopg2.connect(database="shedule_db",
                              user="postgres",
                              password="ph159753da",
                              host="localhost",
                              port="5432")
cursor = connection.cursor()

week = int(datetime.datetime.utcnow().isocalendar()[1]) % 2
if week == 0:
    next_week = 1
else:
    next_week = 0


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Расписание на текущую неделю",
                 "Расписание на следующую неделю")
    bot.send_message(message.chat.id, 'Бот с расписанием МТУСИ', reply_markup=keyboard)


@bot.message_handler(commands=['week'])
def week(message):
    bot.send_message(message.chat.id, f"Эта неделя {'четная' if week == 0 else 'нечетная'}")


@bot.message_handler(commands=['mtuci'])
def mtuci(message):
    bot.send_message(message.chat.id, 'https://mtuci.ru/')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'С помощью этого бота вы можете узнать расписание группы БВТ2203 на 2 семестр 1 курса\n\n'
                                      '/start - начать работу с ботом\n'
                                      '/week - узнать, какая неделя (четная/нечетная)\n'
                                      '/mtuci - ссылка на официальный сайт МТУСИ\n\n'
                                      'Введите день недели, чтобы узнать расписание на этот день текущей недели\n'
                                      'Введите Расписание на текущую неделю, чтобы узнать расписание на текущую неделю\n'
                                      'Введите Расписание на следующую неделю, чтобы узнать расписание на следующую неделю\n')


@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.text.lower() == 'понедельник':
        day_output("Понедельник", message, week)
    elif message.text.lower() == 'вторник':
        day_output("Вторник", message, week)
    elif message.text.lower() == 'среда':
        day_output("Среда", message, week)
    elif message.text.lower() == 'четверг':
        day_output("Четверг", message, week)
    elif message.text.lower() == 'пятница':
        day_output("Пятница", message, week)
    elif message.text.lower() == 'расписание на текущую неделю':
        bot.send_message(message.chat.id, f"Расписание на текущую неделю")
        bot.send_message(message.chat.id, '--------------------------------------------')
        week_output(week, message)
    elif message.text.lower() == 'расписание на следующую неделю':
        bot.send_message(message.chat.id, f"Расписание на следующую неделю")
        bot.send_message(message.chat.id, '--------------------------------------------')
        week_output(next_week, message)
    else:
        bot.send_message(message.chat.id, 'Извините, я Вас не понял')


def day_output(day, message, week):
    query = f"""select t.subject, t.room_numb, t.start_time, te.full_name 
        from timetable t, teacher te 
        where t.week = '{'Четная' if week == 0 else 'Нечетная'}' 
            and t.day = '{day}' 
            and t.subject = te.subject
        order by t.id"""
    cursor.execute(query)
    array = cursor.fetchall()
    print(array)
    bot.send_message(message.chat.id, day)
    bot.send_message(message.chat.id, '--------------------------------------------')
    if array:
        for i in array:
            line = i[0] + "  " + i[1] + "  " + i[2] + "  " + i[3]
            bot.send_message(message.chat.id, line)
    else:
        bot.send_message(message.chat.id, 'В этот день пар нет')
    bot.send_message(message.chat.id, "--------------------------------------------")


def week_output(thisWeek, message):
    day_output("Понедельник", message, thisWeek)
    day_output("Вторник", message, thisWeek)
    day_output("Среда", message, thisWeek)
    day_output("Четверг", message, thisWeek)
    day_output("Пятница", message, thisWeek)


bot.polling(none_stop=True, interval=0)
