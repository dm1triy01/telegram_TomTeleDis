import logging
import os

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
    keyboard = [['Запустить Тома', 'Остановить Тома']]

    reply_markup = ReplyKeyboardMarkup(keyboard,
                                       one_time_keyboard=False,
                                       resize_keyboard=True)
    update.message.reply_text(text.start, reply_markup=reply_markup)


def start_dis(update: Update, context: CallbackContext):
    comm = "systemctl start rut_bot.service"
    os.system(comm)
    update.message.reply_text(text.start_dis)


def stop_dis(update: Update, context: CallbackContext):
    comm = "systemctl stop rut_bot.service"
    os.system(comm)
    update.message.reply_text(text.stop_dis)


def main():
    updater = Updater(secret.secret_key, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(start_dis, pattern='UwU'))
    dispatcher.add_handler(CallbackQueryHandler(stop_dis, pattern='UwU'))
    dispatcher.add_handler(MessageHandler(Filters.regex(r"^Запустить Тома$"), start_dis))
    dispatcher.add_handler(MessageHandler(Filters.regex(r"^Остановить Тома$"), stop_dis))

    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
