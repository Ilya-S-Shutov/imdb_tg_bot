"""
Общие универсальные команды.
"""

from telebot import TeleBot
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, ReplyKeyboardMarkup

from ..states import MainStates
from ..keyboards.common_keyboards import main_commands_kb
from utils.logging_conf import none_handler_exception_logging, handlers_logging
from utils.messages_text import *


@handlers_logging
def get_chat_id(mess: Message | CallbackQuery) -> int | str:
    """
    Извлечение id чата.
    :param mess: Объект сообщения (Message) или коллбэка (CallbackQuery).
    :return:
    """
    if isinstance(mess, CallbackQuery):
        return mess.message.chat.id
    else:
        return mess.from_user.id


@handlers_logging
def start_handler(mess: Message, bot: TeleBot) -> None:
    """
    Обработчик команды вывода стартового сообщения, отвечающий за первоначальное представление.
    :param mess: Объект сообщения (Message) или коллбэка (CallbackQuery).
    :param bot: Объект бота-исполнителя.
    :return:
    """
    bot.set_state(mess.from_user.id, MainStates.main)
    clean_handler(mess, bot)
    send_message(mess.from_user.id, START, bot, reply_markup=main_commands_kb())


@handlers_logging
def help_handler(mess: Message, bot: TeleBot) -> None:
    """
    Обработчик команды вывода help-сообщения.
    :param mess: Объект сообщения (Message) или коллбэка (CallbackQuery).
    :param bot: Объект бота-исполнителя.
    :return:
    """
    bot.set_state(mess.from_user.id, MainStates.main)
    send_message(mess.from_user.id, HELP, bot, reply_markup=main_commands_kb())


@handlers_logging
def send_message(chat_id: int | str, message: str, bot: TeleBot, reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup = None) -> None:
    """
    Общая команда. Формирует сообщение из переданных ей частей (текста, клавиатуры, получателя и отправителя),
    отправляет его, после чего заносит id сообщения в реестр сообщений для возможности дальнейшей работы с этим
    сообщением.
    :param chat_id: Id чата, которому предназначается сообщение.
    :param message: Текст сообщения.
    :param bot: Объект бота-исполнителя.
    :param reply_markup: Объект клавиатуры, которой должно сопровождаться сообщение.
    :return:
    """
    last_mess = bot.send_message(chat_id, message, reply_markup=reply_markup)
    with bot.retrieve_data(chat_id) as data:
        data['temp_messages_ids'].append(last_mess.id)


@handlers_logging
def clean_handler(mess: Message | CallbackQuery, bot: TeleBot) -> None:
    """
    Удаляет все сообщения, id которых занесены в реестр сообщений указанного чата.
    :param mess: Объект сообщения (Message) или коллбэка (CallbackQuery).
    :param bot: Объект бота-исполнителя.
    :return:
    """
    chat_id = get_chat_id(mess)
    with bot.retrieve_data(chat_id) as data:
        if data.get('temp_messages_ids'):
            bot.delete_messages(chat_id, data.get('temp_messages_ids'))
        else:
            data['temp_messages_ids'] = []

@none_handler_exception_logging
def register_base_commands(bot: TeleBot) -> None:
    """
    Регистрация в боте нужных обработчиков.
    :param bot: Объект бота-исполнителя.
    :return:
    """
    bot.register_message_handler(start_handler, commands=['start', 'info'], pass_bot=True)
    bot.register_message_handler(help_handler, commands=['help'], pass_bot=True)
    # bot.register_message_handler(help_handler, content_types=['text'], pass_bot=True)