from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.tg.consts import CallbackData

start_keyboard = InlineKeyboardMarkup().row(
    InlineKeyboardButton('🏠Главное меню', callback_data=CallbackData.OPEN_MAIN_MENU.value),
    InlineKeyboardButton('⭐Про бота', callback_data=CallbackData.ABOUT_BOT.value)
)


main_menu_keyboard = InlineKeyboardMarkup().row(
    InlineKeyboardButton('♟️Играть', callback_data=CallbackData.OPEN_GAME_MENU.value)
).row(
    InlineKeyboardButton('⚙️Настройки', callback_data=CallbackData.OPEN_SETTINGS.value),
    InlineKeyboardButton('📜Правила/Помощь', callback_data=CallbackData.OPEN_RULES_HELP.value),
)

back_to_main_menu_keyboard = InlineKeyboardMarkup().row(
    InlineKeyboardButton('🏠Главное меню', callback_data=CallbackData.OPEN_MAIN_MENU.value)
)

settings_keyboard = InlineKeyboardMarkup().row(
    InlineKeyboardButton('🏠Главное меню', callback_data=CallbackData.OPEN_MAIN_MENU.value),
    InlineKeyboardButton('🔁Вернуть по умолчанию', callback_data=CallbackData.RESET_ALL_SETTINGS.value)
).row(
    InlineKeyboardButton('⌛Минимальное время', callback_data=CallbackData.EDIT_MIN_TIME.value),
    InlineKeyboardButton('⏳Максимальное время', callback_data=CallbackData.EDIT_MAX_TIME.value),
).row(
    InlineKeyboardButton('💻Потоки', callback_data=CallbackData.EDIT_THREADS.value),
    InlineKeyboardButton('💻Глубина', callback_data=CallbackData.EDIT_DEPTH.value),
    InlineKeyboardButton('💻Память', callback_data=CallbackData.EDIT_RAM_HASH.value)
).row(
    InlineKeyboardButton('🧠Уровень игры', callback_data=CallbackData.EDIT_SKILL_LEVEL.value),
    InlineKeyboardButton('🧠ЭЛО', callback_data=CallbackData.EDIT_ELO.value),
    InlineKeyboardButton('🧠Оценка', callback_data=CallbackData.EDIT_WITH_POSITION_EVALUATION.value)
).row(
    InlineKeyboardButton('🌈Цвета', callback_data=CallbackData.EDIT_COLORS.value),
    InlineKeyboardButton('🧭Координаты', callback_data=CallbackData.EDIT_WITH_COORDS.value),
    InlineKeyboardButton('💥Размеры', callback_data=CallbackData.EDIT_SIZE.value)
)

after_edit_settings_keyboard = InlineKeyboardMarkup().row(
    InlineKeyboardButton('🏠Главное меню', callback_data=CallbackData.OPEN_MAIN_MENU.value),
    InlineKeyboardButton('⚙️Настройки', callback_data=CallbackData.OPEN_SETTINGS.value)
)

are_you_sure_reset_settings_keyboard = InlineKeyboardMarkup().row(
    InlineKeyboardButton('✅Сбросить', callback_data=CallbackData.RESET_ALL_SETTINGS_SURE.value),
    InlineKeyboardButton('❌Отмена', callback_data=CallbackData.OPEN_SETTINGS.value)
)

cancel_edit_setting_keyboard = InlineKeyboardMarkup().row(
    InlineKeyboardButton('❌Отмена', callback_data=CallbackData.STOP_EDIT_SETTING.value)
)


def edit_setting_keyboard(attr: str):
    return InlineKeyboardMarkup().row(
        InlineKeyboardButton('✍Изменить', callback_data=CallbackData.START_EDIT_SETTING.value + f'{attr}'),
        InlineKeyboardButton('🔁Сбросить', callback_data=CallbackData.RESET_SETTING.value + f'{attr}'),
    ).row(
        InlineKeyboardButton('⚙️Назад', callback_data=CallbackData.OPEN_SETTINGS.value)
    )
