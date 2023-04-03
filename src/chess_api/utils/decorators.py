import functools
import os

from aiogram.dispatcher.handler import CancelHandler
from loguru import logger
from httpx import RequestError

from src.tg.utils.log_in_chat import log_in_chat

LOG_CHAT = os.environ.get('LOG_CHAT')


def get_func_name(func):
    return getattr(func, 'func_name', None) or getattr(func, '__name__', None) or '<undefined>'


def async_requests_catch(func):
    """
    Декоратор для логирования и отлавливания ошибок при async запросах к шахматной апишке.
    (Потому что ошибки километровые при запросах)
    """

    function_name = get_func_name(func)

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except RequestError as e:
            message = f'Ошибка API "{function_name}": {repr(e)}'

            logger.error(message)
            await log_in_chat(message)

            raise CancelHandler()
    return wrapper


def async_logger_wraps(entry: bool = True, output: bool = True, level: str = "DEBUG"):
    """
    Логгер выполнения async функций.

    :param entry: Выводить ли входные данные.
    :param output: Выводить ли выходные данные.
    :param level: Уровень
    """

    def wrapper(func):
        function_name = get_func_name(func)

        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            logger_ = logger.opt(depth=1)
            if entry:
                logger_.log(level, f'Вызов "{function_name}" (args={args}, kwargs={kwargs})')
            result = await func(*args, **kwargs)
            if output:
                logger_.log(level, f'Результат "{function_name}" (result={result})')
            return result

        return wrapped

    return wrapper
