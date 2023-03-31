from typing import NamedTuple


class EngineMove(NamedTuple):
    """
    Ответ api/chess/move в виде именованного кортежа.
    """

    stockfish_move: str
    prev_moves: str
    orientation: str
    fen: str
    end_type: str | None
    check: str | None

    def to_dict(self):
        return self._asdict()


class EngineEvaluation(NamedTuple):
    """
    Ответ api/chess/position в виде именованного кортежа.
    """

    is_end: bool
    who_win: str | None
    end_type: str
    value: int
    wdl: tuple[int, int, int]
    fen: str

    def to_dict(self):
        return self._asdict()
