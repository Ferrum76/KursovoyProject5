from typing import List, Dict, Any, Optional
from .vacancy import Vacancy


class ParserVacancy:
    """
    Класс для парсинга данных вакансий из API HH.ru.

    Attributes:
        data (List[Dict[str, Any]]): Список вакансий в формате словарей.
    """

    def __init__(self, data: List[Dict[str, Any]]):
        """
        Инициализирует экземпляр ParserVacancy.

        Args:
            data (List[Dict[str, Any]]): Список вакансий в формате словарей.
        """
        self.__data = data

    def parse_vacancies(self, params: Optional[Dict[str, Any]] = None) -> List[Vacancy]:
        """
        Парсит список вакансий и возвращает список экземпляров Vacancy с примененными фильтрами.

        Args:
            params (Optional[Dict[str, Any]], optional): Словарь с фильтрами для применения.
                                                         По умолчанию None.

        Returns:
            List[Vacancy]: Список экземпляров Vacancy после применения фильтров.

        Raises:
            Exception: Если происходит ошибка при парсинге.
        """
        try:
            vacancies_list = self.__creating_vacancy_list()
            # Применение фильтров, если они заданы
            if params:
                vacancies_list = self.__filter_vacancies(vacancies_list, params)
            return vacancies_list
        except Exception as e:
            raise Exception(f'Ошибка при парсинге данных: {e}')

    def __creating_vacancy_list(self) -> List[Vacancy]:
        """
        Преобразует исходные данные в список экземпляров Vacancy с необходимыми полями.

        Returns:
            List[Vacancy]: Список экземпляров Vacancy.
        """
        if not self.__data:
            return []

        vacancies_list = []
        for item in self.__data:
            try:
                salary = item.get('salary') or {}
                snippet = item.get('snippet') or {}
                area = item.get('area') or {}

                vacancy = Vacancy(
                    name=item.get('name', 'Без названия'),
                    desc=area.get('name', 'Без описания'),
                    salary_from=salary.get('from'),
                    salary_to=salary.get('to'),
                    currency=salary.get('currency', "RUB"),
                    url=item.get('url', 'alternate_url'),
                    requirement=snippet.get('requirement', 'Информация отсутствует')
                )
                vacancies_list.append(vacancy)
            except AttributeError as e:
                print(f"Ошибка обработки элемента: {e}, данные элемента: {item}")
                continue
            except Exception as e:
                print(f"Неизвестная ошибка при обработке элемента: {e}, данные элемента: {item}")
                continue

        print(f'Всего вакансий после парсинга: {len(vacancies_list)}')
        return vacancies_list

    def __filter_vacancies(self, data: List[Vacancy], filter_params: Dict[str, Any]) -> List[Vacancy]:
        """
        Применяет фильтры к списку вакансий.

        Args:
            data (List[Vacancy]): Список вакансий для фильтрации.
            filter_params (Dict[str, Any]): Словарь с фильтрами.

        Returns:
            List[Vacancy]: Отфильтрованный список вакансий.
        """
        filtered = data

        # Фильтр по имени
        if 'name' in filter_params:
            filtered = [vac for vac in filtered if filter_params['name'].lower() in vac.name.lower()]

        # Фильтр по зарплате от
        if 'salary_from' in filter_params:
            filtered = [vac for vac in filtered if vac.salary_from and vac.salary_from >= filter_params['salary_from']]

        # Фильтр по зарплате до
        if 'salary_to' in filter_params:
            filtered = [vac for vac in filtered if vac.salary_to and vac.salary_to <= filter_params['salary_to']]

        # Сортировка по зарплате от
        if filter_params.get('sorted_salary_from'):
            filtered.sort(key=lambda x: x.salary_from or 0, reverse=True)

        # Сортировка по зарплате до
        if filter_params.get('sorted_salary_to'):
            filtered.sort(key=lambda x: x.salary_to or 0, reverse=True)

        # Сортировка по средней зарплате (по возрастанию)
        if filter_params.get('sorted_avg_salary_asc'):
            filtered = sorted(filtered)

        # Сортировка по средней зарплате (по убыванию)
        if filter_params.get('sorted_avg_salary_desc'):
            filtered = sorted(filtered, reverse=True)

        # Топ N вакансий
        if 'top_n' in filter_params:
            top_n = filter_params['top_n']
            filtered = filtered[:top_n]

        return filtered
