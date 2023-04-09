from io import BytesIO

from src.chess_api.get_limits import get_limits
from src.chess_api.utils import async_requests_catch, async_logger_wraps, abort
from src.consts import Config


@async_logger_wraps()
@async_requests_catch
async def get_board_image(
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

    # По сути, никогда не случается, потому что вызов всегда с **Setings.get_params(), а там size всегда есть.
    if 'size' not in params.keys():
        params['size'] = (await get_limits())["size"]["max"]

    if 'with_coords' in params.keys():
        params['coords'] = 't' if params['with_coords'] else 'f'

    response = await Config.api_session.get(
        Config.API_URL + 'board',
        params=params, headers=Config.api_headers
    )

    if response.status_code != 200:
        return abort(response.json()["message"])

    return BytesIO(response.content)
