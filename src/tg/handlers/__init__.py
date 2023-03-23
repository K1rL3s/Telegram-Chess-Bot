from aiogram import Dispatcher

from src.tg.handlers.start import register_start
from src.tg.handlers.settings import register_settings


def register_client_handlers(dp: Dispatcher):
    register_start(dp)
    register_settings(dp)
