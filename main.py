import os
import telebot

# The bot token will be securely pulled from your cloud hosting environment variables
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Temporary storage to track user states on the web process
user_states = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 
                 "Hello! Send me the message in this format:\n\n"
                 "**ReceiverUsername**\n"
                 "Your message content here...",
                 parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text

    # Simple parsing: Line 1 = Receiver Username, Rest = Content/Custom Sender Signature
    lines = text.split('\n', 1)
    
    if len(lines) < 2:
        bot.reply_to(message, "Please provide both the receiver's username on line 1 and the message content on line 2.")
        return

    receiver_username = lines[0].strip().replace('@', '')
    content = lines[1].strip()

    # Attempt to send to the receiver
    try:
        # Note: For security, Telegram bots can only message users who have already started/interacted with the bot.
        formatted_message = f"💬 **New Forwarded Message:**\n\n{content}"
        
        # We try to resolve the username. (If the user hasn't started the bot, Telegram API will restrict direct messaging).
        bot.send_message(f"@{receiver_username}", formatted_message, parse_mode="Markdown")
        bot.reply_to(message, f"✅ Success! Your message was sent to @{receiver_username}.")
    except Exception as e:
        bot.reply_to(message, f"❌ Failed to send. Note: The recipient must have started this bot first.\nError: {str(e)}")

# Start polling execution loop
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
