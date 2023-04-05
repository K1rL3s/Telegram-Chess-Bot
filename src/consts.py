import os
from enum import Enum

import httpx


API_URL = os.getenv('API_URL')
TIMEOUT = 30

api_headers = {"Authorization": os.getenv('API_AUTH_KEY')}
api_session = httpx.AsyncClient(follow_redirects=True, timeout=TIMEOUT)


class CallbackData(Enum):
    OPEN_MAIN_MENU = 'open_main_menu'
    OPEN_GAME_MENU = 'open_game_menu'
    OPEN_RULES_HELP = 'open_rules_help'
    OPEN_SETTINGS = 'open_settings_'
    OPEN_SETTINGS_ADVANCED = OPEN_SETTINGS + '_advanced'  # noqa
    OPEN_STATISTIC = 'open_statistic'
    ABOUT_BOT = 'about_bot'

    RESET_ALL_SETTINGS = 'reset_all_settings'
    RESET_ALL_SETTINGS_SURE = RESET_ALL_SETTINGS + '_sure'  # noqa
    START_EDIT_SETTING = 'start_edit_setting_'
    RESET_SETTING = 'reset_setting_'
    STOP_EDIT_SETTING = 'stop_edit_setting'
    EDIT_PREFIX = 'edit_'
    EDIT_MIN_TIME = EDIT_PREFIX + 'min_time'  # noqa
    EDIT_MAX_TIME = EDIT_PREFIX + 'max_time'  # noqa
    EDIT_THREADS = EDIT_PREFIX + 'threads'  # noqa
    EDIT_DEPTH = EDIT_PREFIX + 'depth'  # noqa
    EDIT_RAM_HASH = EDIT_PREFIX + 'ram_hash'  # noqa
    EDIT_SKILL_LEVEL = EDIT_PREFIX + 'skill_level'  # noqa
    EDIT_ELO = EDIT_PREFIX + 'elo'  # noqa
    EDIT_COLORS = EDIT_PREFIX + 'colors'  # noqa
    EDIT_WITH_COORDS = EDIT_PREFIX + 'with_coords'  # noqa
    EDIT_WITH_POSITION_EVALUATION = EDIT_PREFIX + 'with_position_evaluation'  # noqa
    EDIT_SIZE = EDIT_PREFIX + 'size'  # noqa

    PLAY_OLD_GAME = 'play_old_game'
    PLAY_NEW_GAME = 'play_new_game'
    CHOOSE_COLOR_PREFIX = 'choose_color_'
    COLOR_WHITE = CHOOSE_COLOR_PREFIX + 'w'  # noqa
    COLOR_BLACK = CHOOSE_COLOR_PREFIX + 'b'  # noqa

    GAME_STATE_PREFIX = 'state_game_'
    GET_MOVE_TIP = GAME_STATE_PREFIX + 'get_move_tip'  # noqa
    RESIGN = GAME_STATE_PREFIX + 'resign'  # noqa
    RESIGN_SURE = RESIGN + '_sure'  # noqa
