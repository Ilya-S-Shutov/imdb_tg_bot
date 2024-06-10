from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from database import CRUD_instance
from utils.logging_conf import handlers_logging, none_handler_exception_logging


@handlers_logging
def add_new_user(bot: TeleBot, mess: Message | CallbackQuery) -> None:
    CRUD_instance.add_user(mess.from_user.id)






