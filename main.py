import re
import os
import requests
from lxml import etree
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

def wikiscrap(user_message: str) -> str:

    formatted_request = user_message.title().replace(' ', '_')
    url = 'https://en.wikipedia.org/wiki/' + formatted_request

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        return f"Sorry, I couldn't retrieve the Wikipedia page for '{user_message}'. Please try again later."


    tree = etree.HTML(response.content)

    first_paragraph = tree.xpath('string(/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/p[2])')
    second_paragraph = tree.xpath('string(/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/p[3])')

    wikiresult = (f'\n{first_paragraph}\n{second_paragraph}')
    wikiresult = re.sub(r'\[.*?\]', '', wikiresult)

    return wikiresult


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    user_name = update.message.from_user.first_name
    welcome_message = (
        f"Hi {user_name}! I'm your friendly Wikipedia Bot.\n\nJust send me a topic you want to know about, and I'll fetch a summary for you."
    )
    await update.message.reply_text(welcome_message)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    user_input = update.message.text
    summary = wikiscrap(user_input)
    await update.message.reply_text(summary)

def main() -> None:

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()


if __name__ == '__main__':
    main()