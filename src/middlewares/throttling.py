from aiogram import types, Dispatcher
from aiogram.dispatcher.handler import current_handler, CancelHandler
from aiogram.utils.exceptions import Throttled
from loguru import logger

from src.middlewares.base import MyBaseMiddleware
from src.utils.tg.log_in_chat import log_in_chat


class ThrottlingMiddleware(MyBaseMiddleware):
    """
    Простой мидлварь анти-флуд-спам из документации aiogram'а.
    """

    def __init__(self, limit=.75, key_prefix='antiflood'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(
            self, message: types.Message | types.CallbackQuery, *_
    ):
        """
        Этот обработчик вызывается, когда диспетчер получает сообщение.
        """
        # Получаем текущий обработчик
        handler = current_handler.get()
        # Получаем диспетчер из контекста
        dispatcher = Dispatcher.get_current()
        # Если обработчик был настроен декоратором rate_limit,
        # получаем ограничение скорости и ключ от обработчика
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(
                handler, 'throttling_key', f"{self.prefix}_{handler.__name__}"
            )
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.message_throttled(
                message, t
            )  # Если произошёл троттлинг...
            raise CancelHandler()  # Отменяем обработку запроса.

    async def on_process_callback_query(
            self, callback: types.CallbackQuery, data: dict
    ):
        """
        Этот обработчик вызывается, когда диспетчер получает сообщение.
        """
        await self.on_process_message(callback, data)

    async def message_throttled(
            self, message: types.Message | types.CallbackQuery,
            throttled: Throttled
    ):
        """
        Действия на флуд в бота.

        :param message: Сообщение.
        :param throttled: ?
        """

        if isinstance(message, types.CallbackQuery):
            logger.debug(
                f'Тротл callback "{message.data}" '
                f'[{await self.get_short_info(message)}]'
            )
        elif isinstance(message, types.Message):
            logger.debug(
                f'Тротл сообщение "{message.text}" '
                f'[{await self.get_short_info(message)}]'
            )

        if throttled.exceeded_count == 3:  # Число взял из головы
            message = f'Наведение суеты: {await self.get_short_info(message)}'
            logger.info(message)
            await log_in_chat(message)
