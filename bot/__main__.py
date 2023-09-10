import asyncio
from aiogram import Bot, Dispatcher, executor
from aiogram.utils import executor
from bot.commands import set_default_commands
from bot.loader import dp, db
from loguru import logger
from bot import handlers

async def startup(dp: Dispatcher) -> None:
    await db.create_tables() # Connect to the database + migrations from sql/init.sql
    await set_default_commands(dp) # Set up default commands in the bot (/start /kb)
    logger.info("Bot started")

async def shutdown(dp: Dispatcher) -> None:
    await db.close_database()
    logger.info("Bot finished")

if __name__ == "__main__":
    print('OK')
    logger.add(
        "logs/debug.log",
        level="DEBUG",
        format="{time} | {level} | {module}:{function}:{line} | {message}",
        rotation="30 KB",
        compression="zip",
    )
    executor.start_polling(dp, skip_updates=True, on_startup=startup, on_shutdown=shutdown) # точка входа в поллинг бота, запускается startup()
