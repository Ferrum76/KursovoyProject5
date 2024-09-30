from .abstract_class import Saver
from typing import Any, Dict, List, Optional
import json
import os


class JSONSaver(Saver):
    """
    Реализация абстрактного класса Saver для сохранения данных в JSON файл.
    """

    def __init__(self, path: str = 'data/vacancies.json'):
        """
        Инициализирует экземпляр JSONSaver.

        Args:
            path (str, optional): Путь к JSON файлу для сохранения данных.
                                  По умолчанию 'data/vacancies.json'.
        """
        self.__path = path
        os.makedirs(os.path.dirname(self.__path), exist_ok=True)

    def get_path(self) -> str:
        """
        Возвращает путь к JSON файлу.

        Returns:
            str: Путь к JSON файлу.
        """
        return self.__path

    def save(self, data: Dict[str, Any]) -> None:
        """
        Сохраняет данные в JSON файл. Не добавляет дубликаты вакансий.

        Args:
            data (Dict[str, Any]): Данные для сохранения.

        Raises:
            IOError: Если произошла ошибка при записи в файл.
        """
        try:
            existing_data = self.__load_existing_data()
            new_items = data.get('items', [])

            # Избегаем дублирования вакансий по 'name' и 'url'
            existing_items = { (item['name'], item['url']) for item in existing_data.get('items', []) }
            unique_new_items = [item for item in new_items if (item['name'], item['url']) not in existing_items]

            if unique_new_items:
                existing_data.setdefault('items', []).extend(unique_new_items)
                with open(self.__path, 'w', encoding='utf-8') as file:
                    json.dump(existing_data, file, ensure_ascii=False, indent=4)


        except IOError as e:
            raise IOError(f'Ошибка при записи в {self.__path}: {e}')

    def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Получает вакансии из JSON файла по заданным критериям.

        Args:
            criteria (Optional[Dict[str, Any]], optional): Словарь с критериями фильтрации.
                                                         По умолчанию None.

        Returns:
            List[Dict[str, Any]]: Список вакансий, соответствующих критериям.
        """
        try:
            data = self.__load_existing_data()
            vacancies = data.get('items', [])

            if not criteria:
                return vacancies

            filtered = []
            for vacancy in vacancies:
                match = True
                for key, value in criteria.items():
                    if key == 'name' and value.lower() not in vacancy.get('name', '').lower():
                        match = False
                        break
                    if key == 'salary_from' and (vacancy.get('salary_from') is None or vacancy.get('salary_from') < value):
                        match = False
                        break
                    if key == 'salary_to' and (vacancy.get('salary_to') is None or vacancy.get('salary_to') > value):
                        match = False
                        break
                if match:
                    filtered.append(vacancy)

            print(f'Найдено {len(filtered)} вакансий, соответствующих критериям.')
            return filtered

        except IOError as e:
            raise IOError(f'Ошибка при чтении из {self.__path}: {e}')

    def delete(self, record_id: Optional[str] = None) -> None:
        """
        Удаляет все вакансии или конкретную вакансию по идентификатору.

        Args:
            record_id (Optional[str], optional): Идентификатор вакансии для удаления.
                                                Если не указан, удаляются все вакансии.
                                                По умолчанию None.

        Raises:
            IOError: Если произошла ошибка при удалении данных.
        """
        try:
            if not os.path.exists(self.__path):
                return

            if record_id:
                with open(self.__path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                original_length = len(data.get('items', []))
                data['items'] = [item for item in data.get('items', []) if item.get('id') != record_id]
                new_length = len(data['items'])
                if new_length < original_length:
                    with open(self.__path, 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)
                    print(f'Вакансия с id {record_id} удалена из {self.__path}.')
                else:
                    print(f'Вакансия с id {record_id} не найдена в {self.__path}.')
            else:
                # Удаление всех вакансий
                with open(self.__path, 'w', encoding='utf-8') as file:
                    json.dump({"items": []}, file, ensure_ascii=False, indent=4)
                print(f'Все вакансии удалены из {self.__path}.')

        except IOError as e:
            raise IOError(f'Ошибка при удалении данных из {self.__path}: {e}')

    def __load_existing_data(self) -> Dict[str, Any]:
        """
        Загружает существующие данные из JSON файла.

        Returns:
            Dict[str, Any]: Данные из файла.

        Raises:
            IOError: Если произошла ошибка при чтении файла.
        """
        try:
            if not os.path.exists(self.__path):
                return {"items": []}
            with open(self.__path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except IOError as e:
            raise IOError(f'Ошибка при чтении данных из {self.__path}: {e}')
