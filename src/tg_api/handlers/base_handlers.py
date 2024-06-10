from telebot import TeleBot
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, ReplyKeyboardMarkup

from ..states import MainStates
from ..keyboards.common_keyboards import main_commands_kb
from utils.logging_conf import none_handler_exception_logging, handlers_logging
from utils.messages_text import *


@handlers_logging
def get_chat_id(mess: Message | CallbackQuery) -> int | str:
    if isinstance(mess, CallbackQuery):
        return mess.message.chat.id
    else:
        return mess.from_user.id


@handlers_logging
def start_handler(mess: Message, bot: TeleBot) -> None:
    bot.set_state(mess.from_user.id, MainStates.main)
    clean_handler(mess, bot)
    send_message(mess.from_user.id, START, bot, reply_markup=main_commands_kb())


@handlers_logging
def help_handler(mess: Message, bot: TeleBot) -> None:
    bot.set_state(mess.from_user.id, MainStates.main)
    send_message(mess.from_user.id, HELP, bot, reply_markup=main_commands_kb())


@handlers_logging
def send_message(chat_id: int | str, message: str, bot: TeleBot, reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup = None) -> None:
    last_mess = bot.send_message(chat_id, message, reply_markup=reply_markup)
    with bot.retrieve_data(chat_id) as data:
        data['temp_messages_ids'].append(last_mess.id)


@handlers_logging
def clean_handler(mess: Message | CallbackQuery, bot: TeleBot) -> None:
    chat_id = get_chat_id(mess)
    with bot.retrieve_data(chat_id) as data:
        if data.get('temp_messages_ids'):
            bot.delete_messages(chat_id, data.get('temp_messages_ids'))
        else:
            data['temp_messages_ids'] = []

@none_handler_exception_logging
def register_base_commands(bot: TeleBot) -> None:
    bot.register_message_handler(start_handler, commands=['start', 'info'], pass_bot=True)
    bot.register_message_handler(help_handler, commands=['help'], pass_bot=True)
    # bot.register_message_handler(help_handler, content_types=['text'], pass_bot=True)