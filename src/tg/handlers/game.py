from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from src.chess_api import get_board_image, get_engine_move, get_engine_evaluation
from src.db.games import Game
from src.tg.consts import CallbackData
from src.tg.keyboards import (
    pre_game_keyboard, choose_color_keyboard, game_conitnue_keyboard,
    game_end_keyboard, after_tip_keyboard
)
from src.tg.keyboards.game import are_you_sure_resign_keyboard
from src.tg.utils.db_funcs import (
    get_settings, get_current_game, create_new_game,
    update_current_game, stop_current_game
)

i_move_your_turn = 'Я сделал ход "*{}*".'.format


class ChessGame(StatesGroup):
    """
    Пока пользователь в состоянии этой группы, все его текстовые сообщения будут отлавливаться
    обработчиком ходов. При нажатии на любую кнопку состояния прекращается.
    """
    playing = State()


def stop_game(user_id: int) -> str:
    """
    Останавливает игру и возвращает сообщение с итогом.
    :param user_id: Юзер айди.
    :return: Сообщение с итогом.
    """

    evaluation = stop_current_game(user_id)
    message = 'Игра закончилась *{}!*'.format
    if evaluation.end_type != 'checkmate':
        return message('ничьёй')
    return message(f"победой {'белых' if evaluation.value > 0 else 'черных'} (mate in {abs(evaluation.value)})")


def get_evaluation_comment(game: Game) -> str:
    """
    Даёт сообщение с оценкой позиции, нужно при Settings.with_position_evaluation == True

    :param game: Текушая игра.
    :return: Сообщение с оценкой позиции.
    """

    evaluation = get_engine_evaluation(fen=game.fen)
    return '\n' + '\n'.join((
        f'*Оценка позиции*',
        f'Тип оценки: *{evaluation.end_type}*',
        f'Значение: *{evaluation.value / 100 if evaluation.end_type == "cp" else evaluation.value}*',
        f'W/D/L: *{" / ".join(map(str, evaluation.wdl))}*'
    ))


async def pre_game_menu(callback: types.CallbackQuery):
    """
    Обработчик нажатия кнопки "Играть"
    """

    game = get_current_game(callback.from_user.id)
    await callback.message.reply(
        "*Игровое меню!*\n\nВыберите, что хотите увидеть, продолжить или начать.",
        parse_mode='markdown',
        reply_markup=pre_game_keyboard(game)
    )


async def choose_color(callback: types.CallbackQuery):
    """
    Обработчик нажатия кнопки "Новая игра"
    """

    await callback.message.reply(
        "*Новая игра!*\nВыберите цвет, за который будете играть.",
        parse_mode='markdown',
        reply_markup=choose_color_keyboard
    )


async def color_chosen(callback: types.CallbackQuery):
    """
    Обработчик нажатия кнопок с выбором цвета.
    """

    color = callback.data.replace(CallbackData.CHOOSE_COLOR_PREFIX.value, '')
    create_new_game(callback.from_user.id, color)

    if color == 'b':
        state = await ChessGame.playing.set()  # state = None
        await user_move(callback, state, is_user_black=True)
    else:
        await continue_old_game(callback)


async def continue_old_game(callback: types.CallbackQuery):
    """
    Обработчик нажатия кнопки "Продолжить игру".
    Используется функцией color_chosen для генерации первого сообщения при игре за белых.
    """

    if not (game := get_current_game(callback.from_user.id)):
        return
    await ChessGame.playing.set()
    settings = get_settings(callback.from_user.id)
    image = get_board_image(
        fen=game.fen,
        last_move=game.last_move,
        check=game.check,
        orientation=game.orientation,
        **settings.get_params()
    )

    if not game.prev_moves:
        caption = '*Твой ход!*'
    else:
        caption = i_move_your_turn(game.last_move)

    if settings.with_position_evaluation:
        caption += get_evaluation_comment(game)

    await callback.message.reply_photo(
        image,
        caption,
        parse_mode='markdown',
        reply_markup=game_conitnue_keyboard
    )


async def user_move(message: types.Message | types.CallbackQuery, state: FSMContext, is_user_black: bool = False):
    """
    Обработчик сообщения с ходом.
    Используется функцией color_chosen для генерации первого сообщения при игре за черных.

    is_user_black: Юзер играет за черных и это первый ход.
    """

    if is_user_black:
        move = ''
    else:
        move = ''.join(message.text.strip().lower().replace('-', '').split())

    game = get_current_game(message.from_user.id)
    settings = get_settings(message.from_user.id)
    data = get_engine_move(
        user_move=move,
        prev_moves=game.prev_moves,
        orientation=game.orientation,
        **settings.get_params()
    )

    if data is None:
        await message.reply(
            'Это *нелегальный* ход',
            parse_mode='markdown',
            reply_markup=game_conitnue_keyboard
        )
        return

    update_current_game(
        message.from_user.id,
        prev_moves=data.prev_moves,
        last_move=data.stockfish_move,
        check=data.check,
        fen=data.fen,
    )
    image = get_board_image(
        fen=data.fen,
        last_move=data.stockfish_move,
        check=data.check,
        orientation=game.orientation,
        **settings.get_params()
    )

    if data.end_type:
        await state.finish()
        keyboard = game_end_keyboard
        caption = stop_game(message.from_user.id)
    else:
        keyboard = game_conitnue_keyboard
        caption = i_move_your_turn(data.stockfish_move)

        if settings.with_position_evaluation:
            caption += get_evaluation_comment(game)

    if isinstance(message, types.CallbackQuery):
        message = message.message

    await message.reply_photo(
        image,
        caption,
        parse_mode='markdown',
        reply_markup=keyboard
    )


async def move_tip(callback: types.CallbackQuery, state: FSMContext):
    """
    Обработчик нажатия кнопки "Подсказка".
    """

    game = get_current_game(callback.from_user.id)
    settings = get_settings(callback.from_user.id)

    data = get_engine_move(
        user_move=None,
        prev_moves=game.prev_moves,
        orientation='b',
        **settings.get_params()
    )
    await callback.message.reply(
        f'Я бы сделал ход "*{data.stockfish_move}*"',
        parse_mode='markdown',
        reply_markup=after_tip_keyboard
    )


async def resign(callback: types.CallbackQuery, state: FSMContext):
    """
    Обработчик нажатия кнопки "Сдаться".
    """

    is_sure = callback.data.replace(CallbackData.RESIGN.value, '')
    if not is_sure:
        await callback.message.reply(
            "Вы уверены, что хотите сдаться?",
            reply_markup=are_you_sure_resign_keyboard
        )
        return

    await state.finish()
    message = stop_game(callback.from_user.id)
    await callback.message.reply(
        message,
        parse_mode='markdown',
        reply_markup=game_end_keyboard
    )


def register_game(dp: Dispatcher):
    dp.register_callback_query_handler(pre_game_menu, text=CallbackData.OPEN_GAME_MENU.value)
    dp.register_callback_query_handler(choose_color, text=CallbackData.PLAY_NEW_GAME.value)
    dp.register_callback_query_handler(
        color_chosen,
        lambda callback: callback.data.startswith(CallbackData.CHOOSE_COLOR_PREFIX.value)
    )
    dp.register_message_handler(user_move, state=ChessGame.playing)
    dp.register_callback_query_handler(
        continue_old_game,
        text=CallbackData.PLAY_OLD_GAME.value,
    )
    dp.register_callback_query_handler(
        move_tip,
        text=CallbackData.GET_MOVE_TIP.value,
        state=ChessGame.playing
    )
    dp.register_callback_query_handler(
        resign,
        lambda callback: callback.data.startswith(CallbackData.RESIGN.value),
        state=ChessGame.playing
    )
