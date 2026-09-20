import telebot
import requests
import re
from flask import Flask
from threading import Thread
import os

# Flask Web Server Setup (Render-কে ফ্রি রাখার জন্য)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7 for free!"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_server)
    t.start()

# Telegram Bot Setup
BOT_TOKEN = "8674313991:AAHBAQdMTUKbEGfOL6NYGk5Ne7YbzEOzgnc"
bot = telebot.TeleBot(BOT_TOKEN)
API_URL = "https://darktoolshub.site/bot/trueapi.php" 
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 **Welcome!**\nযেকোনো নাম্বার দাও, আমি সেটার ডিটেইলস এবং WhatsApp/Telegram লিংক বের করে দিচ্ছি।", parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_number_lookup(message):
    raw_input = message.text.strip()
    clean_number = re.sub(r'[^\d]', '', raw_input)
    
    if not clean_number:
        bot.reply_to(message, "❌ একটি সঠিক নাম্বার দাও।")
        return

    if clean_number.startswith("01") and len(clean_number) == 11:
        link_number = "88" + clean_number
    else:
        link_number = clean_number

    loading_msg = bot.reply_to(message, "🔍 ডাটা খোঁজা হচ্ছে...")
    wa_link = f"https://wa.me/{link_number}"
    tg_link = f"https://t.me/+{link_number}"

    try:
        api_params = {"num": f"+{link_number}"}
        response = requests.get(API_URL, params=api_params, headers=HEADERS)
        
        try:
            data = response.json()
        except ValueError:
            bot.edit_message_text(chat_id=message.chat.id, message_id=loading_msg.message_id, text="❌ API থেকে ডাটা আনা যাচ্ছে না।")
            return

        if data.get("success"):
            name = data.get("name", "Unknown")
            carrier = data.get("carrier", "Unknown")
            country = data.get("country", "Unknown")
            
            reply_text = (
                f"👤 **Name:** {name}\n"
                f"📱 **Number:** +{link_number}\n"
                f"🏢 **Carrier:** {carrier}\n"
                f"🌍 **Country:** {country}\n\n"
                f"🔗 **Direct Links:**\n"
                f"🟢 [Open in WhatsApp]({wa_link})\n"
                f"✈️ [Open in Telegram]({tg_link})"
            )
        else:
            reply_text = (
                f"❌ **এই নাম্বারের ডিটেইলস API-তে পাওয়া যায়নি।**\n\n"
                f"🔗 **Direct Links:**\n"
                f"🟢 [Open in WhatsApp]({wa_link})\n"
                f"✈️ [Open in Telegram]({tg_link})"
            )

        bot.edit_message_text(chat_id=message.chat.id, message_id=loading_msg.message_id, text=reply_text, parse_mode="Markdown", disable_web_page_preview=True)
            
    except Exception as e:
        bot.edit_message_text(chat_id=message.chat.id, message_id=loading_msg.message_id, text="⚠️ সার্ভারে কানেক্ট করতে সমস্যা হয়েছে।")

# সার্ভার ও বট চালু করা
keep_alive()
print("Bot is running...")
bot.infinity_polling()
