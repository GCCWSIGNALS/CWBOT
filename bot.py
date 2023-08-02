import logging
import os
import sys
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Telegram API token
TELEGRAM_API_TOKEN = os.environ.get("6488455720:AAHbpah1B1P9hhWnAfpHilvCm1Y3Wdk7lwA")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

# Lock file path
lock_file = "/tmp/bot.lock"

def start(update: Update, _: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Price Plan", callback_data='price_plan')],
        [InlineKeyboardButton("Our Services", callback_data='services')],
        [InlineKeyboardButton("Our Signals", callback_data='signals')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "Welcome to Our Friendly Bot! 😊\n\n"
        "I'm here to assist you with our services and signals.\n\n"
        "Please choose an option below:",
        reply_markup=reply_markup
    )

def button_click(update: Update, _: CallbackContext):
    query = update.callback_query
    option = query.data

    if option == 'price_plan':
        query.edit_message_text(
            "Our Price Plan:\n\n"
            "🌟 7-day free trial\n"
            "🌟 After the free trial, the subscription is £34.99/month.\n\n"
            "Subscribe now to get started!"
        )
    elif option == 'services':
        query.edit_message_text(
            "Our Services:\n\n"
            "🔹 Live Trading Sessions\n"
            "🔹 VIP Forex & Gold Signals\n"
            "🔹 Supportive and Helpful Active Community\n\n"
            "Join us now and enjoy our premium services!"
        )
    elif option == 'signals':
        query.edit_message_text(
            "Our Signals:\n\n"
            "🔹 Buy/Sell Signals with Entry and Exit Prices\n"
            "🔹 Take Profit (TP) and Stop Loss (SL) Levels\n"
            "🔹 Copy the signals and follow our expert analysis\n\n"
            "Start making profitable trades with our signals!"
        )

def unknown(update: Update, _: CallbackContext):
    update.message.reply_text(
        "I'm sorry, I don't understand that command. Please choose one of the options below:",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Price Plan", callback_data='price_plan')],
                                          [InlineKeyboardButton("Our Services", callback_data='services')],
                                          [InlineKeyboardButton("Our Signals", callback_data='signals')]])
    )

def error_handler(update: Update, context: CallbackContext):
    """Log the error and send a telegram message to notify the developer."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    update.effective_message.reply_text("An error occurred while processing your update.")

def main():
    # Check if lock file exists
    if os.path.exists(lock_file):
        logger.error("Lock file exists. Make sure that only one bot instance is running.")
        return

    # Create lock file
    with open(lock_file, 'w') as file:
        file.write("")

    # Create the Updater and pass it your bot's token.
    updater = Updater(TELEGRAM_API_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_handler(CallbackQueryHandler(button_click))

    # Log all errors
    dispatcher.add_error_handler(error_handler)

    # Start the Bot
    updater.start_polling()

    # Block until you manually stop the bot
    updater.idle()

    # Delete lock file
    os.remove(lock_file)

if __name__ == '__main__':
    main()
