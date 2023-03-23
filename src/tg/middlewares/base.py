from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware


class MyBaseMiddleware(BaseMiddleware):
    """
    Базовый мидлварь. Он нужен, чтобы метод get_short_info везде был у меня.
    """

    @staticmethod
    def get_short_info(message: types.Message | types.CallbackQuery):
        if isinstance(message, types.Message):
            return f'id={message.from_user.id}, chat={message.chat.id}, username={message.from_user.username}'
        elif isinstance(message, types.CallbackQuery):
            return f'id={message.from_user.id}, ' \
                   f'chat={message.message.chat.id}, ' \
                   f'username={message.from_user.username}'
