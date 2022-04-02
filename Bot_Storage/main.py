import config
from telebot import telebot, types
from files import *


bot = telebot.TeleBot(config.telegram_token)


@bot.message_handler(commands=['start'])
def start(message):
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_delete = types.KeyboardButton('Удалить файл')
    button_get = types.KeyboardButton('Получить файл')
    menu.add(button_delete, button_get)
    msg = f'Привет, {message.from_user.first_name}!\n' \
          f'Я бот, который умеет хранить разные файлы и возвращать их когда это необходимо.'
    bot.send_message(message.chat.id, msg, reply_markup=menu)


@bot.message_handler(content_types=['document'])
def document(message):
    try:
        file = File(message.document.file_id, message.document.file_name, message.caption)
        bot.send_message(message.chat.id, file.add_file(message.chat.id))
    except ValueError:
        bot.send_message(message.chat.id, 'Файл с таким названием нельзя загрузить.')


@bot.message_handler(content_types=['photo', 'audio', 'video'])
def photo(message):
    bot.send_message(message.chat.id, 'Лучше отправьте Ваше фото/аудио/видео как файл')


@bot.message_handler(content_types=['text'])
def text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Ещё раз привет! Приятно познакомиться.')

    elif message.text.lower() == 'спасибо':
        bot.send_message(message.chat.id, 'Всегда пожалуйста!')

    elif message.text == 'Удалить файл' or message.text == 'Получить файл':
        files_list = File.get_files_list(message.chat.id)
        files_menu = types.InlineKeyboardMarkup()
        for file in files_list:
            file_button = types.InlineKeyboardButton(text=Class(file).title, callback_data=str(files_list.index(file)))
            files_menu.add(file_button)
        cancel_button = types.InlineKeyboardButton(text='Отмена', callback_data='cancel')
        files_menu.add(cancel_button)
        if not files_list:
            bot.send_message(message.chat.id, 'В Вашем хранилище пока нет ни одного файла.')
        elif message.text == 'Удалить файл':
            bot.send_message(message.chat.id, text='Выберите файл, который хотите удалить.', reply_markup=files_menu)
        else:
            bot.send_message(message.chat.id, text='Выберите файл, который хотите загрузить.', reply_markup=files_menu)

    else:
        msg = 'Извините, я пока ещё плохо понимаю Вас.\n' \
              'Если хотите удалить или получить файл, то выберите соответствующую кнопку меню.'
        bot.send_message(message.chat.id, msg)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'cancel':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    else:
        files_list = File.get_files_list(call.message.chat.id)
        file = files_list[int(call.data)]
        if call.message.text == 'Выберите файл, который хотите удалить.':
            bot.send_message(call.message.chat.id, Class(file).delete_file(call.message.chat.id))
        else:
            bot.send_document(call.message.chat.id, Class(file).get_file_id())
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


bot.polling(none_stop=True)
