from typing import Type

from aiogram.dispatcher.handler import CancelHandler
from loguru import logger


def abort(message: str | None = None, error: Type[Exception] = CancelHandler):
    """
    Прерывает ответ на сообщение и пишет лог (ответ пользователю?)

    :param message: Сообщение от апишки.
    :param error: Ошибка, которая появится.
    """

    if message:
        logger.warning(message)
    raise error()
