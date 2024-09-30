from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from django.db.models.expressions import result

from .db_manager import DBManager


class Saver(ABC):
    """
    Абстрактный класс Saver, определяющий интерфейс для сохранения данных.
    """

    @abstractmethod
    def save_company(self, data: Dict[str, Any]) -> None:
        """
        Сохраняет данные о компаниях в базу данных. Не добавляет дубликаты компаний.

        Args:
            data (Dict[str, Any]): Данные для сохранения.
        """
        pass

    @abstractmethod
    def save_vacancies(self, data: Dict[str, Any]) -> None:
        """
        Сохраняет данные о вакансиях в базу данных. Не добавляет дубликаты вакансий.

        Args:
            data (Dict[str, Any]): Данные для сохранения.
        """
        pass

    @abstractmethod
    def delete_company(self, company_id: int) -> None:
        """
        Удаляет компанию по идентификатору.

        Args:
            company_id (int): Идентификатор компании для удаления.
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id: int) -> None:
        """
        Удаляет вакансию по идентификатору.

        Args:
            vacancy_id (int): Идентификатор вакансии для удаления.
        """
        pass


class DBSaver(Saver):
    """
    Реализация абстрактного класса Saver для сохранения данных в базу данных PostgreSQL через DBManager.
    """

    def __init__(self, db_manager: DBManager):
        """
        Инициализирует экземпляр DBSaver с подключением к DBManager.

        Args:
            db_manager (DBManager): Экземпляр DBManager для работы с базой данных.
        """
        self.db_manager = db_manager

    def save_company(self, company: Dict[str, Any]) -> int:
        """
        Сохраняет данные о компаниях в базу данных. Не добавляет дубликаты компаний.

        Args:
            data (Dict[str, Any]): Данные для сохранения.
            :param company:
        """
        company_id = self.db_manager.insert_company(company)
        return company_id


    def save_vacancies(self, data: Dict[str, Any]) -> None:
        """
        Сохраняет данные о вакансиях в базу данных. Не добавляет дубликаты вакансий.

        Args:
            data (Dict[str, Any]): Данные для сохранения.
        """
        self.db_manager.insert_vacancy(data)

    def delete_company(self, record_id: Optional[int] = None) -> None:
        """
        Удаляет компанию или все компании из базы данных.

        Args:
            record_id (Optional[int], optional): Идентификатор компании для удаления. Если не указан, удаляются все компании.
        """
        if record_id:
            self.db_manager.delete_company(record_id)
            print(f'Компания с идентификатором {record_id} удалена из базы данных.')
        else:
            self.db_manager.delete_all_companies()
            print('Все компании удалены из базы данных.')

    def delete_vacancy(self, record_id: Optional[int] = None) -> None:
        """
        Удаляет вакансию или все вакансии из базы данных.

        Args:
            record_id (Optional[int], optional): Идентификатор вакансии для удаления. Если не указан, удаляются все вакансии.
        """
        if record_id:
            self.db_manager.delete_vacancy(record_id)
            print(f'Вакансия с идентификатором {record_id} удалена из базы данных.')
        else:
            self.db_manager.delete_all_vacancies()
            print('Все вакансии удалены из базы данных.')
