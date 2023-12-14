import telebot
from stress import *

TOKEN = '6678312127:AAE_UgNnbmEvys2XAObJ8RpRCRle0ej0xYo'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет, я бот, который поможет расставить ударения, скинь мне файл с текстом")


@bot.message_handler(content_types=['document'])
def handle_text(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    filename = message.document.file_name

    with open(filename, 'wb') as f:
        f.write(downloaded_file)

    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

    res, not_decided = accentuate(text, wordforms, lemmas)
    output_filename = filename.split('.')[0] + '_stressed.txt'

    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(res)

    with open(output_filename, 'rb') as f:
        bot.send_document(message.chat.id, f, caption='Вот твой текст с ударениями')

    with open('not_decided.txt', 'w') as f:
        f.write('\n'.join(not_decided))

    with open('not_decided.txt', 'rb') as f:
        bot.send_document(message.chat.id, f, caption='Вот слова, в которых не удалось расставить ударения')


bot.infinity_polling()
