import os
from io import BytesIO

import requests

from src.chess_api.get_limits import get_limits
from src.utils.decorators import requests_catch, logger_wraps
from src.tg.utils.abort import abort

API_URL = os.getenv('API_URL')


@logger_wraps()
@requests_catch
def get_board_image(fen: str, last_move: str, check: str | None, **params) -> BytesIO | None:
    """
    Возвращает изображение текущей позиции на доске.

    :param fen: Текущая позиция в FEN.
    :param last_move: Последний сделанный ход.
    :param check: Клетка с шахом, если такая есть.
    :param params: Остальные ключевые аргументы, такие как "coords", "colors".
    :return: BytesIO PNG.
    """

    size = get_limits()["size"]["max"]

    params = {
        "fen": fen,
        "last_move": last_move,
        "check": check,
        "size": size,
        **params
    }

    response = requests.get(API_URL + 'board', params=params)
    if not response:
        return abort(response.json()["message"])

    return BytesIO(response.content)
