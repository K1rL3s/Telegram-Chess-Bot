from src.utils.chess_api.abort import abort
from src.utils.chess_api.dataclasses import EngineMove
from src.utils.chess_api.decorators import async_requests_catch, async_logger_wraps

from src.consts import Config


@async_logger_wraps()
@async_requests_catch
async def get_engine_move(
        *,
        user_move: str | None,
        prev_moves: str | None,
        orientation: str | None,
        **params
) -> EngineMove | None:
    """
    Получает новый ход от шахматного движка и FEN позицию.

    :param user_move: Ход пользователя.
    :param prev_moves: Предыдущие ходы (история ходов).
    :param orientation: За какой цвет играет пользователь.
    :param params: Остальные параметры, такие как "threads", "depth", "ram_hash", "skill_level",
    :return: Мощный намедтупле с ответом сервера. Если None - нелегальный ход.
    """

    params = {
        "user_move": user_move,
        "prev_moves": prev_moves,
        "orientation": orientation,
        **params
    }
    response = await Config.api_session.get(
        Config.API_URL + 'move',
        params=params, headers=Config.api_headers
    )

    if response.status_code != 200:
        if 'illegal' in (message := response.json()["message"]):
            return None
        return abort(message)

    return EngineMove(**response.json()["response"])
