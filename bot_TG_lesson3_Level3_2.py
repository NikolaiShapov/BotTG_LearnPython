
# t.me/Learn_Python01_Mega_Bot
#from pprint import pprint
import logging
from datetime import datetime
import ephem
from telegram.ext import Updater, CommandHandler, MessageHandler ,Filters
import settings
import random

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log',
                    encoding='utf-8') # логирование ошибок

# PROXY = {'proxy_url': settings.PROXY_URL,
#     'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def greet_user(update, context):
    print('Вызван /start')
    print(update)
    update.message.reply_text('Добро пожаловать в Learn_Python01_Mega_Bot!')

def talk_to_me(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)

def who_operator(expression):
    for sign in expression:
        if sign == '-':
            return sign
        elif sign == '+':
            return sign
        elif sign == '/':
            return sign
        elif sign == '*':
            return sign

def result_operator(exp_1, exp_2, operator):
    if operator == '-':
        return int(exp_1) - int(exp_2)
    elif operator == '+':
        return int(exp_1) + int(exp_2)
    elif operator == '/':
        try:
            res = int(exp_1) / int(exp_2)
            return res
        except ZeroDivisionError:
            return 'На ноль делить нельзя!'
    elif operator == '*':
        return int(exp_1) * int(exp_2)

def calc(update,context):
    '''
    Уровень 3
    На команду /calc 2-3, он должен ответить “-1”.
    Не забудьте обработать возможные ошибки во вводе: пробелы, отсутствие чисел, деление на ноль
    Подумайте, как можно сделать поддержку действий с тремя и более числами
    '''
    logging.info('Вызов команды /calc')
    expression = update.message.text.replace('/calc', '').strip()
    operator = who_operator(expression)
    print(operator)
    expression = expression.replace(' ','')
    expression = expression.replace('\n','')
    expression = expression.replace('\t','')
    if operator:
        exp_1, exp_2, *_temp = expression.split(operator)
        print(exp_1, exp_2, _temp)
        if exp_1.isdigit() and exp_2.isdigit():
            result = result_operator(exp_1, exp_2, operator)
            update.message.reply_text(result)
        else:
            update.message.reply_text('Нужно вводить только числа!')
    else:
        update.message.reply_text('Это не математическое выражение!')


'''
    Подумайте, как можно сделать поддержку действий с тремя и более числами
'''
def mat_to_text(update,context): # записывает выражение в лист например ['1', '-', '2', '+', '3']
    logging.info('Вызвана команда /calc_v1')
    text = update.message.text.replace('/calc_v1', '').strip()
    list_point = []
    number = ''
    for item in text+' ': # добавляем в конец пробел для увеличения прохода цикла +1
        if item.isdigit(): #если чсло, то
            number += item # складываем в одно значение
        elif item in ['-', '+', '*', '/']: #если знак матиматического выражения, то
            if number.isdigit(): #если до это в number лежит число, то
                list_point.append(number) #его тоже добавляем в список
                number = '' #обнуляем
            list_point.append(item) #добавляем в список
        elif not item.isdigit() and number: # если не число но в number лежит что то, то
            list_point.append(number)
            number = ''
        elif not item.isdigit() and not item in ['-', '+', '*', '/', ' ']:
            return update.message.reply_text('Не наша история!')
    print(list_point)
    result = mat_result(list_point)
    update.message.reply_text(result)
    # update.message.reply_text(list_point)

def mat_result(list_mat):
    print(list_mat)
    if len(list_mat) == 1:
        return list_mat[0]
    for index, operator in enumerate(list_mat, start=0):
        if operator in ['*', '/']:
            if operator in ['*']:
                run = int(list_mat[index - 1]) * int(list_mat[index + 1])
                list_mat1 = list_mat[:index - 1] + [run] + list_mat [index +2:]
                return mat_result(list_mat1)
            else:
                try:
                    run = int(list_mat[index - 1]) / int(list_mat[index + 1])
                    list_mat1 = list_mat[:index - 1] + [run] + list_mat [index +2:]
                    return mat_result(list_mat1)
                except ZeroDivisionError:
                    return 'На ноль делить не надо!'
    for index, operator in enumerate(list_mat, start=0):
        if operator in ['-', '+']:
            if operator in['-']:
                run = int(list_mat[index - 1]) - int(list_mat[index + 1])
                list_mat1 = list_mat[:index - 1] + [run] + list_mat [index +2:]
                return mat_result(list_mat1)
            else:
                run = int(list_mat[index - 1]) + int(list_mat[index + 1])
                list_mat1 = list_mat[:index - 1] + [run] + list_mat [index +2:]
                return mat_result(list_mat1)

def mat_to_text2(update,context): # записывает выражение в лист например ['1', '-', '2', '+', '3']
    logging.info('Вызвана команда /calc_v2')
    text = update.message.text.replace('/calc_v2', '').strip()
    list_point = []
    number = ''
    for item in text+' ': # добавляем в конец пробел для увеличения прохода цикла +1
        if item.isdigit(): #если чсло, то
            number += item # складываем в одно значение
        elif item in ['-', '+', '*', '/']: #если знак матиматического выражения, то
            if number.isdigit(): #если до это в number лежит число, то
                list_point.append(number) #его тоже добавляем в список
                number = '' #обнуляем
            list_point.append(item) #добавляем в список
        elif not item.isdigit() and number: # если не число но в number лежит что то, то
            list_point.append(number)
            number = ''
        elif not item.isdigit() and not item in ['-', '+', '*', '/', ' ']:
            return update.message.reply_text('Не наша история!')
    print(list_point)
    result = mat_result_2(list_point)
    update.message.reply_text(result)

def mat_result_2(list_mat):
    while True:
        if len(list_mat) == 1:
            return list_mat[0]
        for index, operator in enumerate(list_mat, start=0):
            if operator in ['*', '/']:
                if operator in ['*']:
                    run = int(list_mat[index - 1]) * int(list_mat[index + 1])
                    list_mat = list_mat[:index - 1] + [run] + list_mat [index +2:]
                    break
                else:
                    try:
                        run = int(list_mat[index - 1]) / int(list_mat[index + 1])
                        list_mat = list_mat[:index - 1] + [run] + list_mat [index +2:]
                        break
                    except ZeroDivisionError:
                        return 'На ноль делить не надо!'
        if list_mat.count('*') == 0 and list_mat.count('/') == 0:
            break
    while True:
        if len(list_mat) == 1:
            return list_mat[0]
        for index, operator in enumerate(list_mat, start=0):
            if operator in ['-', '+']:
                if operator in['-']:
                    run = int(list_mat[index - 1]) - int(list_mat[index + 1])
                    list_mat = list_mat[:index - 1] + [run] + list_mat [index +2:]
                    break
                else:
                    run = int(list_mat[index - 1]) + int(list_mat[index + 1])
                    list_mat = list_mat[:index - 1] + [run] + list_mat [index +2:]
                    break


def main():
    mybot = Updater(settings.API_KEY) # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    #mybot = Updater(settings.API_KEY, request_kwargs = PROXY) # Создаем бота и передаем ему ключ для авторизации на серверах Telegram + Proxy

    dp = mybot.dispatcher #Диспечер
    dp.add_handler(CommandHandler('start', greet_user)) # Добавил к диспечеру обработчик команд, который реагирует на команду /start и вызывает функц. greet_user
    dp.add_handler(CommandHandler('calc', calc)) # Добавил к диспечеру обработчик команд ...
    dp.add_handler(CommandHandler('calc_v1', mat_to_text)) # Добавил к диспечеру обработчик команд ...
    dp.add_handler(CommandHandler('calc_v2', mat_to_text2)) # Добавил к диспечеру обработчик команд ...
    dp.add_handler(MessageHandler(Filters.text, talk_to_me)) # Добавил к диспечеру обработчик команд, укажем, что мы хотим реагировать только на текстовые сообщения

    logging.info('Start Learn_Python01_Mega_Bot')
    mybot.start_polling() # Командуем боту начать ходить в Telegram за сообщениями
    mybot.idle() # Запускаем бота, он будет работать, пока мы его не остановим принудительно

if __name__ == '__main__':
    main()
 # /calc_v1 1-2*4/8+5
 # /calc_v1 1-2+3*98
 # /calc_v1 1-2+3/8
 # /calc_v1 1-2+3/0
 # /calc_v1 1-2+3aa *  32
 # /calc_v1 1-2+3 / 13 - ыва

  # /calc_v2 1-2*4/8+5
 # /calc_v2 1-2+3*98
 # /calc_v2 1-2+3/8
 # /calc_v2 1-2+3/0
 # /calc_v2 1-2+3aa *  32
 # /calc_v2 1-2+3 / 13 - ыва
