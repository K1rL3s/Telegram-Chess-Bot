from aiocache import cached

from src.chess_api.utils import async_requests_catch, async_logger_wraps, abort
from src.consts import Config


@async_logger_wraps()
@async_requests_catch
@cached(ttl=Config.CACHE_LIMIT_REQUEST)
async def get_limits() -> dict[str, dict[str, int]]:
    """
    Возвращает серверные лимиты шахматного движка.
    Используется для ограничения вводимых данных юзером.
    """

    response = await Config.api_session.get(
        Config.API_URL + 'limits',
        headers=Config.api_headers
    )
    if response.status_code != 200:
        return abort(response.json()["message"])
    return response.json()["response"]


@async_logger_wraps()
@async_requests_catch
async def get_defaults() -> dict[str, int]:
    """
    Возвращает серверные значения по умолчанию для шахматного движка.
    Используется базой данных для заполнения значениями по умолчанию и сброса настроек.
    """

    defaults = {param: dct["default"] for param, dct in (await get_limits()).items()}
    defaults.update({'with_coords': True, 'colors': None})
    return defaults
