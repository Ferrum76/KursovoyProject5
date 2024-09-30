# tests/vacancy_test.py

import unittest
from src.vacancy import Vacancy
from dataclasses import dataclass, field
from typing import Optional


class TestVacancy(unittest.TestCase):
    def test_vacancy_initialization_valid(self):
        """
        Тестирует корректную инициализацию объекта Vacancy с валидными данными.
        """
        vacancy = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            salary_from=100000,
            salary_to=150000,
            currency="RUB",
            url="https://hh.ru/vacancy/123456",
            requirement="3+ years of experience"
        )
        self.assertEqual(vacancy.name, "Python Developer")
        self.assertEqual(vacancy.desc, "Develop Python applications")
        self.assertEqual(vacancy.salary_from, 100000)
        self.assertEqual(vacancy.salary_to, 150000)
        self.assertEqual(vacancy.currency, "RUB")
        self.assertEqual(vacancy.url, "https://hh.ru/vacancy/123456")
        self.assertEqual(vacancy.requirement, "3+ years of experience")

    def test_vacancy_initialization_defaults(self):
        """
        Тестирует инициализацию объекта Vacancy с использованием значений по умолчанию.
        """
        vacancy = Vacancy(
            name="Junior Developer",
            desc="Entry-level position",
            url="https://hh.ru/vacancy/789012"
        )
        self.assertEqual(vacancy.salary_from, None)
        self.assertEqual(vacancy.salary_to, None)
        self.assertEqual(vacancy.currency, "RUB")
        self.assertEqual(vacancy.requirement, "Информация отсутствует")

    def test_vacancy_negative_salary_from(self):
        """
        Тестирует инициализацию объекта Vacancy с отрицательным значением salary_from.
        Ожидается, что будет вызвано исключение ValueError.
        """
        with self.assertRaises(ValueError) as context:
            Vacancy(
                name="Python Developer",
                desc="Develop Python applications",
                salary_from=-50000,
                salary_to=150000,
                currency="RUB",
                url="https://hh.ru/vacancy/123456",
                requirement="3+ years of experience"
            )
        self.assertIn("salary_from не может быть отрицательным", str(context.exception))

    def test_vacancy_negative_salary_to(self):
        """
        Тестирует инициализацию объекта Vacancy с отрицательным значением salary_to.
        Ожидается, что будет вызвано исключение ValueError.
        """
        with self.assertRaises(ValueError) as context:
            Vacancy(
                name="Python Developer",
                desc="Develop Python applications",
                salary_from=100000,
                salary_to=-150000,
                currency="RUB",
                url="https://hh.ru/vacancy/123456",
                requirement="3+ years of experience"
            )
        self.assertIn("salary_to не может быть отрицательным", str(context.exception))

    def test_vacancy_salary_from_greater_than_salary_to(self):
        """
        Тестирует инициализацию объекта Vacancy, когда salary_from больше salary_to.
        Ожидается, что будет вызвано исключение ValueError.
        """
        with self.assertRaises(ValueError) as context:
            Vacancy(
                name="Python Developer",
                desc="Develop Python applications",
                salary_from=200000,
                salary_to=150000,
                currency="RUB",
                url="https://hh.ru/vacancy/123456",
                requirement="3+ years of experience"
            )
        self.assertIn("salary_from не может быть больше salary_to", str(context.exception))

    def test_vacancy_invalid_url(self):
        """
        Тестирует инициализацию объекта Vacancy с некорректным URL.
        Ожидается, что будет вызвано исключение ValueError.
        """
        with self.assertRaises(ValueError) as context:
            Vacancy(
                name="Python Developer",
                desc="Develop Python applications",
                salary_from=100000,
                salary_to=150000,
                currency="RUB",
                url="ftp://hh.ru/vacancy/123456",
                requirement="3+ years of experience"
            )
        self.assertIn("url должен начинаться с 'http://' или 'https://'", str(context.exception))

    def test_vacancy_empty_name(self):
        """
        Тестирует инициализацию объекта Vacancy с пустым именем.
        Ожидается, что будет вызвано исключение ValueError.
        """
        with self.assertRaises(ValueError) as context:
            Vacancy(
                name="",
                desc="Develop Python applications",
                salary_from=100000,
                salary_to=150000,
                currency="RUB",
                url="https://hh.ru/vacancy/123456",
                requirement="3+ years of experience"
            )
        self.assertIn("Название вакансии не может быть пустым", str(context.exception))

    def test_vacancy_empty_desc_defaults(self):
        """
        Тестирует инициализацию объекта Vacancy с пустым описанием.
        Ожидается, что описание будет установлено в 'Описание отсутствует'.
        """
        vacancy = Vacancy(
            name="Python Developer",
            desc="",
            salary_from=100000,
            salary_to=150000,
            currency="RUB",
            url="https://hh.ru/vacancy/123456",
            requirement="3+ years of experience"
        )
        self.assertEqual(vacancy.desc, "Описание отсутствует")

    def test_vacancy_get_salary_range_both(self):
        """
        Тестирует метод get_salary_range() для случая, когда указаны both salary_from и salary_to.
        """
        vacancy = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            salary_from=100000,
            salary_to=150000,
            currency="RUB",
            url="https://hh.ru/vacancy/123456",
            requirement="3+ years of experience"
        )
        self.assertEqual(vacancy.get_salary_range(), "100000 - 150000 RUB")

    def test_vacancy_get_salary_range_from_only(self):
        """
        Тестирует метод get_salary_range() для случая, когда указана только salary_from.
        """
        vacancy = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            salary_from=100000,
            salary_to=None,
            currency="RUB",
            url="https://hh.ru/vacancy/123456",
            requirement="3+ years of experience"
        )
        self.assertEqual(vacancy.get_salary_range(), "От 100000 RUB")

    def test_vacancy_get_salary_range_to_only(self):
        """
        Тестирует метод get_salary_range() для случая, когда указана только salary_to.
        """
        vacancy = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            salary_from=None,
            salary_to=150000,
            currency="RUB",
            url="https://hh.ru/vacancy/123456",
            requirement="3+ years of experience"
        )
        self.assertEqual(vacancy.get_salary_range(), "До 150000 RUB")

    def test_vacancy_get_salary_range_none(self):
        """
        Тестирует метод get_salary_range() для случая, когда зарплата не указана.
        """
        vacancy = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            salary_from=None,
            salary_to=None,
            currency="RUB",
            url="https://hh.ru/vacancy/123456",
            requirement="3+ years of experience"
        )
        self.assertEqual(vacancy.get_salary_range(), "Не указана")

    def test_vacancy_to_dict(self):
        """
        Тестирует метод to_dict(), проверяя корректность преобразования объекта Vacancy в словарь.
        """
        vacancy = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            salary_from=100000,
            salary_to=150000,
            currency="RUB",
            url="https://hh.ru/vacancy/123456",
            requirement="3+ years of experience"
        )
        expected_dict = {
            "name": "Python Developer",
            "desc": "Develop Python applications",
            "salary_from": 100000,
            "salary_to": 150000,
            "currency": "RUB",
            "url": "https://hh.ru/vacancy/123456",
            "requirement": "3+ years of experience"
        }
        self.assertEqual(vacancy.to_dict(), expected_dict)

    def test_vacancy_ordering(self):
        """
        Тестирует возможность сравнения объектов Vacancy по атрибутам с compare=True.
        Поскольку только 'name' и 'desc' участвуют в сравнении, проверяем их порядок.
        """
        vacancy1 = Vacancy(
            name="A Developer",
            desc="Develop A applications",
            salary_from=100000,
            salary_to=150000,
            currency="RUB",
            url="https://hh.ru/vacancy/111111",
            requirement="2+ years of experience"
        )
        vacancy2 = Vacancy(
            name="B Developer",
            desc="Develop B applications",
            salary_from=120000,
            salary_to=180000,
            currency="RUB",
            url="https://hh.ru/vacancy/222222",
            requirement="4+ years of experience"
        )
        vacancy3 = Vacancy(
            name="A Developer",
            desc="Develop C applications",
            salary_from=90000,
            salary_to=130000,
            currency="RUB",
            url="https://hh.ru/vacancy/333333",
            requirement="1+ years of experience"
        )

        # vacancy1 < vacancy2 because 'A Developer' < 'B Developer'
        self.assertLess(vacancy1, vacancy2)

        # vacancy1 < vacancy3 because 'A Developer' == 'A Developer' but 'Develop A applications' < 'Develop C applications'
        self.assertLess(vacancy1, vacancy3)

        # vacancy2 > vacancy3
        self.assertGreater(vacancy2, vacancy3)

    def test_vacancy_invalid_url_format(self):
        """
        Тестирует инициализацию объекта Vacancy с URL, не начинающимся с http:// или https://.
        Ожидается, что будет вызвано исключение ValueError.
        """
        with self.assertRaises(ValueError) as context:
            Vacancy(
                name="Python Developer",
                desc="Develop Python applications",
                salary_from=100000,
                salary_to=150000,
                currency="RUB",
                url="www.hh.ru/vacancy/123456",
                requirement="3+ years of experience"
            )
        self.assertIn("url должен начинаться с 'http://' или 'https://'", str(context.exception))

    def test_vacancy_default_currency(self):
        """
        Тестирует инициализацию объекта Vacancy без указания валюты, ожидая значение по умолчанию "RUB".
        """
        vacancy = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            salary_from=100000,
            salary_to=150000,
            url="https://hh.ru/vacancy/123456"
        )
        self.assertEqual(vacancy.currency, "RUB")

    def test_vacancy_default_url(self):
        """
        Тестирует инициализацию объекта Vacancy без указания URL, ожидая значение по умолчанию "".
        """
        vacancy = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            salary_from=100000,
            salary_to=150000,
            requirement="3+ years of experience"
        )
        self.assertEqual(vacancy.url, "")

    def test_vacancy_default_requirement(self):
        """
        Тестирует инициализацию объекта Vacancy без указания требования, ожидая значение по умолчанию.
        """
        vacancy = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            salary_from=100000,
            salary_to=150000,
            url="https://hh.ru/vacancy/123456"
        )
        self.assertEqual(vacancy.requirement, "Информация отсутствует")

    def test_vacancy_missing_optional_fields(self):
        """
        Тестирует инициализацию объекта Vacancy с отсутствующими опциональными полями.
        """
        vacancy = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            url="https://hh.ru/vacancy/123456"
        )
        self.assertIsNone(vacancy.salary_from)
        self.assertIsNone(vacancy.salary_to)
        self.assertEqual(vacancy.currency, "RUB")
        self.assertEqual(vacancy.requirement, "Информация отсутствует")

    def test_vacancy_get_salary_range_no_salary(self):
        """
        Тестирует метод get_salary_range() для вакансии без указанных зарплат.
        """
        vacancy = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            url="https://hh.ru/vacancy/123456"
        )
        self.assertEqual(vacancy.get_salary_range(), "Не указана")

    def test_vacancy_get_salary_range_from_only(self):
        """
        Тестирует метод get_salary_range() для вакансии с указанным только salary_from.
        """
        vacancy = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            salary_from=100000,
            url="https://hh.ru/vacancy/123456"
        )
        self.assertEqual(vacancy.get_salary_range(), "От 100000 RUB")

    def test_vacancy_get_salary_range_to_only(self):
        """
        Тестирует метод get_salary_range() для вакансии с указанным только salary_to.
        """
        vacancy = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            salary_to=150000,
            url="https://hh.ru/vacancy/123456"
        )
        self.assertEqual(vacancy.get_salary_range(), "До 150000 RUB")

    def test_vacancy_get_salary_range_both(self):
        """
        Тестирует метод get_salary_range() для вакансии с указанными и salary_from, и salary_to.
        """
        vacancy = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            salary_from=100000,
            salary_to=150000,
            url="https://hh.ru/vacancy/123456"
        )
        self.assertEqual(vacancy.get_salary_range(), "100000 - 150000 RUB")

    def test_vacancy_to_dict(self):
        """
        Тестирует метод to_dict(), проверяя корректность преобразования объекта Vacancy в словарь.
        """
        vacancy = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            salary_from=100000,
            salary_to=150000,
            currency="USD",
            url="https://hh.ru/vacancy/123456",
            requirement="3+ years of experience"
        )
        expected_dict = {
            "name": "Python Developer",
            "desc": "Develop Python applications",
            "salary_from": 100000,
            "salary_to": 150000,
            "currency": "USD",
            "url": "https://hh.ru/vacancy/123456",
            "requirement": "3+ years of experience"
        }
        self.assertEqual(vacancy.to_dict(), expected_dict)

    def test_vacancy_ordering(self):
        """
        Тестирует возможность сравнения объектов Vacancy по атрибутам с compare=True.
        Поскольку только 'name' и 'desc' участвуют в сравнении, проверяем их порядок.
        """
        vacancy1 = Vacancy(
            name="A Developer",
            desc="Develop A applications",
            salary_from=100000,
            salary_to=150000,
            currency="RUB",
            url="https://hh.ru/vacancy/111111",
            requirement="2+ years of experience"
        )
        vacancy2 = Vacancy(
            name="B Developer",
            desc="Develop B applications",
            salary_from=120000,
            salary_to=180000,
            currency="RUB",
            url="https://hh.ru/vacancy/222222",
            requirement="4+ years of experience"
        )
        vacancy3 = Vacancy(
            name="A Developer",
            desc="Develop C applications",
            salary_from=90000,
            salary_to=130000,
            currency="RUB",
            url="https://hh.ru/vacancy/333333",
            requirement="1+ years of experience"
        )

        # vacancy1 < vacancy2 потому что 'A Developer' < 'B Developer'
        self.assertLess(vacancy1, vacancy2)

        # vacancy1 < vacancy3 потому что 'A Developer' == 'A Developer' но 'Develop A applications' < 'Develop C applications'
        self.assertLess(vacancy1, vacancy3)

        # vacancy2 > vacancy3
        self.assertGreater(vacancy2, vacancy3)

    def test_vacancy_invalid_url_prefix(self):
        """
        Тестирует инициализацию объекта Vacancy с URL, не начинающимся с 'http://' или 'https://'.
        Ожидается, что будет вызвано исключение ValueError.
        """
        with self.assertRaises(ValueError) as context:
            Vacancy(
                name="Python Developer",
                desc="Develop Python applications",
                salary_from=100000,
                salary_to=150000,
                currency="RUB",
                url="ftp://hh.ru/vacancy/123456",
                requirement="3+ years of experience"
            )
        self.assertIn("url должен начинаться с 'http://' или 'https://'", str(context.exception))

    def test_vacancy_empty_url(self):
        """
        Тестирует инициализацию объекта Vacancy с пустым URL.
        """
        vacancy = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            salary_from=100000,
            salary_to=150000,
            currency="RUB",
            url="",
            requirement="3+ years of experience"
        )
        self.assertEqual(vacancy.url, "")

    def test_vacancy_empty_currency_defaults(self):
        """
        Тестирует инициализацию объекта Vacancy без указания валюты, ожидая значение по умолчанию "RUB".
        """
        vacancy = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            salary_from=100000,
            salary_to=150000,
            url="https://hh.ru/vacancy/123456",
            requirement="3+ years of experience"
        )
        self.assertEqual(vacancy.currency, "RUB")

    def test_vacancy_missing_required_fields(self):
        """
        Тестирует инициализацию объекта Vacancy с отсутствующими обязательными полями.
        Ожидается, что будут вызваны соответствующие исключения.
        """
        # Отсутствует имя
        with self.assertRaises(ValueError) as context:
            Vacancy(
                name="",
                desc="Develop Python applications",
                salary_from=100000,
                salary_to=150000,
                currency="RUB",
                url="https://hh.ru/vacancy/123456"
            )
        self.assertIn("Название вакансии не может быть пустым", str(context.exception))

        # Отсутствует URL (хотя URL по умолчанию может быть пустым)
        vacancy = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            salary_from=100000,
            salary_to=150000,
            requirement="3+ years of experience"
        )
        self.assertEqual(vacancy.url, "")

    def test_vacancy_post_init_defaults_desc(self):
        """
        Тестирует метод __post_init__, чтобы убедиться, что описание устанавливается в 'Описание отсутствует',
        если оно пустое.
        """
        vacancy = Vacancy(
            name="Python Developer",
            desc="",
            salary_from=100000,
            salary_to=150000,
            currency="RUB",
            url="https://hh.ru/vacancy/123456",
            requirement="3+ years of experience"
        )
        self.assertEqual(vacancy.desc, "Описание отсутствует")

    def test_vacancy_post_init_no_desc(self):
        """
        Тестирует метод __post_init__, чтобы убедиться, что описание устанавливается в 'Описание отсутствует',
        если поле desc отсутствует.
        """
        # Поскольку в dataclass поле desc обязательное, мы должны передать его как пустую строку или другое значение
        vacancy = Vacancy(
            name="Python Developer",
            desc=None,  # Возможно, обработка None в Vacancy
            salary_from=100000,
            salary_to=150000,
            currency="RUB",
            url="https://hh.ru/vacancy/123456",
            requirement="3+ years of experience"
        )
        self.assertEqual(vacancy.desc, "Описание отсутствует")

    def test_vacancy_post_init_invalid_salary_from_none(self):
        """
        Тестирует метод __post_init__, чтобы убедиться, что None для salary_from не вызывает исключения.
        """
        vacancy = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            salary_from=None,
            salary_to=150000,
            currency="RUB",
            url="https://hh.ru/vacancy/123456",
            requirement="3+ years of experience"
        )
        self.assertIsNone(vacancy.salary_from)

    def test_vacancy_post_init_invalid_salary_to_none(self):
        """
        Тестирует метод __post_init__, чтобы убедиться, что None для salary_to не вызывает исключения.
        """
        vacancy = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            salary_from=100000,
            salary_to=None,
            currency="RUB",
            url="https://hh.ru/vacancy/123456",
            requirement="3+ years of experience"
        )
        self.assertIsNone(vacancy.salary_to)

    def test_vacancy_post_init_salary_from_equals_salary_to(self):
        """
        Тестирует метод __post_init__, чтобы убедиться, что salary_from равен salary_to не вызывает исключения.
        """
        vacancy = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            salary_from=150000,
            salary_to=150000,
            currency="RUB",
            url="https://hh.ru/vacancy/123456",
            requirement="3+ years of experience"
        )
        self.assertEqual(vacancy.salary_from, 150000)
        self.assertEqual(vacancy.salary_to, 150000)

    def test_vacancy_invalid_currency(self):
        """
        Тестирует инициализацию объекта Vacancy с некорректной валютой.
        Хотя валюта может быть любой строкой, валидация не предусмотрена, поэтому ожидается, что объект будет создан.
        """
        vacancy = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            salary_from=100000,
            salary_to=150000,
            currency="EUR",
            url="https://hh.ru/vacancy/123456",
            requirement="3+ years of experience"
        )
        self.assertEqual(vacancy.currency, "EUR")

    def test_vacancy_to_dict_with_defaults(self):
        """
        Тестирует метод to_dict(), проверяя корректность преобразования объекта Vacancy с использованием значений по умолчанию.
        """
        vacancy = Vacancy(
            name="Junior Python Developer",
            desc="Develop Python applications",
            url="https://hh.ru/vacancy/789012"
        )
        expected_dict = {
            "name": "Junior Python Developer",
            "desc": "Develop Python applications",
            "salary_from": None,
            "salary_to": None,
            "currency": "RUB",
            "url": "https://hh.ru/vacancy/789012",
            "requirement": "Информация отсутствует"
        }
        self.assertEqual(vacancy.to_dict(), expected_dict)

    def test_vacancy_str_representation(self):
        """
        Тестирует строковое представление объекта Vacancy (если метод __str__ или __repr__ определен).
        В данном случае, поскольку они не определены, проверяем стандартное представление dataclass.
        """
        vacancy = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            salary_from=100000,
            salary_to=150000,
            currency="RUB",
            url="https://hh.ru/vacancy/123456",
            requirement="3+ years of experience"
        )
        expected_repr = (
            "Vacancy(name='Python Developer', desc='Develop Python applications', "
            "salary_from=100000, salary_to=150000, currency='RUB', "
            "url='https://hh.ru/vacancy/123456', requirement='3+ years of experience')"
        )
        self.assertEqual(repr(vacancy), expected_repr)

    def test_vacancy_equality(self):
        """
        Тестирует равенство двух объектов Vacancy.
        """
        vacancy1 = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            salary_from=100000,
            salary_to=150000,
            currency="RUB",
            url="https://hh.ru/vacancy/123456",
            requirement="3+ years of experience"
        )
        vacancy2 = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            salary_from=100000,
            salary_to=150000,
            currency="RUB",
            url="https://hh.ru/vacancy/123456",
            requirement="3+ years of experience"
        )
        self.assertEqual(vacancy1, vacancy2)

    def test_vacancy_inequality(self):
        """
        Тестирует неравенство двух объектов Vacancy.
        """
        vacancy1 = Vacancy(
            name="Python Developer",
            desc="Develop Python applications",
            salary_from=100000,
            salary_to=150000,
            currency="RUB",
            url="https://hh.ru/vacancy/123456",
            requirement="3+ years of experience"
        )
        vacancy2 = Vacancy(
            name="Senior Python Developer",
            desc="Lead Python projects",
            salary_from=150000,
            salary_to=200000,
            currency="RUB",
            url="https://hh.ru/vacancy/654321",
            requirement="5+ years of experience"
        )
        self.assertNotEqual(vacancy1, vacancy2)


if __name__ == '__main__':
    unittest.main()
