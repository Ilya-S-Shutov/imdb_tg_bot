import logging
import requests

from settings import settings
from utils.logging_conf import none_handler_exception_logging


class ImdbRequests:
    """
    Интерфейс взаимодействия с IMDb.
    """
    @classmethod
    @none_handler_exception_logging
    def _get_response(cls,
                      method: str,
                      url: str,
                      # headers: dict | None = None,
                      params: dict | None = None) -> dict | None:
        """
        Общий метод отправки запроса.
        :param method: Метод запроса.
        :param url: URL.
        :param params: Парметры запроса.
        :return: Содержимое ответа в формате json, преобразованного в словарь. None, если ответ не содержит json.
        """
        headers = {
            "x-rapidapi-key": settings.api.api_key.get_secret_value(),
            "x-rapidapi-host": settings.api.api_host.get_secret_value()
        }

        response = requests.request(method=method,
                                    url=url,
                                    headers=headers,
                                    params=params)
        if response.status_code == 200:
            return response.json()
        return None

    @classmethod
    @none_handler_exception_logging
    def get_overview(cls, title_id: str) -> tuple[float, str] | None:
        """
        Получение дополнительной информации о фильме.
        :param title_id: Id фильма в системе IMDb.
        :return: Кортеж с рейтингом и кратким описанием фильма.
        """
        params = {
            "tconst": str(title_id),
            "country": "US",
            "language": "en-US"}

        url = f'{settings.url.hostname}{settings.url.overview}'

        response = cls._get_response(
            method='GET',
            url=url,
            # headers=headers,
            params=params
        )

        if response:
            data = response['data']['title']
            rating = data['ratingsSummary']['aggregateRating']
            try:
                overview = data['plot']['plotText']['plainText']
            except:
                overview = ""
            return rating, overview

        return None

    @classmethod
    @none_handler_exception_logging
    def search_movies(cls, search_term: str, types: tuple = ('TV', 'MOVIE'), amount: int = 5) -> list | None | None:
        """
        Реализация поиска фильмов и инофрмации о них по запросу. Формирование списка из данных о фильмах.
        :param search_term: Строка для поиска.
        :param types: Тип искомых произведений.
        :param amount: Максимальное кол-во фильмов в подборке.
        :return: Список с данными фильмов.
        """
        params = {
            "searchTerm": search_term,
            "type": ','.join(types),
            "first": int(amount),
            "language": "en-US"
        }

        url = f'{settings.url.hostname}{settings.url.search}'

        response = cls._get_response(
            method='GET',
            url=url,
            # headers=headers,
            params=params
        )

        if response:
            movies_list = []
            # with open('test_api.json', 'w') as f:
            #     import json
            #     json.dump(response, f, indent=4)
            for movie_data_raw in response['data']['mainSearch']['edges']:
                movie_data_raw = movie_data_raw['node']['entity']

                if not movie_data_raw['releaseYear']:
                    continue

                rating, overview = cls.get_overview(movie_data_raw['id'])
                movie_data = {
                    'id': movie_data_raw['id'],
                    'titleText': movie_data_raw['titleText']['text'],
                    'originalTitleText':
                        movie_data_raw['originalTitleText']['text']
                        if not movie_data_raw['titleText']['isOriginalTitle']
                        else "",
                    'year': movie_data_raw['releaseYear']['year'],
                    'type': movie_data_raw['titleType']['id'],
                    'img':
                        movie_data_raw['primaryImage']['url']
                        if movie_data_raw['primaryImage']
                        else "",
                    'rating': rating,
                    'overview': overview,
                }

                movies_list.append(movie_data)
            return movies_list
        return None


if __name__ == '__main__':
    pass
    import json
    data = ImdbRequests.search_movies('Matrix')
    with open('example.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
