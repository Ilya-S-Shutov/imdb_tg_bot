from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def main_commands_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    info_btn = KeyboardButton('/info')
    search_btn = KeyboardButton('/search')
    wishlist_btn = KeyboardButton('/wishlist')
    kb.add(search_btn, wishlist_btn, info_btn)
    return kb


def exit_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    exit_btn = KeyboardButton('/exit')

    kb.add(exit_btn)
    return kb
