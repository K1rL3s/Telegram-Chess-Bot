from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from src.chess_api.get_limits import get_limits, get_defaults
from src.db.settings import Settings
from src.consts import CallbackData, Emojies, Prefixes
from src.keyboards import (
    simple_settings_keyboard, advanced_settings_keyboard,
    edit_setting_keyboard,
    cancel_edit_setting_keyboard, are_you_sure_reset_settings_keyboard,
    get_main_menu_settings_game_keyboard,
)
from src.keyboards.universal import advanced_settings_button, settings_button
from src.db.db_funcs import get_settings, update_settings
from src.utils.tg.states import EditSetting


# Названия простых и продвинутых настроек в базе данных
simple_settings = (
    'skill_level', 'elo',
    'with_coords', 'size'
)
advanced_settings = (
    'min_time', 'max_time',
    'threads', 'depth',
    'ram_hash', 'colors'
)

# Перевод параметра настроек на русский
attr_to_ru_with_description = {
    "min_time": (
        "Мин. время (мс)",
        "Минимальное время движка на подумать"
    ),
    "max_time": (
        "Макс. время (мс)",
        "Максимальное время движка на подумать"
    ),
    "threads": (
        "Потоки",
        "Количество потоков процессора движка\nЧем больше, тем движок сильнее"
    ),
    "depth": (
        "Глубина",
        "Глубина просчёта ходов движка\nЧем больше, тем движок сильнее"
    ),
    "ram_hash": (
        "Память (МБ)",
        "Количество оперативной памяти движка\nЧем больше, тем движок сильнее"
    ),
    "skill_level": (
        "Уровень игры",
        "Уровень игры движка\nЧем больше, тем движок сильнее"
    ),
    "elo": (
        "ЭЛО",
        "ЭЛО движка\nЧем больше, тем движок сильнее"
    ),
    "colors": (
        "Цвета доски",
        "Цвета клеток, координат доски\nМеняет изображение доски"
    ),
    "with_coords": (
        "Координаты",
        "С координатами поле или без\nМеняет изображение доски"
    ),
    "size": (
        "Размер (пискели)",
        "Размер изображения доски, которое присылает бот после своего хода\n"
        "Меняет изображение доски"
    )
}

edit_setting_message = f"""
Чтобы изменить числовую настройку, *напишите число в допустимом диапазоне*.
"""

edit_color_message = f"""
Для настройки цветов клеток и координат напишите сообщение в формате ниже.
*rrggbb* - HEX формат цвета.
*[aa]* - прозрачность при необходимости.
```
...
ключ1 - rrggbb[aa]
ключ2 - rrggbb[aa]
...
```
Доступные ключи:
`square light` (белые клетки),
`square dark` (черные клетка),
`square light lastmove` (белая клетка последний ход),
`square dark lastmove` (чёрная клетка последний ход),
`margin` (фон координат),
`coord` (числа и буквы).

Пример сообщения:
```
square light - ff000088
square dark - 00ff00
margin - ffffff
coord - 000000
```
"""

succes_edit_message = 'Значение *"{}"* успешно изменено на *{}*'.format


def format_settings_value_by_attr(user_id: int, attr: str,
                                  settings: Settings = None,
                                  limit: int = 15) -> str:
    """
    Красивое отображение булевских значений настроек,
    принимается параметр настроек.

    :param user_id: Юзер айди.
    :param attr: Параметр настроек.
    :param settings: Настройки пользователя,
    чтобы не вызывать get_settings много раз.
    :param limit: Максимальная длина значения.
    :return: Красивое отображение.
    """

    if settings is None:
        settings = get_settings(user_id)
    return format_settings_value(getattr(settings, attr), limit)


def format_settings_value(value: str | bool, limit: int = 15) -> str:
    """
    Красивое отображение значений, принимается значение.

    :param value:
    :param limit:
    :return: Красиво.
    """

    if isinstance(value, bool):  # Если настройка булевского типа
        return Emojies.YES_EMOJI.value if value else Emojies.NO_EMOJI.value

    if value is None:
        value = 'по умолчанию'
    elif not isinstance(value, int):
        value = str(value)
        if limit:
            value = value if len(value) < limit else (value[:limit] + '...')
    return value


def generate_settings_message(user_id: int,
                              settings_attrs: tuple[str, ...] | list[
                                  str]) -> str:
    """
    Делает сообщение с настройками пользователя.

    :param user_id: Юзер айди.
    :param settings_attrs: Список/Кортеж настроек.
    :return: Сообщение.
    """

    settings = get_settings(user_id)

    message = (
        f'`{attr_to_ru_with_description[attr][0]:<17}` –  '
        f'*{format_settings_value_by_attr(user_id, attr, settings=settings)}*'
        for attr in settings_attrs
    )

    return '\n'.join(message)


async def generate_setting_preview_message(user_id: int, attr: str) -> str:
    """
    Делает развернутое сообщение про выбранные параметр настроек.

    :param user_id: Юзер айди.
    :param attr: Параметр (как имя колонки в базе данных).
    :return: Сообщение.
    """

    name, desc = attr_to_ru_with_description[attr]
    if isinstance(
        value := format_settings_value_by_attr(user_id, attr, limit=0),
        str
    ):
        message = (
            f'*{name}*',
            f'Текущее значение - *{value}*',
            f'\n{desc}'
        )
    else:
        attr = (await get_limits())[attr]
        message = (
            f'*{name}*',
            f'Текущее значение - *{value}*',
            f'Минимум - *{attr["min"]}*',
            f'Дефолт - *{attr["default"]}*',
            f'Максимум - *{attr["max"]}*',
            f'\n{desc}'
        )
    return '\n'.join(message)


def edit_color_message_value(text: str):
    """
    Обработчик текста сообщения для изменения цвета доски.
    """

    try:
        colors = ';'.join(
            [
                # 20 - наибольший ключ, 8 - rrggbbaa
                f"{k[:20]}-{v.strip('# .,;:')[:8]}" for k, v in
                [s.split(' - ') for s in text.splitlines() if s]
            ][:6]  # 6 - доступных ключей
        )
    except ValueError:
        return None
    return colors


async def settings_menu(callback: types.CallbackQuery):
    """
    Обработчик кнопки "Настройки".
    """

    if callback.data.replace(CallbackData.OPEN_SETTINGS.value, ''):
        settings_attrs = advanced_settings
        settings_keyboard = advanced_settings_keyboard
    else:
        settings_attrs = simple_settings
        settings_keyboard = simple_settings_keyboard

    settings_message = generate_settings_message(
        callback.from_user.id, settings_attrs
    )
    message = '*Настройки!*\nТекущие настройки:\n\n' + settings_message
    await callback.message.reply(
        message,
        reply_markup=settings_keyboard,
        parse_mode='markdown'
    )


async def preview_setting(callback: types.CallbackQuery):
    """
    Обработчик нажатия кнопки любого параметра настроек.
    """

    message = await generate_setting_preview_message(
        callback.from_user.id,
        attr := callback.data.lower().replace(Prefixes.EDIT_PREFIX.value, '')
    )
    await callback.message.reply(
        message,
        reply_markup=edit_setting_keyboard(attr),
        parse_mode='markdown'
    )


async def reset_current_setting(callback: types.CallbackQuery):
    """
    Обработчик сброса выбранного параметра настроек.
    """

    attr = callback.data.replace(CallbackData.RESET_SETTING.value, '').lower()

    default = (await get_defaults())[attr]
    new_value = (
        await update_settings(callback.from_user.id, **{attr: default})
    )[attr]

    name = attr_to_ru_with_description[attr][0]
    setting_button = (settings_button
                      if attr in simple_settings
                      else advanced_settings_button)

    await callback.message.reply(
        succes_edit_message(name, format_settings_value(new_value, limit=0)),
        reply_markup=get_main_menu_settings_game_keyboard(setting_button),
        parse_mode='markdown'
    )


async def start_state_edit_setting(callback: types.CallbackQuery,
                                   state: FSMContext):
    """
    Обработчик нажатия кнопки "Изменить"
    при просмотре любого параметра настроек.
    """

    attr = callback.data.replace(CallbackData.START_EDIT_SETTING.value,
                                 '').lower()

    if 'color' in attr:
        message = edit_color_message
    elif isinstance(format_settings_value_by_attr(callback.from_user.id, attr),
                    str):
        return await edit_bool_setting(callback.message, callback.from_user.id,
                                       attr)
    else:
        message = edit_setting_message

    await EditSetting.edit_setting.set()

    async with state.proxy() as data:
        data['attr'] = attr

    await callback.message.reply(
        message,
        reply_markup=cancel_edit_setting_keyboard,
        parse_mode='markdown'
    )


async def edit_bool_setting(message: types.Message, user_id: int, attr: str):
    """
    Обработчик нажатия кнопки "Изменить"
    при просмотре параметра булевского типа.
    """

    settings = get_settings(user_id)
    await update_settings(user_id, **{attr: not getattr(settings, attr)})
    await message.edit_text(
        await generate_setting_preview_message(user_id, attr),
        parse_mode="markdown",
        reply_markup=edit_setting_keyboard(attr)
    )


async def edit_setting(message: types.Message, state: FSMContext):
    """
    Обработчик сообщения после начала изменения любого параметра настроек.
    """

    async with state.proxy() as data:
        attr = data['attr']

    text = message.text.lower()

    if isinstance(format_settings_value_by_attr(message.from_user.id, attr),
                  str):
        if 'color' in attr:
            value = edit_color_message_value(message.text)
        else:
            value = None
    else:
        value = int(text) if text.isdigit() else None

    name = attr_to_ru_with_description[attr][0]
    if value is None:
        await message.reply(
            f'*{name}*\n'
            f'Не удалось обработать это сообщение, попробуйте ещё раз',
            reply_markup=cancel_edit_setting_keyboard,
            parse_mode='markdown'
        )
        return

    new_value = (await update_settings(message.from_user.id, **{attr: value}))[
        attr]
    setting_button = (settings_button
                      if attr in simple_settings
                      else advanced_settings_button)

    await message.reply(
        succes_edit_message(name, format_settings_value(new_value, limit=0)),
        reply_markup=get_main_menu_settings_game_keyboard(setting_button),
        parse_mode='markdown'
    )

    await state.finish()


async def cancel_state_edit_setting(callback: types.CallbackQuery,
                                    state: FSMContext):
    """
    Обработчик нажатия кнопки "Отмена" во время изменения любого параметра.
    """

    async with state.proxy() as data:
        attr = data["attr"]

    setting_button = (settings_button
                      if attr in simple_settings
                      else advanced_settings_button)

    await callback.message.reply(
        f'Изменение *"{attr_to_ru_with_description[attr][0]}"* отменено',
        reply_markup=get_main_menu_settings_game_keyboard(setting_button),
        parse_mode='markdown'
    )
    await state.finish()


async def reset_all_settings(callback: types.CallbackQuery):
    """
    Обработчик подтверждения сброса всех настроек.
    """

    is_sure = callback.data.replace(CallbackData.RESET_ALL_SETTINGS.value, '')

    if not is_sure:
        await callback.message.reply(
            "Вы уверены, "
            "что хотите сбросить все настройки на значения по умолчанию?",
            reply_markup=are_you_sure_reset_settings_keyboard
        )
        return

    await update_settings(callback.from_user.id, **(await get_defaults()))
    await callback.message.reply(
        "Настройки сброшены на значения по умолчанию",
        reply_markup=get_main_menu_settings_game_keyboard()
    )


def register_settings(dp: Dispatcher):
    dp.register_callback_query_handler(cancel_state_edit_setting,
                                       state=EditSetting)

    dp.register_callback_query_handler(
        settings_menu,
        lambda callback: callback.data.startswith(
            CallbackData.OPEN_SETTINGS.value
        )
    )
    dp.register_callback_query_handler(
        preview_setting,
        lambda callback: callback.data.startswith(Prefixes.EDIT_PREFIX.value)
    )
    dp.register_callback_query_handler(
        start_state_edit_setting,
        lambda callback: callback.data.startswith(
            CallbackData.START_EDIT_SETTING.value
        )
    )
    dp.register_message_handler(edit_setting, state=EditSetting.edit_setting)
    dp.register_callback_query_handler(
        reset_current_setting,
        lambda callback: callback.data.startswith(
            CallbackData.RESET_SETTING.value
        )
    )

    dp.register_callback_query_handler(
        reset_all_settings,
        lambda callback: callback.data.startswith(
            CallbackData.RESET_ALL_SETTINGS.value
        )
    )
