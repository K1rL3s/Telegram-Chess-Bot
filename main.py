from aiogram import Dispatcher, executor
from loguru import logger

from __init__ import dp
from src.consts import Config
from src.tg.handlers import register_client_handlers
from src.tg.middlewares import setup_middlewares


async def all_errors(update, error):
    logger.error(f'Exception Error: {error}, {update=}')


async def on_startup(dp: Dispatcher):
    setup_middlewares(dp)
    register_client_handlers(dp)
    dp.register_errors_handler(all_errors, exception=Exception)


if __name__ == '__main__':
    logger.info('Запуск бота...')
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, timeout=Config.TIMEOUT)
    logger.info('Выключение бота')
