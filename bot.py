import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

users = set()

# Get token from environment variable
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users.add(user_id)
    await update.message.reply_text("✅ You are now connected! Anything you send will be broadcast to others.")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender_id = update.effective_user.id
    sender_name = update.effective_user.first_name

    for user in users:
        if user != sender_id:
            try:
                if update.message.text:
                    await context.bot.send_message(chat_id=user, text=f"{sender_name}: {update.message.text}")

                elif update.message.photo:
                    await context.bot.send_photo(chat_id=user,
                                                 photo=update.message.photo[-1].file_id,
                                                 caption=f"{sender_name}: {update.message.caption or ''}")

                elif update.message.video:
                    await context.bot.send_video(chat_id=user,
                                                 video=update.message.video.file_id,
                                                 caption=f"{sender_name}: {update.message.caption or ''}")

                elif update.message.document:
                    await context.bot.send_document(chat_id=user,
                                                    document=update.message.document.file_id,
                                                    caption=f"{sender_name}: {update.message.caption or ''}")

                elif update.message.audio:
                    await context.bot.send_audio(chat_id=user,
                                                 audio=update.message.audio.file_id,
                                                 caption=f"{sender_name}: {update.message.caption or ''}")

                elif update.message.voice:
                    await context.bot.send_voice(chat_id=user,
                                                 voice=update.message.voice.file_id,
                                                 caption=f"{sender_name} sent a voice message")

                elif update.message.sticker:
                    await context.bot.send_sticker(chat_id=user, sticker=update.message.sticker.file_id)

                else:
                    await context.bot.send_message(chat_id=user, text=f"{sender_name} sent something unsupported.")

            except Exception as e:
                print(f"Could not send to {user}: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, broadcast))

    print("🚀 Bot is running on Render...")
    app.run_polling()

if __name__ == "__main__":
    main()

