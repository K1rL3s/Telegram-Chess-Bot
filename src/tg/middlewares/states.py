from aiogram import types, Dispatcher
from loguru import logger

from src.tg.middlewares.base import MyBaseMiddleware
from src.tg.consts import CallbackData


class ChessGameStateMiddleware(MyBaseMiddleware):
    """
    Мидлварь, который отменяет состояние игры, если пользователь нажал на что-то, не относящее к игре,
    или написал какую-то команду.
    """

    def __init__(self, dispatcher: Dispatcher):
        super().__init__()
        self.dispatcher = dispatcher

    async def on_pre_process_callback_query(self, callback: types.CallbackQuery, data: dict):
        state = await self.dispatcher.storage.get_state(
            chat=types.Chat.get_current().id,
            user=types.User.get_current().id
        )
        if not state:
            return
        if state.startswith('ChessGame') and \
                not callback.data.startswith(CallbackData.GAME_STATE_PREFIX.value):
            await self.dispatcher.current_state(
                chat=types.Chat.get_current().id,
                user=types.User.get_current().id
            ).finish()
            logger.debug(f'Состояние игры отменено кнопкой [{self.get_short_info(callback)}]')

    async def on_pre_process_message(self, message: types.Message, data: dict):
        state = await self.dispatcher.storage.get_state(
            chat=types.Chat.get_current().id,
            user=types.User.get_current().id
        )
        if not state:
            return
        if state.startswith('ChessGame') and message.is_command():
            await self.dispatcher.current_state(
                chat=types.Chat.get_current().id,
                user=types.User.get_current().id
            ).finish()
            logger.debug(f'Состояние игры отменено командой [{self.get_short_info(message)}]')
