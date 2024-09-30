import unittest
from unittest import mock
from src.parser_vacancy import ParserVacancy
from src.vacancy import Vacancy
from typing import Dict, Any, List


class TestParserVacancy(unittest.TestCase):
    def setUp(self):
        # Пример исходных данных для тестов
        self.sample_data = [
            {
                "name": "Python Developer",
                "salary": {
                    "from": 100000,
                    "to": 150000,
                    "currency": "RUB"
                },
                "snippet": {
                    "requirement": "3+ years of experience"
                },
                "area": {
                    "name": "Москва"
                },
                "url": "https://hh.ru/vacancy/123456"
            },
            {
                "name": "Senior Python Developer",
                "salary": {
                    "from": 150000,
                    "to": 200000,
                    "currency": "RUB"
                },
                "snippet": {
                    "requirement": "5+ years of experience"
                },
                "area": {
                    "name": "Санкт-Петербург"
                },
                "url": "https://hh.ru/vacancy/654321"
            },
            {
                "name": "Java Developer",
                "salary": {
                    "from": 90000,
                    "to": 140000,
                    "currency": "RUB"
                },
                "snippet": {
                    "requirement": "2+ years of experience"
                },
                "area": {
                    "name": "Новосибирск"
                },
                "url": "https://hh.ru/vacancy/111222"
            },
            # Вакансия с отсутствующими полями
            {
                "name": "Data Scientist",
                # "salary" отсутствует
                "snippet": {
                    "requirement": "4+ years of experience"
                },
                # "area" отсутствует
                "url": "https://hh.ru/vacancy/333444"
            },
            # Вакансия с некорректными данными
            {
                "name": None,  # Некорректное название
                "salary": {
                    "from": -50000,  # Некорректная зарплата
                    "to": 100000,
                    "currency": "RUB"
                },
                "snippet": {
                    "requirement": "No experience required"
                },
                "area": {
                    "name": "Казань"
                },
                "url": "https://hh.ru/vacancy/555666"
            }
        ]
        self.parser = ParserVacancy(data=self.sample_data)

    @mock.patch('builtins.print')
    def test_creating_vacancy_list(self, mock_print):
        """
        Тестирует метод __creating_vacancy_list(), проверяя корректное создание объектов Vacancy.
        """
        expected_vacancies = [
            Vacancy(
                name="Python Developer",
                desc="Москва",
                salary_from=100000,
                salary_to=150000,
                currency="RUB",
                url="https://hh.ru/vacancy/123456",
                requirement="3+ years of experience"
            ),
            Vacancy(
                name="Senior Python Developer",
                desc="Санкт-Петербург",
                salary_from=150000,
                salary_to=200000,
                currency="RUB",
                url="https://hh.ru/vacancy/654321",
                requirement="5+ years of experience"
            ),
            Vacancy(
                name="Java Developer",
                desc="Новосибирск",
                salary_from=90000,
                salary_to=140000,
                currency="RUB",
                url="https://hh.ru/vacancy/111222",
                requirement="2+ years of experience"
            ),
            Vacancy(
                name="Data Scientist",
                desc="Без описания",
                salary_from=None,
                salary_to=None,
                currency="RUB",
                url="",
                requirement="4+ years of experience"
            )
            # Вакансия с некорректными данными должна быть пропущена
        ]
        result = self.parser._ParserVacancy__creating_vacancy_list()
        self.assertEqual(len(result), 4)  # Одну вакансию пропустили из-за ошибок
        for vac in expected_vacancies:
            self.assertIn(vac, result)
        # Проверяем, что print был вызван с корректным сообщением
        mock_print.assert_called_with(f'Всего вакансий после парсинга: 4')

    def test_parse_vacancies_no_params(self):
        """
        Тестирует метод parse_vacancies() без фильтров, ожидая полный список вакансий.
        """
        result = self.parser.parse_vacancies()
        self.assertEqual(len(result), 4)  # Одну вакансию пропустили из-за ошибок
        self.assertIsInstance(result, List)
        self.assertTrue(all(isinstance(vac, Vacancy) for vac in result))

    def test_parse_vacancies_with_name_filter(self):
        """
        Тестирует метод parse_vacancies() с фильтром по названию вакансии.
        """
        params = {"name": "Python Developer"}
        result = self.parser.parse_vacancies(params=params)
        self.assertEqual(len(result), 2)
        for vac in result:
            self.assertIn("python developer", vac.name.lower())

    def test_parse_vacancies_with_salary_from_filter(self):
        """
        Тестирует метод parse_vacancies() с фильтром по минимальной зарплате.
        """
        params = {"salary_from": 120000}
        result = self.parser.parse_vacancies(params=params)
        self.assertEqual(len(result), 1)
        for vac in result:
            self.assertIsNotNone(vac.salary_from)
            self.assertGreaterEqual(vac.salary_from, 120000)

    def test_parse_vacancies_with_salary_to_filter(self):
        """
        Тестирует метод parse_vacancies() с фильтром по максимальной зарплате.
        """
        params = {"salary_to": 140000}
        result = self.parser.parse_vacancies(params=params)
        self.assertEqual(len(result), 1)
        for vac in result:
            self.assertIsNotNone(vac.salary_to)
            self.assertLessEqual(vac.salary_to, 140000)

    def test_parse_vacancies_with_sorted_salary_from(self):
        """
        Тестирует метод parse_vacancies() с сортировкой по зарплате от.
        """
        params = {"sorted_salary_from": True}
        result = self.parser.parse_vacancies(params=params)
        salaries = [vac.salary_from if vac.salary_from else 0 for vac in result]
        self.assertEqual(salaries, sorted(salaries, reverse=True))

    def test_parse_vacancies_with_sorted_salary_to(self):
        """
        Тестирует метод parse_vacancies() с сортировкой по зарплате до.
        """
        params = {"sorted_salary_to": True}
        result = self.parser.parse_vacancies(params=params)
        salaries = [vac.salary_to if vac.salary_to else 0 for vac in result]
        self.assertEqual(salaries, sorted(salaries, reverse=True))

    def test_parse_vacancies_with_top_n(self):
        """
        Тестирует метод parse_vacancies() с выборкой топ N вакансий.
        """
        params = {"top_n": 2}
        result = self.parser.parse_vacancies(params=params)
        self.assertEqual(len(result), 2)

    def test_parse_vacansies_with_avg_salary_asc(self):
        """
        Тестирует метод parse_vacancies() с вычислением средней зарплаты вакансий.
        """
        params = {"sorted_avg_salary_asc": True}
        result = self.parser.parse_vacancies(params=params)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].salary_to, None)
        self.assertEqual(result[1].salary_to, 140000)
        self.assertEqual(result[2].salary_to, 150000)
        self.assertEqual(result[3].salary_to, 200000)

    def test_parse_vacansies_with_avg_salary_desc(self):
        """
        Тестирует метод parse_vacancies() с вычислением средней зарплаты вакансий.
        """
        params = {"sorted_avg_salary_desc": True}
        result = self.parser.parse_vacancies(params=params)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].salary_to, 200000)
        self.assertEqual(result[1].salary_to, 150000)
        self.assertEqual(result[2].salary_to, 140000)
        self.assertEqual(result[3].salary_to, None)

    def test_parse_vacancies_with_multiple_filters(self):
        """
        Тестирует метод parse_vacancies() с несколькими фильтрами одновременно.
        """
        params = {
            "name": "Python Developer",
            "salary_from": 100000,
            "salary_to": 150000,
            "sorted_salary_from": True,
            "top_n": 1
        }
        result = self.parser.parse_vacancies(params=params)
        self.assertEqual(len(result), 1)
        self.assertIn("python developer", result[0].name.lower())
        self.assertIsNotNone(result[0].salary_from)
        self.assertGreaterEqual(result[0].salary_from, 100000)
        self.assertIsNotNone(result[0].salary_to)
        self.assertLessEqual(result[0].salary_to, 150000)

    @mock.patch('builtins.print')
    def test_creating_vacancy_list_with_errors(self, mock_print):
        """
        Тестирует метод __creating_vacancy_list(), проверяя обработку ошибок в данных.
        """
        # Добавим данные с некорректными значениями уже в setUp
        result = self.parser._ParserVacancy__creating_vacancy_list()
        self.assertEqual(len(result), 4)  # Одна вакансия с ошибками пропущена
        mock_print.assert_called_with(f'Всего вакансий после парсинга: 4')

    @mock.patch('builtins.print')
    def test_creating_vacancy_list_missing_fields(self, mock_print):
        """
        Тестирует метод __creating_vacancy_list(), проверяя обработку вакансий с отсутствующими полями.
        """
        # В уже существующих данных есть вакансия с отсутствующими полями
        result = self.parser._ParserVacancy__creating_vacancy_list()
        self.assertEqual(len(result), 4)
        # Проверяем, что вакансия с отсутствующими полями правильно обработана
        vacancy = next((vac for vac in result if vac.name == "Data Scientist"), None)
        self.assertIsNotNone(vacancy)
        self.assertEqual(vacancy.desc, "Без описания")
        self.assertIsNone(vacancy.salary_from)
        self.assertIsNone(vacancy.salary_to)
        self.assertEqual(vacancy.url, "https://hh.ru/vacancy/333444")
        self.assertEqual(vacancy.requirement, "4+ years of experience")

    def test_parse_vacancies_no_data(self):
        """
        Тестирует метод parse_vacancies() при пустых исходных данных.
        """
        empty_parser = ParserVacancy(data=[])
        result = empty_parser.parse_vacancies()
        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main()
