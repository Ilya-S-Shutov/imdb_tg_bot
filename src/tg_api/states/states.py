from telebot.handler_backends import State, StatesGroup


class SearchStates(StatesGroup):
    """
    Группа состояний для реализации функционала поиска и формирования подборок фильмов.
    """
    request_search = State()
    show_found_results = State()


class MainStates(StatesGroup):
    """
    Группа основных состояний.
    """
    main = State()


class WishlistStates(StatesGroup):
    """
    Группа состояний для реализации функционала работы со списком желаемого.
    """
    wishlist = State()
    single = State()