from aiogram import Bot

from src.consts import Config


async def log_in_chat(*args: str):
    """
    Сообщение в указанный чат, используется для уведомления об ошибках.
    """

    if not Config.LOG_CHAT:  # LOG_CHAT не указан
        return False

    await Bot.get_current().send_message(
        Config.LOG_CHAT, '\n\n'.join(args)
    )

    return True
