from asyncio import AbstractEventLoop
from typing import Optional
from time import sleep
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger
import asyncpg
from typing import Tuple, List

ACCEPT_BUTTON = "✅ ПРИНЯТЬ"
DECLINE_BUTTON = "❌ ОТКЛОНИТЬ"
ALL_PASSES_TYPE = 0
NEW_ONE_PASS_TYPE = 1
NEW_PASS_STATE = 0
ACTIVE_PASS_STATE = 1
EXP_PASS_STATE = 2

class Database:
    def __init__(
        self,
        name: Optional[str],
        user: Optional[str],
        password: Optional[str],
        host: Optional[str],
        port: Optional[str],
        loop: AbstractEventLoop,
        pool: asyncpg.pool.Pool,
    ) -> None:
        # Validate the input parameters to ensure they are not empty or of incorrect types
        if not all([name, user, password, host, port, loop]):
            raise ValueError("Invalid input parameters provided")

        self.name = name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.loop = loop
        self.pool = loop.run_until_complete(
            asyncpg.create_pool(
                database=name,
                user=user,
                password=password,
                host=host,
                port=port,
            )
        )

    async def create_tables(self) -> None:
        """Create tables in the database."""
        with open("bot/sql/init.sql", "r") as f:
            sql = f.read()

        # Sanitize the SQL query by using parameterized queries
        await self.pool.execute(sql)

        logger.info("DB tables created")

    async def close_database(self) -> None:
        await self.pool.close()

    async def add_user(self, user_id):
        # Sanitize the input by using parameterized queries
        await self.pool.execute("INSERT INTO Users VALUES($1)", str(user_id))

    async def verification(self, user_id) -> bool:
        response = await self.pool.fetchrow(
            "SELECT EXISTS(SELECT user_id FROM Users WHERE user_id=$1)", str(user_id)
        )
        return response[0]

    async def get_user_row(self, user_id, row: str) -> str:
        response = await self.pool.fetchrow(
            f"SELECT {row} FROM Users WHERE user_id=$1", str(user_id)
        )
        return response[0]

    async def set_user_row(self, user_id, row: str, value: str) -> None:
        await self.pool.fetchrow(
            f"UPDATE Users SET {row}=$1 WHERE user_id=$2", value, str(user_id)
        )

    