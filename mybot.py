import telebot
import config
import sys


token = sys.argv[1]
config.PATH_TO_DB = sys.argv[2]
proxy = sys.argv[3]
telebot.apihelper.proxy = {'https': proxy}
bot = telebot.TeleBot(token)

import bot_dbase


@bot.message_handler(commands=['start'])
def greetings(message):
    config.state = 0
    bot.send_message(message.chat.id, bot_dbase.get_column(token=token, column='greetings'))
    bot_dbase.init_db()
    bot_dbase.insert_id_into_table(token=token, chat_id=int(message.chat.id))
    bot_dbase.update_user_state(token=token, chat_id=int(message.chat.id), user_state=int(config.state))


@bot.message_handler(content_types=['text'])
def talking(message):
    if not bot_dbase.user_is_exist(token=token, chat_id=message.chat.id):
        bot.send_message(message.chat.id, bot_dbase.get_column(token=token, column='advice'))
    elif bot_dbase.get_state_by_chat_id(token=token, chat_id=int(message.chat.id)) == 0:
        res = bot_dbase.update_user_id(token=token, chat_id=int(message.chat.id), user_id=str(message.text))
        if res == 'replaced' or res == 'your':
            config.state = 1
            bot_dbase.update_user_state(token=token, chat_id=int(message.chat.id), user_state=int(config.state))
            bot.send_message(message.chat.id, bot_dbase.get_column(token=token, column='approval'))
        else:
            bot.send_message(message.chat.id, bot_dbase.get_column(token=token, column='change_name'))
    elif message.text == '3' and bot_dbase.get_state_by_chat_id(token=token, chat_id=int(message.chat.id)) == 1:
        bot.send_message(message.chat.id, bot_dbase.get_info())
    elif message.text.lower() == 'отписка' and \
            bot_dbase.get_state_by_chat_id(token=token, chat_id=int(message.chat.id)) == 1:
        bot_dbase.unsubscribe(token=token, chat_id=message.chat.id)
        bot.send_message(message.chat.id, bot_dbase.get_column(token=token, column='unsubscribe'))


bot.polling()
