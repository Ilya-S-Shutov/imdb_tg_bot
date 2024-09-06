from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from database import CRUD_instance
from utils.logging_conf import handlers_logging, none_handler_exception_logging


@handlers_logging
def add_new_user(bot: TeleBot, mess: Message | CallbackQuery) -> None:
    """
    Прослойка, которая проверяет, есть ли отправитель сообщения в БД и, если пользователь не найден, добавляет его.
    :param mess: Объект сообщения (Message) или коллбэка (CallbackQuery).
    :param bot: Объект бота-исполнителя.
    :return:
    """
    CRUD_instance.add_user(mess.from_user.id)






