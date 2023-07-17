from aiogram import types, Dispatcher

from src.consts import CallbackData
from src.keyboards import (
    start_keyboard, main_menu_keyboard,
    back_to_main_menu_keyboard, get_main_menu_settings_game_keyboard,
    after_stats_keyboard,
)
from src.db.db_funcs import create_new_user, get_user, get_global_statistic


about_message = """
Привет! 👋
Я [шахматный чат-бот проект](https://github.com/K1rL3s/Telegram-Chess-Bot) для Яндекс Лицея 2022/2023.
Если я не отвечаю при открытии настроек или тому подобное, то напиши /start
"""  # noqa

rules_help_message = """
Правила шахмат:
...

Пишите ходы в формате "*КлеткаКлетка*" на английском, например: "*e2e4*", "*a8b8*".

Для превращения пешки надо добавить букву фигуры в ход, например: "*c7c8q*" - превращение в королеву.
*q* - королева, *r* - ладья, *b* - слон, *n* - конь. 

...
"""  # noqa


async def start(message: types.Message):
    """
    Обработчик /start.
    """

    await create_new_user(
        message.from_user.id,
        (
                message.from_user.username or
                message.from_user.first_name or
                message.from_user.last_name
        )  # XD
    )
    await message.reply(
        about_message, reply_markup=start_keyboard,
        parse_mode='markdown'
    )


async def main_menu(message: types.Message | types.CallbackQuery):
    """
    Обработчик /menu, /меню и кнопок "Главное меню"
    """

    if isinstance(message, types.CallbackQuery):
        message = message.message

    text = "Привет, я - *меню!*\n" \
           "Если я не отвечаю при открытии настроек или тому подобное, " \
           "то напиши /start"

    await message.reply(
        text,
        reply_markup=main_menu_keyboard,
        parse_mode='markdown'
    )


async def about(message: types.Message | types.CallbackQuery):
    """
    Обработчик /about и кнопки "Про бота"
    """

    if isinstance(message, types.CallbackQuery):
        message = message.message

    await message.reply(
        about_message,
        reply_markup=back_to_main_menu_keyboard,
        parse_mode='markdown'
    )


async def rules_help(message: types.Message | types.CallbackQuery):
    """
    Обработчик кнопки "Правила/Помощь"
    """

    if isinstance(message, types.CallbackQuery):
        message = message.message

    await message.reply(
        rules_help_message,
        reply_markup=get_main_menu_settings_game_keyboard(),
        parse_mode='markdown'
    )


async def statistic(callback: types.CallbackQuery):
    """
    Обработчик нажатия кнопки "Статистика".
    """

    user = get_user(callback.from_user.id)
    message = '\n'.join(
        (
            f'*Статистика!*\n',
            f'Игр - *{user.total_games}*',
            f'Побед - *{user.total_wins}*',
            f'Ничьей - *{user.total_draws}*',
            f'Поражений - *{user.total_defeats}*',
            f'Винрейт - '
            f'*{user.total_wins / (user.total_games or 1) * 100:.0f}%*',
        )
    )
    await callback.message.reply(
        message,
        parse_mode='markdown',
        reply_markup=after_stats_keyboard
    )


async def global_statistic(callback: types.CallbackQuery):
    """
    Обработчик нажатия кнопки "Общая Статистика".
    """

    top_users = await get_global_statistic()
    await callback.message.reply(
        top_users,
        parse_mode='markdown',
        reply_markup=get_main_menu_settings_game_keyboard()
    )


def register_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])

    dp.register_callback_query_handler(
        main_menu,
        text=CallbackData.OPEN_MAIN_MENU.value
    )
    dp.register_message_handler(main_menu, commands=['menu', 'меню'])

    dp.register_callback_query_handler(
        about,
        text=CallbackData.ABOUT_BOT.value
    )
    dp.register_message_handler(about, commands=['about'])

    dp.register_callback_query_handler(
        rules_help,
        text=CallbackData.OPEN_RULES_HELP.value
    )
    dp.register_message_handler(rules_help, commands=['rules', 'правила'])

    dp.register_callback_query_handler(
        statistic,
        text=CallbackData.OPEN_STATISTIC.value
    )
    dp.register_callback_query_handler(
        global_statistic,
        text=CallbackData.OPEN_GLOBAL_STATISTIC.value
    )
