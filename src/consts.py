import os
from enum import Enum

from dotenv import load_dotenv

import httpx


load_dotenv()


class Config:
    CHESS_TG_TOKEN = os.getenv("CHESS_TG_TOKEN")
    API_URL = os.getenv("API_URL")
    LOG_CHAT = os.getenv('LOG_CHAT')
    UPS = int(os.getenv('UPS') or 0)
    CACHE_LIMIT_REQUEST = int(os.getenv('CACHE_LIMIT_REQUEST') or 0)
    CACHE_GLOBAL_TOP = int(os.getenv('CACHE_GLOBAL_TOP') or 0)
    GLOBAL_TOP = int(os.getenv('GLOBAL_TOP') or 10)

    # Начальная позиция в шахматах по FEN
    START_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    TIMEOUT = 30

    api_headers = {"Authorization": os.getenv('API_AUTH_KEY')}
    api_session = httpx.AsyncClient(
        follow_redirects=True, timeout=TIMEOUT
    )


class Prefixes(Enum):
    EDIT_PREFIX = 'edit_'
    PREGAME_PREFIX = 'pregame_'
    CHOOSE_COLOR_PREFIX = PREGAME_PREFIX + 'choose_color_'  # noqa
    GAME_STATE_PREFIX = 'state_game_'


class CallbackData(Enum):
    OPEN_MAIN_MENU = 'open_main_menu'
    OPEN_GAME_MENU = 'open_game_menu'
    OPEN_RULES_HELP = 'open_rules_help'
    OPEN_SETTINGS = 'open_settings_'
    OPEN_SETTINGS_ADVANCED = OPEN_SETTINGS + 'advanced'  # noqa
    OPEN_STATISTIC = 'open_statistic'
    OPEN_GLOBAL_STATISTIC = 'open_global_statistic'
    ABOUT_BOT = 'about_bot'

    RESET_ALL_SETTINGS = 'reset_all_settings'
    RESET_ALL_SETTINGS_SURE = RESET_ALL_SETTINGS + '_sure'  # noqa
    START_EDIT_SETTING = 'start_edit_setting_'
    RESET_SETTING = 'reset_setting_'
    STOP_EDIT_SETTING = 'stop_edit_setting'
    EDIT_MIN_TIME = Prefixes.EDIT_PREFIX.value + 'min_time'
    EDIT_MAX_TIME = Prefixes.EDIT_PREFIX.value + 'max_time'
    EDIT_THREADS = Prefixes.EDIT_PREFIX.value + 'threads'
    EDIT_DEPTH = Prefixes.EDIT_PREFIX.value + 'depth'
    EDIT_RAM_HASH = Prefixes.EDIT_PREFIX.value + 'ram_hash'
    EDIT_SKILL_LEVEL = Prefixes.EDIT_PREFIX.value + 'skill_level'
    EDIT_ELO = Prefixes.EDIT_PREFIX.value + 'elo'
    EDIT_COLORS = Prefixes.EDIT_PREFIX.value + 'colors'
    EDIT_WITH_COORDS = Prefixes.EDIT_PREFIX.value + 'with_coords'
    EDIT_SIZE = Prefixes.EDIT_PREFIX.value + 'size'

    PLAY_OLD_GAME = Prefixes.PREGAME_PREFIX.value + 'play_old_game'
    PLAY_NEW_GAME = Prefixes.PREGAME_PREFIX.value + 'play_new_game'

    COLOR_WHITE = Prefixes.CHOOSE_COLOR_PREFIX.value + 'w'
    COLOR_BLACK = Prefixes.CHOOSE_COLOR_PREFIX.value + 'b'

    GET_MOVE_TIP = Prefixes.GAME_STATE_PREFIX.value + 'get_move_tip'
    RESIGN = Prefixes.GAME_STATE_PREFIX.value + 'resign'
    GET_POSITION_EVALUATION = (
            Prefixes.GAME_STATE_PREFIX.value + 'get_position_evaluation'
    )
    RESIGN_SURE = RESIGN + '_sure'  # noqa


class Emojies(Enum):
    YES_EMOJI = "✅"
    NO_EMOJI = "❌"
