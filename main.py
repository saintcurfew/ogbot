from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = '7961345627:AAGjOlzGh7NvjGyPa3vjTZAj5ZNKduBQGjY'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a URL and I'll generate a preview!")

def get_og_data(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        og_image = soup.find("meta", property="og:image")
        og_title = soup.find("meta", property="og:title")
        return {
            "title": og_title['content'] if og_title else url,
            "image": og_image['content'] if og_image else None
        }
    except:
        return None

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not url.startswith("http"):
        await update.message.reply_text("Please send a valid URL.")
        return

    og = get_og_data(url)
    if not og or not og['image']:
        await update.message.reply_text("Could not extract OG image.")
        return

    caption = f"{og['title']}\n{url}"

    try:
        await update.message.reply_photo(photo=og['image'], caption=caption)
    except:
        await update.message.reply_text("Error sending image. Here's the title and link:\n" + caption)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    app.run_polling()
