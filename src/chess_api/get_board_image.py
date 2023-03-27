import os
from io import BytesIO

import requests

from src.chess_api.get_limits import get_limits
from src.utils.decorators import requests_catch, logger_wraps
from src.chess_api.abort import abort


API_URL = os.getenv('API_URL')
headers = {"Authorization": os.getenv('API_AUTH_KEY')}


@logger_wraps()
@requests_catch
def get_board_image(
        *,
        fen: str,
        last_move: str | None = None,
        check: str | None = None,
        orientation: str = 'w',
        **params) -> BytesIO:
    """
    Возвращает изображение текущей позиции на доске.

    :param fen: Текущая позиция в FEN.
    :param last_move: Последний сделанный ход.
    :param check: Клетка с шахом, если такая есть.
    :param orientation: Цвет игрока.
    :param params: Остальные ключевые аргументы, такие как "coords", "colors".
    :return: BytesIO PNG.
    """

    params = {
        "fen": fen,
        "last_move": last_move,
        "check": check,
        "orientation": orientation,
        **params
    }

    if 'size' not in params.keys():
        params['size'] = get_limits()["size"]["max"]

    if 'with_coords' in params.keys():
        params['coords'] = 't' if params['with_coords'] else 'f'

    response = requests.get(API_URL + 'board', params=params, headers=headers)

    if not response:
        return abort(response.json()["message"])

    return BytesIO(response.content)
