# t.me/Learn_Python01_Mega_Bot
#from pprint import pprint
import logging
from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler ,Filters
import settings
from base_city import dict_base_city
import random

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log',
                    encoding='utf-8') # логирование ошибок

def greet_user(update, context):
    print('Вызван /start')
    print(update)
    update.message.reply_text('Добро пожаловать в Learn_Python01_Mega_Bot!')

def talk_to_me(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)

def Bot_reply_city(city, id, context):# узнаем на какую букву нужен Город и выбираем его
    symbol = city[-1].lower()

    if symbol.lower() in ('ь','ъ','ы'): # на эти буквы городов нет
        symbol = city[-2]
    symbol_2 = symbol #второй символ для И=Й или Е=Ё
    if symbol.lower() == 'и':
        symbol_2 = 'й'
    if symbol.lower() == 'е':
        symbol_2 = 'ё'

    list_symbol_city = []
    for town, town_up in context.user_data['city'].items(): # Создаем список городов начинающихся на посл. букву города пользователя
        if town[0] == symbol or town[0] == symbol_2:
            list_symbol_city.append(town_up)
    town_bot = random.choice(list_symbol_city) # выбор Бота
    print(f'Bot city: {town_bot}')
    return({id: [town_bot.lower(), town_bot]}) # Возвращаем Dict {id:city.lower(), city}

def del_city_list(city, id, context):
    try:
        city_up = context.user_data['city'].pop(city.lower())
        print(f'Delet city {city_up} is dict.\nCount citys: {len(context.user_data["city"])}')
    except KeyError:
        print(f'KeyError def del_city_list({city}, {id})')

def corret_write_city_user_data(city,context):
    if not context.user_data['city'].get(city.lower()) is None:
        return True
    else:
        print('corret_write_city_user_data: False')
        return False

def corret_first_end_symbol(word_user, word_bot):
    if word_bot[-1] in ('ь','ъ','ы') and word_user[0].lower() == word_bot[-2].lower(): # на эти буквы городов нет
        return True
    elif word_bot[-1] in ('и','й') and word_user[0].lower() in ('и','й'): # буквы равны
        return True
    elif word_bot[-1] in ('е', 'ё') and word_user[0].lower() in ('е', 'ё'): # буквы равны
        return True
    elif word_user[0].lower() == word_bot[-1].lower():
        return True
    else:
        return False

def first_symbol(word_bot):
    if word_bot[-1] in ('ь','ъ','ы'): # на эти буквы городов нет
        return word_bot[-2]
    if word_bot[-1] in ('и','й'): # на эти буквы равны
        return ('"и" или "й"')
    if word_bot[-1] in ('е', 'ё'): # на эти буквы равны
        return ('"е" или "ё"')
    return word_bot[-1]

def game_city(update,context):
    '''
    Уровень 3
        Научите бота играть в города.
        Правила такие:
        - внутри бота есть список городов,
        - пользователь пишет /cities Москва и если в списке такой город есть, бот отвечает городом на букву "а" - "Альметьевск, ваш ход".
        Оба города должны удаляться из списка.
        Помните, с ботом могут играть несколько пользователей одновременно
    '''
    logging.info(f'{datetime.now()} Вызов команды /wordcount')
    if update.message.text.strip() == '/cities': # При вводе просто команды /cities выводим правила игры.
        update.message.reply_text(f'ПАВИЛА ИГРЫ В ГОРОДА:\nБуква И = Й, Е = Ё.\nЕсли город закачиватеься на "ь","ъ","ы"\
            тогда город должен начинаться на 2 букву с конца.\n Команда: "/cities restart" запускает игру заного!\n\
            Начать играть: "/cities Название_Города" например: "/cities Москва".')
        return
    city = context.args[0]
    chat_id = update.message.chat.id
    print(city)

    if city.lower() == 'restart':
        if len(context.user_data) != 0:
            context.user_data.clear()
            update.message.reply_text('Restart! Ваш ход...')
            return
        else:
            update.message.reply_text('Restart? Вы еще даже не начали играть). Ваш ход...')
            return

    if context.user_data.get(chat_id):
        city_bot = context.user_data[chat_id][0] # Берем city.lower
        city_bot_up = context.user_data[chat_id][1] # Берем city origenal
        if corret_first_end_symbol(city, city_bot):
            correct_city = corret_write_city_user_data(city,context)
            if correct_city:
                del_city_list(city, chat_id, context) # Убираем город пользователя
                context.user_data.update(Bot_reply_city(city, chat_id, context)) # Выбор Бота. {'chat_id':[city.lower, city]}
                city_bot, city_bot_up = context.user_data[chat_id]
                del_city_list(city_bot, chat_id, context) # Убираем город Бота
                update.message.reply_text(f'{city_bot_up}, ваш ход') # Отвечаем пользователю
                return
            else:
                update.message.reply_text('Такого города нет, попробуйте еще раз!')
                print('Такого города нет, попробуйте еще раз!')
                return
        else:
            end_symbol_bot = first_symbol(city_bot)
            update.message.reply_text(f'Город должен начинаться с буквы: {end_symbol_bot}')
            print(f'Город должен начинаться с буквы: {end_symbol_bot}')
            return

    else:
        if city.lower() in dict_base_city:
            update.message.reply_text(f'Повторить ПАВИЛА ИГРЫ В ГОРОДА никогда не лишне:\nБуква И = Й, Е = Ё.\nЕсли город \
            закачиватеься на "ь","ъ","ы" тогда город должен начинаться на 2 букву с конца.\n Команда: "/cities restart"\
            запускает игру заного!\nНачать играть: "/cities Название_Города" например: "/cities Москва".')
            citys = dict_base_city.copy()
            context.user_data.update({'city':citys})
            del_city_list(city, chat_id, context) # Убираем город пользователя
            context.user_data.update(Bot_reply_city(city, chat_id, context)) # Выбор Бота. в context.user_data должен поподать {'chat_id':[city.lower, city]}
            city_bot, city_bot_up = context.user_data[chat_id]
            del_city_list(city_bot, chat_id, context) # Убираем город Бота
            update.message.reply_text(f'{city_bot_up}, ваш ход') # Отвечаем пользователю
            return
        else:
            update.message.reply_text('Такого города нет, попробуйте еще раз!')
            return

def main():
    mybot = Updater(settings.API_KEY) # Создаем бота и передаем ему ключ для авторизации на серверах Telegram

    dp = mybot.dispatcher #Диспечер
    dp.add_handler(CommandHandler('start', greet_user)) # Добавил к диспечеру обработчик команд, который реагирует на команду /start и вызывает функц. greet_user
    dp.add_handler(CommandHandler('cities', game_city)) # Добавил к диспечеру обработчик команд ...
    dp.add_handler(MessageHandler(Filters.text, talk_to_me)) # Добавил к диспечеру обработчик команд, укажем, что мы хотим реагировать только на текстовые сообщения

    logging.info(f'{datetime.now()} Start Learn_Python01_Mega_Bot')
    mybot.start_polling() # Командуем боту начать ходить в Telegram за сообщениями
    mybot.idle() # Запускаем бота, он будет работать, пока мы его не остановим принудительно

if __name__ == '__main__':
    main()
