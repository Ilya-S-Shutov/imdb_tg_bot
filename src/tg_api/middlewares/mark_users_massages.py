from telebot import TeleBot
from telebot.types import Message

from ..states import MainStates
from utils.logging_conf import handlers_logging


@handlers_logging
def mark_user_mess(bot: TeleBot, mess: Message) -> None:
    """
    Прослойка, отвечающая за регистрацию сообщений, полученых от пользователя, в реестре сообщений данного чата.
    :param mess: Объект сообщения (Message) или коллбэка (CallbackQuery).
    :param bot: Объект бота-исполнителя.
    :return:
    """
    if not bot.get_state(mess.from_user.id):
        bot.set_state(mess.from_user.id, MainStates.main)
    with bot.retrieve_data(mess.from_user.id) as data:
        if not data.get('temp_messages_ids'):
            data['temp_messages_ids'] = []
        data['temp_messages_ids'].append(mess.id)