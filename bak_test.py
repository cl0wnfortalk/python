import asyncio
import datetime
import logging 
from psycopg import AsyncConnection
# import psycopg2 
from os import getenv
from dotenv import load_dotenv
from telegram import Update 
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# time configuration (for logging issues)

now = datetime.datetime.now()

# logger configurations 

logger = logging.getLogger(__name__)
logging.basicConfig(filename="journal.log", 
                    encoding="utf-8",
                    level=logging.DEBUG)

# custom Exceptions 

class NoCredsProvided(Exception):
    pass 

# setting up enviroment
# getting passwords and API keys 
# postgresql

load_dotenv("POSTGRES")
load_dotenv("TELEGRAM")

if getenv("POSTGRES"):
    pg_pswd = getenv("POSTGRES")
else:
    logger.critical(f"{now}: PostgreSQL password was not provided")
    raise NoCredsProvided("PostgreSQL password was not provided")

# telegram bot API key

if getenv("TELEGRAM"):
    tg_api = getenv("TELEGRAM")
else:
    logger.critical(f"{now}: Telegram bot API key was not provided")
    raise NoCredsProvided("Telegram bot API key was not provided")

# creating telegram app

QU, WAIT, FINAL = range(3)

instruction = '''
В этом опроснике содержатся группы утверждений. 
Внимательно прочитайте каждую группу утверждений. 
Затем определите в каждой группе одно
утверждение, которое лучше всего соответствует 
тому, как Вы себя чувствовали НА
ЭТОЙ НЕДЕЛЕ И СЕГОДНЯ. В ответном сообщении 
отправьте НОМЕР соответствующего утверждения, 
если оно коррелирует с Вашим состоянием.
Убедитесь, что Вы прочли все утверждения в каждой группе
'''

app = ApplicationBuilder().token(tg_api).build()


async def start(update:Update, 
                context:ContextTypes.DEFAULT_TYPE):
    context.user_data["count"] = 5
    context.user_data["answers"] = 0
    await update.message.reply_text(instruction)
    # return QU
    return await get_question(update, context)

async def get_question(update:Update, 
                       context:ContextTypes.DEFAULT_TYPE):
    # connecting to database 
    conn = await AsyncConnection.connect(f"dbname=postgres user=postgres password={pg_pswd} host=localhost")
    context.user_data["conn"] = conn
    count = context.user_data.get("count")
    context.user_data["count"] -= 1
    # getting groups of questions one by one
    if (conn):
        async with conn.cursor() as curs:
            await curs.execute(f"SELECT q FROM questions WHERE qgroup={count}")
            rows = await curs.fetchall()
            block = "\n\n".join([f"❄ {row[0]}" for row in sorted(rows)])
            await update.message.reply_text(block)            
            return WAIT

async def wait_answer(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # waiting for user's answer
    user_response = update.message.text
    count = context.user_data.get("count")
    if count >= 0 and user_response.isdigit():
        context.user_data["answers"] += int(user_response)
        if count == 0:
            result = context.user_data["answers"]
            await update.message.reply_text(f"Ваш результат: {result}")
            return await get_results(update, context)
        return await get_question(update, context)
    else:
        await update.message.reply_text("Пожалуйста, отправьте число, соответствующее вашему ответу.")
        return WAIT
    
async def get_results(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # getting test's results
    result = context.user_data["answers"]
    conn = context.user_data.get("conn")
    # replace on switch case formular
    res_id = 999
    if result >= 0 and result <= 9:
        res_id = 1
        emoji = "😊"
    elif result >= 10 and result <= 15:
        res_id = 2
        emoji = "😳"
    elif result >= 16 and result <= 19:
        res_id = 3
        emoji = "😰"
    elif result >= 20 and result <= 29:
        res_id = 4
        emoji = "😱"
    elif result >= 30 and result <= 63:
        res_id = 5
        emoji = "😭"

    async with conn.cursor() as curs:
        await curs.execute(f"SELECT res FROM results WHERE id={res_id};")
        res_fetched = await curs.fetchall()
        if res_fetched:
            await update.message.reply_text(f"Ваш результат : {res_fetched[0][0]} {emoji}")
        else:
            await update.message.reply_text("Ошибка.")


async def stop_bot(update:Update, context:
                ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Спасибо! Будьте здоровы!")
    return ConversationHandler.END

def main() -> None:
    conv_handler = ConversationHandler(
        entry_points = [CommandHandler("start", start)],
        states = {
            QU: [MessageHandler(filters.TEXT, get_question)],
            WAIT: [MessageHandler(filters.TEXT, wait_answer)],
            FINAL: [MessageHandler(filters.TEXT, get_results)],
        },
        fallbacks=[CommandHandler("stop", stop_bot)],
    )

    app.add_handler(conv_handler)
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()




