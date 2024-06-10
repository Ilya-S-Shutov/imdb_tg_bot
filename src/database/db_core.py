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
        logging.info(f'New user {user_id} added!')
        User.get_or_create(user_id=user_id)


    @staticmethod
    def get_movie(title: str, year: int) -> int:
        return Movie.get_or_none(Movie.title == title, Movie.year == year)

    @staticmethod
    def _get_user(user_tg_id) -> int:
        return User.get_or_none(User.user_id == user_tg_id)

    @staticmethod
    def add_movie(
            title: str,
            year: int,
            rating: float,
            movie_type: str,
            img: str,
            overview: str,
            orig_title: str | None = None):

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
    def get_users_wishlist(user_id: int) -> list:
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