import os

from dotenv import load_dotenv


class Config:
    """
    Конфигурация приложения.
    """

    def __init__(self, path: str = '.env'):
        self.__path = path
        self.__config = self.__load_config()

    def __load_config(self) -> dict:
        """
        Загружает конфигурацию из .env.

        Returns:
            dict: Конфигурация.
        """
        load_dotenv(dotenv_path=self.__path)
        return {
            'company_names': os.getenv('COMPANY_NAMES').split(', '),
            'vacancies_path': os.getenv('VACANCIES_PATH'),
            'db': {
                'user': os.getenv('DATABASE_USER'),
                'password': os.getenv('DATABASE_PASSWORD'),
                'host': os.getenv('DATABASE_HOST'),
                'port': os.getenv('DATABASE_PORT'),
                'name': os.getenv('DATABASE_NAME'),
            }
        }

    def get_company_names(self) -> list:
        """
        Возвращает список названий компаний.

        Returns:
            list: Список названий компаний.
        """
        return self.__config['company_names']

    def get_vacancies_path(self) -> str:
        """
        Возвращает путь к JSON файлу с вакансиями.

        Returns:
            str: Путь к JSON файлу с вакансиями.
        """
        return self.__config['vacancies_path']

    def get_db(self) -> dict:
        """
        Возвращает параметры для подключения к базе данных.

        Returns:
            dict: Параметры для подключения к базе данных.
        """
        return self.__config['db']
