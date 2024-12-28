import asyncio 
import aiohttp 
import logging
import datetime
from os import getenv 
from dotenv import load_dotenv
from telegram import Update 
from telegram.ext import (
    ApplicationBuilder,
    ConversationHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# custom exceptions 

class NoApiKeyProvidedException(Exception):
    pass

# logger configurations

logger = logging.getLogger(__name__)
logging.basicConfig(filename="journal.log",
                    encoding="utf-8",
                    level=logging.DEBUG)
record_time = datetime.datetime.now()

# providing TG API key

load_dotenv("TG_API")

if getenv("TG_API"):
    tg_api = getenv("TG_API")
else:
    logger.critical(f"{record_time}: Telegram Bot API key was not provided")
    raise NoApiKeyProvidedException("Telegram API IS NOT provided")

# providing TG UNSPLASH_API

if getenv("UNSPLASH_API"):
    unspl_api = getenv("UNSPLASH_API")
else:
    logger.critical(f"{record_time}: Unsplash API key was not provided")
    raise NoApiKeyProvidedException("Unsplash API IS NOT provided")

# providing TG UNSPLASH_API PUBLIC

if getenv("UNSPLASH_API_PUB"):
    unspl_api_pub = getenv("UNSPLASH_API_PUB")
else:
    logger.critical(f"{record_time}: Unsplash API key was not provided")
    raise NoApiKeyProvidedException("Unsplash API IS NOT provided")

# telegram bot application 

app = ApplicationBuilder().token(tg_api).build()

QUERY = range(1)

async def start(update:Update, context:
                ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("What kind of picture do you want to request?")
    return QUERY 

async def query_picture(update:Update, context:
                ContextTypes.DEFAULT_TYPE):
    query_input = update.message.text

    # Unsplash Developers API
    url = f"https://api.unsplash.com/photos/?client_id={unspl_api_pub}&query={query_input}&per_page=5"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if (response.ok):
                photos = await response.json()
            else:
                await update.message.reply_text("Connection error")
                ConversationHandler.END
                return False
            
            if photos:
                messages = []
                for photo in photos:
                    messages.append(photo['urls']['small'])  
                # sends objects separately
                for img in messages:
                    await update.message.reply_text(img)
            else:
                await update.message.reply_text("No photos found for your query.")

    return ConversationHandler.END
    

async def stop_bot(update:Update, context:
                ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Thanks for visiting!")
    
    return ConversationHandler.END

def main() -> None:
    conv_handler = ConversationHandler(
        entry_points = [CommandHandler("start", start)],
        states = {
            QUERY: [MessageHandler(filters.TEXT, query_picture)],
        },
        fallbacks=[CommandHandler("stop", stop_bot)],
    )
    app.add_handler(conv_handler)

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
