"""
Обработчики для работы с списком желаемого.
"""

from telebot import TeleBot
from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove

from database import CRUD_instance
from .base_handlers import get_chat_id, clean_handler, send_message, help_handler
from ..keyboards.common_keyboards import main_commands_kb
from ..keyboards.wishlist_keyboards import create_back_remove_kb, create_exit_remove_info_kb
from ..states.states import WishlistStates, MainStates
from utils.logging_conf import none_handler_exception_logging, handlers_logging
from utils.messages_text import *


@handlers_logging
def wishlist_handler(mess: Message | CallbackQuery, bot: TeleBot) -> None:
    """
    Обработчик, отвечающий за начало работы пользователя со списком желаемого.
    Выводит список желаемого с функциональными кнопками.
    :param mess: Объект сообщения (Message) или коллбэка (CallbackQuery).
    :param bot: Объект бота-исполнителя.
    :return:
    """
    clean_handler(mess, bot)
    chat_id = get_chat_id(mess)
    movies_list = CRUD_instance.get_users_wishlist(chat_id)
    bot.set_state(chat_id, WishlistStates.wishlist)
    with bot.retrieve_data(chat_id) as data:
        data["movies_list"] = movies_list
    send_message(chat_id, YOUR_LIST, bot)
    for index, movie in enumerate(movies_list, 0):
        send_message(
            chat_id,
            f"{movie.title}, {movie.year}",
            bot,
            reply_markup=create_exit_remove_info_kb(index)
        )


@handlers_logging
def show_movie_details(call: CallbackQuery, bot: TeleBot) -> None:
    """
    Обработчик, отвечающий за демонстрацию подробностей о выбранном фильме.
    :param mess: Объект сообщения (Message) или коллбэка (CallbackQuery).
    :param bot: Объект бота-исполнителя.
    :return:
    """
    clean_handler(call, bot)
    chat_id = get_chat_id(call)
    index = int(call.data.split()[1])
    bot.set_state(chat_id, WishlistStates.single)
    with bot.retrieve_data(chat_id) as data:
        movie = data["movies_list"][index]
        text_message = (f"{movie.title}/{movie.original_title}\n"
                        f"Year of release: {movie.year}\n"
                        f"Type: {movie.type} | Rating: {movie.rating}\n"
                        f"{movie.overview}")
        try:
            if movie.img_url:
                sent_photo = bot.send_photo(chat_id, photo=movie.img_url)
                data['temp_messages_ids'].append(sent_photo.id)
        except:
            pass

    send_message(chat_id, text_message, bot, reply_markup=create_back_remove_kb(index))


@handlers_logging
def remove_user_to_movie_link(call: CallbackQuery, bot: TeleBot) -> None:
    """
    Обработчик, отвечающий за удаление фильма из списка желаемого.
    :param mess: Объект сообщения (Message) или коллбэка (CallbackQuery).
    :param bot: Объект бота-исполнителя.
    :return:
    """
    chat_id = get_chat_id(call)
    index = int(call.data.split()[1])
    with bot.retrieve_data(chat_id) as data:
        movie = data["movies_list"][index]
        if CRUD_instance.delete_link(chat_id, movie.title, movie.year):
            bot.answer_callback_query(call.id, REMOVED, show_alert=False)
        data["movies_list"].remove(movie)
    wishlist_handler(call, bot)


@handlers_logging
def stop_wishlist(mess: Message | CallbackQuery, bot: TeleBot) -> None:
    """
    Обработчик, отвечающий за завершение работы со списком желаемого.
    :param mess: Объект сообщения (Message) или коллбэка (CallbackQuery).
    :param bot: Объект бота-исполнителя.
    :return:
    """
    chat_id = get_chat_id(mess)
    clean_handler(mess, bot)
    # send_message(chat_id, CLOSED, bot, reply_markup=main_commands_kb())
    help_handler(mess, bot)


@none_handler_exception_logging
def register_wishlist_handlers(bot: TeleBot) -> None:
    """
    Регистрация необходимых обработчиков.
    :param mess: Объект сообщения (Message) или коллбэка (CallbackQuery).
    :param bot: Объект бота-исполнителя.
    :return:
    """
    bot.register_message_handler(wishlist_handler, commands=['wishlist'], pass_bot=True)
    bot.register_callback_query_handler(
        wishlist_handler,
        func=lambda call: call.data == 'back',
        state=[WishlistStates.single],
        pass_bot=True
    )

    bot.register_callback_query_handler(
        show_movie_details,
        func=lambda call: call.data.split()[0] == 'details',
        state=[WishlistStates.wishlist],
        pass_bot=True
    )

    bot.register_callback_query_handler(
        remove_user_to_movie_link,
        func=lambda call: call.data.split()[0] == 'remove',
        state=[WishlistStates.wishlist, WishlistStates.single],
        pass_bot=True
    )

    bot.register_callback_query_handler(
        stop_wishlist,
        func=lambda call: call.data.split()[0] == 'exit',
        state=[WishlistStates.wishlist, WishlistStates.single],
        pass_bot=True
    )