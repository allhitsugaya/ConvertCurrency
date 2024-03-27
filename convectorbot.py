import telebot
from telebot import types
from currency_converter import CurrencyConverter

bot = telebot.TeleBot('YOUR_TOKEN')
currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Вітаю, я бот для конвертації валюти!')
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount 
    try:
        amount = int(message.text.strip())
        if amount > 0:
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
            btn0 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
            btn1 = types.InlineKeyboardButton('GBP/USD', callback_data='gbp/usd')
            btn2 = types.InlineKeyboardButton('Інше значення', callback_data='else')
            markup.add(btn, btn0, btn1, btn2)
            bot.send_message(message.chat.id, 'Оберіть пару валют!', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Введіть значення неменше 0!')
            bot.register_next_step_handler(message, summa)
    except ValueError:
        bot.send_message(message.chat.id, 'Введіть коректне значення!')
        bot.register_next_step_handler(message, summa)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f"Виходить: {round(res,2)}.Можете знову ввести сумму!")
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Введіть пару значень через /')
        bot.register_next_step_handler(call.message, mycurrency)

def mycurrency(call):
    try:
        values = call.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.chat.id, f"Виходить: {round(res,2)}.Можете знову ввести сумму!")
        bot.register_next_step_handler(call, summa)
    except Exception:
        bot.send_message(call.chat.id, f"Щось пішло не так(((")
        bot.register_next_step_handler(call, summa)

bot.polling(none_stop=True)
