from aiogram import Dispatcher, executor
from aiogram.utils.exceptions import TelegramAPIError
from loguru import logger

from __init__ import dp
from src.tg.handlers import register_client_handlers
from src.tg.middlewares import setup_middlewares


async def all_telegram_errors(update, error):
    logger.error(f'TelegramAPIERROR: {update=}, {error}')


async def on_startup(dp: Dispatcher):
    setup_middlewares(dp)
    register_client_handlers(dp)
    dp.register_errors_handler(all_telegram_errors, exception=TelegramAPIError)


if __name__ == '__main__':
    logger.info('Запуск бота...')
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    logger.info('Выключение бота')
