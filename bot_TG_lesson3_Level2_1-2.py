# t.me/Learn_Python01_Mega_Bot
#from pprint import pprint
import logging
from datetime import datetime
import ephem
from telegram.ext import Updater, CommandHandler, MessageHandler ,Filters
import settings

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

def wordcount(update,context):
    '''
    Уровень 2
        Реализуйте в боте команду /wordcount которая считает слова в присланной фразе.
        Например на запрос /wordcount Привет как дела бот должен ответить: 3 слова.
        Не забудьте:
        Добавить проверки на пустую строку
        Как можно обмануть бота, какие еще проверки нужны?
    '''
    logging.info('Вызов команды /wordcount')
    text = update.message.text.replace('/wordcount', '').strip().split()
    count_word = 0
    for slovo in text:
        if not(len(slovo) == 1 and slovo.isalnum() == False):
            count_word += 1
    update.message.reply_text(f'{count_word} слов(а)')

def next_full_moon(update, context):
    '''
    Уровень 2
        Реализуйте в боте команду, которая отвечает на вопрос “Когда ближайшее полнолуние?”
        Например /next_full_moon 2019-01-01
        Чтобы узнать, когда ближайшее полнолуние, используйте ephem.next_full_moon(ДАТА)
    '''
    logging.info('Вызов команды /next_full_moon')
    data = update.message.text.replace('/next_full_moon', '').strip()
    if data == '':
        data = datetime.today()
        data_next_full_moon = ephem.next_full_moon(data)
        update.message.reply_text(data_next_full_moon)
    else:
        try:
            data = datetime.strptime(data, "%Y-%m-%d")
            data_next_full_moon = ephem.next_full_moon(data)
            update.message.reply_text(data_next_full_moon)
        except ValueError:
            update.message.reply_text("Вы ввели не коректный формат! Необходимо ввобдить в формате '/next_full_moon 2019-01-01'")

def main():
    mybot = Updater(settings.API_KEY) # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    #mybot = Updater(settings.API_KEY, request_kwargs = PROXY) # Создаем бота и передаем ему ключ для авторизации на серверах Telegram + Proxy

    dp = mybot.dispatcher #Диспечер
    dp.add_handler(CommandHandler('start', greet_user)) # Добавил к диспечеру обработчик команд, который реагирует на команду /start и вызывает функц. greet_user
    dp.add_handler(CommandHandler('wordcount', wordcount)) # Добавил к диспечеру обработчик команд ...
    dp.add_handler(CommandHandler('next_full_moon', next_full_moon)) # Добавил к диспечеру обработчик команд ...
    dp.add_handler(MessageHandler(Filters.text, talk_to_me)) # Добавил к диспечеру обработчик команд, укажем, что мы хотим реагировать только на текстовые сообщения

    logging.info('Start Learn_Python01_Mega_Bot')
    mybot.start_polling() # Командуем боту начать ходить в Telegram за сообщениями
    mybot.idle() # Запускаем бота, он будет работать, пока мы его не остановим принудительно

if __name__ == '__main__':
    main()
