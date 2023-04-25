from aiogram import Dispatcher

from src.handlers.start import register_start
from src.handlers.settings import register_settings
from src.handlers.game import register_game
from src.handlers.errors import register_errors


def register_client_handlers(dp: Dispatcher):
    register_start(dp)
    register_settings(dp)
    register_game(dp)


def register_error_handlers(dp: Dispatcher):
    register_errors(dp)
