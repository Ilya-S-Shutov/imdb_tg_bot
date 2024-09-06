"""
Клавиатуры для работы со списком желаемого.
"""

from telebot.util import quick_markup
from telebot.types import InlineKeyboardMarkup


def create_exit_remove_info_kb(index: int) -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопками: Выход, Удалить, Детали.
    :param index: индекс добавляемого фильма.
    :return:
    """
    kb = quick_markup({
        'Exit': {'callback_data': 'exit'},
        'Remove': {'callback_data': f'remove {index}'},
        'Details': {'callback_data': f'details  {index}'},
    }, row_width=3)
    return kb


def create_back_remove_kb(index: int) -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопками: Выход, Удалить, Назад.
    :param index: индекс добавляемого фильма.
    :return:
    """
    kb = quick_markup({
        'Exit': {'callback_data': 'exit'},
        'Remove': {'callback_data': f'remove {index}'},
        'Back': {'callback_data': 'back'},
    }, row_width=3)
    return kb
