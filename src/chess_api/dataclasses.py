from typing import NamedTuple


class EngineMove(NamedTuple):
    stockfish_move: str
    prev_moves: str
    orientation: str
    fen: str
    end_type: str | None
    check: str | None

    def to_dict(self):
        return self._asdict()


class EngineEvaluation(NamedTuple):
    is_end: bool
    who_win: str | None
    end_type: str
    value: int
    wdl: tuple[int, int, int]
    fen: str

    def to_dict(self):
        return self._asdict()
