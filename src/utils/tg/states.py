from aiogram.dispatcher.filters.state import StatesGroup, State


class ChessGame(StatesGroup):
    """
    Пока пользователь в состоянии этой группы,
    все его текстовые сообщения будут отлавливаться обработчиком ходов.
    При нажатии на кнопку, не относящуюся к игре, или использовании команды,
    состояния прерываются.
    Waiting нужен, чтобы пользователь не жал всякое, пока бот думает.
    """
    playing = State()
    waiting = State()


class EditSetting(StatesGroup):
    """
    Состояние для отлова сообщения после начала изменения настроек.
    """
    edit_setting = State()
