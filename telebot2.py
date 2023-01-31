import telebot
from config import keys, TOKEN
from extensions import ConvertException, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message):
    text = '''Чтобы начать работу введите команду боту в следующем формате:
    \n<имя валюты> 
    \n <в какую валюту перевести> 
    \n <количество переводимой валюты> 
    \n <Чтобы увидеть доступные валюты введите /value'''
    if message.text == '/help':
        bot.reply_to(message, text)
    elif message.text == '/start':
        bot.send_message(message.chat.id, 'Привет, это небольшой конвертер валют. Чтобы узнать как он работает введите /help')

@bot.message_handler(commands=['value'])
def value(message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        value = message.text.split(' ')

        if len(value) != 3:
            raise ConvertException(f'Слишком много параметров.')

        quote, base, amount = value
        a = APIException.convert(quote, base, amount)
    except ConvertException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {a}'
        bot.send_message(message.chat.id, text)

bot.polling()