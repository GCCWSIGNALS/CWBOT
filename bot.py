import logging
import traceback
import os
import sys
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Telegram API token
TELEGRAM_API_TOKEN = "YOUR_TELEGRAM_API_TOKEN"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

lock_file = "/tmp/bot.lock"

def start(update: Update, _: CallbackContext):
    try:
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
    except Exception as e:
        logging.error("An error occurred during start handler: %s", traceback.format_exc())

def button_click(update: Update, _: CallbackContext):
    try:
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
    except Exception as e:
        logging.error("An error occurred during button_click handler: %s", traceback.format_exc())

def unknown(update: Update, _: CallbackContext):
    try:
        update.message.reply_text(
            "I'm sorry, I don't understand that command. Please choose one of the options below:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Price Plan", callback_data='price_plan')],
                                              [InlineKeyboardButton("Our Services", callback_data='services')],
                                              [InlineKeyboardButton("Our Signals", callback_data='signals')]])
        )
    except Exception as e:
        logging.error("An error occurred during unknown handler: %s", traceback.format_exc())

def main():
    try:
        # Print the token to the console for debugging purposes
        print(f"Token: {TELEGRAM_API_TOKEN}")

        updater = Updater(token=TELEGRAM_API_TOKEN, use_context=True)
        dispatcher = updater.dispatcher

        # Add handlers
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(MessageHandler(Filters.command, unknown))
        dispatcher.add_handler(CallbackQueryHandler(button_click))

        # Start long polling
        updater.start_polling()

    except Exception as e:
        logging.error("An error occurred during bot execution: %s", traceback.format_exc())

if __name__ == "__main__":
    if os.path.isfile(lock_file):
        print(f"Lock file {lock_file} exists, bot is already running. Exiting...")
        sys.exit()
    # Create lock file
    with open(lock_file, 'w') as file:
        file.write("lock")
    try:
        main()
    finally:
        # Make sure we delete the lock file
        os.remove(lock_file)
