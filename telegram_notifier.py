from telegram.ext import Updater

class TelegramNotifier:
    def __init__(self):
        self.client = Updater("2126958170:AAEj2G0a8j33aaPSgVydkqEQGlY4TTg5lHU")

    def send_message(self, msg):
        self.client.bot.send_message("-736146093", msg)
