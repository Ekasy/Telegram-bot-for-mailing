import telebot


class Bot:
    bot = None

    def __init__(self, token_, proxy_):
        telebot.apihelper.proxy = {'https': proxy_}
        self.bot = telebot.TeleBot(token=token_)

    def get_bot_name(self):
        try:
            return self.bot.get_me().first_name
        except:
            return 'not exist'

    def send_message(self, chat_id, message):
        self.bot.send_message(chat_id, message)
