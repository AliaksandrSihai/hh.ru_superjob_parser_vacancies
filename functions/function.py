from classes.abstract.abstract_class import InputError
from classes.hh.get_info_from_hh import VacancyHH


def user_interaction():
    platforms = ["HeadHunter", "SuperJob"]
    end = False
    while not end:
        chose_platforms = input("Здравствуйте, выберите платформу для поиска вакансий:\n"
                                f"1- {','.join(platforms)}\n"
                                f"2- {platforms[0]}\n"
                                f"3- {platforms[1]}\n"
                                "4- Выход\n")
        if chose_platforms == "1":
            print(f"Выбранные платформы - {','.join(platforms)} ")
            vacancies_from_hh = (VacancyHH())
            # superjob_api = SuperJobAPI()
        elif chose_platforms == "2":
            print(f"Выбранная платформа - {platforms[0]}")
            # vacancies_from_hh = Vacancy()
            vacancies_from_hh = VacancyHH()
        elif chose_platforms == "3":
            print(f"Выбранная платформа - {platforms[1]}")
        # superjob_api = SuperJobAPI()
        elif chose_platforms == "4":
            print("Хорошего дня и удачного поиска!")
            end = True
            break
        else:
            raise InputError

        search_query = input("Введите ключевое слово: ")
        vacancies_from_hh.get_vacancies(search_query)
        filter_words = int(input("Введите критерий сортировки вакансий:\n"
                                 "'Дата публикации' -- 1 \n"
                                 "'Название вакансии' -- 2 \n"
                                 "'Город' -- 3 \n"))
        if isinstance(filter_words, int):
            per_page = int(input("Введите количество вакансий для вывода: "))
            # if isinstance(per_page, int):
            if filter_words == 1:
                print("Сортировка по дате публикации")
                vacancy_sort = vacancies_from_hh.sort_by('Дата публикации', per_page)
            elif filter_words == 2:
                print("Сортировка по названию:")
                vacancy_sort = vacancies_from_hh.sort_by('Название вакансии', per_page)
            elif filter_words == 3:
                print("Сортировка по городу")
                city = input("Введите название города: ")
                vacancy_sort = vacancies_from_hh.sort_by(city, per_page)
            else:
                raise InputError
        else:
            raise InputError

        print("Найденные вакансии:")
        for x in vacancy_sort:
            print(x)
        print()
        vacancies_from_hh.add_file([])
        while True:
            next_move = int(input("Выберите дальнейшее действие: \n"
                                  "1 - добавление вакансии в json-файл\n"
                                  "2 - удаление вакансии из json-файла\n"
                                  "3 - получение информации о вакансии из файла\n"
                                  "4 - сравнение вакансий по заработной плате\n"
                                  "5 - вернуться к поиску\n"
                                  "6 - выход\n"))
            if isinstance(next_move, int):
                if next_move == 1:
                    add_vacancy = input(
                        "Для добавления вакансии в  файл,укажите 'id вакансии': ")
                    vacancy_add_list = []
                    if isinstance(add_vacancy, str):
                        for x in vacancy_sort:
                            if x['id вакансии'] == add_vacancy:
                                vacancy_add = VacancyHH(vacancy_id=x['id вакансии'],
                                                        vacancy_name=x['Название вакансии'],
                                                        vacancy_date=x['Дата публикации'],
                                                        vacancy_url=x['https cсылка'],
                                                        vacancy_salary=x['Заработная плата'],
                                                        vacancy_city=x['Город'],
                                                        vacancy_requirement=x['Требование'],
                                                        vacancy_responsibility=x['Обязанности']
                                                        )
                                vacancy_add_list.append(vacancy_add.to_json())
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
                    print(f"Информация о вакансии с id {id_vacancy}: ")
                    vacancies_from_hh.get_vacancies_by(id_vacancy)
                    continue
                elif next_move == 4:
                    print("Для сравнения вакансий по заработной плате введите id вакансий:")
                    id_vac_x = input("Вакансия №1: ")
                    id_vac_y = input("Вакансия №2: ")
                    salary = vacancies_from_hh.get_vacancies_by(id_vac_x, id_vac_y)
                    vacancies_from_hh.vacancy_salary = salary[0].split('-')[0] if salary and salary[0].split('-')[0].isdigit() else 0
                    vacancies_from_hh.other_salary = salary[1].split('-')[0] if salary and salary[1].split('-')[0].isdigit() else 0
                    if vacancies_from_hh.vacancy_salary >= vacancies_from_hh.other_salary:
                        print(f"Вакансия {id_vac_x} c заработной платой {vacancies_from_hh.vacancy_salary},\n"
                              f"больше или равна вакансии {id_vac_y} c заработной платой {vacancies_from_hh.other_salary}")
                    else:
                        print(f"Вакансия {id_vac_y} c заработной платой {vacancies_from_hh.vacancy_salary},\n"
                              f"меньше или равна вакансии {id_vac_x} c заработной платой {vacancies_from_hh.other_salary}")

                    continue
                elif next_move == 5:
                    print("Вернуться к поиску")
                    break
                elif next_move == 6:
                    print("Хорошего дня и удачного поиска!")
                    end = True
                    break
            else:
                raise InputError


    # if not filtered_vacancies:
    #     print("Нет вакансий, соответствующих заданным критериям.")
    #     return

