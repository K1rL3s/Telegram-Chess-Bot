import os

import requests

from src.utils.decorators import requests_catch, logger_wraps
from src.tg.utils.abort import abort

API_URL = os.getenv('API_URL')


@logger_wraps()
@requests_catch
def get_engine_evaluation(*, fen: str | None = None, prev_moves: str | None = None):
    """
    Возвращает оценку позиции в сантипешках или ходов до мата.

    :param fen: Текущая позиция в FEN.
    :param prev_moves: История ходов в партии.
    """

    if not fen and not prev_moves:
        raise RuntimeError("Хотя бы кого-то из них надо, можно нормально? Чё такое-то, а?")

    params = {
        "fen": fen,
        "prev_moves": prev_moves
    }
    response = requests.get(API_URL + 'position', params=params)
    if not response:
        return abort(response.json()["message"])

    return ...
