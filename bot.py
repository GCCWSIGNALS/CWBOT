import logging
import traceback
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, Dispatcher
from flask import Flask, request
import os

# Telegram API token
TELEGRAM_API_TOKEN = "6488455720:AAHbpah1B1P9hhWnAfpHilvCm1Y3Wdk7lwA"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Flask app
app = Flask(__name__)

@app.route("/" + TELEGRAM_API_TOKEN, methods=["POST"])
def update():
    dispatcher.process_update(Update.de_json(request.get_json(force=True), bot))
    return "ok"

@app.route("/set_webhook", methods=["GET", "POST"])
def set_webhook():
    s = bot.set_webhook("https://cwbot.onrender.com/{}".format(TELEGRAM_API_TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route("/")
def index():
    return "."

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

        join_button = [InlineKeyboardButton("Join", url='https://t.me/GC_CW1')]

        if option == 'price_plan':
            keyboard = [
                [InlineKeyboardButton("Price Plan", callback_data='price_plan')],
                [InlineKeyboardButton("Our Services", callback_data='services')],
                [InlineKeyboardButton("Our Signals", callback_data='signals')],
                join_button
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                "Our Price Plan:\n\n"
                "🌟 7-day free trial\n"
                "🌟 After the free trial, the subscription is £34.99/month.\n\n"
                "Subscribe now to get started!",
                reply_markup=reply_markup
            )
        elif option == 'services':
            keyboard = [
                [InlineKeyboardButton("Price Plan", callback_data='price_plan')],
                [InlineKeyboardButton("Our Services", callback_data='services')],
                [InlineKeyboardButton("Our Signals", callback_data='signals')],
                join_button
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                "Our Services:\n\n"
                "🔹 Live Trading Sessions\n"
                "🔹 VIP Forex & Gold Signals\n"
                "🔹 Supportive and Helpful Active Community\n\n"
                "Join us now and enjoy our premium services!",
                reply_markup=reply_markup
            )
        elif option == 'signals':
            keyboard = [
                [InlineKeyboardButton("Price Plan", callback_data='price_plan')],
                [InlineKeyboardButton("Our Services", callback_data='services')],
                [InlineKeyboardButton("Our Signals", callback_data='signals')],
                join_button
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                "Our Signals:\n\n"
                "🔹 Buy/Sell Signals with Entry and Exit Prices\n"
                "🔹 Take Profit (TP) and Stop Loss (SL) Levels\n"
                "🔹 Copy the signals and follow our expert analysis\n\n"
                "Start making profitable trades with our signals!",
                reply_markup=reply_markup
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
    global bot
    global dispatcher

    bot = Bot(token=TELEGRAM_API_TOKEN)
    dispatcher = Dispatcher(bot=bot, update_queue=None, use_context=True)

    # handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_handler(CallbackQueryHandler(button_click))

    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', '5000')))

if __name__ == "__main__":
    main()
