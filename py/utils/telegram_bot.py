from subprocess import run

from py.utils import code_secrets
from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)


def process_msg(update: Update, context: CallbackContext):
    msg = update.message.text  # type: str
    msg_from = update.message.from_user.id
    run(
        [
            "/home/ubuntu/venv/bin/python",
            "/home/ubuntu/py/utils/telegram_bot_hot_update.py",
            "--user",
            str(msg_from),
            "--msg",
            str(msg),
        ]
    )


updater = Updater(code_secrets.TELEGRAM)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text, process_msg))
updater.start_polling()

# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()
