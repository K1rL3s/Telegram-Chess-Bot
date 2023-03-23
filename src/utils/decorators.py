import functools

from aiogram.dispatcher.handler import CancelHandler
from loguru import logger
from requests import RequestException


def get_func_name(func):
    return getattr(func, 'func_name', None) or getattr(func, '__name__', None) or '<undefined>'


def requests_catch(func):
    """
    Декоратор для логирования и отлавливания ошибок при запросах к шахматной апишке.
    (Потому что там ошибки километровые)
    """

    function_name = get_func_name(func)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RequestException as e:
            logger.error(
                f'Ошибка API "{function_name}": {e.__class__.__module__}.{e.__class__.__qualname__}: {e}'
            )
            raise CancelHandler()
        except CancelHandler as e:
            logger.error(
                f'Ошибка TG "{function_name}": {args=}  |  {kwargs=}'
            )
            raise e
    return wrapper


def logger_wraps(entry: bool = True, output: bool = True, level: str = "DEBUG"):
    """
    Логгер выполнения функции.

    :param entry: Выводить ли входные данные.
    :param output: Выводить ли выходные данные.
    :param level: Уровень
    """

    def wrapper(func):
        function_name = get_func_name(func)

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger_ = logger.opt(depth=1)
            if entry:
                logger_.log(level, f'Вызов "{function_name}" (args={args}, kwargs={kwargs})')
            result = func(*args, **kwargs)
            if output:
                logger_.log(level, f'Результат "{function_name}" (result={result})')
            return result

        return wrapped

    return wrapper
