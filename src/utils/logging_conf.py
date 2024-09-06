import logging
import traceback
from functools import wraps
from collections.abc import Iterable

# from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from settings import settings

term_log_handler = logging.StreamHandler()
term_log_handler.setFormatter(
    logging.Formatter("[%(asctime)s] %(name)s:%(funcName)s:%(threadName)s:%(levelname)s | %(message)s")
)

logger = logging.getLogger("logger")
logger.addHandler(term_log_handler)
logger.setLevel(logging.INFO)


def none_handler_exception_logging(func):
    """
    Вывод в лог информации о начале/окончании работы декорируемой функции, а также вывод сообщений об ошибках, если
    таковые возникают.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        _send_log_debug("Starting: %s", func.__name__)
        try:
            result = func(*args, **kwargs)
            _send_log_debug("Finished: %s", func.__name__)
            return result
        except Exception as err:
            _send_log_error("Failed: %s === %s \n %s", func.__name__, err, traceback.format_exc())
    return wrapper


def _find_in_args(args: Iterable) -> Message | None:
    """
    Определение типа аргумента: сообщение или коллбэк.
    :param args: Кортеж объектов, полученный основной функцией. Предполагается, что это строки, сообщения или коллбэки.
    :return: Объект сообщения, если получилось извлечь.
    """
    for arg in args:
        if isinstance(arg, Message):
            return arg
        elif isinstance(arg, CallbackQuery):
            return arg.message


def _get_message_info(*args, **kwargs) -> (str | int, str):
    """
    Извлечение из сообщений идентификатора чата и текста сообщения, если есть.
    """
    message_args = _find_in_args(args)
    if message_args is not None:
        return message_args.chat.id, message_args.text

    message_kwargs = _find_in_args(kwargs.values())
    if message_kwargs is not None:
        return message_kwargs.chat.id, message_kwargs.text

    return "UNKNOWN", "UNKNOWN"


def _send_log_debug(mess: str,
                    *mess_args, **mess_kwargs) -> None:
    """
    Отправка сообщений уровня DEBUG в консольный и текстовый лог.
    :param mess: Текст шаблона сообщения.
    :return:
    """
    logging.debug(
        mess,
        *mess_args,
        **mess_kwargs
    )
    logger.debug(
        mess,
        *mess_args,
        **mess_kwargs
    )


def _send_log_error(mess: str,
                   *mess_args, **mess_kwargs) -> None:
    """
    Отправка сообщений уровня ERROR в консольный и текстовый лог.
    :param mess: Текст шаблона сообщения.
    :return:
    """
    logging.error(
        mess,
        *mess_args,
        **mess_kwargs
    )
    logger.info(
        mess,
        *mess_args,
        **mess_kwargs
    )


def handlers_logging(func):
    """
    Логирование хода работы обработчиков.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        chat_id, text = _get_message_info(*args, **kwargs)
        _send_log_debug(
            settings.log_handler_start_message_format,
            func.__name__,
            chat_id,
            str(text)
        )
        try:
            result = func(*args, **kwargs)
            _send_log_debug(
                settings.log_handler_finish_message_format,
                func.__name__,
                chat_id,
                str(text)
            )
            return result
        except Exception as err:
            _send_log_error(
                settings.log_handler_error_message_format,
                func.__name__,
                chat_id,
                str(text),
                err,
                traceback.format_exc()
            )

    return wrapper


if __name__ == '__main__':

    @none_handler_exception_logging
    def my_func(a, b):
        print(a/b)

    my_func(5, 0)

