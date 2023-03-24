from aiogram import types
from loguru import logger

from src.tg.middlewares.base import MyBaseMiddleware


class LoggingMiddleware(MyBaseMiddleware):
    """
    Мидлварь для логов.
    """

    async def on_pre_process_callback_query(self, callback: types.CallbackQuery, data: dict):
        logger.debug(
            f'Вызван callback "{callback.data}" [{self.get_short_info(callback)}]'
        )

    async def on_post_process_callback_query(self, callback: types.CallbackQuery, result, data: dict):
        logger.debug(
            f'Отработан callback "{callback.data}" [{self.get_short_info(callback)}]'
        )

    async def on_pre_process_message(self, message: types.Message, data: dict):
        logger.debug(
            f'Получено сообщение "{" ".join(message.text.splitlines())}" [{self.get_short_info(message)}]'
        )

    async def on_post_process_message(self, message: types.Message, result, data: dict):
        logger.debug(
            f'Отработано сообщение "{" ".join(message.text.splitlines())}" [{self.get_short_info(message)}]'
        )
