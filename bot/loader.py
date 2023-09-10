import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from bot.database import Database

load_dotenv('.env')
token = os.environ.get("BOT_TOKEN") or ''
bot = Bot(token=token, parse_mode="html")
loop = asyncio.get_event_loop()
dp = Dispatcher(bot, loop=loop)
db = Database(
    name=os.environ.get("POSTGRES_DB"),
    user=os.environ.get("POSTGRESQL_USERNAME"),
    password=os.environ.get("POSTGRES_PASSWORD"),
    host=os.environ.get("DATABASE_HOST"),
    port=os.environ.get("DATABASE_PORT"),
    loop=loop,
    pool=None,
)

MAIL = os.environ.get("MAIL") or ''
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD") or ''
# Print the value of BOT_TOKEN from the environment variables
# This can be used for debugging
# print(f'ENV: {os.environ.get("BOT_TOKEN")}')