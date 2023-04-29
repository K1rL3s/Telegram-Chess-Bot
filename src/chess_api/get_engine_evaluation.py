from src.utils.chess_api.abort import abort
from src.utils.chess_api.dataclasses import EngineEvaluation
from src.utils.chess_api.decorators import async_requests_catch, async_logger_wraps
from src.consts import Config


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
        raise RuntimeError(
            "Хотя бы кого-то из них надо, можно нормально? Чё такое-то, а?"
        )

    params = {
        "fen": fen,
        "prev_moves": prev_moves
    }
    response = await Config.api_session.get(
        Config.API_URL + 'position',
        params=params, headers=Config.api_headers
    )

    if response.status_code != 200:
        return abort(response.json()["message"])

    return EngineEvaluation(**response.json()["response"])
