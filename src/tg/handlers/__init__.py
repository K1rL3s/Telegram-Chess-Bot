from aiogram import Dispatcher

from src.tg.handlers.start import register_start
from src.tg.handlers.settings import register_settings
from src.tg.handlers.game import register_game
from src.tg.handlers.errors import register_errors


def register_client_handlers(dp: Dispatcher):
    register_start(dp)
    register_settings(dp)
    register_game(dp)


def register_error_handlers(dp: Dispatcher):
    register_errors(dp)
