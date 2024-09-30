from .abstract_class import AbstractHH
import requests
from requests import Session, Response
from typing import List, Dict, Any, Optional


BASE_API_HH_URL = 'https://api.hh.ru/vacancies'


class FromHHru(AbstractHH):
    """
    Класс для подключения к API HH.ru и получения вакансий.

    Attributes:
        url_get (str): URL для получения вакансий.
        session (Session): Сессия для выполнения HTTP-запросов.
        per_page (int): Количество вакансий на страницу.
    """

    def __init__(self, url_get: str = BASE_API_HH_URL, per_page: int = 100):
        """
        Инициализирует новый экземпляр класса FromHHru.

        Args:
            url_get (str, optional): URL для получения вакансий. По умолчанию 'https://api.hh.ru/vacancies'.
            per_page (int, optional): Количество вакансий на страницу. По умолчанию 100.
        """
        self.__url_get = url_get
        self.__per_page = per_page
        self.__session = Session()
        self.__session.headers.update({
            'User-Agent': 'VacancyParser/1.0 (contact@yourdomain.com)'  # Замените на имя вашего приложения и действительный email
        })

    def __repr__(self) -> str:
        """
        Возвращает строковое представление объекта.

        Returns:
            str: Строковое представление объекта, включающее URL API и количество вакансий на страницу.
        """
        return f'FromHHru(url_get="{self.__url_get}", per_page={self.__per_page})'

    def get_vacancies(self, keyword: str, max_pages: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Получает список вакансий из API на основе предоставленного ключевого слова.

        Args:
            keyword (str): Ключевое слово для поиска вакансий.
            max_pages (Optional[int], optional): Максимальное количество страниц для получения.
                                                 По умолчанию None (получить все доступные страницы).

        Returns:
            List[Dict[str, Any]]: Список вакансий, полученных из API.

        Raises:
            ValueError: Если ключевое слово пустое.
            requests.HTTPError: Если запрос к API завершился неудачно.
            requests.RequestException: Для других ошибок, связанных с запросом.
        """
        if not keyword or not keyword.strip():
            raise ValueError("Ключевое слово для поиска не может быть пустым.")

        vacancies: List[Dict[str, Any]] = []
        page = 0

        while True:
            params = {
                'text': keyword,
                'page': page,
                'per_page': self.__per_page
            }
            try:
                response: Response = self.__session.get(self.__url_get, params=params, timeout=10)
                response.raise_for_status()
            except requests.HTTPError as http_err:
                raise http_err
            except requests.RequestException as req_err:
                raise req_err

            data = response.json()
            items = data.get('items', [])
            vacancies.extend(items)

            # Проверяем, достигли ли мы последней страницы
            total_pages = data.get('pages')
            if total_pages is None:
                break

            if page >= total_pages - 1:
                break

            page += 1
            if max_pages and page >= max_pages:
                break

        print(f'Всего вакансий получено: {len(vacancies)}')
        return vacancies

    def close_session(self) -> None:
        """
        Закрывает сессию для HTTP-запросов.
        """
        self.__session.close()
