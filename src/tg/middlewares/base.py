from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware


class MyBaseMiddleware(BaseMiddleware):
    """
    Базовый мидлварь. Он нужен, чтобы метод get_short_info везде был у меня.
    """

    @staticmethod
    def get_short_info(message: types.Message | types.CallbackQuery):
        username = (message.from_user.username or
                    message.from_user.first_name or
                    message.from_user.last_name)  # XD

        if isinstance(message, types.Message):
            return f'id={message.from_user.id}, ' \
                   f'chat={message.chat.id}, ' \
                   f'username={username}'

        elif isinstance(message, types.CallbackQuery):
            return f'id={message.from_user.id}, ' \
                   f'chat={message.message.chat.id}, ' \
                   f'username={username}'
