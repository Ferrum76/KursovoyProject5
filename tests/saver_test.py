import unittest
import tempfile
import os
import json
from unittest import mock
from src.saver import JSONSaver


class TestJSONSaver(unittest.TestCase):
    def setUp(self):
        # Создаем временную директорию и файл для тестов
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_file = os.path.join(self.temp_dir.name, 'vacancies.json')
        # Инициализируем JSONSaver с временным путем
        self.saver = JSONSaver(path=self.temp_file)

    def tearDown(self):
        # Закрываем временную директорию
        self.temp_dir.cleanup()

    def test_save_single_vacancy(self):
        # Сохраняем одну вакансию
        vacancy = {
            "name": "Python Developer",
            "desc": "Develop Python applications",
            "salary_from": 100000,
            "salary_to": 150000,
            "currency": "RUB",
            "url": "https://hh.ru/vacancy/123456",
            "requirement": "3+ years of experience"
        }
        self.saver.save({"items": [vacancy]})

        # Проверяем, что вакансия сохранена
        with open(self.temp_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.assertIn(vacancy, data["items"])
            self.assertEqual(len(data["items"]), 1)

    def test_save_multiple_vacancies(self):
        # Сохраняем несколько вакансий
        vacancies = [
            {
                "name": "Python Developer",
                "desc": "Develop Python applications",
                "salary_from": 100000,
                "salary_to": 150000,
                "currency": "RUB",
                "url": "https://hh.ru/vacancy/123456",
                "requirement": "3+ years of experience"
            },
            {
                "name": "Senior Python Developer",
                "desc": "Lead Python projects",
                "salary_from": 150000,
                "salary_to": 200000,
                "currency": "RUB",
                "url": "https://hh.ru/vacancy/654321",
                "requirement": "5+ years of experience"
            }
        ]
        self.saver.save({"items": vacancies})

        # Проверяем, что вакансии сохранены
        with open(self.temp_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.assertEqual(len(data["items"]), 2)
            for vacancy in vacancies:
                self.assertIn(vacancy, data["items"])

    def test_save_duplicates(self):
        # Сохраняем вакансию дважды и проверяем, что дубликаты не добавляются
        vacancy = {
            "name": "Python Developer",
            "desc": "Develop Python applications",
            "salary_from": 100000,
            "salary_to": 150000,
            "currency": "RUB",
            "url": "https://hh.ru/vacancy/123456",
            "requirement": "3+ years of experience"
        }
        self.saver.save({"items": [vacancy]})
        self.saver.save({"items": [vacancy]})

        # Проверяем, что вакансия сохранена только один раз
        with open(self.temp_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.assertEqual(len(data["items"]), 1)

    def test_get_vacancies_no_criteria(self):
        # Сохраняем несколько вакансий
        vacancies = [
            {
                "name": "Python Developer",
                "desc": "Develop Python applications",
                "salary_from": 100000,
                "salary_to": 150000,
                "currency": "RUB",
                "url": "https://hh.ru/vacancy/123456",
                "requirement": "3+ years of experience"
            },
            {
                "name": "Senior Python Developer",
                "desc": "Lead Python projects",
                "salary_from": 150000,
                "salary_to": 200000,
                "currency": "RUB",
                "url": "https://hh.ru/vacancy/654321",
                "requirement": "5+ years of experience"
            }
        ]
        self.saver.save({"items": vacancies})

        # Получаем все вакансии без фильтров
        result = self.saver.get_vacancies()
        self.assertEqual(len(result), 2)
        for vacancy in vacancies:
            self.assertIn(vacancy, result)

    def test_get_vacancies_with_name_filter(self):
        # Сохраняем несколько вакансий
        vacancies = [
            {
                "name": "Python Developer",
                "desc": "Develop Python applications",
                "salary_from": 100000,
                "salary_to": 150000,
                "currency": "RUB",
                "url": "https://hh.ru/vacancy/123456",
                "requirement": "3+ years of experience"
            },
            {
                "name": "Senior Python Developer",
                "desc": "Lead Python projects",
                "salary_from": 150000,
                "salary_to": 200000,
                "currency": "RUB",
                "url": "https://hh.ru/vacancy/654321",
                "requirement": "5+ years of experience"
            },
            {
                "name": "Java Developer",
                "desc": "Develop Java applications",
                "salary_from": 90000,
                "salary_to": 140000,
                "currency": "RUB",
                "url": "https://hh.ru/vacancy/111222",
                "requirement": "2+ years of experience"
            }
        ]
        self.saver.save({"items": vacancies})

        # Фильтруем вакансии по названию "Python Developer"
        criteria = {"name": "Python Developer"}
        result = self.saver.get_vacancies(criteria)
        self.assertEqual(len(result), 2)
        for vacancy in vacancies[:2]:
            self.assertIn(vacancy, result)

    def test_get_vacancies_with_salary_filter(self):
        # Сохраняем несколько вакансий
        vacancies = [
            {
                "name": "Junior Python Developer",
                "desc": "Develop Python applications",
                "salary_from": 80000,
                "salary_to": 120000,
                "currency": "RUB",
                "url": "https://hh.ru/vacancy/333444",
                "requirement": "1+ years of experience"
            },
            {
                "name": "Python Developer",
                "desc": "Develop Python applications",
                "salary_from": 100000,
                "salary_to": 150000,
                "currency": "RUB",
                "url": "https://hh.ru/vacancy/123456",
                "requirement": "3+ years of experience"
            },
            {
                "name": "Senior Python Developer",
                "desc": "Lead Python projects",
                "salary_from": 150000,
                "salary_to": 200000,
                "currency": "RUB",
                "url": "https://hh.ru/vacancy/654321",
                "requirement": "5+ years of experience"
            }
        ]
        self.saver.save({"items": vacancies})

        # Фильтруем вакансии с зарплатой от 100000
        criteria = {"salary_from": 100000}
        result = self.saver.get_vacancies(criteria)
        self.assertEqual(len(result), 2)
        for vacancy in vacancies[1:]:
            self.assertIn(vacancy, result)

        # Фильтруем вакансии с зарплатой до 150000
        criteria = {"salary_to": 150000}
        result = self.saver.get_vacancies(criteria)
        self.assertEqual(len(result), 2)
        self.assertIn(vacancies[0], result)
        self.assertIn(vacancies[1], result)

    def test_delete_specific_vacancy(self):
        # Сохраняем несколько вакансий
        vacancies = [
            {
                "id": "123456",
                "name": "Python Developer",
                "desc": "Develop Python applications",
                "salary_from": 100000,
                "salary_to": 150000,
                "currency": "RUB",
                "url": "https://hh.ru/vacancy/123456",
                "requirement": "3+ years of experience"
            },
            {
                "id": "654321",
                "name": "Senior Python Developer",
                "desc": "Lead Python projects",
                "salary_from": 150000,
                "salary_to": 200000,
                "currency": "RUB",
                "url": "https://hh.ru/vacancy/654321",
                "requirement": "5+ years of experience"
            }
        ]
        self.saver.save({"items": vacancies})

        # Удаляем вакансию с id "123456"
        with mock.patch('builtins.print') as mocked_print:
            self.saver.delete(record_id="123456")
            mocked_print.assert_called_with(f'Вакансия с id 123456 удалена из {self.temp_file}.')

        # Проверяем, что вакансия удалена
        with open(self.temp_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.assertEqual(len(data["items"]), 1)
            self.assertEqual(data["items"][0]["id"], "654321")

        # Попытка удалить несуществующую вакансию
        with mock.patch('builtins.print') as mocked_print:
            self.saver.delete(record_id="000000")
            mocked_print.assert_called_with(f'Вакансия с id 000000 не найдена в {self.temp_file}.')

    def test_delete_all_vacancies(self):
        # Сохраняем несколько вакансий
        vacancies = [
            {
                "id": "123456",
                "name": "Python Developer",
                "desc": "Develop Python applications",
                "salary_from": 100000,
                "salary_to": 150000,
                "currency": "RUB",
                "url": "https://hh.ru/vacancy/123456",
                "requirement": "3+ years of experience"
            },
            {
                "id": "654321",
                "name": "Senior Python Developer",
                "desc": "Lead Python projects",
                "salary_from": 150000,
                "salary_to": 200000,
                "currency": "RUB",
                "url": "https://hh.ru/vacancy/654321",
                "requirement": "5+ years of experience"
            }
        ]
        self.saver.save({"items": vacancies})

        # Удаляем все вакансии
        with mock.patch('builtins.print') as mocked_print:
            self.saver.delete()
            mocked_print.assert_called_with(f'Все вакансии удалены из {self.temp_file}.')

        # Проверяем, что все вакансии удалены
        with open(self.temp_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.assertEqual(len(data["items"]), 0)



if __name__ == '__main__':
    unittest.main()
