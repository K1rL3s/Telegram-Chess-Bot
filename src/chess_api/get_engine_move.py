import os

import requests

from src.chess_api.dataclasses import EngineMove
from src.utils.decorators import requests_catch, logger_wraps
from src.tg.utils.abort import abort

API_URL = os.getenv('API_URL')


@logger_wraps()
@requests_catch
def get_engine_move(
        *,
        user_move: str | None,
        prev_moves: str | None,
        orientation: str | None,
        **params
) -> EngineMove:
    """
    Получает новый ход от шахматного движка и FEN позицию.

    :param user_move: Ход пользователя.
    :param prev_moves: Предыдущие ходы (история ходов).
    :param orientation: За какой цвет играет пользователь.
    :param params: Остальные параметры, такие как "threads", "depth", "ram_hash", "skill_level",
    :return: Мощный намедтупле с ответом сервера.
    """

    params = {
        "user_move": user_move,
        "prev_moves": prev_moves,
        "orientation": orientation,
        **params
    }
    response = requests.get(API_URL + 'move', params=params)
    if not response:
        return abort(response.json()["message"])

    return EngineMove(**response.json()["response"])
