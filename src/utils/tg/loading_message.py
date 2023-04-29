import asyncio

from aiogram import types

from src.consts import Config
from src.keyboards import get_main_menu_settings_game_keyboard


class LoadingMessage:
    message: types.Message
    _future: asyncio.Task

    """
    Использовать `create_loading_message` для инициалзации!

    Класс, который отправляет сообщение в ответ на действие, 
    которое требует длительной работы сервера.
    Временное сообщение обновляется классом, к нему добавляются точки.
    Потом текст сообщения редактируется на нужный или сообщение удаляется.
    """

    def __init__(self, reply_to: types.Message, wait_message: str, ups: int):
        self.text = wait_message
        self.reply_to = reply_to
        self.ups = ups

    async def async_init(self):
        self.message = await self.reply_to.reply(
            f'*{self.text}*',
            parse_mode='markdown'
        )
        self._future = asyncio.ensure_future(self._infity_update())

    async def _infity_update(self):
        """
        Цикл с обновлением точек в конце сообщения.
        """
        if not self.ups:
            return

        # Обновление точек до таймаута на сервере
        for _ in range(self.ups * Config.TIMEOUT):
            await asyncio.sleep(1 / self.ups)
            await self._update_dots()

        # Уведомление об ошибке
        await self.edit_text(
            '*Возникла ошибка на сервере...* :(',
            parse_mode='markdown',
            reply_markup=get_main_menu_settings_game_keyboard()
        )

    async def _update_dots(self):
        """
        Обновление точек.
        """
        if self.text[-3:].count('.') == 3:
            self.text = self.text[:-3]
        else:
            self.text += '.'

        await self.message.edit_text(
            f'*{self.text}*',
            parse_mode='markdown'
        )

    @property
    def edit_text(self):
        """
        Изменение этого сообщения "извне".
        """
        self._future.cancel()
        return self.message.edit_text

    async def delete(self):
        """
        Удаление этого сообщения "извне".
        """
        self._future.cancel()
        await self.message.delete()


async def create_loading_message(
        reply_to: types.Message,
        wait_message: str = 'Загрузка...',
        ups: int = Config.UPS,
) -> LoadingMessage:
    """
    :param reply_to: Сообщение, на кнопку которого нажали /
    Сообщение юзера с ходом.
    :param wait_message: Текст, который будет в сообщении при загрузке. Без *.
    :param ups: Сколько раз в секунду обновлять точки в конце сообщения.
    :return: Экземпляр класса LoadingMessage
    """

    loading_message = LoadingMessage(reply_to, wait_message, ups)
    await loading_message.async_init()
    return loading_message
