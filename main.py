from types import NoneType

import src.config as cfg
import src.saver as db_saver
import src.db_manager as db
import src.hh_api as api


def interface(config: cfg.Config) -> None:
    """
    Функция для взаимодействия с пользователем через консоль.
    Позволяет искать вакансии, применять фильтры и сохранять результаты.
    """
    print('Добро пожаловать в интерактивный поиск вакансий на сайте hh.ru')

    # Получаем параметры базы данных из конфигурации
    db_params = config.get_db()
    db_params['dbname'] = db_params.pop('name')  # Преобразуем ключ 'name' в 'dbname' для psycopg2

    # Создаем экземпляр DBManager
    db_manager = db.DBManager(db_params)

    # Создаем экземпляр Saver
    saver = db_saver.DBSaver(db_manager)

    # Получаем список компаний из конфигурации
    company_names = config.get_company_names()

    # Создаем экземпляр для работы с API hh.ru
    hh_api = api.FromHHru()

    while True:
        print("\nВыберите действие:")
        print("1 - Загрузить вакансии в базу данных")
        print("2 - Показать компании и количество вакансий")
        print("3 - Показать все вакансии")
        print("4 - Показать среднюю зарплату по вакансиям")
        print("5 - Показать вакансии с зарплатой выше средней")
        print("6 - Поиск вакансий по ключевому слову")
        print("7 - Удалить все вакансии")
        print("8 - Удалить все компании")
        print("9 - Выход")

        choice = input("Введите номер действия: ")

        if choice == '1':
            # Загружаем данные о вакансиях и сохраняем в базу данных
            for company_name in company_names:
                print(f"\nЗагружаем вакансии для компании: {company_name}")
                try:
                    vacancies = hh_api.get_vacancies(company_name)
                    if vacancies:
                        # Добавляем информацию о компании в базу данных
                        company_data = {
                            'name': company_name,
                            'url': None,
                            'description': None
                        }
                        company_id = saver.save_company(company_data)

                        # Обрабатываем вакансии и добавляем company_id
                        for vacancy in vacancies:
                            try:
                                vacancy_data = {
                                    'company_id': company_id,
                                    'title': vacancy.get('name', 'вакансия без названия'),
                                    'url': vacancy.get('url', 'alternate_url'),
                                    'description': vacancy.get('snippet', {}).get('responsibility', '')
                                }
                                if vacancy.get('salary', {}) is not None:
                                    vacancy_data['salary_from'] = vacancy.get('salary', {}).get('from', 0)
                                    vacancy_data['salary_to'] = vacancy.get('salary', {}).get('to', 0)
                                else:
                                    vacancy_data['salary_from'] = 0
                                    vacancy_data['salary_to'] = 0

                                # Добавляем вакансию в базу данных, если она новая
                                saver.save_vacancies(vacancy_data)
                            except Exception as e:
                                print(f"Ошибка при обработке вакансии {vacancy}: {e}")
                    else:
                        print(f"Нет доступных вакансий для компании {company_name}")
                except Exception as e:
                    print(f"Ошибка при загрузке вакансий для компании {company_name}: {e}")
        elif choice == '2':
            companies = db_manager.get_companies_and_vacancies_count()
            if not companies:
                print("\nНет данных о компаниях и количестве вакансий.")
                continue
            print("\nКомпании и количество вакансий:")
            for company in companies:
                print(f"Компания: {company['name']}, Количество вакансий: {company['vacancy_count']}")
        elif choice == '3':
            vacancies = db_manager.get_all_vacancies()
            print("\nСписок всех вакансий:")
            for vacancy in vacancies:
                salary_from = vacancy['salary_from'] or 'не указано'
                salary_to = vacancy['salary_to'] or 'не указано'
                print(f"Компания: {vacancy['company_name']}, Вакансия: {vacancy['title']}, "
                      f"Зарплата: от {salary_from} до {salary_to}, Ссылка: {vacancy['url']}")
        elif choice == '4':
            avg_salary = db_manager.get_avg_salary()
            if avg_salary:
                print(f"\nСредняя зарплата по вакансиям: {avg_salary:.2f}")
            else:
                print("\nДанные о зарплатах отсутствуют.")
        elif choice == '5':
            vacancies = db_manager.get_vacancies_with_higher_salary()
            if vacancies:
                print("\nВакансии с зарплатой выше средней:")
                for vacancy in vacancies:
                    salary_from = vacancy['salary_from'] or 'не указано'
                    salary_to = vacancy['salary_to'] or 'не указано'
                    print(f"Компания: {vacancy['company_name']}, Вакансия: {vacancy['title']}, "
                          f"Зарплата: от {salary_from} до {salary_to}, Ссылка: {vacancy['url']}")
            else:
                print("\nНет вакансий с зарплатой выше средней или данные о зарплатах отсутствуют.")
        elif choice == '6':
            keyword = input("Введите ключевое слово для поиска: ")
            vacancies = db_manager.get_vacancies_with_keyword(keyword)
            if vacancies:
                print(f"\nВакансии, содержащие '{keyword}':")
                for vacancy in vacancies:
                    print(f"Компания: {vacancy['company_name']}, Вакансия: {vacancy['title']}, Ссылка: {vacancy['url']}")
            else:
                print(f"\nНет вакансий, содержащих '{keyword}'.")
        elif choice == '7':
            confirmation = input("Вы уверены, что хотите удалить все вакансии? (да/нет): ")
            if confirmation.lower() == 'да' or confirmation.lower() == 'yes' or confirmation.lower() == 'y':
                saver.delete_vacancy()
                print("Все вакансии удалены.")
            else:
                print("Удаление вакансий отменено.")
        elif choice == '8':
            confirmation = input("Вы уверены, что хотите удалить все компании и связанные с ними вакансии? (да/нет): ")
            if confirmation.lower() == 'да' or confirmation.lower() == 'yes' or confirmation.lower() == 'y':
                saver.delete_company()
                print("Все компании и связанные вакансии удалены.")
            else:
                print("Удаление компаний отменено.")
        elif choice == '9':
            print("\nСпасибо за использование программы. До свидания!")
            db_manager.close()
            hh_api.close_session()
            break
        else:
            print("\nНеверный выбор. Пожалуйста, выберите действующий пункт меню.")

if __name__ == "__main__":
    cfg = cfg.Config()
    interface(cfg)
