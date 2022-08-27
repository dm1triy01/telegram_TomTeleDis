import logging
import os
import subprocess

from telegram import Update, ReplyKeyboardMarkup
import telegram.ext
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler

import secret
import text

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    keyboard = [['Запустить', 'Остановить', 'Статус']]

    reply_markup = ReplyKeyboardMarkup(keyboard,
                                       one_time_keyboard=False,
                                       resize_keyboard=True)
    update.message.reply_text(text.start, reply_markup=reply_markup)


def start_dis(update: Update, context: CallbackContext):
    res = subprocess.run(["systemctl", "start", "tom_discord.service"])
    if res.returncode == 0:
        update.message.reply_text("Бот запущен")
    else:
        update.message.reply_text("❌Ошибка")


def stop_dis(update: Update, context: CallbackContext):
    subprocess.run(["systemctl", "stop", "tom_discord.service"])
    update.message.reply_text("Бот остановлен")


def status_dis(update: Update, context: CallbackContext):
    res = subprocess.run(["systemctl", "is-active", "tom_discord.service"], stdout=subprocess.PIPE, text=True)
    print(res.returncode)
    if res.returncode == 0:
        update.message.reply_text("🟢Активен")
    else:
        update.message.reply_text("🔴Выключен")


def main():
    updater = Updater(secret.secret_key, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(start_dis, pattern='UwU'))
    dispatcher.add_handler(CallbackQueryHandler(stop_dis, pattern='UwU'))
    dispatcher.add_handler(CallbackQueryHandler(status_dis, pattern='UwU'))
    dispatcher.add_handler(MessageHandler(Filters.regex(r"^Запустить$"), start_dis))
    dispatcher.add_handler(MessageHandler(Filters.regex(r"^Остановить$"), stop_dis))
    dispatcher.add_handler(MessageHandler(Filters.regex(r"^Статус$"), status_dis))

    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
