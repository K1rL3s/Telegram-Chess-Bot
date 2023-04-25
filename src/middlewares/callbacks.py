from aiogram import types
from aiogram.utils.exceptions import InvalidQueryID

from src.middlewares.base import MyBaseMiddleware
from src.utils.tg.log_in_chat import log_in_chat


class CallbackQueryMiddleware(MyBaseMiddleware):
    """
    Мидлварь, который отвечает на callback query за меня.
    """

    @staticmethod
    async def on_post_process_callback_query(callback: types.CallbackQuery, *_):
        try:
            await callback.answer()
        except InvalidQueryID as e:
            await log_in_chat('Слишком долгий ответ на callback!!!', str(e))
            raise e
