import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROUP_ID = int(os.environ.get("GROUP_ID"))

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Quiz bot is ready! Send a .txt file to create quizzes.")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    if document.mime_type != 'text/plain':
        await update.message.reply_text("❌ Please send a .txt file only.")
        return

    file = await context.bot.get_file(document.file_id)
    content = await file.download_as_bytearray()
    text = content.decode("utf-8")

    questions = text.strip().split("\n\n")
    for block in questions:
        lines = block.strip().split("\n")
        if len(lines) != 6:
            continue
        question = lines[0]
