import os

import requests

from src.chess_api.dataclasses import EngineEvaluation
from src.utils.decorators import requests_catch, logger_wraps
from src.chess_api.abort import abort


API_URL = os.getenv('API_URL')
headers = {"Authorization": os.getenv('API_AUTH_KEY')}


@logger_wraps()
@requests_catch
def get_engine_evaluation(
        *,
        fen: str | None = None,
        prev_moves: str | None = None
) -> EngineEvaluation:
    """
    Возвращает оценку позиции в сантипешках или ходов до мата.

    :param fen: Текущая позиция в FEN.
    :param prev_moves: История ходов в партии.
    :return: Мощный намедтупле с ответом сервера.
    """

    if not fen and not prev_moves:
        raise RuntimeError("Хотя бы кого-то из них надо, можно нормально? Чё такое-то, а?")

    params = {
        "fen": fen,
        "prev_moves": prev_moves
    }
    response = requests.get(API_URL + 'position', params=params, headers=headers)

    if not response:
        return abort(response.json()["message"])

    return EngineEvaluation(**response.json()["response"])
