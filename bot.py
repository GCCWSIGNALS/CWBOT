import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Replace 'YOUR_TELEGRAM_API_TOKEN' with your actual Telegram API token
TELEGRAM_API_TOKEN = '6069137445:AAFSbxOcA0du2vlkX50rwgAClj2Blo3CrvE'

# Replace 'https://cwbot.onrender.com/' with the actual public URL provided by Render
WEBHOOK_URL = 'https://cwbot.onrender.com/'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, _: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📊 Price Plan 📊", callback_data='price_plan')],
        [InlineKeyboardButton("💼 Our Services 💼", callback_data='services')],
        [InlineKeyboardButton("🚀 Our Signals 🚀", callback_data='signals')],
        [InlineKeyboardButton("👉 JOIN VIP 👈", url='https://t.me/GC_CW1')]
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
        query.message.reply_text(
            "Our Price Plan:\n\n"
            "🌟 7-day free trial\n"
            "🌟 After the free trial, the subscription is £34.99/month.\n\n"
            "Subscribe now to get started!"
        )
    elif option == 'services':
        query.message.reply_text(
            "Our Services:\n\n"
            "🔹 Live Trading Sessions\n"
            "🔹 VIP Forex & Gold Signals\n"
            "🔹 Supportive and Helpful Active Community\n\n"
            "Join us now and enjoy our premium services!"
        )
    elif option == 'signals':
        query.message.reply_text(
            "Our Signals:\n\n"
            "🔹 Buy/Sell Signals with Entry and Exit Prices\n"
            "🔹 Take Profit (TP) and Stop Loss (SL) Levels\n"
            "🔹 Copy the signals and follow our expert analysis\n\n"
            "Start making profitable trades with our signals!"
        )

def unknown(update: Update, _: CallbackContext):
    update.message.reply_text(
        "I'm sorry, I don't understand that command. Please choose one of the options below:",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📊 Price Plan 📊", callback_data='price_plan')],
                                          [InlineKeyboardButton("💼 Our Services 💼", callback_data='services')],
                                          [InlineKeyboardButton("🚀 Our Signals 🚀", callback_data='signals')],
                                          [InlineKeyboardButton("👉 JOIN VIP 👈", url='https://t.me/GC_CW1')]])
    )

def main():
    updater = Updater(TELEGRAM_API_TOKEN)
    dispatcher = updater.dispatcher

    # Add handlers using the new handler API
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, unknown))
    dispatcher.add_handler(CallbackQueryHandler(button_click))

    # Start the webhook instead of polling
    # The webhook will listen for updates from Telegram servers
    updater.start_webhook(listen="0.0.0.0",
                          port=8443,
                          url_path=TELEGRAM_API_TOKEN,
                          webhook_url=WEBHOOK_URL + TELEGRAM_API_TOKEN)

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == "__main__":
    main()
