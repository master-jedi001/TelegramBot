import telebot
import config
import random


class Game:
    games = dict()

    def __init__(self, chat_id):
        self.bot_number = random.randint(1, 100)
        self.attempts = 7
        Game.games[chat_id] = self

    def gameplay(self, message):
        if not message.text.isdigit():
            bot.send_message(message.chat.id, 'Нужно вводить только целые положительные числа. Попробуй ещё раз.')
            bot.register_next_step_handler(message, self.gameplay)

        elif self.attempts > 0:
            if int(message.text) > self.bot_number:
                self.attempts -= 1
                bot.send_message(message.chat.id, f'Задуманное число меньше. Осталось попыток: {self.attempts}')
                bot.register_next_step_handler(message, self.gameplay)

            elif int(message.text) < self.bot_number:
                self.attempts -= 1
                bot.send_message(message.chat.id, f'Задуманное число больше. Осталось попыток: {self.attempts}')
                bot.register_next_step_handler(message, self.gameplay)

            else:
                bot.send_message(message.chat.id, 'Мои поздравления! Ты отгадал задуманное мной число!')
        else:
            bot.send_message(message.chat.id, 'К сожалению, все попытки закончились. Ты проиграл!')


bot = telebot.TeleBot(config.telegram_token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, мой друг!')


@bot.message_handler(commands=['game'])
def play(message):
    Game(message.chat.id)
    bot.send_message(message.chat.id, 'Я загадал целое число от 1 до 100, а ты должен его отгадать.')
    bot.send_message(message.chat.id, f'Количество оставшихся попыток: {Game.games[message.chat.id].attempts}')
    bot.register_next_step_handler(message, Game.games[message.chat.id].gameplay)


@bot.message_handler(content_types=['text'])
def text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Ещё раз привет!')
    else:
        bot.send_message(message.chat.id, 'Я только учусь и пока ещё не понимаю тебя.')
        bot.send_message(message.chat.id, 'Но мы можем сыграть в игру. Для этого напиши: /game')


bot.polling(none_stop=True)
