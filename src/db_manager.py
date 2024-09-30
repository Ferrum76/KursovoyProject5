from typing import Dict, Any, List, Optional

import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class DBManager:
    """класс DBManager для работы с данными в БД."""

    def __init__(self, db_params: Dict[str, Any] = None):
        self.__db_params = db_params
        if self.__db_params is None:
            raise ValueError("Параметры подключения к базе данных должны быть предоставлены.")
        try:
            self.conn = psycopg2.connect(
                dbname=self.__db_params['dbname'],
                user=self.__db_params['user'],
                password=self.__db_params['password'],
                host=self.__db_params['host'],
                port=self.__db_params['port']
            )
            self.__create_tables()
        except psycopg2.DatabaseError as e:
            print(f"Ошибка подключения к базе данных: {e}")
            raise

    def get_companies_and_vacancies_count(self) -> List[Dict[str, Any]]:
        """
        Получает список всех компаний и количество вакансий у каждой компании.

        Returns:
            List[Dict[str, Any]]: Список словарей с названием компании и количеством вакансий.
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT companies.name, COUNT(vacancies.id) as vacancy_count
                FROM companies 
                LEFT JOIN vacancies ON companies.id = vacancies.company_id 
                GROUP BY companies.name;
            """)
            return cur.fetchall()

    def get_all_vacancies(self) -> List[Dict[str, Any]]:
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.

        Returns:
            List[Dict[str, Any]]: Список вакансий с подробной информацией.
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT companies.name as company_name, vacancies.title, vacancies.salary_from, vacancies.salary_to, vacancies.url
                FROM vacancies 
                JOIN companies ON vacancies.company_id = companies.id;
            """)
            return cur.fetchall()

    def get_avg_salary(self) -> Optional[float]:
        """
        Получает среднюю зарплату по вакансиям.

        Returns:
            Optional[float]: Средняя зарплата или None, если данных нет.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG((salary_from + salary_to) / 2.0)
                FROM vacancies
                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL;
            """)
            result = cur.fetchone()[0]
            return result

    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Получает список всех вакансий, в названии которых содержится заданное ключевое слово.

        Args:
            keyword (str): Ключевое слово для поиска.

        Returns:
            List[Dict[str, Any]]: Список вакансий, соответствующих ключевому слову.
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT companies.name as company_name, vacancies.title, vacancies.url
                FROM vacancies 
                JOIN companies ON vacancies.company_id = companies.id
                WHERE vacancies.title ILIKE %s;
            """, (f'%{keyword}%',))
            return cur.fetchall()

    def get_vacancies_with_higher_salary(self) -> List[Dict[str, Any]]:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.

        Returns:
            List[Dict[str, Any]]: Список вакансий с подробной информацией.
        """
        avg_salary = self.get_avg_salary()
        if avg_salary is None:
            return []
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT companies.name as company_name, vacancies.title, vacancies.salary_from, vacancies.salary_to, vacancies.url
                FROM vacancies
                JOIN companies ON vacancies.company_id = companies.id
                WHERE (vacancies.salary_from + vacancies.salary_to) / 2.0 > %s;
            """, (avg_salary,))
            return cur.fetchall()

    def __create_tables(self) -> None:
        """
        Создает таблицы companies и vacancies в базе данных, если они не существуют.
        """
        with self.conn.cursor() as cur:
       # Создание таблицы компаний
            cur.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    url VARCHAR(255),
                    description TEXT
                );
            """)

            # Создание таблицы вакансий
            cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    id SERIAL PRIMARY KEY,
                    company_id INT REFERENCES companies(id) ON DELETE CASCADE,
                    title VARCHAR(255) NOT NULL,
                    salary_from INT,
                    salary_to INT,
                    url VARCHAR(255),
                    description TEXT
                );
            """)

            self.conn.commit()

    def close(self) -> None:
        """
        Закрывает соединение с базой данных.
        """
        self.conn.close()

    def insert_company(self, company: Dict[str, Any]) -> int:
        """
        Вставляет информацию о компании в таблицу companies.

        Args:
            company (Dict[str, Any]): Словарь с данными компании.

        Returns:
            int: Идентификатор вставленной компании.
        """
        with self.conn.cursor() as cur:
            try:
                cur.execute("SELECT id FROM companies WHERE name = %s;", (company.get('name'),))
                result = cur.fetchone()
                if result:
                    return result[0]
                cur.execute("""
                    INSERT INTO companies (name, url, description)
                    VALUES (%s, %s, %s)
                    RETURNING id;
                """, (company.get('name'), company.get('url'), company.get('description')))
                company_id = cur.fetchone()[0]
            except Exception as e:
                print(e)
                company_id = None
            finally:
                self.conn.commit()
            return company_id

    def insert_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """
        Вставляет информацию о вакансии в таблицу vacancies.

        Args:
            vacancy (Dict[str, Any]): Словарь с данными вакансии.
        """
        with self.conn.cursor() as cur:
            cur.execute("SELECT id FROM companies WHERE url = %s;", (vacancy.get('url'),))
            result = cur.fetchone()
            if result:
                return result[0]
            cur.execute("""
                INSERT INTO vacancies (company_id, title, salary_from, salary_to, url, description)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (
                vacancy.get('company_id'),
                vacancy.get('title'),
                vacancy.get('salary_from'),
                vacancy.get('salary_to'),
                vacancy.get('url'),
                vacancy.get('description')
            ))
            self.conn.commit()

    def delete_vacancy(self, vacancy_id: int) -> None:
        """
        Удаляет вакансию по идентификатору.

        Args:
            vacancy_id (int): Идентификатор вакансии для удаления.
        """
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM vacancies WHERE id = %s;", (vacancy_id,))
            self.conn.commit()

    def delete_all_vacancies(self) -> None:
        """
        Удаляет все вакансии из таблицы vacancies.
        """
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM vacancies;")
            self.conn.commit()

    def delete_company(self, company_id: int) -> None:
        """
        Удаляет компанию по идентификатору и все связанные с ней вакансии.

        Args:
            company_id (int): Идентификатор компании для удаления.
        """
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM companies WHERE id = %s;", (company_id,))
            self.conn.commit()

    def delete_all_companies(self) -> None:
        """
        Удаляет все компании из таблицы companies и все связанные вакансии.
        """
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM companies;")
            self.conn.commit()
