from enum import Enum


class CallbackData(Enum):
    OPEN_MAIN_MENU = 'open_main_menu'
    OPEN_GAME_MENU = 'open_game_menu'
    OPEN_RULES_HELP = 'open_rules_help'
    OPEN_SETTINGS = 'open_settings'
    OPEN_STATISTIC = 'open_statistic'
    ABOUT_BOT = 'about_bot'

    RESET_ALL_SETTINGS = 'reset_all_settings'
    RESET_ALL_SETTINGS_SURE = RESET_ALL_SETTINGS + '_sure'  # noqa
    START_EDIT_SETTING = 'start_edit_setting_'
    RESET_SETTING = 'reset_setting_'
    STOP_EDIT_SETTING = 'stop_edit_setting'
    EDIT_MIN_TIME = 'edit_min_time'
    EDIT_MAX_TIME = 'edit_max_time'
    EDIT_THREADS = 'edit_threads'
    EDIT_DEPTH = 'edit_depth'
    EDIT_RAM_HASH = 'edit_ram_hash'
    EDIT_SKILL_LEVEL = 'edit_skill_level'
    EDIT_ELO = 'edit_elo'
    EDIT_COLORS = 'edit_colors'
    EDIT_WITH_COORDS = 'edit_with_coords'
    EDIT_WITH_POSITION_EVALUATION = 'edit_with_position_evaluation'
    EDIT_SIZE = 'edit_size'

    PLAY_OLD_GAME = 'play_old_game'
    PLAY_NEW_GAME = 'play_new_game'
    CHOOSE_COLOR_PREFIX = 'choose_color_'
    COLOR_WHITE = CHOOSE_COLOR_PREFIX + 'w'  # noqa
    COLOR_BLACK = CHOOSE_COLOR_PREFIX + 'b'  # noqa

    GAME_STATE_PREFIX = 'state_game_'
    GET_MOVE_TIP = GAME_STATE_PREFIX + 'get_move_tip'  # noqa
    RESIGN = GAME_STATE_PREFIX + 'resign'  # noqa
    RESIGN_SURE = RESIGN + '_sure'  # noqa
