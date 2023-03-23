from aiogram.dispatcher.handler import CancelHandler
from loguru import logger


def abort(message: str | None = None):
    """
    Прерывает ответ на сообщение и пишет лог (ответ пользователю?)

    :param message: Сообщение от апишки.
    """

    if message:
        logger.warning(message)
    raise CancelHandler()
