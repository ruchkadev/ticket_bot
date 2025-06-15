import json
import uuid
from pathlib import Path

import qrcode
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, ConversationHandler, filters

DB_FILE = 'database.json'
QR_FOLDER = Path('tickets/qr')
QR_FOLDER.mkdir(parents=True, exist_ok=True)

NAME, PHONE = range(2)

def save_data(uid, data):
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            db = json.load(f)
    except FileNotFoundError:
        db = {}
    db[uid] = data
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Введите своё имя:")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Введите номер телефона:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text
    name = context.user_data['name']
    uid = str(uuid.uuid4())
    link = f"http://localhost:8000/u/{uid}"

    # Сохраняем данные
    save_data(uid, {"name": name, "phone": phone, "link": link})

    # Генерируем QR
    img = qrcode.make(link)
    qr_path = QR_FOLDER / f"{uid}.png"
    img.save(qr_path)

    # Отправляем QR и ссылку
    await update.message.reply_photo(photo=open(qr_path, 'rb'),
                                   caption=f"Ваш билет готов!\nСсылка: {link}")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отменено.")
    return ConversationHandler.END

def main():
    TOKEN = "ВАШ_ТОКЕН_БОТА"

    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(conv_handler)
    print("Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
