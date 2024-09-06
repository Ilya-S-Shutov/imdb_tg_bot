"""
Обработчики для работы с функцией поиска фильмов и формирования подборок.
"""

from telebot import TeleBot
from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove

from database import CRUD_instance
from .base_handlers import get_chat_id, clean_handler, send_message, help_handler
from imdb_api import ImdbRequests
from ..keyboards.search_keyboards import *
from ..keyboards.common_keyboards import main_commands_kb, exit_kb
from ..states import SearchStates, MainStates
from utils.logging_conf import none_handler_exception_logging, handlers_logging
from utils.messages_text import *


@handlers_logging
def search_handler(mess: Message, bot: TeleBot) -> None:
    """
    Обработчик команды инициализации поиска фильмов.
    :param mess: Объект сообщения (Message) или коллбэка (CallbackQuery).
    :param bot: Объект бота-исполнителя.
    :return:
    """
    clean_handler(mess, bot)
    bot.set_state(mess.from_user.id, SearchStates.request_search)

    send_message(mess.from_user.id, ASK_SEARCH_TERM, bot)


@handlers_logging
def get_search_term_handler(mess: Message, bot: TeleBot) -> None:
    """
    Обработчик, отвечающий за получение и фиксацию строки поиска.
    :param mess: Объект сообщения (Message) или коллбэка (CallbackQuery).
    :param bot: Объект бота-исполнителя.
    :return:
    """
    if mess.text:
        with bot.retrieve_data(mess.from_user.id, mess.chat.id) as data:
            data['search_term'] = mess.text
        send_message(mess.from_user.id, WAIT_SEARCH, bot)
    request_search_query_handler(mess, bot)


@handlers_logging
def request_search_query_handler(mess: Message, bot: TeleBot) -> None:
    """
    Обработчик, отвечающий за формирование и отправку запроса поиска, на основе полученной от пользователя строки.
    :param mess: Объект сообщения (Message) или коллбэка (CallbackQuery).
    :param bot: Объект бота-исполнителя.
    :return:
    """
    with bot.retrieve_data(mess.from_user.id, mess.chat.id) as data:
        data['found_movies_list'] = ImdbRequests.search_movies(mess.text)
        if not data['found_movies_list']:
            last_mess = bot.send_message(mess.from_user.id, NOT_FOUND)
            data['temp_messages_ids'].append(last_mess.id)
            return
        data['current_movie_index'] = 0
    bot.set_state(mess.from_user.id, SearchStates.show_found_results)
    show_movie_list_info_handler(mess, bot)


@handlers_logging
def show_movie_list_info_handler(mess: Message | CallbackQuery, bot: TeleBot) -> None:
    """
    Обработчик, отвечающий за пошаговый вывод информации о фильмах.
    :param mess: Объект сообщения (Message) или коллбэка (CallbackQuery).
    :param bot: Объект бота-исполнителя.
    :return:
    """
    chat_id = get_chat_id(mess)

    with bot.retrieve_data(chat_id) as data:
        movie = data['found_movies_list'][data['current_movie_index']]
        length = len(data['found_movies_list'])
        count = data['current_movie_index']
        data['current_movie_index'] += 1

    text_message = (f"{movie['titleText']}/{movie['originalTitleText']}\n"
                    f"Year of release: {movie['year']}\n"
                    f"Type: {movie['type']} | Rating: {movie['rating']}\n"
                    f"{movie['overview']}")
    try:
        if movie['img']:
            last_mess = bot.send_photo(chat_id, photo=movie['img'])
            data['temp_messages_ids'].append(last_mess.id)
    except:
        pass

    if count + 1 == length:
        kb = create_exit_add_kb(count)
        send_message(chat_id, text_message, bot, reply_markup=kb)
    else:
        kb = create_exit_add_next_kb(count)
        send_message(chat_id, text_message, bot, reply_markup=kb)

    if isinstance(mess, CallbackQuery):
        bot.answer_callback_query(mess.id)


@handlers_logging
def stop_search_handler(mess: Message | CallbackQuery, bot: TeleBot) -> None:
    """
    Обработчик, отвечающий за остановку пошаговой выдачи фильмов и возврат к основному состоянию.
    :param mess: Объект сообщения (Message) или коллбэка (CallbackQuery).
    :param bot: Объект бота-исполнителя.
    :return:
    """
    chat_id = get_chat_id(mess)
    clean_handler(mess, bot)
    bot.answer_callback_query(mess.id, STOP_SEARCHING)
    help_handler(mess, bot)


@handlers_logging
def add_to_wishlist_handler(call: CallbackQuery, bot: TeleBot) -> None:
    """
    Обработчик, отвечающий добавление фильма в список желаний пользователя.
    :param mess: Объект сообщения (Message) или коллбэка (CallbackQuery).
    :param bot: Объект бота-исполнителя.
    :return:
    """
    index = int(call.data.split()[1])
    chat_id = get_chat_id(call)
    with bot.retrieve_data(chat_id) as data:
        movie = data['found_movies_list'][index]
    CRUD_instance.add_movie_to_user(
        user_id=chat_id,
        title=movie['titleText'],
        year=movie['year'],
        movie_type=movie['type'],
        img=movie['img'],
        overview=movie['overview'],
        rating=movie['rating'],
        orig_title=movie['originalTitleText']
    )
    bot.answer_callback_query(call.id, ADDED)


@none_handler_exception_logging
def register_search_handlers(bot: TeleBot) -> None:
    """
    Регистрация необходимых обработчиков.
    :param bot: Объект бота-исполнителя.
    :return:
    """
    bot.register_message_handler(search_handler, commands=['search'], pass_bot=True)
    bot.register_message_handler(get_search_term_handler, state=[SearchStates.request_search], pass_bot=True)

    bot.register_message_handler(stop_search_handler, commands=['next'], state=[SearchStates.show_found_results], pass_bot=True)
    bot.register_callback_query_handler(
        show_movie_list_info_handler,
        func=lambda call: call.data == 'next',
        state=[SearchStates.show_found_results],
        pass_bot=True
    )

    bot.register_message_handler(stop_search_handler, commands=['exit'], state=[SearchStates.show_found_results], pass_bot=True)
    bot.register_callback_query_handler(
        stop_search_handler,
        func=lambda call: call.data == 'exit',
        state=[SearchStates.show_found_results],
        pass_bot=True
    )

    bot.register_callback_query_handler(
        add_to_wishlist_handler,
        func=lambda call: call.data.split()[0] == 'add',
        pass_bot=True
    )