from aiogram import types
from loguru import logger

from src.middlewares.base import MyBaseMiddleware


class LoggingMiddleware(MyBaseMiddleware):
    """
    Мидлварь для логов.
    """

    async def on_pre_process_callback_query(self, callback: types.CallbackQuery, *_):
        logger.debug(
            f'Вызван callback "{callback.data}" [{await self.get_short_info(callback)}]'
        )

    async def on_post_process_callback_query(self, callback: types.CallbackQuery, *_):
        logger.debug(
            f'Отработан callback "{callback.data}" [{await self.get_short_info(callback)}]'
        )

    async def on_pre_process_message(self, message: types.Message, *_):
        logger.debug(
            f'Получено сообщение "{" ".join(message.text.splitlines())}" [{await self.get_short_info(message)}]'
        )

    async def on_post_process_message(self, message: types.Message, *_):
        logger.debug(
            f'Отработано сообщение "{" ".join(message.text.splitlines())}" [{await self.get_short_info(message)}]'
        )
