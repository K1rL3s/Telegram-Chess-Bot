import os
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from src.db import db_session


load_dotenv()

abs_path = Path().absolute()

logger.add(
    abs_path / 'logs' / 'logs.log',
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} {level:<7} {message}",
    level='DEBUG',
    rotation="00:00",
    compression="zip",
    # serialize=True
)

db_session.global_init(abs_path / 'src' / 'db' / 'database.sqlite')
db_sess = db_session.create_session()

storage = MemoryStorage()

bot = Bot(token=os.getenv("CHESS_TG_TOKEN"))
dp = Dispatcher(bot=bot, storage=storage)
