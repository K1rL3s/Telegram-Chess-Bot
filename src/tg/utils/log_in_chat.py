import os

from aiogram import Bot


LOG_CHAT = os.environ.get('LOG_CHAT')


async def log_in_chat(*args: str):
    """
    Сообщение в указанный чат, используется для уведомления об ошибках.
    """

    if not LOG_CHAT:  # LOG_CHAT не указан
        return False

    await Bot.get_current().send_message(LOG_CHAT, '\n\n'.join(args))

    return True
