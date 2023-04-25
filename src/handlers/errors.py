from aiogram import Dispatcher
from aiogram.utils.exceptions import MessageToEditNotFound
from loguru import logger


async def message_to_edit_not_found(*_):
    """
    Юзер может удалить сообщение бота, пока бот грузит инфу,
    поэтому я так зачитерил. Хз, круто ли так делать.
    """
    return True


async def all_errors(update, error):
    logger.error(f'Exception Error: {error}, {update=}')


def register_errors(dp: Dispatcher):
    dp.register_errors_handler(message_to_edit_not_found, exception=MessageToEditNotFound)
    dp.register_errors_handler(all_errors, exception=Exception)
