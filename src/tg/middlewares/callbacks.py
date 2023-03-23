from aiogram import types

from src.tg.middlewares.base import MyBaseMiddleware


class CallbackQueryMiddleware(MyBaseMiddleware):
    """
    Мидлварь, который отвечает на callback query за меня.
    """

    async def on_post_process_callback_query(self, callback: types.CallbackQuery, result, data: dict):
        await callback.answer()
