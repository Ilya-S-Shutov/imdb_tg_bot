__all__ = ['CRUD_instance']
import logging
import peewee as pw

from .models import *


class CRUD:
    def __init__(self):
        User.create_table()
        Movie.create_table()
        WishList.create_table()


    @staticmethod
    def add_user(user_id: int) -> None:
        """
        Добавить пользователя в БД.
        :param user_id: id пользователя в tg.
        :return:
        """
        logging.info(f'New user {user_id} added!')
        User.get_or_create(user_id=user_id)


    @staticmethod
    def get_movie(title: str, year: int) -> int | None:
        """
        Получить id фильма, если такой есть.
        :param title: Название фильма.
        :param year: Год релиза фильма.
        :return: id фильма или None, если фильма не найден.
        """
        return Movie.get_or_none(Movie.title == title, Movie.year == year)

    @staticmethod
    def _get_user(user_tg_id) -> int | None:
        """
        Получить id пользователя в БД, если пользователь есть, по его tg id.
        :param user_tg_id: id пользователя в tg.
        :return: id пользователя в БД, если есть, иначе None.
        """
        return User.get_or_none(User.user_id == user_tg_id)

    @staticmethod
    def add_movie(
            title: str,
            year: int,
            rating: float,
            movie_type: str,
            img: str,
            overview: str,
            orig_title: str | None = None) -> Movie:
        """
        Добавление записи с данными фильма в БД.
        :param title: Название.
        :param year: Год релиза.
        :param rating: Рейтинг.
        :param movie_type: Тип: Сериал/фильм/прочее.
        :param img: Ссылка на постер к фильму.
        :param overview: Краткое описание фильма.
        :param orig_title: Оригинальное название, если отличается от англоязычного.
        :return: Объект модели Movie.
        """

        new_movie = Movie.create(
            title=title,
            year=year,
            rating=rating,
            type=movie_type,
            img_url=img,
            overview=overview,
            original_title=orig_title
        )
        logging.info(f'New Movie {title}, {year} added!')
        return new_movie

    def add_movie_to_user(self,
                          user_id: int,
                          title: str,
                          year: int,
                          rating: float,
                          movie_type: str,
                          img: str,
                          overview: str,
                          orig_title: str | None = None) -> None:
        """
        Добавление связи: пользователь — фильм.
        :param user_id: id пользователя.
        :param title: Название.
        :param year: Год релиза.
        :param rating: Рейтинг фильма.
        :param movie_type: Тип: Сериал/Фильм/прочее.
        :param img: Ссылка на постер к фильму.
        :param overview: Краткое описание.
        :param orig_title: Оригинальное название, если отличается от англоязычного.
        :return:
        """
        movie = self.get_movie(title, year)
        if not movie:
            movie = self.add_movie(
                title=title,
                year=year,
                rating=rating,
                movie_type=movie_type,
                img=img,
                overview=overview,
                orig_title=orig_title
            )

        movie.save()
        logging.info(f'New link {user_id} -- {title} {year} added!')
        WishList.get_or_create(user_id=User.get(User.user_id == user_id), movie_id=movie)

    @staticmethod
    def get_users_wishlist(user_id: int) -> list[Movie]:
        """
        Собирает список фильмов, связанных с конкретным пользователем.
        :param user_id: Id пользователя в Бд.
        :return: Список с объектами модели Movie.
        """
        movies_list = [film for film in Movie.select().join(
            WishList,
            on=(WishList.movie_id == Movie.id)
        ).join(
            User,
            on=(WishList.user_id == User.id)
        ).where(User.user_id == user_id)
                ]
        # return [
        #     (movie.title, str(movie.year)) for movie in movies_list
        # ]
        return movies_list

    def delete_link(self, user_tg_id: int, title: str, year: int) -> bool:
        """
        Удаление связки пользователь — фильм.
        :param user_tg_id: id пользователя в tg.
        :param title: Название фильма.
        :param year: Год релиза фильма.
        :return: Успех/неудача выполнения удаления.
        """
        movie = self.get_movie(title, year)
        user = self._get_user(user_tg_id)
        if movie and user:
            try:
                WishList.delete_instance(WishList.get(WishList.movie_id == movie.id, WishList.user_id == user.id))
                logging.info(f'Link {user_tg_id} -- {title} {year} deleted!')
            except Exception:
                return False
            return True


CRUD_instance = CRUD()


if __name__ == '__main__':
    pass
    # User.create_table()
    # Movie.create_table()
    # WishList.create_table()
    # CRUD.add_movie_to_user(1234, 'qw1234e', 20123, 'Iv13an1', 4.2)
    # my_list = CRUD.get_users_wishlist(1234)
    # print(my_list)
    #
    # for film in my_list:
    #     print(film.title)

    # CRUD.delete_link(1234, 'qwe', 2023, 'Ivan1')