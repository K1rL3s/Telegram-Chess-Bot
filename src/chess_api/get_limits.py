import os

import requests
# Мне понравилось, что не кэшируется ошибка, потому что функция не выполняется из-за выброса ошибки.
from cachetools.func import ttl_cache

from src.utils.decorators import requests_catch, logger_wraps
from src.chess_api.abort import abort


API_URL = os.getenv('API_URL')


@logger_wraps()
@requests_catch
@ttl_cache()
def get_limits() -> dict[str, dict[str, int]]:
    """
    Возвращает серверные лимиты шахматного движка.
    Используется для ограничения вводимых данных юзером.
    """

    response = requests.get(API_URL + 'limits')
    if not response:
        return abort(response.json()["message"])
    return response.json()["response"]


@logger_wraps()
@requests_catch
@ttl_cache()
def get_defaults() -> dict[str, int]:
    """
    Возвращает серверные значения по умолчанию для шахматного движка.
    Используется базой данных для заполнения значениями по умолчанию.
    """

    defaults = {param: dct["default"] for param, dct in get_limits().items()}
    defaults.update({'with_coords': True, 'with_position_evaluation': False, 'colors': None})
    return defaults
