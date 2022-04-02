import telebot
import config
import openweathermap as weather

bot = telebot.TeleBot(config.telegram_token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот, который по названию города находит его погоду.')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    language = message.from_user.language_code
    mess = weather.Weather(message.text).get(language)
    bot.send_message(message.chat.id, mess)


bot.polling(none_stop=True)
