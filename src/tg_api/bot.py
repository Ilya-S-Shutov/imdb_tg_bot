from pydantic import SecretStr
from telebot import TeleBot, custom_filters, apihelper
from telebot.storage import StateMemoryStorage

from .handlers import register_base_commands, register_search_handlers, register_wishlist_handlers
from .middlewares import register_middlewares
from .states import MainStates
from utils.logging_conf import none_handler_exception_logging, logger


@none_handler_exception_logging
def create_bot(token: SecretStr) -> TeleBot:
    storage = StateMemoryStorage()
    apihelper.ENABLE_MIDDLEWARE = True

    bot = TeleBot(token.get_secret_value(), num_threads=4, state_storage=storage)

    register_search_handlers(bot)
    register_wishlist_handlers(bot)
    register_base_commands(bot)
    register_middlewares(bot)

    bot.add_custom_filter(custom_filters.StateFilter(bot))

    logger.info("Bot started!")
    return bot
