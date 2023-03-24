from aiogram import Dispatcher

from src.tg.middlewares.throttling import ThrottlingMiddleware
from src.tg.middlewares.callbacks import CallbackQueryMiddleware
from src.tg.middlewares.logging import LoggingMiddleware
from src.tg.middlewares.states import ChessGameStateMiddleware


def setup_middlewares(dp: Dispatcher):
    dp.middleware.setup(CallbackQueryMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(LoggingMiddleware())
    dp.middleware.setup(ChessGameStateMiddleware(dp))
