from pathlib import Path

from aiogram import Dispatcher, Bot, executor
from loguru import logger
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from src.consts import Config
from src.db import db_session
from src.handlers import register_client_handlers, register_error_handlers
from src.middlewares import setup_middlewares


async def on_startup(dp: Dispatcher):
    setup_middlewares(dp)
    register_client_handlers(dp)
    register_error_handlers(dp)


def main():
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

    bot = Bot(token=Config.CHESS_TG_TOKEN)
    dp = Dispatcher(bot=bot, storage=MemoryStorage())

    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup,
        timeout=Config.TIMEOUT
    )


if __name__ == '__main__':
    logger.info('Запуск бота...')
    main()
    logger.info('Выключение бота')
