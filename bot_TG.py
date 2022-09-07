
# t.me/Learn_Python01_Mega_Bot
#from pprint import pprint
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler ,Filters
import settings

logging.basicConfig(filename='bot.log', level=logging.INFO) # логирование ошибок

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def greet_user(update, context):
    print('Вызван /start')
    print(update)
    update.message.reply_text('Добро пожаловать в Learn_Python01_Mega_Bot!')

def talk_to_me(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)

def main():
    mybot = Updater(settings.API_KEY) # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    #mybot = Updater(settings.API_KEY, request_kwargs = PROXY) # Создаем бота и передаем ему ключ для авторизации на серверах Telegram + Proxy

    dp = mybot.dispatcher #Диспечер
    dp.add_handler(CommandHandler('start', greet_user)) # Добавил к диспечеру обработчик команд, который реагирует на команду /start и вызывает функц. greet_user
    dp.add_handler(MessageHandler(Filters.text, talk_to_me)) # Добавил к диспечеру обработчик команд, укажем, что мы хотим реагировать только на текстовые сообщения

    logging.info('Start Learn_Python01_Mega_Bot')
    mybot.start_polling() # Командуем боту начать ходить в Telegram за сообщениями
    mybot.idle() # Запускаем бота, он будет работать, пока мы его не остановим принудительно

if __name__ == '__main__':
    main()
