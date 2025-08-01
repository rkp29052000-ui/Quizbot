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
        options = [line[3:].strip() for line in lines[1:5]]
        answer_letter = lines[5].split(":")[-1].strip().upper()
        try:
            correct_option_id = ["A", "B", "C", "D"].index(answer_letter)
        except ValueError:
            continue

        await context.bot.send_poll(
            chat_id=GROUP_ID,
            question=question,
            options=options,
            type="quiz",
            correct_option_id=correct_option_id,
            is_anonymous=False,
        )

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.TEXT, handle_document))
    app.run_pol_
