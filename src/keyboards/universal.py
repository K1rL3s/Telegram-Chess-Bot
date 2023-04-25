from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.consts import CallbackData


main_menu_button = InlineKeyboardButton('🏠Главное меню', callback_data=CallbackData.OPEN_MAIN_MENU.value)
settings_button = InlineKeyboardButton('⚙️Настройки', callback_data=CallbackData.OPEN_SETTINGS.value)
advanced_settings_button = InlineKeyboardButton('⚙️Настройки', callback_data=CallbackData.OPEN_SETTINGS_ADVANCED.value)
rules_help_button = InlineKeyboardButton('📜Правила', callback_data=CallbackData.OPEN_RULES_HELP.value)
game_menu_button = InlineKeyboardButton('♟️Играть', callback_data=CallbackData.OPEN_GAME_MENU.value)
statistics_button = InlineKeyboardButton('📃Статистика', callback_data=CallbackData.OPEN_STATISTIC.value)
global_statistics_button = InlineKeyboardButton(
    '📃Общая статистика',
    callback_data=CallbackData.OPEN_GLOBAL_STATISTIC.value
)


start_keyboard = InlineKeyboardMarkup().row(
    main_menu_button,
    InlineKeyboardButton('⭐Про бота', callback_data=CallbackData.ABOUT_BOT.value)
)

main_menu_keyboard = InlineKeyboardMarkup().row(
    game_menu_button
).row(
    settings_button,
    rules_help_button,
    statistics_button
)

back_to_main_menu_keyboard = InlineKeyboardMarkup().row(
    main_menu_button
)

after_stats_keyboard = InlineKeyboardMarkup().row(
    main_menu_button,
    settings_button,
    game_menu_button,
).row(
    global_statistics_button,
)

def get_main_menu_settings_game_keyboard(setting_button: InlineKeyboardButton = settings_button):
    """
    На место кнопки с настройками можно засунуть другую.
    Используется, чтобы вставить кнопку с продвинутыми настройками после настройки таковых.
    """

    return InlineKeyboardMarkup().row(
        main_menu_button,
        setting_button,
        game_menu_button
    )
