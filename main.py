from src.hh_api import FromHHru
from src.parser_vacancy import ParserVacancy
from src.saver import JSONSaver
import src.utils as utils


def print_vacancies(vacancies: list) -> None:
    """
    Печатает список вакансий в удобочитаемом формате.

    Args:
        vacancies (list): Список вакансий для отображения.
    """
    if not vacancies:
        print("Нет вакансий, соответствующих заданным критериям.")
        return

    for idx, vacancy in enumerate(vacancies, start=1):
        print(f"\n{idx}. {vacancy['name']}")
        print(f"   Описание: {vacancy['desc']}")
        if vacancy.get('salary_from') or vacancy.get('salary_to'):
            salary = vacancy.get('salary_from')
            salary_to = vacancy.get('salary_to')
            currency = vacancy.get('currency', 'RUB')
            if salary and salary_to:
                print(f"   Зарплата: {salary} - {salary_to} {currency}")
            elif salary:
                print(f"   Зарплата: От {salary} {currency}")
            elif salary_to:
                print(f"   Зарплата: До {salary_to} {currency}")
        else:
            print("   Зарплата: Не указана")
        print(f"   Требования: {vacancy.get('requirement')}")
        print(f"   Ссылка: {vacancy.get('url')}")


def interface() -> None:
    """
    Функция для взаимодействия с пользователем через консоль.
    Позволяет искать вакансии, применять фильтры и сохранять результаты.
    """
    print('Добро пожаловать в интерактивный поиск вакансий на сайте hh.ru')

    while True:
        try:
            cmd = input(utils.menu()).strip().lower()

            if cmd in ['help', '1']:
                print('Вызов списка команд.')
                print(utils.menu())
                continue

            elif cmd in ['search', '2']:
                user_vacancy = input('Введите вакансию для поиска на сайте hh.ru: ').strip()
                if not user_vacancy:
                    continue

                # Инициализация компонентов
                hh = FromHHru()
                vacancies_data = hh.get_vacancies(keyword=user_vacancy, max_pages=None)
                hh.close_session()

                pv = ParserVacancy(data=vacancies_data)
                parse_vacancies = pv.parse_vacancies()

                saver = JSONSaver(path='data/vacancies.json')
                res = {"items": [vacancy.to_dict() for vacancy in parse_vacancies]}
                saver.save(res)

                print(f'Найдено: {len(parse_vacancies)} вакансий по запросу "{user_vacancy}" и сохранено в файл вакансий в {saver.get_path()}')

                # Запрос на добавление фильтров
                add_filters = input('Требуется ли добавить фильтры к вакансиям? (да/нет): ').strip().lower()
                if add_filters == 'да':
                    params = {}
                    while True:
                        sub_cmd = input(utils.get_info_commands_criteria()).strip().lower()

                        if sub_cmd in ['stop', '11']:
                            break

                        elif sub_cmd in ['help', '1']:
                            print(utils.get_info_commands_criteria())
                            continue

                        elif sub_cmd in ['name', '2']:
                            name_vac = input('Введите название вакансии: ').strip()
                            if name_vac and name_vac != '':
                                params['name'] = name_vac
                                print(f'Добавлен фильтр: {utils.PARAMS_ADDED["name"]} = {name_vac}')
                            else:
                                print('Название вакансии не может быть пустым.')

                        elif sub_cmd in ['salary_from', '3']:
                            salary_from = input('Введите зарплату от: ').strip()
                            if salary_from.isdigit() and int(salary_from) >= 0:
                                params['salary_from'] = int(salary_from)
                                print(f'Добавлен фильтр: {utils.PARAMS_ADDED["salary_from"]} = {salary_from}')
                            else:
                                print('Зарплата от должна быть неотрицательным числом.')

                        elif sub_cmd in ['salary_to', '4']:
                            salary_to = input('Введите зарплату до: ').strip()
                            if salary_to.isdigit() and int(salary_to) >= 0:
                                params['salary_to'] = int(salary_to)
                                print(f'Добавлен фильтр: {utils.PARAMS_ADDED["salary_to"]} = {salary_to}')
                            else:
                                print('Зарплата до должна быть неотрицательным числом.')

                        elif sub_cmd in ['sorted_salary_from', '5']:
                            params['sorted_salary_from'] = True
                            print(f'Добавлен фильтр: {utils.PARAMS_ADDED["sorted_salary_from"]}')

                        elif sub_cmd in ['sorted_salary_to', '6']:
                            params['sorted_salary_to'] = True
                            print(f'Добавлен фильтр: {utils.PARAMS_ADDED["sorted_salary_to"]}')

                        elif sub_cmd in ['sorted_avg_salary_asc', '7']:
                            params['sorted_avg_salary_asc'] = True
                            print(f'Добавлен фильтр: {utils.PARAMS_ADDED["sorted_avg_salary_asc"]}')

                        elif sub_cmd in ['sorted_avg_salary_desc', '8']:
                            params['sorted_avg_salary_desc'] = True
                            print(f'Добавлен фильтр: {utils.PARAMS_ADDED["sorted_avg_salary_desc"]}')

                        elif sub_cmd in ['top_n', '9']:
                            top_n = input('Введите топ N вакансий: ').strip()
                            if top_n.isdigit() and int(top_n) > 0:
                                params['top_n'] = int(top_n)
                                print(f'Добавлен фильтр: {utils.PARAMS_ADDED["top_n"]} = {top_n}')
                            else:
                                print('Топ N вакансий должно быть положительным числом.')

                        elif sub_cmd in ['add', '10']:
                            if not params:
                                print('Нет добавленных фильтров для применения.')
                                continue
                            parse_vacancies = pv.parse_vacancies(params=params)
                            saver.delete()
                            res['items'] = [vacancy.to_dict() for vacancy in parse_vacancies]
                            saver.save(res)
                            print(f'Фильтры применены. Найдено: {len(parse_vacancies)} вакансий и сохранено в файл вакансий в {saver.get_path()}')
                            print('Фильтры добавлены и применены к вакансиям.')
                            break

                        elif sub_cmd in ['done', '11']:
                            print('Применение текущих фильтров.')
                            break

                        elif sub_cmd in ['clear', '12']:
                            params.clear()
                            print('Фильтры очищены.')
                            print('Фильтры очищены.')

                        else:
                            print('Неизвестная команда. Введите "help" для списка доступных команд.')

                        # Отображение текущих добавленных фильтров
                        if params:
                            print(utils.get_params_info_commands_criteria(params))
                        else:
                            print('\tНет добавленных критериев.')



                # Запрос на очистку файла вакансий
                name_exit = input('Хотите очистить файл вакансий? (да/нет): ').strip().lower()
                if name_exit in ['да', 'yes', 'y']:
                    saver.delete()
                    print('Файл вакансий очищен')
                    print('Файл вакансий очищен.')

            elif cmd in ['exit', '3']:
                print('До свидания, спасибо за использование интерактивного поиска вакансий на сайте hh.ru')
                print('Пользователь завершил работу программы.')
                break

            else:
                print('Неизвестная команда. Введите "help" для списка доступных команд.')
                print('Неизвестная команда. Введите "help" для списка доступных команд.')

        except Exception as e:
            print(f'Произошла ошибка: {e}')


if __name__ == "__main__":
    interface()
