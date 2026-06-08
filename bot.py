from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

TOKEN = "7991649276:AAGPpCTx6uqPLRKFr6hCxeADUCSxVfAp8ZM"
CHANNEL_USERNAME = "@mdcmovie"

movies = {}
ADMIN_ID = 5837813502

# CHECK JOIN
async def is_joined(bot, user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    joined = await is_joined(context.bot, user_id)

    if not joined:
        keyboard = [
            [InlineKeyboardButton("📢 Kanalga qo‘shilish",
                                  url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")],
            [InlineKeyboardButton("✅ Tekshirish", callback_data="check")]
        ]

        await update.message.reply_text(
            "❗ Botdan foydalanish uchun kanalga qo‘shiling!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    await update.message.reply_text("Salom bro 🤖 Bot ishlayapti!")

# CHECK BUTTON
async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    joined = await is_joined(context.bot, user_id)

    if joined:
        await query.answer("✅ Tasdiqlandi!")
        await query.message.edit_text("🎬 Endi botdan foydalanishingiz mumkin!")
    else:
        await query.answer("❌ Hali qo‘shilmagansiz!", show_alert=True)

# ADD CODE
async def add_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Siz admin emassiz")
        return

    args = context.args
    if len(args) < 2:
        await update.message.reply_text("❌ Format: /kod 34 123")
        return

    movies[args[0]] = args[1]
    await update.message.reply_text(f"✅ Kod qo‘shildi: {args[0]}")

# MOVIE
async def handle_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    joined = await is_joined(context.bot, user_id)

    if not joined:
        await update.message.reply_text("❗ Avval kanalga qo‘shiling 👉 @mdcmovie")
        return

    text = update.message.text.strip()

    if text in movies:
        await context.bot.copy_message(
            chat_id=update.effective_chat.id,
            from_chat_id="-1003926152488",
            message_id=int(movies[text])
        )
    else:
        await update.message.reply_text("❌ Kino topilmadi")

# BOT
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("kod", add_code))
app.add_handler(CallbackQueryHandler(check_join))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_movie))

print("Bot ishlayapti...")
app.run_polling()

async def is_joined(bot, user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False