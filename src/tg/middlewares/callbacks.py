from aiogram import types
from aiogram.utils.exceptions import InvalidQueryID

from src.tg.middlewares.base import MyBaseMiddleware
from src.tg.utils.log_in_chat import log_in_chat


class CallbackQueryMiddleware(MyBaseMiddleware):
    """
    Мидлварь, который отвечает на callback query за меня.
    """

    @staticmethod
    async def on_post_process_callback_query(callback: types.CallbackQuery, result, data: dict):
        try:
            await callback.answer()
        except InvalidQueryID as e:
            await log_in_chat('Слишком долгий ответ на callback!!!', str(e))
            raise e
