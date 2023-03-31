from src.chess_api.utils import EngineEvaluation, async_requests_catch, async_logger_wraps, abort
from src.consts import API_URL, api_headers, api_session


@async_logger_wraps()
@async_requests_catch
async def get_engine_evaluation(
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
    response = await api_session.get(API_URL + 'position', params=params, headers=api_headers)

    if response.status_code != 200:
        return abort(response.json()["message"])

    return EngineEvaluation(**response.json()["response"])
