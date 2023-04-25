from aiogram import Dispatcher

from src.middlewares.throttling import ThrottlingMiddleware
from src.middlewares.callbacks import CallbackQueryMiddleware
from src.middlewares.logging import LoggingMiddleware
from src.middlewares.states import ChessGameStateMiddleware


def setup_middlewares(dp: Dispatcher):
    dp.middleware.setup(CallbackQueryMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(LoggingMiddleware())
    dp.middleware.setup(ChessGameStateMiddleware(dp))
