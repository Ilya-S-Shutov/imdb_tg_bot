from telebot import TeleBot

from .add_new_user import add_new_user
from .mark_users_massages import mark_user_mess
from utils.logging_conf import handlers_logging, none_handler_exception_logging


@handlers_logging
def register_middlewares(bot: TeleBot) -> None:
    bot.register_middleware_handler(add_new_user, update_types=['message'])
    bot.register_middleware_handler(mark_user_mess, update_types=['message'])