from telebot.util import quick_markup
from telebot.types import InlineKeyboardMarkup


def create_exit_add_next_kb(index: int) -> InlineKeyboardMarkup:
    kb = quick_markup({
        'Exit': {'callback_data': 'exit'},
        'Add': {'callback_data': f'add {index}'},
        'Next': {'callback_data': 'next'},
    }, row_width=3)
    return kb


def create_exit_add_kb(index: int) -> InlineKeyboardMarkup:
    kb = quick_markup({
        'Exit': {'callback_data': 'exit'},
        'Add': {'callback_data': f'add {index}'}
    }, row_width=2)
    return kb