from aiogram import types


class LoadingMessage:
    message: types.Message

    """
    Класс, который отправляет сообщение в ответ на действие, которое требует длительной работы сервера.
    Потом текст сообщения редактируется на нужный и или сообщение удаляется.
    """

    def __init__(self, reply_to: types.Message, wait_message: str = '*Загрузка...*'):
        """
        :param reply_to: Сообщение, на кнопку которого нажали / Сообщение юзера с ходом.
        :param wait_message: Текст, который будет в сообщении при загрузке.
        """
        self.text = wait_message
        self.reply_to = reply_to

    async def async_init(self):
        self.message = await self.reply_to.reply(self.text, parse_mode='markdown')

    async def edit_message(self, *args, **kwargs):
        await self.message.edit_text(*args, **kwargs)

    async def delete(self):
        await self.message.delete()


async def create_loading_message(
        reply_to: types.Message,
        wait_message: str = '*Загрузка...*',
) -> LoadingMessage:
    """
    :param reply_to: Сообщение, на кнопку которого нажали / Сообщение юзера с ходом.
    :param wait_message: Текст, который будет в сообщении при загрузке.
    :param wait_message: Текст, который будет в сообщении при загрузке.
    :return Экземпляр класса LoadingMessage
    """

    loading_message = LoadingMessage(reply_to, wait_message)
    await loading_message.async_init()
    return loading_message
