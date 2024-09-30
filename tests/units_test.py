import unittest
from src.utils import menu, get_info_commands_criteria, get_params_info_commands_criteria, PARAMS_ADDED

class TestUtils(unittest.TestCase):
    def test_menu(self):
        """
        Тестирует функцию menu(), проверяя корректность возвращаемой строки меню.
        """
        expected_menu = (
            "\nДоступные команды:\n"
            "1. help - помощь\n"
            "2. search - поиск вакансий\n"
            "3. exit - выход\n"
            "Введите команду: "
        )
        self.assertEqual(menu(), expected_menu)

    def test_get_info_commands_criteria(self):
        """
        Тестирует функцию get_info_commands_criteria(), проверяя корректность возвращаемой строки критериев фильтрации.
        """
        expected_criteria = (
            "\nДоступные критерии фильтрации:\n"
            "1. help - показать критерии\n"
            "2. name - название вакансии\n"
            "3. salary_from - зарплата от\n"
            "4. salary_to - зарплата до\n"
            "5. sorted_salary_from - сортировка по зарплате от\n"
            "6. sorted_salary_to - сортировка по зарплате до\n"
            "7. top_n - топ N вакансий\n"
            "8. add - применить фильтры\n"
            "9. done - завершить добавление фильтров\n"
            "10. clear - очистить фильтры\n"
            "11. stop - отменить добавление фильтров\n"
            "Введите критерий: "
        )
        self.assertEqual(get_info_commands_criteria(), expected_criteria)

    def test_get_params_info_commands_criteria_empty(self):
        """
        Тестирует функцию get_params_info_commands_criteria() с пустым словарем фильтров.
        Ожидается, что будет возвращена строка с сообщением о отсутствии фильтров.
        """
        params = {}
        expected_output = "Текущие фильтры:\n"
        self.assertEqual(get_params_info_commands_criteria(params), expected_output)

    def test_get_params_info_commands_criteria_with_boolean_filters(self):
        """
        Тестирует функцию get_params_info_commands_criteria() с фильтрами, содержащими булевы значения.
        """
        params = {
            "sorted_salary_from": True,
            "sorted_salary_to": True
        }
        expected_output = (
            "Текущие фильтры:\n"
            "\tСортировка по зарплате от\n"
            "\tСортировка по зарплате до\n"
        )
        self.assertEqual(get_params_info_commands_criteria(params), expected_output)

    def test_get_params_info_commands_criteria_with_value_filters(self):
        """
        Тестирует функцию get_params_info_commands_criteria() с фильтрами, содержащими значения.
        """
        params = {
            "name": "Senior Python Developer",
            "salary_from": 150000,
            "salary_to": 200000,
            "top_n": 10
        }
        expected_output = (
            "Текущие фильтры:\n"
            "\tНазвание вакансии: Senior Python Developer\n"
            "\tЗарплата от: 150000\n"
            "\tЗарплата до: 200000\n"
            "\tТоп N вакансий: 10\n"
        )
        self.assertEqual(get_params_info_commands_criteria(params), expected_output)

    def test_get_params_info_commands_criteria_mixed_filters(self):
        """
        Тестирует функцию get_params_info_commands_criteria() с смешанными типами фильтров.
        """
        params = {
            "name": "Python Developer",
            "sorted_salary_from": True,
            "top_n": 5
        }
        expected_output = (
            "Текущие фильтры:\n"
            "\tНазвание вакансии: Python Developer\n"
            "\tСортировка по зарплате от\n"
            "\tТоп N вакансий: 5\n"
        )
        self.assertEqual(get_params_info_commands_criteria(params), expected_output)

    def test_get_params_info_commands_criteria_unknown_key(self):
        """
        Тестирует функцию get_params_info_commands_criteria() с неизвестным ключом фильтра.
        Ожидается, что будет использован сам ключ без перевода.
        """
        params = {
            "unknown_filter": "Some Value"
        }
        expected_output = (
            "Текущие фильтры:\n"
            "\tunknown_filter: Some Value\n"
        )
        self.assertEqual(get_params_info_commands_criteria(params), expected_output)

    def test_params_added_contains_all_keys(self):
        """
        Тестирует, что PARAMS_ADDED содержит все ожидаемые ключи фильтров.
        """
        expected_keys = [
            "name",
            "salary_from",
            "salary_to",
            "sorted_salary_from",
            "sorted_salary_to",
            "top_n"
        ]
        for key in expected_keys:
            self.assertIn(key, PARAMS_ADDED)
            self.assertIsInstance(PARAMS_ADDED[key], str)

    def test_params_added_correct_mapping(self):
        """
        Тестирует, что PARAMS_ADDED правильно сопоставляет ключи фильтров с их описаниями.
        """
        expected_mapping = {
            "name": "Название вакансии",
            "salary_from": "Зарплата от",
            "salary_to": "Зарплата до",
            "sorted_salary_from": "Сортировка по зарплате от",
            "sorted_salary_to": "Сортировка по зарплате до",
            "top_n": "Топ N вакансий"
        }
        self.assertEqual(PARAMS_ADDED, expected_mapping)

if __name__ == '__main__':
    unittest.main()
