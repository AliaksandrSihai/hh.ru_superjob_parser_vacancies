from classes.abstract.abstract_class import InputError
from classes.hh.get_info_from_hh import Vacancy


def user_interaction():
    platforms = ["HeadHunter", "SuperJob"]
    chose_platforms = input("Здравствуйте, выберите платформу для поиска вакансий:\n "
                            f"1-{platforms}\n"
                            f"2-{platforms[0]}\n"
                            f"3- {platforms[1]}\n")
    if chose_platforms == "1":
        print(f"Выбранные платформы - {platforms} ")
        vacancies_from_hh = Vacancy()
        # superjob_api = SuperJobAPI()
    elif chose_platforms == "2":
        print(f"Выбранная платформа - {platforms[0]}")
        # vacancies_from_hh = Vacancy()
        vacancies_from_hh = Vacancy()
    elif chose_platforms == "3":
        print(f"Выбранная платформа - {platforms[1]}")
    # superjob_api = SuperJobAPI()
    else:
        raise InputError

    search_query = input("Введите название вакансии: ")
    filter_words = int(input("Введите критерий сортировки вакансий:\n"
                             "'Дата публикации' -- 1 \n"
                             "'Название вакансии' -- 2 \n"
                             "'Город' -- 3 \n"))
    if isinstance(filter_words, int):
        per_page = int(input("Введите количество вакансий для вывода: "))
        if isinstance(per_page, int):
            vacancies_from_hh.get_vacancies(search_query)
            vacancy_sort = []
            if filter_words == 1:
                print("Сортировка по дате публикации")
                vacancy_sort = vacancies_from_hh.sorted_vacancy(per_page, 'Дата публикации')
            elif filter_words == 2:
                print("Сортировка по названию:")
                vacancy_sort = vacancies_from_hh.sorted_vacancy(per_page, 'Название вакансии')
            elif filter_words == 3:
                city = input("Введите название города: ")
                print("Сортировка по городу: ")
                vacancy_sort = vacancies_from_hh.sorted_vacancy(per_page, city)
            else:
                raise InputError
        else:
            raise InputError
    else:
        raise InputError

    print("Найденные вакансии:")
    for x in vacancy_sort:
        print(x)
    while True:
        next_move = int(input("Выберите дальнейшее действие: \n"
                              "1 - добавление вакансии в json-файл\n"
                              "2 - удаление вакансии из json-файла\n"
                              "3 - получение информации о вакансии из файла\n"
                              "4 - выход\n"))
        if isinstance(next_move, int):
            if next_move == 1:
                add_vacancy = input(
                    "Для добавления вакансии в  файл,укажите 'id вакансии': ")
                vacancy_add_list = []
                if isinstance(add_vacancy, str):
                    for x in vacancy_sort:
                        if x['id вакансии'] == add_vacancy:
                            vacancy_add = Vacancy(vacancy_id=x['id вакансии'],
                                                  vacancy_name=x['Название вакансии'],
                                                  vacancy_date=x['Дата публикации'],
                                                  vacancy_url=x['https cсылка'],
                                                  vacancy_salary=x['Заработная плата'],
                                                  vacancy_city=x['Город'],
                                                  vacancy_requirement=x['Требование'],
                                                  vacancy_responsibility=x['Обязанности']
                                                  )
                            vacancy_add_list.append(vacancy_add.to_json())
                            print(vacancy_add)
                            print(vacancy_add.to_json())
                            continue
                    vacancies_from_hh.add_vacancy(vacancy_add_list)
                    print()
                    print("Вакансия добавлена в файл!")
                    print()
                    continue
                else:
                    raise InputError
            elif next_move == 2:
                delete_vacancy = input(
                    "Для удаления вакансии из файла,укажите 'id вакансии': ")
                if isinstance(delete_vacancy, str):
                    vacancies_from_hh.delete_vacancy(delete_vacancy)
                    continue
                else:
                    raise InputError
            elif next_move == 3:
                print("Для получения полной информации о  вакансии по  укажите её id : ")
                id_vacancy = input("id вакансии: ")
                vacancies_from_hh.get_vacancies_by(id_vacancy)
            elif next_move == 4:
                print("Хорошего дня и удачного поиска!")
                break
            else:
                raise InputError
        else:
            raise InputError

    # vacancies_from_hh.sorted_vacancy()
    # vacancies_from_superjob = ...
    # superjob_vacancies = ...(search_query, top_n)
    #
    # filtered_vacancies = filter_vacancies(hh_vacancies, superjob_vacancies, filter_words)
    #
    # if not filtered_vacancies:
    #     print("Нет вакансий, соответствующих заданным критериям.")
    #     return
    #
    # sorted_vacancies = sort_vacancies(filtered_vacancies)
    # top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    # print_vacancies(top_vacancies)
