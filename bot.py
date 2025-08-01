# force redeploy test
import os
import logging
from telegram import Update, Poll
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")  # Telegram group chat ID where polls will be posted

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def handle_txt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.document:
        return

    doc = update.message.document
    if doc.mime_type != "text/plain":
        await update.message.reply_text("❌ Please send a plain .txt file.")
        return

    file = await doc.get_file()
    file_path = await file.download_to_drive()

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    questions = content.strip().split("\n\n")
    count = 0

    for q in questions:
        lines = q.strip().split("\n")
        if len(lines) < 6:
            continue
        question = lines[0]
        options = lines[1:5]
        answer_line = lines[5]
        if "Answer" not in answer_line:
            continue
        correct = answer_line[-1]
        try:
            correct_index = "ABCD".index(correct.upper())
        except:
            continue

        await context.bot.send_poll(
            chat_id=GROUP_ID,
            question=question,
            options=options,
            type=Poll.QUIZ,
            correct_option_id=correct_index,
            is_anonymous=False
        )
        count += 1

    await update.message.reply_text(f"✅ {count} quizzes posted.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.Document.FILE_EXTENSION("txt"), handle_txt))
    app.run_polling()
