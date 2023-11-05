#!/usr/bin/env python3
import lib.handler as handler
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from telegram import Update, User
import lib.globals as g

def main():
    # Create handler
    command_handler = handler.RequestHandler(openai_api_key=g.OPENAI_API_KEY)

    # Start a telegram bot
    updater = Updater(g.TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Create handlers
    start_handler = CommandHandler('start', command_handler.start_command_handler)
    help_handler = CommandHandler('help', command_handler.help_command_handler)
    picgen_handler = CommandHandler('picgen', command_handler.picgen_command_handler)
    variation_handler = CommandHandler('variation', command_handler.variation_command_handler)
    describe_handler = CommandHandler('describe', command_handler.description_command_handler)
    rephrase_handler = CommandHandler('rephrase', command_handler.rephrase_command_handler)
    unknown_handler = MessageHandler(Filters.command, command_handler.unknown_command_handler)

    # Add handlers to dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(picgen_handler)
    dispatcher.add_handler(variation_handler)
    dispatcher.add_handler(describe_handler)
    dispatcher.add_handler(rephrase_handler)
    dispatcher.add_handler(unknown_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    main()