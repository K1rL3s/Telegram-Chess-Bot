from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.db.games import Game
from src.consts import CallbackData
from src.tg.keyboards.universal import rules_help_button, main_menu_button, statistics_button


continue_game_button = InlineKeyboardButton('⏯Продолжить игру', callback_data=CallbackData.PLAY_OLD_GAME.value)
pause_game_button = InlineKeyboardButton('⏸️Пауза', callback_data=CallbackData.OPEN_GAME_MENU.value)
hint_button = InlineKeyboardButton('💡Подсказка', callback_data=CallbackData.GET_MOVE_TIP.value)
resign_button = InlineKeyboardButton('🇫🇷Cдаться', callback_data=CallbackData.RESIGN.value)


def pre_game_keyboard(current_game: Game | None) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    if current_game:
        keyboard.add(continue_game_button)
    keyboard.insert(
        InlineKeyboardButton('🆕Новая игра', callback_data=CallbackData.PLAY_NEW_GAME.value),
    ).row(
        main_menu_button,
        rules_help_button,
        statistics_button
    )
    return keyboard


choose_color_keyboard = InlineKeyboardMarkup().row(
    InlineKeyboardButton('♙Белый', callback_data=CallbackData.COLOR_WHITE.value),
    InlineKeyboardButton('♟️Чёрный', callback_data=CallbackData.COLOR_BLACK.value)
).row(
    InlineKeyboardButton('⏪Назад', callback_data=CallbackData.OPEN_GAME_MENU.value)
)

game_conitnue_keyboard = InlineKeyboardMarkup().row(
    pause_game_button,
    hint_button,
    resign_button
)

illegal_move_keyboard = InlineKeyboardMarkup().row(
    pause_game_button,
    hint_button
).row(
    rules_help_button,
    resign_button,
)

after_tip_keyboard = InlineKeyboardMarkup().row(
    pause_game_button,
    resign_button
)

are_you_sure_resign_keyboard = InlineKeyboardMarkup().row(
    continue_game_button,
    InlineKeyboardButton('🇫🇷Cдаться', callback_data=CallbackData.RESIGN_SURE.value),
)

game_end_keyboard = InlineKeyboardMarkup().row(
    main_menu_button,
    statistics_button
)
