from aiogram import types, Dispatcher
from aiogram.dispatcher.handler import CancelHandler
from loguru import logger

from src.utils.tg.states import ChessGame
from src.middlewares.base import MyBaseMiddleware
from src.consts import Prefixes


class ChessGameStateMiddleware(MyBaseMiddleware):
    """
    Мидлварь, который отменяет состояние игры, если пользователь нажал на что-то,
    не относящее к игре, или написал какую-то команду.
    Также ставит ChessGame.playing после обработки события с ChessGame.waiting.
    """

    def __init__(self, dispatcher: Dispatcher):
        super().__init__()
        self.dispatcher = dispatcher

    async def get_chessgame_state(self) -> str | None:
        state = await self.get_state()

        if not state:
            return
        if not state.startswith('ChessGame'):
            return

        return state

    async def set_playing_after_waiting(self, obj: types.Message | types.CallbackQuery, type_: str):

        if not (state := await self.get_chessgame_state()):
            return

        if state.endswith('waiting'):
            await ChessGame.playing.set()
            logger.debug(f'Возврат playing после waiting "{type_}" [{await self.get_short_info(obj)}]')


    async def on_pre_process_callback_query(self, callback: types.CallbackQuery, *_):
        if not (state := await self.get_chessgame_state()):
            return

        if callback.data.startswith(Prefixes.PREGAME_PREFIX.value) and state.endswith('waiting'):
            await callback.answer()
            logger.debug(f'Отмена обработки callback "{callback.data}" [{await self.get_short_info(callback)}]')
            raise CancelHandler()

        if not callback.data.startswith(Prefixes.GAME_STATE_PREFIX.value):
            await self.dispatcher.current_state(
                chat=types.Chat.get_current().id,
                user=types.User.get_current().id
            ).finish()
            logger.debug(f'Состояние игры отменено кнопкой [{await self.get_short_info(callback)}]')

    async def on_pre_process_message(self, message: types.Message, *_):
        if not await self.get_state():
            return

        if message.is_command():
            await self.dispatcher.current_state(
                chat=types.Chat.get_current().id,
                user=types.User.get_current().id
            ).finish()
            logger.debug(f'Состояние игры отменено командой [{await self.get_short_info(message)}]')

    async def on_post_process_message(self, message: types.Message, *_):
        await self.set_playing_after_waiting(message, 'message')

    async def on_post_process_callback_query(self, callback: types.CallbackQuery, *_):
        await self.set_playing_after_waiting(callback, 'callback')
