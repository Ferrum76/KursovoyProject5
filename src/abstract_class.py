from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class AbstractHH(ABC):
    """
    Абстрактный класс для подключения к API платформы с вакансиями.
    """

    @abstractmethod
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
            Exception: Если произошла ошибка при выполнении запроса.
        """
        pass


class Saver(ABC):
    """
    Абстрактный класс для сохранения данных о вакансиях.
    """

    @abstractmethod
    def get_path(self) -> str:
        """
        Возвращает путь к файлу или директории для сохранения данных.

        Returns:
            str: Путь для сохранения данных.
        """
        pass

    @abstractmethod
    def save(self, data: Any) -> None:
        """
        Сохраняет предоставленные данные.

        Args:
            data (Any): Данные для сохранения.

        Raises:
            Exception: Если произошла ошибка при сохранении данных.
        """
        pass

    @abstractmethod
    def delete(self, record_id: Optional[str] = None) -> None:
        """
        Удаляет запись(и) по заданному идентификатору.

        Args:
            record_id (Optional[str], optional): Идентификатор записи для удаления.
                                                Если не указан, удаляются все записи.
                                                По умолчанию None.

        Raises:
            Exception: Если произошла ошибка при удалении данных.
        """
        pass


class Parser(ABC):
    """
    Абстрактный класс для парсинга данных о вакансиях.
    """

    @abstractmethod
    def parse_vacancies(self, data: List[Dict[str, Any]], params: Optional[Dict[str, Any]] = None) -> List[Any]:
        """
        Парсит список вакансий и возвращает обработанные объекты.

        Args:
            data (List[Dict[str, Any]]): Список вакансий в формате словарей.
            params (Optional[Dict[str, Any]], optional): Словарь с фильтрами для применения.
                                                         По умолчанию None.

        Returns:
            List[Any]: Список обработанных объектов вакансий.

        Raises:
            Exception: Если произошла ошибка при парсинге данных.
        """
        pass
