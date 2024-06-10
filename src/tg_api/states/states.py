from telebot.handler_backends import State, StatesGroup


class SearchStates(StatesGroup):
    request_search = State()
    show_found_results = State()


class MainStates(StatesGroup):
    main = State()


class WishlistStates(StatesGroup):
    wishlist = State()
    single = State()