from typing import Dict, Any


PARAMS_ADDED = {
    "name": "Название вакансии",
    "salary_from": "Зарплата от",
    "salary_to": "Зарплата до",
    "sorted_salary_from": "Сортировка по зарплате от",
    "sorted_salary_to": "Сортировка по зарплате до",
    "sorted_avg_salary_asc": "Сортировка по средней зарплате в порядке возрастания",
    "sorted_avg_salary_desc": "Сортировка по средней зарплате в порядке убывания",
    "top_n": "Топ N вакансий"
}


def menu() -> str:
    """
    Возвращает строку меню для взаимодействия с пользователем.

    Returns:
        str: Строка меню.
    """
    return (
        "\nДоступные команды:\n"
        "1. help - помощь\n"
        "2. search - поиск вакансий\n"
        "3. exit - выход\n"
        "Введите команду: "
    )


def get_info_commands_criteria() -> str:
    """
    Возвращает строку с критериями фильтрации вакансий.

    Returns:
        str: Строка с критериями фильтрации.
    """
    return (
        "\nДоступные критерии фильтрации:\n"
        "1. help - показать критерии\n"
        "2. name - название вакансии\n"
        "3. salary_from - зарплата от\n"
        "4. salary_to - зарплата до\n"
        "5. sorted_salary_from - сортировка по зарплате от\n"
        "6. sorted_salary_to - сортировка по зарплате до\n"
        "7. sorted_avg_salary_asc - сортировка по средней зарплате по возрастанию\n"
        "8. sorted_avg_salary_desc - сортировка по средней зарплате по убыванию\n"
        "9. top_n - топ N вакансий\n"
        "10. add - применить фильтры\n"
        "11. done - завершить добавление фильтров\n"
        "12. clear - очистить фильтры\n"
        "13. stop - отменить добавление фильтров\n"
        "Введите критерий: "
    )


def get_params_info_commands_criteria(params: Dict[str, Any]) -> str:
    """
    Возвращает строку с текущими примененными фильтрами.

    Args:
        params (Dict[str, Any]): Словарь с текущими фильтрами.

    Returns:
        str: Строка с текущими фильтрами.
    """
    info = "Текущие фильтры:\n"
    for key, value in params.items():
        if isinstance(value, bool):
            info += f"\t{PARAMS_ADDED.get(key, key)}\n"
        else:
            info += f"\t{PARAMS_ADDED.get(key, key)}: {value}\n"
    return info
